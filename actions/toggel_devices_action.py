from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.results import Results
from actions.firebase_controller.firebase_controller import FirebaseController


class ActionTurnOnDevice(Action):

    def name(self) -> Text:
        return "action_turn_on_device"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()

        device_id = tracker.get_slot("device_id")
        result = controller.updateSwitchingState(
            state= True ,
            device_type_id = device_id ,
            device_id= device_id,
            device_type= tracker.get_slot("device_type")
        )

        if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
            dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")
        elif result == Results.DEVICE_NOT_FOUND:
            dispatcher.utter_message(response="utter_device_not_found")
        else:
            if tracker.get_slot("room_name") != None:
                dispatcher.utter_message(response="utter_turned_on_device_with_room_name")
            else:
                dispatcher.utter_message(response="utter_turned_on_device")

        return []
    

class ActionTurnOffDevice(Action):
    
        def name(self) -> Text:
            return "action_turn_off_device"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            controller = FirebaseController.instance()

            device_id = tracker.get_slot("device_id")
            result = controller.updateSwitchingState(
                state= False ,
                device_type_id = device_id ,
                device_id= device_id ,
                device_type= tracker.get_slot("device_type")
            )

            if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
                dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")
            elif result == Results.DEVICE_NOT_FOUND:
                dispatcher.utter_message(response="utter_device_not_found")
            else:
                if tracker.get_slot("room_name") != None:
                    dispatcher.utter_message(response="utter_turned_off_device_with_room_name")
                else:
                    dispatcher.utter_message(response="utter_turned_off_device")
    
            return []