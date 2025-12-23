import os
from typing import Final
from enum import StrEnum, auto


class PathHelper:
    """
    Класс для облегчения взаимодействия с путями
    """
    class Resources(StrEnum):
        """
        Перечисление со всеми файлами внутри ресурсов
        """
        IMAGES = auto() # папка с картинками
        STICKERS = 'stickers.json' # стикеры
        STRINGS = 'strings.json' # строки

    __root_path: str = None
    __INIT_FILE_NAME: Final[str] = "__init__.py"
    __SETTINGS_FOLDER: Final[str] = 'settings'
    __SESSION_FOLDER: Final[str] = 'session'
    __LOG_FOLDER: Final[str] = 'log'
    __RESOURCES_FOLDER: Final[str] = 'resources'

    @classmethod
    def join(cls, *args: str) -> str:
        """
        Вспомогательный метод на замену обычному os.path.join
        :param args: Названия файлов для соединения
        :return: Путь к файлу
        """
        root, *other = args
        path = os.path.join(root, *other)
        return path.replace('\\', '/')

    @classmethod
    def get_root_path(cls) -> str:
        """
        Возвращает название коренной директории проекта
        """
        if cls.__root_path is None:
            cls.__root_path = cls.__find_root_path(os.path.dirname(__file__))
        return cls.__root_path

    @classmethod
    def get_settings_folder(cls) -> str:
        """
        Возвращает путь к директории с настройками
        """
        return cls.join(cls.get_root_path(), cls.__SETTINGS_FOLDER)

    @classmethod
    def get_session_folder(cls) -> str:
        """
        Возвращает путь к директории с созданными сессиями
        """
        return cls.join(cls.get_root_path(), cls.__SESSION_FOLDER)

    @classmethod
    def get_log_folder(cls) -> str:
        """
        Возвращает путь к директории с логами
        """
        return cls.join(cls.get_root_path(), cls.__LOG_FOLDER)

    @classmethod
    def get_resources_folder(cls) -> str:
        """
        Возвращает путь к директории с ресурсами
        """
        return cls.join(cls.get_root_path(), cls.__RESOURCES_FOLDER)

    @classmethod
    def get_images_folder(cls) -> str:
        """
        Возвращает путь к директории с изображениями
        """
        return cls.join(cls.get_resources_folder(), cls.Resources.IMAGES)

    @classmethod
    def get_strings_resource(cls) -> str:
        """
        Возвращает путь к файлу со строками
        """
        return cls.join(cls.get_resources_folder(), cls.Resources.STRINGS)

    @classmethod
    def get_stickers_resource(cls) -> str:
        """
        Возвращает путь к файлу с ID стикеров
        """
        return cls.join(cls.get_resources_folder(), cls.Resources.STICKERS)

    @classmethod
    def __find_root_path(cls, path: str) -> str:
        """
        Метод для нахождения корня проекта
        :param path: Путь для старта поиска
        :return: Путь к корню проекта
        """
        if cls.__INIT_FILE_NAME in os.listdir(path):
            return cls.__find_root_path(os.path.dirname(path))
        return path
