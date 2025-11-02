from utils.singleton import Singleton
import logging
from typing import Final
from utils.path_helper import PathHelper
import os


class Logger(metaclass=Singleton):
    __LOG_FILENAME: Final[str] = 'log.log'
    __FORMAT: Final[str] = "%(asctime)s %(levelname)s %(message)s"

    def __init__(self) -> None:
        self.__logger = logging.getLogger()
        log_path = PathHelper.join(PathHelper.get_log_folder(), self.__LOG_FILENAME)

        if not os.path.exists(log_folder := PathHelper.get_log_folder()):
            os.mkdir(log_folder)

        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.__FORMAT)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

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

