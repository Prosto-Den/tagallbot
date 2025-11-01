from typing import Literal, Final
from pyrogram import utils, Client
from pyrogram.types import ChatMember
from utils.path_helper import PathHelper
from utils.file_manipulator import FileManipulator
from settings.settings import Settings
from typing import Final


class ChatUtils:
    #TODO возможно стоит вынести в настройки
    USER_LINK: Final[str] = '[{}](tg://user?id={})'

    #TODO написать потом утилиту для строк. Пока размещу тут, мне надо быстро
    #TODO это явно не всё, надо будет расширять
    MAPPING: dict[str, str] = {'*': r'\*', '|': r'\|', '_': r'\_', '{': r'\{', '}': r'\}',
                               '(': r'\(', ')' : r'\)', '[': r'\[', ']': r'\]', '-': r'\-',
                               '.': r'\.', '`': r'\`', '#': r'\#', '+': '\+', '!': r'\!'}

    """
    Утилиты для работы с чатом
    """
    @staticmethod
    def __get_peer_type_new(peer_id: int) -> Literal['user', 'channel', 'chat']:
        """
        Функция для определения типа чата. Создана на замену функции из библиотеки
        :param peer_id: ID чата
        :return: Тип чата
        """
        peer_id_str = str(peer_id)
        if not peer_id_str.startswith("-"):
            return "user"
        elif peer_id_str.startswith("-100"):
            return "channel"
        else:
            return "chat"

    @classmethod
    async def get_chat_members(cls, chat_id: int) -> list:
        """
        Функция для получения никкеймов пользователей в чате.
        :param chat_id: ID чата
        :return: Список с никкеймами/ID пользователей чата
        """
        result: list[str] = list()

        # TODO создание сессии надо вынести в отдельный класс
        # Заменяем нерабочую функцию из библиотеки на свою
        utils.get_peer_type = cls.__get_peer_type_new
        # размещаем все сессии в одной папке
        session_folder = PathHelper.get_session_folder()
        FileManipulator.create_folder(session_folder)

        API_ID: Final[int] = Settings.get_bot_config().API_ID
        API_HASH: Final[str] = Settings.get_bot_config().API_HASH
        TOKEN: Final[str] = Settings.get_bot_config().TOKEN

        async with Client(str(chat_id), API_ID, API_HASH, workdir=session_folder, bot_token=TOKEN) as app:
            member: ChatMember
            async for member in app.get_chat_members(chat_id):
                if member.user and not member.user.is_bot:
                    #TODO экранирование строки потом поменять
                    name = member.user.first_name
                    for char, escaped in cls.MAPPING.items():
                        name = name.replace(char, escaped)
                    user_link = cls.USER_LINK.format(name, member.user.id)
                    result.append(''.join([user_link, '\n']))
        return result
