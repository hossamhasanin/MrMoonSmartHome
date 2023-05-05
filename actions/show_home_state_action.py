from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.firebase_controller import FirebaseController
from actions.firebase_controller.ask_llm import AskLlm
import logging


class ActionShowHomeState(Action):

    def name(self) -> Text:
        return "action_show_home_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()

        dispatcher.utter_message(text="Home state is good")

        return []