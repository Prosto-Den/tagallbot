from aiogram import Bot, Dispatcher
from settings import Settings
from utils.singleton import Singleton


# i suggest custom class is a good way to structure and incapsulate program logic
#TODO проверить, что singleton ничего не сломал
class ProstoBot(Bot, metaclass=Singleton):
    """
    Класс бота
    """
    def __init__(self, token: str):
        super().__init__(token=token)
        self.prekl_msg: dict[int, str] = dict()

bot = ProstoBot(Settings.get_bot_config().TOKEN)
dp = Dispatcher()
