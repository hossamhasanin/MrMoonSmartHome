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

class AvailableDeviceTypes(Enum):
    DOOR = 1
    TEMP = 2
    LED = 3
    SMART_PLUG = 4
    RGBL = 5
    GAS_LEAK_ALARM = 6
    PEOPLE_COUNTER = 7
    PASSWORD_WRONG_ALARM = 9
    POWER_CONSUMPTION = 10

device_types_avialable_operations = {
    AvailableDeviceTypes.DOOR.value: [],
    AvailableDeviceTypes.TEMP.value: [],
    AvailableDeviceTypes.LED.value: [AvailableOperations.SWITCH],
    AvailableDeviceTypes.SMART_PLUG.value: [AvailableOperations.SWITCH],
    AvailableDeviceTypes.RGBL.value: [AvailableOperations.SWITCH, AvailableOperations.SETTING_COLOR],
    AvailableDeviceTypes.GAS_LEAK_ALARM.value: [],
    AvailableDeviceTypes.PEOPLE_COUNTER.value: [],
    AvailableDeviceTypes.PASSWORD_WRONG_ALARM.value: [],
    AvailableDeviceTypes.POWER_CONSUMPTION.value: []
}

states_prompts_templates = {
    AvailableDeviceTypes.DOOR.value: lambda isOn: "The door is " + ("open" if isOn else "closed"),
    AvailableDeviceTypes.TEMP.value: lambda temp: "The temperature is " + str(temp) + " celsius",
    AvailableDeviceTypes.LED.value: lambda isOn, room_name: "The " + room_name + " normal lights are " + ("on" if isOn else "off"),
    AvailableDeviceTypes.SMART_PLUG.value: lambda isOn, room_name: "The " + room_name + " smart plug is " + ("on" if isOn else "off"),
    AvailableDeviceTypes.RGBL.value: lambda isOn , room_name , color: "The " + room_name + " RGB lights are " + ("on" if isOn else "off") + " and has a " + color + " color.",
    AvailableDeviceTypes.GAS_LEAK_ALARM.value: lambda isOn: "The gas leak alarm is " + ("on" if isOn else "off"),
    AvailableDeviceTypes.PEOPLE_COUNTER.value: lambda numOfPeople: "The number of people in the room is " + str(numOfPeople),
    AvailableDeviceTypes.PASSWORD_WRONG_ALARM.value: lambda isOn: "The password wrong alarm is " + ("on" if isOn else "off"),
    AvailableDeviceTypes.POWER_CONSUMPTION.value: lambda powerConsumption: "The power consumption is " + str(powerConsumption) + " watts"
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

    @abstractmethod
    def getDevicesStates(self):
        pass

    @abstractmethod
    def updateColorLight(self, color: int , device_type: str, room_name: str) -> Results:
        pass