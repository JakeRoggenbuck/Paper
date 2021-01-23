from enum import Enum
from termcolor import colored


VERSION = 0.1


class FutureImplementation:
    def __init__(self, version_expected: int = 0):
        self.message = f"FutureImplementation"
        if version_expected != 0:
            self.message = f"{self.message} {version_expected}"

    def __repr__(self):
        return colored(self.message, "red")


class OrderedEnum(Enum):
    """Refrence https://docs.python.org/3/library/enum.html#orderedenum"""

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class RunType(OrderedEnum):
    NORMAL = 0
    VERBOSE = 1
    DEBUG = 2
    STEP_THROUGH_DEBUG = 3
