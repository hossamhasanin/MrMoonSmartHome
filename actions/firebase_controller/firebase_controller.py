from actions.firebase_controller.icontroller import IController , device_types_avialable_operations
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations , AvailableColorsToSet
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging

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


    def updateSwitchingState(self, state: bool , device_type_id: int , device_id: int , device_type: str) -> Results:
        if device_id == -1 and device_type is not None:
            return Results.DEVICE_NOT_FOUND
        
        if AvailableOperations.SWITCH not in device_types_avialable_operations[device_type_id]:
            return Results.NOT_ALLOWED_OPERATION_ON_DEVICE
        
        ref = db.reference("states/" + str(device_id))
        ref.update({"isOn": state})
        
        return Results.DONE_SUCCESSFULLY

    def updateAllSwitchingStates(self, state: bool , device_type: str , room_name: str) -> Results:
        if device_type is None:
            return Results.DEVICE_NOT_FOUND
        
        ref = db.reference("metadata")
        metadata = ref.get()
        found_devices_ids = []
        for device in metadata:
            if device is not None:
                if room_name is not None:
                    if room_name in device["room_name"] and device_type in device["device_type"] and AvailableOperations.SWITCH in device_types_avialable_operations[device["device_type_id"]]:
                        found_devices_ids.append(device["device_id"])
                else:
                    if device_type in device["device_type"] and AvailableOperations.SWITCH in device_types_avialable_operations[device["device_type_id"]]:
                        found_devices_ids.append(device["device_id"])
            
        if len(found_devices_ids) == 0:
            return Results.DEVICE_NOT_FOUND
        
        logging.info("updateAllSwitchingStates - found devices: " + str(found_devices_ids))
        transaction_dict = {}
        for device_id in found_devices_ids:
            transaction_dict[str(device_id) + "/isOn"] = state
        
        set_ref = db.reference("states")
        set_ref.update(transaction_dict)

        return Results.DONE_SUCCESSFULLY

    def updateColorLight(self, color: int, device_type_id: int, device_id: int, device_type: str) -> Results:
        if device_id == -1 and device_type is not None:
            return Results.DEVICE_NOT_FOUND
        
        if color is None:
            return Results.NO_COLOR_DETECTED
        
        if color == AvailableColorsToSet.NONE.value:
            return Results.NOT_ALLOWED_COLOR
        
        if AvailableOperations.SETTING_COLOR not in device_types_avialable_operations[device_type_id]:
            return Results.NOT_ALLOWED_OPERATION_ON_DEVICE
        
        ref = db.reference("states/" + str(device_id))
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
        

        
