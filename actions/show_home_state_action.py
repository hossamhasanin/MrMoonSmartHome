from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.firebase_controller import FirebaseController
from actions.firebase_controller.icontroller import states_prompts_templates , AvailableDeviceTypes
from actions.firebase_controller.ask_llm import AskLlm
import logging


class ActionShowHomeState(Action):

    def name(self) -> Text:
        return "action_show_home_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()
        ask_llm = AskLlm(tracker=tracker)

        states = controller.getDevicesStates()

        state_prompts = ""
        for i , state in enumerate(states):
            if state == None:
                continue

            device_type_id = controller.metadata[i]["device_type_id"]
            if device_type_id != AvailableDeviceTypes.POWER_CONSUMPTION:
                state_prompts += states_prompts_templates[device_type_id](state , controller.metadata[i]) + "\n"
        
        answer = ask_llm.ask_llm_for_device_state(state_prompts)

        dispatcher.utter_message(text= answer)

        return []