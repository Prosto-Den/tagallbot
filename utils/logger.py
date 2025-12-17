from utils.singleton import Singleton
import logging
from typing import Final
from utils.path_helper import PathHelper
import os
import datetime


def today() -> str:
    return datetime.datetime.today().strftime("%d-%m-%Y")


class Logger(metaclass=Singleton):
    __FORMATTER: Final[logging.Formatter] = logging.Formatter("%(asctime)s %(levelname)s %(messages)s",
                                                              datefmt='%d-%m-%Y %H:%M:%S')
    __LOGGER_LEVEL: Final[int] = logging.DEBUG

    def __init__(self) -> None:
        self.__logger = logging.getLogger()

        if not os.path.exists(log_folder := PathHelper.get_log_folder()):
            os.mkdir(log_folder)

        self.__logger.setLevel(self.__LOGGER_LEVEL)

        self.__stream_handler = logging.StreamHandler()
        self.__stream_handler.setFormatter(self.__FORMATTER)
        self.__stream_handler.setLevel(self.__LOGGER_LEVEL)

        self.__file_handler = self.__create_file_handler()

        self.__logger.addHandler(self.__stream_handler)
        self.__logger.addHandler(self.__file_handler)

    def __create_file_handler(self) -> logging.FileHandler:
        """
        Создаёт хендлер для записи логов в файл
        :return: Хендлер для записи логов в файл
        """
        log_path = PathHelper.join(PathHelper.get_log_folder(), ''.join([today(), '.log']))
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(self.__FORMATTER)
        file_handler.setLevel(self.__LOGGER_LEVEL)
        return logging.FileHandler(log_path)

    def update_file_handler(self) -> None:
        """
        Метод для обновления хендлера файлов. Нужен, чтобы задать новое имя для файлов
        """
        self.__logger.removeHandler(self.__file_handler)
        self.__file_handler = self.__create_file_handler()
        self.__logger.addHandler(self.__file_handler)

    def info(self, message: str) -> None:
        """
        Записать информационное сообщение.
        :param message: Сообщение
        """
        self.__logger.info(message)

    def warn(self, message: str) -> None:
        """
        Записать предупреждающее сообщение.
        :param message: Сообщение
        """
        self.__logger.warning(message)

    def debug(self, message: str) -> None:
        """
        Записать отладочную информацию.
        :param message: Сообщение
        """
        self.__logger.debug(message)

    def error(self, message: str) -> None:
        """
        Записать информацию об ошибке.
        :param message: Сообщение
        """
        self.__logger.error(message, exc_info=True, stacklevel=2)

