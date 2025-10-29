from pydantic import BaseModel, Field
from typing import Final


#TODO имеет смысл настроить доступные реакции для каждого чата
# только надо проверить, умеет ли SQLite сохранять эмоджи
class SettingsModel(BaseModel):
    MESSAGE_SYMBOLS_LIMIT: Final[int] = Field(..., alias='messageSymbolsLimit', frozen=True)
    MAX_MESSAGE_PER_MINUTE: Final[int] = Field(..., alias='maxMessagePerMinute', frozen=True)
    AVAILABLE_COMMANDS: Final[dict[str, str]] = Field(..., alias='availableCommands', frozen=True)
    AVAILABLE_REACTIONS: Final[tuple] = Field(..., alias='availableReactions')
