from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionFallBackToLlm(Action):

    def __init__(self):
        self.llm_url = 'https://a07f-34-91-37-35.ngrok-free.app/message'

    def name(self) -> Text:
        return "action_fallback_to_llm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # call an API to get the response from LLM
        response = self.call_llm_api(tracker.latest_message['text'])

        dispatcher.utter_message(text=response)

        return []
    
    def call_llm_api(self, message):
        # call LLM API and return the response
        # do a request to LLM API
        response = requests.get(self.llm_url, params={'prompt': message})
        # parse the response json
        response_json = response.json()
        return response_json['message']
