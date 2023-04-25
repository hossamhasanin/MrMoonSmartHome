from abc import ABC, abstractmethod
from results import Result
from avialable_operations import AvialableOperations
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
    3: [AvialableOperations.SWITCH],
    4: [AvialableOperations.SWITCH],
    5: [AvialableOperations.SWITCH, AvialableOperations.SETTING_COLOR],
    6: [],
    7: [],
    9: [],
    10: []
}

class IController(ABC):

    @abstractmethod
    def updateSwitchingState(self, state: bool , device_type_id: int , device_id: int) -> Result:
        pass