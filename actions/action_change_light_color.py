from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.results import Results
from actions.firebase_controller.firebase_controller import FirebaseController
from actions.firebase_controller.avialable_operations import AvailableColorsToSet


class ActionChangeLightColor(Action):

    def name(self) -> Text:
        return "action_change_light_color"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        controller = FirebaseController.instance()

        light_color = tracker.get_slot("light_color")
        colorId = AvailableColorsToSet.map_from_text_to_color(text=light_color) if light_color is not None else None

        if tracker.get_slot("all_devices_selected") is not None:
            result = controller.updateAllColorLights(
                color= colorId ,
                device_type= tracker.get_slot("device_type"),
                room_name= tracker.get_slot("room_name")
            )

            if result == Results.DEVICE_NOT_FOUND:
                dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
            elif result == Results.NOT_ALLOWED_COLOR:
                dispatcher.utter_message(response="utter_not_allowed_color")
            elif result == Results.NO_COLOR_DETECTED:
                dispatcher.utter_message(response="utter_no_color_detected")
            else:
                if tracker.get_slot("room_name") != None:
                    dispatcher.utter_message(response="utter_changed_color_all_lights_with_room_name")
                else:
                    dispatcher.utter_message(response="utter_changed_color_all_lights")
        else:
            result = controller.updateColorLight(
                color= colorId ,
                device_type= tracker.get_slot("device_type"),
                room_name= tracker.get_slot("room_name")
            )

            if result == Results.NOT_ALLOWED_OPERATION_ON_DEVICE:
                dispatcher.utter_message(response="utter_can_not_change_color_of_device")
            elif result == Results.DEVICE_NOT_FOUND:
                dispatcher.utter_message(response="utter_no_devices_found_with_given_specs")
            elif result == Results.NOT_ALLOWED_COLOR:
                dispatcher.utter_message(response="utter_not_allowed_color")
            elif result == Results.NO_COLOR_DETECTED:
                dispatcher.utter_message(response="utter_no_color_detected")
            else:
                if tracker.get_slot("room_name") != None:
                    dispatcher.utter_message(response="utter_changed_color_device_with_room_name")
                else:
                    dispatcher.utter_message(response="utter_changed_color_device")

        return []