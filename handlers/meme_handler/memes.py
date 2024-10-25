from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from getMeme import get_random_meme
from bot import bot


meme_router = Router(name = 'memes')


@meme_router.message(Command(commands=['meme']))
async def send_meme(message: Message) -> None:
    chat_id = message.chat.id

    text = message.text.split(' ')
    text.pop(0)

    text = ' '.join(text)

    meme = FSInputFile(get_random_meme())

    match meme.filename.split('.')[-1]:
        case 'gif':
            await bot.send_animation(chat_id, meme, caption=text)

        case 'mp4':
            await bot.send_video(chat_id, meme, caption=text)

        case _:
            await bot.send_photo(chat_id, meme, caption=text)