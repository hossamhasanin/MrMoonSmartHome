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

        # with open("G:\\Projects\\AI\\rasaChat\\bot\\models\\devices_ids.pkl", "rb") as file:
        #     devices_ids = pickle.load(file)
        #     self.devices_ids = devices_ids
        # with open("G:\\Projects\\AI\\rasaChat\\bot\\models\\rooms_embeddings.pkl", "rb") as file:
        #     rooms_data = pickle.load(file)
        #     self.current_rooms = rooms_data['sentences']
        # with open("G:\\Projects\\AI\\rasaChat\\bot\\models\\devices_embeddings.pkl", "rb") as file:
        #     devices_data = pickle.load(file)
        #     self.current_devices = devices_data['sentences']
        # self.model = SentenceTransformer("G:\\Projects\\AI\\rasaChat\\bot\\models\\all-MiniLM-L12-v2")
        # self.devices_index = faiss.IndexFlatIP(self.embedding_dim)
        # self.rooms_index = faiss.IndexFlatIP(self.embedding_dim)
        # self.rooms_index.add(rooms_data['embeddings'])
        # self.devices_index.add(devices_data['embeddings'])

    # def getDevicesIds(self, device_type: str, room_name: str) -> list[int]:
    #     stored_device_type = ""

    #     if device_type is not None:
    #         device_type_embed = self.model.encode(device_type)
    #         device_score , device_index = self.devices_index.search(np.array([device_type_embed]), 1) 
    #         stored_device_type = self.current_devices[device_index[0][0]] if device_score[0][0] > self.threshold else ""
        
    #     stored_room_name = ""
    #     if room_name is not None:
    #         room_name_embed = self.model.encode(room_name)
    #         room_score , room_index = self.rooms_index.search(np.array([room_name_embed]), 1)
    #         stored_room_name = self.current_rooms[room_index[0][0]] if room_score[0][0] > self.threshold else ""    
        
    #     logging.info("stored_device_type: " + stored_device_type)
    #     logging.info("stored_room_name: " + stored_room_name)
    #     if stored_device_type == "":
    #         return []
        
    #     query = ""
    #     if stored_room_name != "":
    #         query = stored_room_name + "_" + stored_device_type
    #     else:
    #         query = stored_device_type
        
    #     logging.info("query: " + query)
    #     if query in self.devices_ids:
    #         logging.info("found "+ str(self.devices_ids[query]) + " devices")
    #         return self.devices_ids[query]
    #     else:
    #         return []


    def updateSwitchingState(self, state: bool , devices_ids: List[int]) -> Results:
        if devices_ids is None or len(devices_ids) == 0:
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

    # def updateAllSwitchingStates(self, state: bool , device_type: str , room_name: str) -> Results:
    #     if device_type is None:
    #         return Results.DEVICE_NOT_FOUND
        
    #     ref = db.reference("metadata")
    #     metadata = ref.get()
    #     found_devices_ids = []
    #     for device in metadata:
    #         if device is not None:
    #             if room_name is not None:
    #                 if room_name in device["room_name"] and device_type in device["device_type"] and AvailableOperations.SWITCH in device_types_avialable_operations[device["device_type_id"]]:
    #                     found_devices_ids.append(device["device_id"])
    #             else:
    #                 if device_type in device["device_type"] and AvailableOperations.SWITCH in device_types_avialable_operations[device["device_type_id"]]:
    #                     found_devices_ids.append(device["device_id"])
            
    #     if len(found_devices_ids) == 0:
    #         return Results.DEVICE_NOT_FOUND
        
    #     logging.info("updateAllSwitchingStates - found devices: " + str(found_devices_ids))
    #     transaction_dict = {}
    #     for device_id in found_devices_ids:
    #         transaction_dict[str(device_id) + "/isOn"] = state
        
    #     set_ref = db.reference("states")
    #     set_ref.update(transaction_dict)

    #     return Results.DONE_SUCCESSFULLY

    def updateColorLight(self, color: int, device_type_id: int,  device_type: str) -> Results:
        if device_type_id == -1 and device_type is not None:
            return Results.DEVICE_NOT_FOUND
        
        if color is None:
            return Results.NO_COLOR_DETECTED
        
        if color == AvailableColorsToSet.NONE.value:
            return Results.NOT_ALLOWED_COLOR
        
        if AvailableOperations.SETTING_COLOR not in device_types_avialable_operations[device_type_id]:
            return Results.NOT_ALLOWED_OPERATION_ON_DEVICE
        
        ref = db.reference("states/" + str(device_type_id))
        ref.update({"colorId": color})
        
        return Results.DONE_SUCCESSFULLY
    
    def updateAllColorLights(self, color: int, device_type: str, room_name: str) -> Results:
        if device_type is None:
            return Results.DEVICE_NOT_FOUND
        
        if color is None:
            return Results.NO_COLOR_DETECTED

        if color == AvailableColorsToSet.NONE.value:
            return Results.NOT_ALLOWED_COLOR
        
        ref = db.reference("metadata")
        metadata = ref.get()
        found_devices_ids = []
        for device in metadata:
            if device is not None:
                if room_name is not None:
                    if room_name in device["room_name"] and device_type in device["device_type"] and AvailableOperations.SETTING_COLOR in device_types_avialable_operations[device["device_type_id"]]:
                        found_devices_ids.append(device["device_id"])
                else:
                    if device_type in device["device_type"] and AvailableOperations.SETTING_COLOR in device_types_avialable_operations[device["device_type_id"]]:
                        found_devices_ids.append(device["device_id"])
            
        if len(found_devices_ids) == 0:
            return Results.DEVICE_NOT_FOUND
        
        logging.info("updateAllColorLights - found devices: " + str(found_devices_ids))
        transaction_dict = {}
        for device_id in found_devices_ids:
            transaction_dict[str(device_id) + "/colorId"] = color
        
        set_ref = db.reference("states")
        set_ref.update(transaction_dict)

        return Results.DONE_SUCCESSFULLY
        

        
