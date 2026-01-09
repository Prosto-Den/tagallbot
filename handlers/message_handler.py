from bot import bot
from aiogram import Router, F
from aiogram.types import Message, ReplyParameters, FSInputFile
from filters import CustomFilters, SupportMessage
from random import choice
from asyncio import sleep as asleep
from utils.path_helper import PathHelper
import re


#TODO поместить бы это всё дело в класс...
messages_router = Router()


@messages_router.message(F.text, CustomFilters.is_repeated)
async def repeat_message(message: Message) -> None:
    """
    Повторяет текст сообщения, если два последних сообщения в чате имеют одинаковый текст
    и написаны разными пользователями
    :param message: Сообщение в телеграмме
    """
    await bot.send_message(message.chat.id, message.text)
    SupportMessage.get(message.chat.id).sent_message = message.text


@messages_router.message(F.text, CustomFilters.is_gru_in_message)
async def send_gru_image(message: Message) -> None:
    chat_id: int = message.chat.id

    path_to_photo = PathHelper.join(PathHelper.get_images_folder(), 'gru.jpg')
    gru_photo = FSInputFile(path_to_photo)
    gru_text = re.search(r'\b[Гг][Рр][Юю]\b', message.text).group()

    await bot.send_photo(chat_id, gru_photo, reply_to_message_id=message.message_id,
                         reply_parameters=ReplyParameters(message_id=message.message_id,
                                                          chat_id=chat_id,
                                                          quote=gru_text))


@messages_router.message(F.text, CustomFilters.is_apologies_in_message)
async def send_shrek_apologies_image(message: Message) -> None:
    chat_id: int = message.chat.id
    match_result = bot.prekl_msg.get(message.chat.id)

    path_to_photo = PathHelper.join(PathHelper.get_images_folder(), 'shrek_apologies.png')
    shrek_photo = FSInputFile(path_to_photo)

    await bot.send_photo(chat_id, shrek_photo, reply_to_message_id=message.message_id,
                         reply_parameters=ReplyParameters(message_id=message.message_id,
                                                          chat_id=chat_id,
                                                          quote=match_result))

@messages_router.message(F.text, CustomFilters.is_prekl)
async def prekl_message(message: Message) -> None:
    """
    Для "приколов" в чате. На да ответит что нужно, на нет тоже.
    :param message: Сообщение в тг
    """
    chat_id: int = message.chat.id
    match_result = bot.prekl_msg.get(message.chat.id)

    match match_result:
        case 'да':
            text = choice(['манда', 'пизда', 'стикер'])

            if text == 'стикер':
                await bot.send_sticker(chat_id,
                                       'CAACAgIAAxkBAAEPr09pB5QDTCHtzfEGYoAtOcndtc03MQAC1RMAAhHkuUghZnRitjQWEzYE')
            else:
                await bot.send_message(chat_id, text)

        case 'нет':
            await bot.send_message(chat_id, 'минет')

        case 'ок':
            await bot.send_message(chat_id, 'кок')

        # just in case
        case _:
            await bot.send_message(chat_id, f'э бля а как ответить на это говно: {match_result}')
            bot.get_logger().warn(f"Не получилось ответить на сообщение {message.text}")

@messages_router.message(F.text, CustomFilters.is_yes_no_question)
async def SOSAL(message: Message) -> None:
    """
    Сосал?
    :param message:  Сообщение тг
    """
    chat_id = message.chat.id
    await asleep(1)
    await bot.send_message(chat_id, "Сосал?")
