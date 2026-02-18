from pydantic import BaseModel, Field


class StickersModel(BaseModel):
    """
    Модель для хранения ID стикеров из Телеграмма
    """
    kirkorov: str = Field(alias='kirkorov', frozen=True)
    gru: str = Field(alias='gru', frozen=True)
    mandarin: str = Field(alias='mandarin', frozen=True)
    shrek: str = Field(alias='shrek', frozen=True)
