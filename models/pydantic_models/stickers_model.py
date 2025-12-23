from pydantic import BaseModel, Field


class StickersModel(BaseModel):
    kirkorov_sticker: str = Field(..., frozen=True)
