from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.ask_llm import AskLlm



class ActionChangeLightColor(Action):

    def name(self) -> Text:
        return "action_ask_llm_for_entities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ask_llm = AskLlm(tracker=tracker)
        answer = ask_llm.ask_llm_for_entity_extraction()
        devices_ids = answer["devices_ids"]
        device_type = answer["device_type"]
        room_name = answer["room_name"]

        return [
            SlotSet("devices_ids", devices_ids),
            SlotSet("device_type", device_type),
            SlotSet("room_name", room_name)
        ]