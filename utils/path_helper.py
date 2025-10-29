import os
from typing import Final


class PathHelper:
    """
    Класс для облегчения взаимодействия с путями
    """
    __root_path: str = None
    __INIT_FILE_NAME: Final[str] = "__init__.py"
    __SETTINGS_FOLDER: Final[str] = 'settings'
    __SESSION_FOLDER: Final[str] = 'session'

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
        Возвращает путь к папке с созданными сессиями
        """
        return cls.join(cls.get_root_path(), cls.__SESSION_FOLDER)

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
