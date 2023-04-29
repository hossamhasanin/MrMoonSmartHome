from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.results import Results
from actions.firebase_controller.firebase_controller import FirebaseController
from actions.firebase_controller.ask_llm import AskLlm
import logging


class ActionTurnOnDevice(Action):

    def name(self) -> Text:
        return "action_turn_on_device"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()
        
        devices_ids = tracker.get_slot("devices_ids")[0]
        device_type = tracker.get_slot("device_type")
        room_name = tracker.get_slot("room_name")
        if (device_type is None and room_name is None) or devices_ids == -1:
            ask_llm = AskLlm(tracker=tracker)
            answer = ask_llm.ask_llm_for_entity_extraction()
            devices_ids = answer["devices_ids"]
            device_type = answer["device_type"]
            room_name = answer["room_name"]
            # if answer["room_name"] is not None or answer["device_type"] is not None:
            #     devices_ids = controller.getDevicesIds(device_type=answer["device_type"] , room_name=answer["room_name"])
            #     devices_ids = len(devices_ids) > 0 and devices_ids or -1
            #     logging.info("devices_ids: " + str(devices_ids))
            #     device_type = answer["device_type"]
            #     room_name = answer["room_name"]

        # devices_ids supports mentioning multiple devices types so the sape of it is : devices_ids: [[3]]
        # currently we support only one device type at a time so we take the first element of the list
        
        result = controller.updateSwitchingState(
            state= True ,
            devices_ids= devices_ids
        )

        if result == Results.DEVICE_NOT_FOUND:
                dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
        
        if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
                dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")
                return [AllSlotsReset()]

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

        return [AllSlotsReset()]
    

class ActionTurnOffDevice(Action):
    
        def name(self) -> Text:
            return "action_turn_off_device"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            controller = FirebaseController.instance()

            devices_ids = tracker.get_slot("devices_ids")[0]
            result = controller.updateSwitchingState(
                state= False ,
                devices_ids= devices_ids
            )

            if result == Results.DEVICE_NOT_FOUND:
                    dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
            
            if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
                    dispatcher.utter_message(response="utter_cannot_turn_on_or_off_device")
                    return [AllSlotsReset()]

            if tracker.get_slot("all_devices_selected") is not None:
                if tracker.get_slot("room_name") != None:
                    dispatcher.utter_message(response="utter_turned_off_all_devices_with_room_name")
                else:
                    dispatcher.utter_message(response="utter_turned_off_all_devices")
            else:
                if tracker.get_slot("room_name") != None:
                    dispatcher.utter_message(response="utter_turned_off_device_with_room_name")
                else:
                    dispatcher.utter_message(response="utter_turned_off_device")

            return []