from typing import Type, TypeVar
from pydantic import BaseModel
import json


T = TypeVar('T', bound=BaseModel)


class JsonReader:
    """
    Класс для считывания данных из json файлов
    """
    @staticmethod
    def read_as_model(path: str, model: Type[T]) -> T:
        """
        Считывает данные из json в модель
        :param path: Путь к json файлу
        :param model: Тип модель, в которую будут записаны данные
        :return: Объект модели с данными
        """
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return model(**data)
