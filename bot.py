from aiogram import Bot, Dispatcher, F
from aiogram.methods import DeleteWebhook
from aiogram.filters import Command
from aiogram.types import Message
from chatMembers import get_chat_members
from settings.settings import TOKEN
import asyncio


bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command(commands = ['all']))
async def tag_all(message: Message):
    chat_id: int = message.chat.id

    usernames: list = await get_chat_members(chat_id)
    text: str = ''.join(usernames)

    await message.reply(text)


@dp.message(F.text)
async def mention(message: Message) -> None:
    data = await bot.me()

    if f'@{data.username}' in message.text:
        await tag_all(message)


async def main():
    await bot(DeleteWebhook(drop_pending_updates = True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())