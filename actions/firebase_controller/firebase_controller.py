from typing import Any, Text, Dict, List
from .results import Results
from actions.firebase_controller.icontroller import IController , device_types_avialable_operations
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations , AvailableColorsToSet
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging
import pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class FirebaseController(IController):

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        if not FirebaseController.__instance:
            FirebaseController.__instance = FirebaseController(*args, **kwargs)
        return FirebaseController.__instance

    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('G:\\Projects\\AI\\rasaChat\\bot\\service_key.json')

        # Initialize the app with a None auth variable, limiting the server's access
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://voiced-home-assistant-default-rtdb.europe-west1.firebasedatabase.app/',
            'databaseAuthVariableOverride': None
        })

        with open("G:\\Projects\\AI\\rasaChat\\bot\\models\\metadata.pkl", "rb") as file:
            metadata = pickle.load(file)
            self.metadata = metadata
        

        with open("G:\\Projects\\AI\\rasaChat\\bot\\models\\devices_ids.pkl", "rb") as file:
            devices_ids = pickle.load(file)
            self.devices_ids = devices_ids


    def updateSwitchingState(self, state: bool , device_type: str, room_name: str) -> Results:
        devices_ids = self._getDevicesIds(device_type, room_name)
        if len(devices_ids) == 0:
            return Results.DEVICE_NOT_FOUND
        
        update_dict = {}
        for device_id in devices_ids:
            if AvailableOperations.SWITCH in device_types_avialable_operations[self.metadata[device_id]["device_type_id"]]:
                update_dict[str(device_id) + "/isOn"] = state
        
        if len(update_dict) == 0:
            return Results.NOT_ALLOWED_OPERATION_ON_DEVICE
            
        ref = db.reference("states")
        ref.update(update_dict)
        
        return Results.DONE_SUCCESSFULLY

    def updateColorLight(self, color: int, device_type: str, room_name: str) -> Results:
        devices_ids = self._getDevicesIds(device_type, room_name)
        if len(devices_ids) == 0:
            return Results.DEVICE_NOT_FOUND
        
        if color is None:
            return Results.NO_COLOR_DETECTED
        
        if color == AvailableColorsToSet.NONE.value:
            return Results.NOT_ALLOWED_COLOR
        
        update_dict = {}
        for device_id in devices_ids:
            if AvailableOperations.SETTING_COLOR in device_types_avialable_operations[self.metadata[device_id]["device_type_id"]]:
                update_dict[str(device_id) + "/colorId"] = color
        
        if len(update_dict) == 0:
            return Results.NOT_ALLOWED_OPERATION_ON_DEVICE
            
        ref = db.reference("states")
        ref.update(update_dict)
        
        return Results.DONE_SUCCESSFULLY

    def getDevicesStates(self):
        ref = db.reference("states")
        return ref.get()

        
