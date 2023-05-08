from enum import Enum

class AvailableOperations(Enum):
    SWITCH = 0
    SETTING_COLOR = 1
    SETTING_AC_COMMAND = 2

class AcSupportedCommands(Enum):
    AC_LOWER_TEMPRATURE = 0
    AC_RISE_TEMPRATURE = 1



class AvailableColorsToSet(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PINCK = 5
    SKY_BLUE = 6
    WHITE = 7

    @staticmethod
    def map_from_text_to_color(text: str):
        if text == "red":
            return AvailableColorsToSet.RED.value
        elif text == "green":
            return AvailableColorsToSet.GREEN.value
        elif text == "yellow":
            return AvailableColorsToSet.YELLOW.value
        elif text == "blue":
            return AvailableColorsToSet.BLUE.value
        elif text == "pink":
            return AvailableColorsToSet.PINCK.value
        elif text == "sky blue":
            return AvailableColorsToSet.SKY_BLUE.value
        elif text == "white":
            return AvailableColorsToSet.WHITE.value
        else:
            return AvailableColorsToSet.NONE.value
    
    @staticmethod
    def map_from_color_to_text(color: int):
        if color == AvailableColorsToSet.RED.value:
            return "red"
        elif color == AvailableColorsToSet.GREEN.value:
            return "green"
        elif color == AvailableColorsToSet.YELLOW.value:
            return "yellow"
        elif color == AvailableColorsToSet.BLUE.value:
            return "blue"
        elif color == AvailableColorsToSet.PINCK.value:
            return "pink"
        elif color == AvailableColorsToSet.SKY_BLUE.value:
            return "sky blue"
        elif color == AvailableColorsToSet.WHITE.value:
            return "white"
        else:
            return "none"