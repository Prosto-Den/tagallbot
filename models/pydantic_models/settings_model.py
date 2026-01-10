from pydantic import BaseModel, Field
from typing import Final


class SettingsModel(BaseModel):
    MESSAGE_SYMBOLS_LIMIT: Final[int] = Field(..., alias='messageSymbolsLimit', frozen=True)
    MAX_MESSAGE_PER_MINUTE: Final[int] = Field(..., alias='maxMessagePerMinute', frozen=True)
    DATE_FORMAT: Final[str] = Field(..., alias='dateFormat', frozen=True)
    DATE_FORMAT_WITH_TIME: Final[str] = Field(..., alias='dateFormatWithTime', frozen=True)
