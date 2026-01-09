from aiogram import Bot, Dispatcher
from settings import Settings
from utils.singleton import Singleton
from utils.logger import Logger


class ProstoBot(Bot, metaclass=Singleton):
    """
    Класс бота
    """
    def __init__(self, token: str):
        super().__init__(token=token)
        self.prekl_msg: dict[int, str] = dict()
        self.__logger = Logger()

    #TODO мб логгер надо не сюда выносить
    def get_logger(self) -> Logger:
        """
        Получить логгер
        """
        return self.__logger

bot = ProstoBot(Settings.get_bot_config().TOKEN)
dp = Dispatcher()
