from typing import Final
from utils.path_helper import PathHelper
from utils.json_reader import JsonReader
from models.pydantic_models.strings_model import StringsModel, LoggerStringsModel
from models.pydantic_models.stickers_model import StickersModel
from aiogram.types import FSInputFile
from enum import StrEnum, auto
import os


class Images:
    gru_image = 'gru.jpg'
    shrek_image = 'shrek_apologies.png'


class TempFiles:
    gif_file = 'bot_gif.gif'


class ResourceHandler:
    __AVAILABLE_COMMANDS: Final[str] = 'commands.json'
    __STRINGS: Final[str] = 'strings.json'
    __LOGGER_STRINGS: Final[str] = 'logger_strings.json'
    __STICKERS_FILE: Final[str] = 'stickers.json'

    class FileTypes(StrEnum):
        IMAGE = auto()
        TEMP = auto()

    @classmethod
    def get_available_commands(cls) -> dict[str, str]:
        """
        Выдать словарь с доступными командами для бота
        :return: Словарь с доступными командами
        """
        path = PathHelper.join(PathHelper.get_strings_folder(), cls.__AVAILABLE_COMMANDS)
        return JsonReader.read_as_dict(path)

    @classmethod
    def get_strings_resources(cls) -> StringsModel:
        """
        Выдать модель со строковыми ресурсами бота
        :return: Модель со строками
        """
        path = PathHelper.join(PathHelper.get_strings_folder(), cls.__STRINGS)
        return JsonReader.read_as_model(path, StringsModel)

    @classmethod
    def get_logger_strings_resources(cls) -> LoggerStringsModel:
        """
        Выдать модель со строковыми ресурсами для логгера
        :return: Модель
        """
        path = PathHelper.join(PathHelper.get_strings_folder(), cls.__LOGGER_STRINGS)
        return JsonReader.read_as_model(path, LoggerStringsModel)

    @classmethod
    def get_temp_file(cls, file_name: str) -> FSInputFile | None:
        """
        Возвращает файл из папки temp
        :param file_name: Название файла
        :return: FSInputFile, если файл с таким именем существует, иначе None
        """
        return cls.__get_file(cls.FileTypes.TEMP, file_name)

    @classmethod
    def get_image_file(cls, file_name: str) -> FSInputFile | None:
        """
        Возвращает файл из папки images
        :param file_name: название файла
        :return: FSInputFile, если файл с таким именем существует, иначе None
        """
        return cls.__get_file(cls.FileTypes.IMAGE, file_name)

    @classmethod
    def get_stickers_resources(cls) -> StickersModel:
        """
        Выдать модель с ID стикеров телеграмма
        :return: Модель
        """
        path = PathHelper.join(PathHelper.get_resources_folder(), cls.__STICKERS_FILE)
        return JsonReader.read_as_model(path, StickersModel)

    @classmethod
    def __get_file(cls, file_type: FileTypes, file_name: str) -> FSInputFile | None:
        """
        Возвращает объект файла, который можно прикрепить к сообщению
        :param file_type: Тип файла
        :param file_name: Имя файла
        :return: Объект с файлом, если путь к файлу существует, иначе None
        """
        match file_type:
            case cls.FileTypes.TEMP:
                path = PathHelper.join(PathHelper.get_temp_folder(), file_name)
            case cls.FileTypes.IMAGE:
                path = PathHelper.join(PathHelper.get_images_folder(), file_name)
            case _:
                return None
        if os.path.exists(path):
            return FSInputFile(path)
        return None
