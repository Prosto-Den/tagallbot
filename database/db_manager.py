import aiosqlite as asql
from models.database_models import BaseDBModel
from utils.path_helper import PathHelper
from typing import Type, TypeVar


T = TypeVar('T', bound=BaseDBModel)


class DBManager:
    """
    Класс для работы с БД
    """
    @classmethod
    async def execute(cls, statement: str, *args) -> None:
        """
        Выполнить запрос
        :param statement: Текст запроса
        :param args: Параметры запроса
        """
        async with asql.connect(PathHelper.get_database_path()) as conn:
            cursor: asql.Cursor
            async with conn.cursor() as cursor:
                await cursor.execute(statement, *args)
                await conn.commit()

    @classmethod
    async def execute_one(cls, statement: str, model: Type[T], *args) -> T | None:
        """
        Выполнить запрос и получить один элемент данных
        :param statement: Текст запроса
        :param model: Тип для выходной модели
        :param args: Параметры запроса
        :return: Модель типа model, наполненная данными из БД, если запрос выполнился удачно, иначе None
        """
        result = await cls.execute_many(statement, model, *args)
        return result[0] if result else None

    @classmethod
    async def execute_many(cls, statement: str, model: Type[T], *args) -> list[T]:
        """
        Выполнить запрос и получить несколько элементов с данными
        :param statement: Текст запроса
        :param model: Тип для выходной модели
        :param args: Параметры запроса
        :return: Список с моделями типа model, если запрос выполнился удачно, иначе пустой список
        """
        async with asql.connect(PathHelper.get_database_path()) as conn:
            cursor: asql.Cursor
            async with conn.cursor() as cursor:
                await cursor.execute(statement, args)
                rows = await cursor.fetchall()
        return [model.create_from_row(row) for row in rows]
