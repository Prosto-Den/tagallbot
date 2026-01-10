from pydantic import BaseModel, Field


class StickersModel(BaseModel):
    """
    Модель для хранения ID стикеров из Телеграмма
    """
    kirkorov: str = Field(alias='kirkorov', frozen=True)
