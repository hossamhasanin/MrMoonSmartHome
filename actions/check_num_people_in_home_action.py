from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.firebase_controller.firebase_controller import FirebaseController


class ActionCheckNumOfPeopleInHome(Action):

    def name(self) -> Text:
        return "action_number_of_people_in_home"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        controller = FirebaseController.instance()

        num_of_people = controller.getNumOfPeople()

        dispatcher.utter_message(response="utter_number_of_people_in_home" , number_of_people=num_of_people)

        return []