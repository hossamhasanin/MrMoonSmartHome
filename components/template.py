import logging
from typing import Any, Text, Dict, List, Type , Optional
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
import pathlib
from rasa.shared.nlu.constants import (
    TEXT,
    INTENT,
    INTENT_NAME_KEY,
    PREDICTED_CONFIDENCE_KEY
)

logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    component_types = [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class CustomComponentTemplate(GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        return []

    @staticmethod
    def required_packages() -> List[Text]:
        # Not needed dont edit
        """Any extra python dependencies required for this component to run."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """ Note: section optional you could edit if needed """

        # Here you can specify default values for configuration variables
        # define config variables that can be overwritten by the user in the pipeline
        # for example:
        # return {"epochs": 5}
        return {}

    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
        model_storage: ModelStorage,
        resource: Resource
    ) -> None:
        """ Note: section optional you could edit if needed """
        # Here you can initialize variables that depend on config (passed via the pipeline)
        # for example:
        # self.epochs = config.get("epochs")
        # self.model = None

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """This method is called to create a component (see the parent class for full docstring)."""
        return cls(config, execution_context.node_name, model_storage, resource)
    
    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """This method is called to load a component (see the parent class for full docstring)."""
        # Here you should edit it to load your model in memory
        # to get directory path use pathlib.Path("path/to/your/model") for example:
        # directory_path = pathlib.Path("models")
        # so to load your model use directory_path / "your_model_name" for example:
        # model = load_model(directory_path / "your_model_name")

        # this is my example delete it and replace it with your code
        try:
            # create a component instance
            component = cls(config, execution_context.node_name, model_storage, resource)
            # load your model
            directory_path = pathlib.Path("models")

            logger.info("SignUpIdForEntities load the model")
            # save your model in the component instance in the model variable
            # Here we set the loaded model to the component instance
            # Note that you have to create a variable called model in the component __init__ method above and set it to None or any default value
            component.model = SentenceTransformer(directory_path / "model_name.pt")
            logger.info("SignUpIdForEntities load")

            return component
        except Exception as e:
            logger.error("SignUpIdForEntities load error")
            logger.error(e)
            return cls(config, execution_context.node_name, model_storage, resource)
        ###########################################
            
    

    def process(self, messages: List[Message]) -> List[Message]:
        """Process incoming messages."""
        # Here you can process the incoming messages and set the intent and entities
        # you should edit this method to set the intent and entities
        for message in messages:
            self._set_intents(message)
        return messages

    def _set_intents(self, message: Message, **kwargs: Any) -> None:
        # Here use your model to get the intent from the message
        userTextMessage = message.get(TEXT)
        # then use your preprocessing method to preprocess the message text
        # preprocessed = preprocess(userTextMessage)
        # then use your model to get the intent from the preprocessed message
        # prediction , confidence_score = model(preprocessed)
        extracted_intent = {INTENT_NAME_KEY: prediction, PREDICTED_CONFIDENCE_KEY: confidence_score}
        # then set the intent to the message
        message.set(INTENT, extracted_intent, add_to_output=True)


    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Process the training examples."""
        # Here you can process the training examples and set the intent and entities
        # Don't edit this method you don't need it
        self.process(training_data.training_examples)
        return training_data

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        # Don't edit this method you don't need it
        pass