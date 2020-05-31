from enum import Enum, auto


class MemorySegType(Enum):
    """
    Details different memory segments of VM
    """

    M_ARGUMENT = auto()
    M_LOCAL = auto()
    M_STATIC = auto()
    M_CONSTANT = auto()
    M_THIS = auto()
    M_THAT = auto()
    M_POINTER = auto()
    M_TEMP = auto()
