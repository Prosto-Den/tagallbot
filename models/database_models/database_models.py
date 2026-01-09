from dataclasses import dataclass
from abc import ABC, abstractmethod
from aiosqlite import Row
from typing import override


class BaseDBModel(ABC):
    @abstractmethod
    def as_tuple(self) -> tuple:
        """
        Выдать данные модели в виде кортежа
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def create_from_row(row: Row) -> 'BaseDBModel':
        """
        Создать объект модели из данных, пришедших их БД
        :param row: Ряд
        :return:
        """
        pass


@dataclass(slots=True)
class GifSettingsModel(BaseDBModel):
    """
    Модель для хранения данных настроек для создания гифки.
    Для каждого пользователя создаются свои настройки
    """
    user_id: int        # id пользователя
    height: int  = 50   # высота гифки
    width: int   = 300  # ширина гифки
    speed: int = 5    # скорость текста

    @override
    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.user_id, self.height, self.width, self.speed

    @staticmethod
    @override
    def create_from_row(row: Row) -> 'GifSettingsModel':
        return GifSettingsModel(row[0], row[1], row[2], row[3])
