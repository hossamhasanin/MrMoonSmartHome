from rasa_sdk import Tracker
from typing import Any, Text, Dict, List
import requests
import re
import logging

class AskLlm():

    def __init__(self , tracker: Tracker):
        self.tracker = tracker
        self.llm_url = 'http://c62b-34-87-186-75.ngrok-free.app/'

    def ask_llm_for_entity_extraction(self):
        logging.info("Asking LLM for entity extraction")

        coversation_history = self.get_conversation_history()
        # call an API to get the response from LLM
        response = self.call_llm_api(coversation_history , "extract_entities")
        logging.info("LLM response: " + str(response))
        # room_name = None
        # device_type = None
        
        # # Search for room name and device type using regular expressions
        # match = re.search(r"room_name\((.*?)\)", response)
        # if match:
        #     room_name = match.group(1)
        
        # match = re.search(r"device_type\((.*?)\)", response)
        # if match:
        #     device_type = match.group(1)

        # logging.info("Extracted entities: " + str({"room_name" : room_name , "device_type" : device_type}))
        
        # Return extracted entities
        return response
    
    def get_conversation_history(self) -> Text:
        logging.info("Getting conversation history")
        coversation_history = ""
        for event in self.tracker.events:
            # get the latest messages between user and bot
            if event.get('event') == 'user':
                coversation_history += event.get('text')
                coversation_history += "\n"
            elif event.get('event') == 'bot':
                coversation_history += event.get('text')
                coversation_history += "\n"

        logging.info("Conversation history: " + coversation_history)
        return coversation_history

    def call_llm_api(self, message , endpoint : Text):
        # call LLM API and return the response
        # do a request to LLM API
        response = requests.get(self.llm_url+endpoint, params={'prompt': message} , timeout=30)
        # parse the response json
        response_json = response.json()
        return response_json['output']