from actions.firebase_controller.icontroller import IController , device_types_avialable_operations
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
        

        
