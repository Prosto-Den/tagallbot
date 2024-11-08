from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot import bot
from dataclasses import dataclass

class SupportMessage:
    @dataclass(slots=True)
    class MessageState:
        repeated_message: str = None
        sent_message: str = None
    
    __chats: dict[int, MessageState] = {}

    @staticmethod
    def get(chat_id: int) -> MessageState:
        if SupportMessage.__chats.get(chat_id):
            return SupportMessage.__chats[chat_id]
        SupportMessage.__chats[chat_id] = SupportMessage.MessageState()
        return SupportMessage.__chats[chat_id]



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

    @staticmethod
    async def is_repeated(message: Message) -> bool:
        messages = SupportMessage.get(message.chat.id)
        if messages.repeated_message == message.text and messages.sent_message != message.text:
            return True
        messages.repeated_message = message.text
        return False
