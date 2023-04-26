from abc import ABC, abstractmethod
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations
# device types ids
# doorStateId = 1,
#     tempId = 2,
#     led1Id = 3,
#     electriId = 4,
#     rgblStateId = 5,
#     gasLeakAlarmId = 6,
#     numOfPeopleId = 7,
#     passwordWrongAlarmId = 9,
#     powerConsumptionId = 10,
device_types_avialable_operations = {
    1: [],
    2: [],
    3: [AvailableOperations.SWITCH],
    4: [AvailableOperations.SWITCH],
    5: [AvailableOperations.SWITCH, AvailableOperations.SETTING_COLOR],
    6: [],
    7: [],
    9: [],
    10: []
}

class IController(ABC):

    @abstractmethod
    def updateSwitchingState(self, state: bool , device_type_id: int , device_id: int , device_type: str) -> Results:
        pass

    @abstractmethod
    def updateAllSwitchingStates(self, state: bool , device_type: str , room_name: str) -> Results:
        pass

    @abstractmethod
    def updateColorLight(self, color: int , device_type_id: int , device_id: int , device_type: str) -> Results:
        pass

    @abstractmethod
    def updateAllColorLights(self, color: int , device_type: str , room_name: str) -> Results:
        pass