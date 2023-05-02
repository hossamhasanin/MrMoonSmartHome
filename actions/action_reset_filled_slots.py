from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.ask_llm import AskLlm



class ActionResetFilledSlots(Action):

    def name(self) -> Text:
        return "action_reset_filled_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [AllSlotsReset()]