from bot import bot, conn
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from random import choice
from database import Meme


get_meme_router = Router()


@get_meme_router.message(Command(commands = 'random'))
async def get_random_meme(message: Message) -> None:
    chat_id: int = message.chat.id

    memes: list[Meme] = conn.get_all_memes()
    random_meme: Meme = choice(memes)

    caption = 'Название: {:s}\nТеги: {:s}'.format(random_meme.name, random_meme.tags)

    await bot.send_photo(chat_id, random_meme.id, caption = caption)