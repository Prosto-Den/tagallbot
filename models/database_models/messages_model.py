from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import Integer, Text


class Base(DeclarativeBase):
    # id чата. Будем брать id, который даёт Telegram
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)


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


class Admins(Base):
    """
    Таблица с данными по администраторам чатов
    """
    __tablename__ = 'admins'

    # id пользователя. Будем брать id, который даёт Telegram
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    # id чата. Будем брать id, который даёт Telegram
    chat_id: Mapped[int] = mapped_column('chat_id', ForeignKey('chats.id'))


class Messages(Base):
    """
    Модель для хранения сообщений чата
    """
    __tablename__ = 'messages'

    # id сообщения. Будем брать id, который даёт Telegram
    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    # текст сообщения. Будем хранить только уникальные тексты, не имеет смысла хранить одинаковые фразы
    text: Mapped[str] = mapped_column('text', Text, unique=True)
    # id чата. Внешний ключ к таблице Chats
    chat_id: Mapped[int] = mapped_column('chat_id', ForeignKey('chats.id'))
    admin_id: Mapped[int] = mapped_column('admin_id', ForeignKey('admins.id'))


