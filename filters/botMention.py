from aiogram.types import Message
from bot import bot


class CustomFilters:
    @staticmethod
    async def is_mentioned(message: Message) -> bool:
        data = await bot.me()

        return f'@{data.username}' in message.text


