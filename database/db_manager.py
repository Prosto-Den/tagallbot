from sqlalchemy import create_engine
from sqlalchemy import Engine
from utils.singleton import Singleton
from sqlalchemy.orm import Session
from models.database_models.messages_model import Chats, Admins, Base
from sqlalchemy import select, update, insert, Executable, Row
from aiogram.types import Message
from typing import Type, Sequence, Any


class DBManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__engine = create_engine('sqlite:///./base.db')
        self.__connection = self.__engine.connect()

        Base.metadata.create_all(self.__engine)

    def __del__(self) -> None:
        self.__connection.close()

    def execute_with_fetchall(self, statement: Executable) -> Sequence[Row[Any]]:
        cursor = self.__connection.execute(statement)
        return cursor.fetchall()

    def execute_with_fetchone(self, statement: Executable) -> Sequence[Row[Any]]:
        cursor = self.__connection.execute(statement)
        return cursor.fetchone()

    def execute_with_commit(self, statement: Executable) -> None:
        self.__connection.execute(statement)
        self.__connection.commit()
