from enum import StrEnum, auto


class GifSettingsCallBackData(StrEnum):
    """
    Callback data для клавиатуры с настройками для гифок
    """
    WIDTH = auto()
    HEIGHT = auto()
    SPEED = auto()


class YesNoCallBackData(StrEnum):
    """
    Callback data для да/нет клавиатуры
    """
    YES = auto()
    NO = auto()
