from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionTurnOnDevice(Action):

    def name(self) -> Text:
        return "action_turn_on_device"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_turned_on_device")

        return []
    

class ActionTurnOffDevice(Action):
    
        def name(self) -> Text:
            return "action_turn_off_device"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            dispatcher.utter_message(response="utter_turned_off_device")
    
            return []