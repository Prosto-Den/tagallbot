from aiogram import Bot, Dispatcher
from settings import TOKEN
from database import Connection


bot = Bot(TOKEN)
dp = Dispatcher()
conn = Connection()
