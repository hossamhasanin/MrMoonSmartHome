from abc import ABC, abstractmethod
from actions.firebase_controller.results import Results
from actions.firebase_controller.avialable_operations import AvailableOperations , AvailableColorsToSet , AcSupportedCommands
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
    AvailableDeviceTypes.DOOR.value: lambda state_dict , metadata: "The door is " + ("open" if state_dict["isOn"] else "closed"),
    AvailableDeviceTypes.TEMP.value: lambda state_dict , metadata: "The temperature is " + str(state_dict["temprature"]) + " celsius",
    AvailableDeviceTypes.LED.value: lambda state_dict , metadata: "The " + metadata["room_name"] + " normal lights are " + ("on" if state_dict["isOn"] else "off"),
    AvailableDeviceTypes.SMART_PLUG.value: lambda state_dict , metadata: "The " + metadata["room_name"] + " smart plug is " + ("on" if state_dict["isOn"] else "off"),
    AvailableDeviceTypes.RGBL.value: lambda state_dict , metadata: "The " + metadata["room_name"] + " RGB lights are " + ("on" if state_dict["isOn"] else "off") + " and has a " + AvailableColorsToSet.map_from_color_to_text(state_dict["colorId"]) + " color.",
    AvailableDeviceTypes.GAS_LEAK_ALARM.value: lambda state_dict , metadata: "The gas leak alarm is " + ("on" if state_dict["isOn"] else "off"),
    AvailableDeviceTypes.PEOPLE_COUNTER.value: lambda state_dict , metadata: "The number of people in the room is " + str(state_dict["peopleCounter"]),
    AvailableDeviceTypes.PASSWORD_WRONG_ALARM.value: lambda state_dict , metadata: "The password wrong alarm is " + ("on" if state_dict["isOn"] else "off")
    # AvailableDeviceTypes.POWER_CONSUMPTION.value: lambda powerConsumption: "The power consumption is " + str(powerConsumption) + " watts"
}

class IController(ABC):

    devices_ids = {}

    def _getDevicesIds(self, device_type: str, room_name: str) -> list[int]:
        query = room_name + "_" + device_type
        if room_name is not None and query in self.devices_ids:
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

    @abstractmethod
    def sendAcCommand(self, command: AcSupportedCommands , temperature: int , room_name: str) -> Results:
        pass

    @abstractmethod
    def getCurrentHomeTemperature(self) -> int:
        pass

    @abstractmethod
    def getAvgLastRecordedPowerConsumptions(self) -> float:
        pass