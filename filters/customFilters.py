from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot import bot
import re

from dataclasses import dataclass


class SupportMessage:
    @dataclass(slots=True)
    class MessageState:
        repeated_message: str = None
        sent_message: str = None
        user_id: int = None

    __chats: dict[int, MessageState] = {}

    @classmethod
    def get(cls, chat_id: int) -> MessageState:
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

        if (messages.repeated_message == message.text and
            messages.sent_message != message.text and
            message.from_user.id != messages.user_id):
            return True

        messages.repeated_message = message.text
        messages.user_id = message.from_user.id
        return False

    @staticmethod
    async def has_reply_message(message: Message) -> bool:
        return message.reply_to_message is not None

    @staticmethod
    async def is_archive(message: Message) -> bool:
        print("custom filter: is_archive,", message.chat.id, bot.arxive_chats)
        return message.chat.id in bot.arxive_chats

    @staticmethod
    async def is_prekl(message: Message) -> bool:
        match = re.match(r'\b(ок|да|нет)[., ?!]*$', message.text.lower())

        if match:
            bot.prekl_msg[message.chat.id] = match.group(1)
            return True

        bot.prekl_msg[message.chat.id] = ""
        return False

    @staticmethod
    async def is_yes_no_question(message: Message):
        last_sentence = re.search(r'([\w~ ,]+?)\?$', message.text.lower())
        if last_sentence:
            last_sentence = last_sentence.group(1)
        else:
            return False

        if re.search(r'(почему|как|откуда|куда|зачем|где|сколько|кто|что|когда|какой)', last_sentence):
            return False
        return True
        