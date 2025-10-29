from bot import bot, memory
from aiogram.filters import Command
from settings import Settings
from aiogram import Router, F
from utils.chat_utils import ChatUtils
from aiogram.types import Message, ReactionTypeEmoji
from typing import NoReturn, Sequence
from filters import CustomFilters, SupportMessage
from sys import getsizeof
from random import choice
from asyncio import sleep as asleep

#TODO поместить бы это всё дело в класс...

messages_router = Router()


@messages_router.message(Command(commands=['help']))
async def help(message: Message) -> None:
    """
    Выводит информацию о доступных командах (/help)
    :param message: Сообщение в телеграмме
    """
    text = '\n'.join([f'{key} - {value}' for key, value in Settings.get_settings().AVAILABLE_COMMANDS.items()])
    await message.reply(text)


@messages_router.message(Command(commands=['spam']))
async def spam(message: Message) -> None:
    """
    Функция для спама сообщениями (/spam <n> <сообщение>)
    :param message: Сообщение в телеграмме
    """
    def check_values(number: int, words: Sequence[str]) -> NoReturn | None:
        """
        Функция для проверки валидности значений
        :param number: Кол-во сообщений. Должно быть больше 0
        :param words: Последовательность слов для повтора. Длина последовательности должна быть больше 0
        :return: Ничего, если всё нормально, поднимает исключение, если что-то не так
        """
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
                if ((getsizeof(repeat_string) - getsizeof(repeat_string[0]) + 1) * number
                        + getsizeof(repeat_string[0]) >= memory.max_ram):
                    await message.reply('забыл...')
                    return
                
                text: str = repeat_string * number
                while text:
                    if (len(text) > (index := Settings.get_settings().MESSAGE_SYMBOLS_LIMIT) and
                            text[index] not in (' ', '\n')):
                        for i in range(index, 0, -1):
                            if text[i] in (' ', '\n'):
                                index = i
                                break

                    await bot.send_message(chat_id, text[:index])
                    text = text[index:]
                    message_counter += 1
                    if message_counter >= Settings.get_settings().MAX_MESSAGE_PER_MINUTE:
                        break

            except ValueError:
                await message.reply('Нормально кол-во сообщений укажи')

            except SyntaxError:
                await message.reply('Нормально команду напиши')
        case _:
            await message.reply('Нормально команду напиши')


@messages_router.message(Command(commands=['all']))
async def tag_all(message: Message) -> None:
    """
    Тегает всех пользователей в чате (/all)
    :param message: Сообщение в телеграмме
    """
    chat_id: int = message.chat.id

    usernames: list = await ChatUtils.get_chat_members(chat_id)
    text: str = ''.join(usernames)

    await message.reply(text)


@messages_router.message(Command(commands = ['react']), CustomFilters.has_reply_message)
async def set_reaction(message:Message) -> None:
    """
    Ставит реакцию на сообщение (/react <эмоджи>)
    :param message: Сообщение в телеграмме
    """
    emoji: str = message.text.split(' ')[-1]

    if emoji in Settings.get_settings().AVAILABLE_REACTIONS:
        reaction = ReactionTypeEmoji(emoji = emoji)
        await message.reply_to_message.react([reaction])
    else:
        await message.reply('Нормально команду используй')


@messages_router.message(F.text, CustomFilters.is_mentioned)
async def mention(message: Message) -> None:
    """
    Тегает всех пользователей чата при упоминании бота (@prostoTagAllBot)
    :param message: Сообщение в телеграмме
    """
    await tag_all(message)


@messages_router.message(F.text, CustomFilters.is_repeated)
async def repeat_message(message: Message) -> None:
    """
    Повторяет текст сообщения, если два последних сообщения в чате имеют одинаковый текст
    и написаны разными пользователями
    :param message: Сообщение в телеграмме
    """
    await bot.send_message(message.chat.id, message.text)
    SupportMessage.get(message.chat.id).sent_message = message.text

@messages_router.message(F.text, CustomFilters.is_prekl)
async def KOK(message: Message) -> None:
    """
    Для "приколов" в чате. На да ответит что нужно, на нет тоже.
    :param message: Сообщение в тг
    """
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

@messages_router.message(F.text, CustomFilters.is_yes_no_question)
async def SOSAL(message: Message) -> None:
    """
    Сосал?
    :param message:  Сообщение тг
    """
    chat_id = message.chat.id
    await asleep(1)
    await bot.send_message(chat_id, "Сосал?")
