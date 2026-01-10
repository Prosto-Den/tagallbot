from enum import StrEnum, auto


class ChatActions(StrEnum):
    """
    Перечисление действий, совершаемых при отправке сообщения
    """
    TYPING = auto()
    UPLOAD_PHOTO = auto()
    RECORD_VIDEO = auto()
    UPLOAD_VIDEO = auto()
    RECORD_VOICE = auto()
    UPLOAD_VOICE = auto()
    UPLOAD_DOCUMENT = auto()
    CHOOSE_STICKER = auto()
    FIND_LOCATION = auto()
    RECORD_VIDEO_NOTE = auto()
    UPLOAD_VIDEO_NOTE = auto()
