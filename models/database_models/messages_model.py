from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import Integer, Text
from typing import override
from enum import StrEnum, auto


class ModelTypes(StrEnum):
    """
    Перечисление с типами таблиц
    """
    BASE = auto()
    CHATS = auto()
    ADMINS = auto()
    #MESSAGES = auto()


class Base(DeclarativeBase):
    """
    Базовый класс для моделей
    """
    #TODO я не знаю, как по-нормальному сделать, но я не хочу писать метод для каждого класса
    @property
    def type(self) -> ModelTypes:
        """
        Выдать тип модели
        :return: Тип Модели
        """
        return ModelTypes.BASE


class Chats(Base):
    """
    Модель с данными по чатам
    """
    __tablename__ = 'chats'

    # id чата. Будем брать id, который даёт Telegram
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    # название чата
    name: Mapped[str] = mapped_column('name', Text)
    # id создателя чата. Будем брать id, который даёт Telegram
    owner: Mapped[int] = mapped_column('owner', Integer)


    @override
    @property
    def type(self) -> ModelTypes:
        return ModelTypes.CHATS


class Admins(Base):
    """
    Таблица с данными по администраторам чатов
    """
    __tablename__ = 'admins'

    # id пользователя. Будем брать id, который даёт Telegram
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    # id чата. Будем брать id, который даёт Telegram
    chat_id: Mapped[int] = mapped_column('chat_id', ForeignKey('chats.id'))


    @override
    @property
    def type(self) -> ModelTypes:
        return ModelTypes.ADMINS


# class Messages(Base):
#     """
#     Модель для хранения сообщений чата
#     """
#     __tablename__ = 'messages'
#
#     # id сообщения. Будем брать id, который даёт Telegram
#     id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
#     # текст сообщения. Будем хранить только уникальные тексты, не имеет смысла хранить одинаковые фразы
#     text: Mapped[str] = mapped_column('text', Text, unique=True)
#     # id чата. Внешний ключ к таблице Chats
#     chat_id: Mapped[int] = mapped_column('chat_id', ForeignKey('chats.id'))
#     # id администратора. Внешний ключ к таблице Admins
#     admin_id: Mapped[int] = mapped_column('admin_id', ForeignKey('admins.id'))
#
#
#     @override
#     @property
#     def type(self) -> ModelTypes:
#         return ModelTypes.MESSAGES
