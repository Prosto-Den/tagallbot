from bot import bot
from aiogram.filters import Command
from settings import COMMANDS, MAX_MESSAGES_PER_MINUTE, MESSAGE_SYMBOLS_LIMIT
from aiogram import Router, F
from getChatMembers import get_chat_members
from aiogram.types import Message
from typing import NoReturn
from filters import CustomFilters


messages_router = Router()


@messages_router.message(Command(commands=['help']))
async def help(message: Message) -> None:
    text = '\n'.join([f'{key} - {value}' for key, value in COMMANDS.items()])

    await message.reply(text)


@messages_router.message(Command(commands=['spam']))
async def spam(message: Message) -> None:
    # функция для проверки валидности значений
    def check_values(number: int, words: list) -> NoReturn | None:
        if number < 0:
            raise ValueError
        if len(words) < 1:
            raise SyntaxError

    chat_id: int = message.chat.id
    enter: str = '\n' if '\n' in message.text else ' '

    message_text: list[str] = message.text.replace('\n', ' ').split(' ')
    message_counter: int = 0

    match message_text:
        case [_, amount, *word]:
            try:
                number = int(amount)
                check_values(number, word)

                text: str = (' '.join(word) + enter) * number

                while text:
                    if len(text) > (index := MESSAGE_SYMBOLS_LIMIT) and text[index] not in (' ', '\n'):
                        for i in range(index, 0, -1):
                            if text[i] in (' ', '\n'):
                                index = i
                                break

                    await bot.send_message(chat_id, text[:index])
                    text = text[index:]

                    message_counter += 1
                    if message_counter >= MAX_MESSAGES_PER_MINUTE:
                        break

            except ValueError:
                await message.reply('Нормально кол-во сообщений укажи')

            except SyntaxError:
                await message.reply('Нормально команду напиши')
        case _:
            await message.reply('Нормально команду напиши')


@messages_router.message(Command(commands=['all']))
async def tag_all(message: Message) -> None:
    chat_id: int = message.chat.id

    usernames: list = await get_chat_members(chat_id)
    text: str = ''.join(usernames)

    await message.reply(text)


@messages_router.message(F.text, CustomFilters.is_mentioned)
async def mention(message: Message) -> None:
    await tag_all(message)
