from typing import Any, Text, Dict, List
from actions.firebase_controller.results import Results
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.firebase_controller import FirebaseController
from actions.firebase_controller.avialable_operations import AcSupportedCommands


class ActionSetTemperatureValue(Action):

    def name(self) -> Text:
        return "action_set_temperature_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()

        set_temperature = tracker.get_slot("temperature")
        room_name = tracker.get_slot("room_name")

        actuall_temperature = controller.getCurrentHomeTemperature()

        dif = actuall_temperature - set_temperature

        result = None
        if dif > 0:
            result = controller.sendAcCommand(
                command= AcSupportedCommands.AC_LOWER_TEMPRATURE,
                temperature= dif,
                room_name= room_name
            )
        elif dif < 0:
            result = controller.sendAcCommand(
                command= AcSupportedCommands.AC_RISE_TEMPRATURE,
                temperature= dif * -1,
                room_name= room_name
            )
        
        if result == Results.DEVICE_NOT_FOUND:
            dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
        elif result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
            dispatcher.utter_message(response="utter_cannot_change_temperature")
        else:
            dispatcher.utter_message(response="utter_temperature_set")

        return []