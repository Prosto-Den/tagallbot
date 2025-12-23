from pydantic import BaseModel, Field


class StringsModel(BaseModel):
    yes: str = Field(..., frozen=True)
    no: str = Field(..., frozen=True)
    ok: str = Field(..., frozen=True)
    yes_prekls: list[str] = Field(..., frozen=True)
    no_prekl: str = Field(frozen=True)
    kok: str = Field(frozen=True)
    sticker: str = Field(frozen=True)
    sosal_question: str = Field(..., frozen=True)
