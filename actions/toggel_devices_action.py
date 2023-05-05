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
        
        device_type = tracker.get_slot("device_type")
        room_name = tracker.get_slot("room_name")
        
        result = controller.updateSwitchingState(
            state= True ,
            device_type= device_type ,
            room_name= room_name
        )

        if result == Results.DEVICE_NOT_FOUND:
            dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
        
        if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
            dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")

        if tracker.get_slot("all_devices_selected") is not None:
            if room_name != None:
                dispatcher.utter_message(response="utter_turned_on_all_devices_with_room_name")
            else:
                dispatcher.utter_message(response="utter_turned_on_all_devices")
        else:
            if room_name != None:
                dispatcher.utter_message(response="utter_turned_on_device_with_room_name" , device_type=device_type , room_name=room_name)
            else:
                dispatcher.utter_message(response="utter_turned_on_device" , device_type=device_type)

        return []
    

class ActionTurnOffDevice(Action):
    
        def name(self) -> Text:
            return "action_turn_off_device"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            controller = FirebaseController.instance()

            device_type = tracker.get_slot("device_type")
            room_name = tracker.get_slot("room_name")

            result = controller.updateSwitchingState(
                state= False ,
                device_type= device_type ,
                room_name= room_name
            )

            if result == Results.DEVICE_NOT_FOUND:
                dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
            
            if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
                dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")

            if tracker.get_slot("all_devices_selected") is not None:
                if room_name != None:
                    dispatcher.utter_message(response="utter_turned_off_all_devices_with_room_name" , room_name=room_name , device_type=device_type)
                else:
                    dispatcher.utter_message(response="utter_turned_off_all_devices" , device_type=device_type)
            else:
                if room_name != None:
                    dispatcher.utter_message(response="utter_turned_off_device_with_room_name" , device_type=device_type , room_name=room_name)
                else:
                    dispatcher.utter_message(response="utter_turned_off_device" , device_type=device_type)

            return []