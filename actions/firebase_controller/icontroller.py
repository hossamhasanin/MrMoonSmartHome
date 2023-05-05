from abc import ABC, abstractmethod
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations
from enum import Enum
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

# class AvailableDeviceTypes(Enum):
#     DOOR = 1
#     TEMP = 2
#     LED = 3
#     SMART_PLUG = 4
#     RGBL = 5
#     GAS_LEAK_ALARM = 6
#     PEOPLE_COUNTER = 7
#     PASSWORD_WRONG_ALARM = 9
#     POWER_CONSUMPTION = 10

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

    devices_ids = {}

    def _getDevicesIds(self, device_type: str, room_name: str) -> list[int]:
        query = room_name + "_" + device_type
        if query in self.devices_ids:
            return self.devices_ids[query]
        else:
            query = device_type
            if query in self.devices_ids:
                return self.devices_ids[query]
            else:
                return []

    @abstractmethod
    def updateSwitchingState(self, state: bool ,device_type: str, room_name: str) -> Results:
        pass

    # @abstractmethod
    # def updateAllSwitchingStates(self, state: bool , device_type: str , room_name: str) -> Results:
    #     pass

    @abstractmethod
    def updateColorLight(self, color: int , device_type: str, room_name: str) -> Results:
        pass

    # @abstractmethod
    # def updateAllColorLights(self, color: int , device_type: str , room_name: str) -> Results:
    #     pass