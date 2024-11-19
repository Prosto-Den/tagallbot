from bot import bot, memory
from aiogram.filters import Command
from settings import COMMANDS, MAX_MESSAGES_PER_MINUTE, MESSAGE_SYMBOLS_LIMIT
from aiogram import Router, F
from getChatMembers import get_chat_members
from aiogram.types import Message, ReactionTypeEmoji
from typing import NoReturn
from filters import CustomFilters, SupportMessage
from random import choice
from sys import getsizeof

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
                if number > 1_000_000:
                    await message.reply('В штангу дал?')
                    return
                check_values(number, word)

                repeat_string = ' '.join(word) + enter
                # dont ask
                if  (getsizeof(repeat_string) - getsizeof(repeat_string[0]) + 1) * number + getsizeof(repeat_string[0]) >= memory.max_ram:
                    await message.reply('забыл...')
                    return
                
                text: str = repeat_string * number
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


@messages_router.message(Command(commands = ['react']), CustomFilters.has_reply_message)
async def set_reaction(message:Message) -> None:
    emoji: str = message.text.split(' ')[1]

    reaction = ReactionTypeEmoji(emoji = emoji)

    await message.reply_to_message.react([reaction])


@messages_router.message(F.text, CustomFilters.is_mentioned)
async def mention(message: Message) -> None:
    await tag_all(message)


@messages_router.message(F.text, CustomFilters.is_repeated)
async def support(message: Message) -> None:
    await bot.send_message(message.chat.id, message.text)
    SupportMessage.get(message.chat.id).sent_message = message.text


@messages_router.message(F.text, CustomFilters.is_prekl)
async def KOK(message: Message) -> None:
    chat_id: int = message.chat.id
    match_result = bot.prekl_msg.get(message.chat.id)

    match match_result:
        case 'да':
            text = choice(['манда', 'пизда'])
            await bot.send_message(chat_id, text)

        case 'нет':
            await bot.send_message(chat_id, 'минет')

        case 'ок':
            await bot.send_message(chat_id, 'кок')
        
        # just in case
        case _:
            await bot.send_message(chat_id, f'э бля а как ответить на это говно: {match_result}')
            raise ValueError(f"Invalid match result: {match_result} in message: {message.text}")
