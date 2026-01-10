from typing import Type, TypeVar, Any
from pydantic import BaseModel
import json


T = TypeVar('T', bound=BaseModel)


class JsonReader:
    """
    Класс для считывания данных из json файлов
    """
    @classmethod
    def read_as_model(cls, path: str, model: Type[T]) -> T:
        """
        Считывает данные из json в pydantic модель
        :param path: Путь к json файлу
        :param model: Тип модели, в которую будут записаны данные
        :return: Объект модели с данными
        """
        return model(**cls.read_as_dict(path))

    @staticmethod
    def read_as_dict(path: str) -> dict[str, Any]:
        """
        Считать данные из json в словарь
        :param path: Путь к json файлу
        :return: Словарь с данными
        """
        with open(path, 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
        return data
