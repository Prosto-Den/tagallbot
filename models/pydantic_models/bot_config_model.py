from pydantic import BaseModel, Field


class BotConfigModel(BaseModel):
    API_HASH: str = Field(..., frozen=True)
    API_ID: int = Field(..., frozen=True)
    TOKEN: str = Field(..., frozen=True)
