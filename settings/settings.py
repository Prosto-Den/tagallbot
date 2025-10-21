from models.pydantic_models.bot_config_model import BotConfigModel
from models.pydantic_models.settings_model import SettingsModel
from utils.json_reader import JsonReader
from utils.path_helper import PathHelper
from typing import Final


class Settings:
    """
    Класс для работы с настройками бота
    """
    __SETTINGS_FILENAME: Final[str] = 'settings.json'
    __BOT_CONFIG_FILENAME: Final[str] = 'bot_config.json'
    __bot_config: BotConfigModel = None
    __settings: SettingsModel = None


    @classmethod
    def get_settings(cls) -> SettingsModel:
        """
        Получить модель с настройками
        """
        if cls.__settings is None:
            path = PathHelper.join(PathHelper.get_settings_folder(), cls.__SETTINGS_FILENAME)
            cls.__settings = JsonReader.read_as_model(path, SettingsModel)
        return cls.__settings

    @classmethod
    def get_bot_config(cls) -> BotConfigModel:
        """
        Получить модель с конфигурацией бота
        """
        if cls.__bot_config is None:
            path = PathHelper.join(PathHelper.get_settings_folder(), cls.__BOT_CONFIG_FILENAME)
            cls.__bot_config = JsonReader.read_as_model(path, BotConfigModel)
        return cls.__bot_config
