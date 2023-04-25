from enum import Enum

class Results(Enum):
    DONE_SUCCESSFULLY = 0
    NOT_ALLOWED_OPERATION_ON_DEVICE = 1
    DEVICE_NOT_FOUND = 2