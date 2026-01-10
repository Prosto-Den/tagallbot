from enum import StrEnum, auto


class ChatTypes(StrEnum):
    PRIVATE = auto()
    GROUP = auto()
    SUPERGROUP = auto()
    CHANNEL = auto()
