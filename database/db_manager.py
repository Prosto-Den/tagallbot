from sqlalchemy import create_engine
from sqlalchemy import Engine
from utils.singleton import Singleton
from sqlalchemy.orm import Session
from models.database_models.messages_model import Messages, Chats, Admins, Base
from sqlalchemy import select, update, insert
from aiogram.types import Message


class DBManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.__engine: Engine = create_engine("sqlite:///./base.db")
        self.__session = Session(self.__engine)

        Base.metadata.create_all(self.__engine)


    def add_message(self, message: Message) -> None:
        pass
