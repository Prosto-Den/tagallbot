from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot import bot


class CustomFilters:
    @staticmethod
    async def is_mentioned(message: Message) -> bool:
        data = await bot.me()

        return f'@{data.username}' in message.text

    @staticmethod
    def is_private_chat(message: Message) -> bool:
        return message.chat.type == 'private'

    @staticmethod
    async def is_any_state(_, state: FSMContext) -> bool:
        current_state = await state.get_state()
        return current_state is not None
