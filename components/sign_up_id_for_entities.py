import logging
from typing import Any, Text, Dict, List, Type , Optional
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.extractors.extractor import EntityExtractorMixin
from rasa.shared.nlu.training_data.message import Message
import pathlib
from rasa.shared.nlu.constants import (
    TEXT_TOKENS,
    ENTITY_ATTRIBUTE_TYPE,
    ENTITY_ATTRIBUTE_START,
    ENTITY_ATTRIBUTE_END,
    ENTITY_ATTRIBUTE_VALUE,
    ENTITIES,
)
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    component_types = [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=False
)
class SignUpIdForEntities(EntityExtractorMixin, GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        return []

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
                "symantic_model": "all-MiniLM-L12-v2" ,
                "embedding_dim": 384,
                "entity_name": "device_id",
                "threshold": 0.55,
                "non_sign_up_id": -1
            }

    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
        model_storage: ModelStorage,
        resource: Resource
    ) -> None:
        self.symantic_model = config.get("symantic_model")
        self.embedding_dim = config.get("embedding_dim")
        self.entity_name = config.get("entity_name")
        self.threshold = config.get("threshold")
        self.non_sign_up_id = config.get("non_sign_up_id")
        self.devices_index = faiss.IndexFlatIP(self.embedding_dim)
        self.rooms_index = faiss.IndexFlatIP(self.embedding_dim)
        self.current_rooms = []
        self.current_devices = []
        self.current_devices_ids = {}
        self.model = None
        
        # with model_storage.read_from(resource) as directory_path:
        #     self.model: SentenceTransformer = SentenceTransformer(directory_path / self.symantic_model)

        # with model_storage.read_from(resource) as directory_path:
        #     self.model = SentenceTransformer(directory_path / self.symantic_model)
        #     with open(directory_path / "rooms_embeddings.pkl", "rb") as file:
        #         stored_data = pickle.load(file)
        #         self.current_rooms = stored_data['sentences']
        #         self.rooms_index.add(stored_data['embeddings'])
        #     with open(directory_path / "devices_embeddings.pkl", "rb") as file:
        #         stored_data = pickle.load(file)
        #         self.current_devices = stored_data['sentences']
        #         self.devices_index.add(stored_data['embeddings'])
        #     # {"<room_name>_<device_type>": <device_id>}
        #     with open(directory_path / "devices_ids.pkl", "rb") as file:
        #         stored_data = pickle.load(file)
        #         self.current_devices_ids = stored_data
        #     logger.info("SignUpIdForEntities load")

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        logger.info("SignUpIdForEntities create")
        return cls(config, execution_context.node_name, model_storage, resource)
    
    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        try:
            component = cls(config, execution_context.node_name, model_storage, resource)
            directory_path = pathlib.Path("models")
            logger.info("SignUpIdForEntities symbol model " + str(directory_path / component.symantic_model))
            with open(directory_path / "rooms_embeddings.pkl", "rb") as file:
                rooms_data = pickle.load(file)
                current_rooms = rooms_data['sentences']
            with open(directory_path / "devices_embeddings.pkl", "rb") as file:
                devices_data = pickle.load(file)
                current_devices = devices_data['sentences']
                
            # {"<room_name>_<device_type>": <device_id>}
            with open(directory_path / "devices_ids.pkl", "rb") as file:
                stored_data = pickle.load(file)
                current_devices_ids = stored_data

            logger.info("SignUpIdForEntities load the model")
            component.model = SentenceTransformer(directory_path / component.symantic_model)
            component.current_rooms = current_rooms
            component.current_devices = current_devices
            component.current_devices_ids = current_devices_ids
            component.rooms_index.add(rooms_data['embeddings'])
            component.devices_index.add(devices_data['embeddings'])
            logger.info("SignUpIdForEntities load")

            return component
        except Exception as e:
            logger.error("SignUpIdForEntities load error")
            logger.error(e)
            return cls(config, execution_context.node_name, model_storage, resource)
            
    

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            self._set_entities(message)
        return messages

    def _set_entities(self, message: Message, **kwargs: Any) -> None:
        # get the entities from the message
        extracted_room_name = ""
        extracted_device_type = ""
        extracted_entities = message.get(ENTITIES, [])
        for entity in extracted_entities:
            if entity.get(ENTITY_ATTRIBUTE_TYPE) == "room_name":
                extracted_room_name = entity.get(ENTITY_ATTRIBUTE_VALUE)
            if entity.get(ENTITY_ATTRIBUTE_TYPE) == "device_type":
                extracted_device_type = entity.get(ENTITY_ATTRIBUTE_VALUE)
        
        if extracted_device_type == "":
            self._return_empty_entity(message)
            return
        
        device_type_embed = self.model.encode(extracted_device_type)
        device_score , device_index = self.devices_index.search(np.array([device_type_embed]), 1)

        if device_score[0][0] < self.threshold:
            self._return_empty_entity(message)
            return
        
        stored_device_type = self.current_devices[device_index[0][0]]
        stored_room_name = ""

        if extracted_room_name != "":
            room_name_embed = self.model.encode(extracted_room_name)
            room_score , room_index = self.rooms_index.search(np.array([room_name_embed]), 1)
            if room_score[0][0] > self.threshold:
                stored_room_name = self.current_rooms[room_index[0][0]]

        query = ""
        if stored_room_name == "":
            query = stored_device_type
        else:    
            query = stored_room_name + "_" + stored_device_type

        if query not in self.current_devices_ids:
            self._return_empty_entity(message)
            return

        logger.info("SignUpIdForEntities query: " + query)
        extracted_entities.append({
            ENTITY_ATTRIBUTE_TYPE: self.entity_name,
            ENTITY_ATTRIBUTE_VALUE: self.current_devices_ids[query],
            ENTITY_ATTRIBUTE_START: 0,
            ENTITY_ATTRIBUTE_END: 0
        })
        message.set(ENTITIES, extracted_entities, add_to_output=True)
    
    def _return_empty_entity(self, message: Message) -> None:
        extracted_entities = message.get(ENTITIES, [])
        extracted_entities.append({
            ENTITY_ATTRIBUTE_TYPE: self.entity_name,
            ENTITY_ATTRIBUTE_VALUE: self.non_sign_up_id,
            ENTITY_ATTRIBUTE_START: 0,
            ENTITY_ATTRIBUTE_END: 0
        })
        message.set(ENTITIES, extracted_entities, add_to_output=True)

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        self.process(training_data.training_examples)
        return training_data

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass