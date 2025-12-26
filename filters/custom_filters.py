from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dataclasses import dataclass
from bot import bot
from random import randint
import re


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
    """
    Класс с фильтрами
    """
    @staticmethod
    async def is_mentioned(message: Message) -> bool:
        """
        Был ли бот упомянут в сообщении
        :param message: Сообщение
        :return: True - "пинг" бота был найден в сообщении, иначе False
        """
        data = await bot.me()
        return f'@{data.username}' in message.text

    @staticmethod
    def is_private_chat(message: Message) -> bool:
        """
        Является ли этот чат личным (приватным)
        :param message: Сообщение
        :return: True - чат личный, иначе False
        """
        return message.chat.type == 'private'

    @staticmethod
    async def is_any_state(_, state: FSMContext) -> bool:
        """
        Находится ли машина состояний в хоть каком-то состоянии
        :param state: Состояние машины
        :return: True - если состояние не None, иначе False
        """
        current_state = await state.get_state()
        return current_state is not None

    @staticmethod
    async def is_repeated(message: Message) -> bool:
        """
        Является ли это сообщение повторением предыдущего
        :param message: Сообщение в телеграмме
        :return: True - если текст сообщения одинаков с текстом предыдущего сообщения, а
                 также написано другим пользователем, иначе False
        """
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
        """
        Является ли сообщение ответом на другое сообщение
        :param message: Сообщение
        :return: True - сообщение отвечает на какое-то сообщение, иначе False
        """
        return message.reply_to_message is not None

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
        """
        Содержит ли сообщение вопрос, на который можно ответить да/нет?
        :param message: Сообщение из тг
        :return: True - содержит, иначе False
        """
        # работает регулярка не всегда правильно, но большую часть определяет
        last_sentence = re.search(r'([\w~ ,]+?)\?+$', message.text.lower())
        if last_sentence:
            last_sentence = last_sentence.group(1)
        else:
            return False

        if re.search(r'(почему|как|откуда|куда|зачем|где|сколько|кто|что|когда|какой)', last_sentence):
            return False
        return True

    @staticmethod
    async def random(chance: int) -> bool:
        """
        Выполнить обработку сообщения с некоторым шансом
        :param chance: Шанс обработки сообщения (<=0 - сообщение обработано не будет,
        >=100 - сообщение будет обработано
        :return: True - обработать сообщение, False - не обрабатывать
        """
        return randint(0, 99) < chance

    @staticmethod
    async def is_gru_in_message(message: Message) -> bool:
        return re.search(r'\b[Гг][Рр][Юю]\b', message.text) is not None

    @staticmethod
    async def is_apologies_in_message(message: Message) -> bool:
        pattern = r'(?i)\b(?:извини(?:те)?|простите|прошу\s+прощения|приношу\s+извинения|сорри|прости)\b'
        return re.search(pattern, message.text) is not None
