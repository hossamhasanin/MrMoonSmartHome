from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.firebase_controller import FirebaseController


class ActionShowElectricityUsage(Action):

    def name(self) -> Text:
        return "action_electricity_usage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()

        consumption = controller.getAvgLastRecordedPowerConsumptions()

        dispatcher.utter_message(response="utter_electricity_usage" , amount=consumption , period= "hour")

        return []