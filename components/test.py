import pytest
import pathlib

from rasa.shared.nlu.training_data.message import Message
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.local_model_storage import LocalModelStorage
from rasa.engine.graph import ExecutionContext
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer

from .sign_up_id_for_entities import SignUpIdForEntities


@pytest.fixture
def entity_extractor():
    """Generate a tfidf vectorizer with a tmpdir as the model storage."""
    node_storage = LocalModelStorage(pathlib.Path("G:\\Projects\\AI\\rasaChat\\bot\\models\\"))
    print(pathlib.Path("G:\\Projects\\AI\\rasaChat\\bot\\models\\") / "sign_up_id_for_entities")
    node_resource = Resource("")
    context = ExecutionContext(node_storage, node_resource)
    m = SignUpIdForEntities(
        config=SignUpIdForEntities.get_default_config(),
        name=context.node_name,
        resource=node_resource,
        model_storage=node_storage,
    )
    return m


@pytest.mark.parametrize(
    "text, expected",
    [("turn on the kithchen light", 1)],
)
def test_sparse_feats_added(entity_extractor, text, expected):
    """Checks if the sizes are appropriate."""
    # Create a message
    msg = Message({"text": "turn on the living room lights" , "intent": "turn_on_device" , "entities": [
            {"start": 11, "end": 18, "value": "living room", "entity": "room_name"},
            {"start": 19, "end": 24, "value": "lights", "entity": "device_type"}
        ]})

    entity_extractor.process([msg])
    # Check that the message has been processed correctly
    entities = msg.get("entities")
    print(entities)
    assert entities[2]["value"] == expected