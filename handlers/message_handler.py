from bot import bot
from aiogram import Router, F
from aiogram.types import Message, ReplyParameters
from filters import CustomFilters, SupportMessage
from random import choice
from asyncio import sleep as asleep
from resources import ResourceHandler, Images
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

    if gru_photo := ResourceHandler.get_image_file(Images.gru_image):
        await bot.send_photo(chat_id, gru_photo, reply_to_message_id=message.message_id,
                            reply_parameters=ReplyParameters(message_id=message.message_id,
                                                            chat_id=chat_id,
                                                            quote=bot.saved_msg[chat_id]))
    else:
        strings = ResourceHandler.get_strings_resources()
        logger_strings = ResourceHandler.get_logger_strings_resources()
        await message.reply(strings.send_photo_error)
        bot.get_logger().warn(logger_strings.search_file_error)


@messages_router.message(F.text, CustomFilters.is_apologies_in_message)
async def send_shrek_apologies_image(message: Message) -> None:
    if shrek_photo := ResourceHandler.get_image_file(Images.shrek_image):
        chat_id: int = message.chat.id
        match_result = bot.saved_msg.get(message.chat.id)
        await bot.send_photo(chat_id, shrek_photo, reply_to_message_id=message.message_id,
                            reply_parameters=ReplyParameters(message_id=message.message_id,
                                                            chat_id=chat_id,
                                                            quote=match_result))
    else:
        strings = ResourceHandler.get_strings_resources()
        logger_strings = ResourceHandler.get_logger_strings_resources()
        await message.reply(strings.send_photo_error)
        bot.get_logger().warn(logger_strings.search_file_error)


@messages_router.message(F.text, CustomFilters.is_prekl)
async def prekl_message(message: Message) -> None:
    """
    Для "приколов" в чате. На да ответит что нужно, на нет тоже.
    :param message: Сообщение в тг
    """
    chat_id: int = message.chat.id
    match_result = bot.saved_msg.get(message.chat.id)
    strings = ResourceHandler.get_strings_resources()

    match match_result:
        case strings.yes:
            text: str = choice([strings.prekl1, strings.prekl2, strings.prekl3, strings.yes_image])
            match text:
                case strings.prekl3:
                    stickers = ResourceHandler.get_stickers_resources()
                    await bot.send_sticker(chat_id, stickers.kirkorov)

                case strings.yes_image:
                    image = ResourceHandler.get_image_file(Images.mandarin_image)
                    await bot.send_photo(chat_id, image)

                case _:
                    await bot.send_message(chat_id, text)

        case strings.no:
            await bot.send_message(chat_id, strings.prekl4)

        case strings.ok:
            await bot.send_message(chat_id, strings.kok)

        # just in case
        case _:
            strings = ResourceHandler.get_strings_resources()
            logger_strings = ResourceHandler.get_logger_strings_resources()
            await message.reply(strings.how_to_answer)
            bot.get_logger().warn(logger_strings.answer_error.format(message.text))


@messages_router.message(F.text, CustomFilters.is_yes_no_question)
async def SOSAL(message: Message) -> None:
    """
    Сосал?
    :param message:  Сообщение тг
    """
    chat_id = message.chat.id
    strings = ResourceHandler.get_strings_resources()
    await asleep(1)
    await bot.send_message(chat_id, strings.sosal)
