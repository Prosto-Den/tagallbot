from bot import bot, memory
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReactionTypeEmoji, FSInputFile, CallbackQuery
from settings.settings import Settings
from utils.chat_utils import ChatUtils
from typing import NoReturn, Sequence
from sys import getsizeof
from aiogram.exceptions import TelegramBadRequest
from filters.custom_filters import CustomFilters
from utils.gif_creator import GIFCreator
from database.gif_settings_manager import GifSettingManager
from keyboards.inline_keyboard import gif_settings_keyboard, GifSettingsCallBackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from resources.resource_handler import ResourceHandler
from custom_types import ChatTypes, ChatActions


commands_router = Router()


class GifSettingsStateMachine(StatesGroup):
    """
    Машина состояний для изменения настроек создания гифок
    """
    width = State()
    height = State()
    speed = State()


@commands_router.message(Command(commands=['help']))
async def help(message: Message) -> None:
    """
    Выводит информацию о доступных командах (/help)
    :param message: Сообщение в телеграмме
    """
    text = '\n'.join([f'{key} - {value}' for key, value in ResourceHandler.get_available_commands().items()])
    await message.reply(text)


@commands_router.message(Command(commands=['spam']))
async def spam(message: Message) -> None:
    """
    Функция для спама сообщениями (/spam <n> <сообщение>)
    :param message: Сообщение в телеграмме
    """

    def __check_values(number: int, words: Sequence[str]) -> NoReturn | None:
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

    strings = ResourceHandler.get_strings_resources()
    logger_strings = ResourceHandler.get_logger_strings_resources()

    #TODO хочу вынести парсинг отсюда
    match message_text:
        case [_, number, *word]:
            try:
                number = int(number)
                if number > 1_000_000:
                    await message.reply(strings.too_large_number)
                    return
                __check_values(number, word)

                repeat_string = ' '.join(word) + enter
                # dont ask
                if ((getsizeof(repeat_string) - getsizeof(repeat_string[0]) + 1) * number
                        + getsizeof(repeat_string[0]) >= memory.max_ram):
                    await message.reply(strings.forget)
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
                bot.get_logger().warn(logger_strings.incorrect_message_amount.format(message.text))
                await message.reply(strings.incorrect_message_amount)

            except SyntaxError:
                bot.get_logger().warn(logger_strings.incorrect_message_use.format(message.text))
                await message.reply(strings.incorrect_command_use)
        case _:
            bot.get_logger().warn(logger_strings.incorrect_message_use.format(message.text))
            await message.reply(strings.incorrect_command_use)


@commands_router.message(Command(commands=['all']))
async def tag_all(message: Message) -> None:
    """
    Тегает всех пользователей в чате (/all)
    :param message: Сообщение в телеграмме
    """
    chat_id: int = message.chat.id

    usernames: list = await ChatUtils.get_chat_members(chat_id)
    text: str = ''.join(usernames)

    await message.reply(text, parse_mode='MarkdownV2')


@commands_router.message(F.text, CustomFilters.is_mentioned)
async def mention(message: Message) -> None:
    """
    Тегает всех пользователей чата при упоминании бота (@prostoTagAllBot)
    :param message: Сообщение в телеграмме
    """
    await tag_all(message)


@commands_router.message(Command(commands=['react']), CustomFilters.has_reply_message)
async def set_reaction(message: Message) -> None:
    """
    Ставит реакцию на сообщение (/react <эмоджи>)
    :param message: Сообщение в телеграмме
    """
    emoji = message.text.split(' ')[-1]
    reaction = ReactionTypeEmoji(emoji=emoji)
    strings = ResourceHandler.get_strings_resources()
    logger_strings = ResourceHandler.get_logger_strings_resources()
    try:
        bot.get_logger().info(logger_strings.try_to_set_reaction.format(emoji))
        await message.reply_to_message.react([reaction])
    except TelegramBadRequest:
        bot.get_logger().error(logger_strings.set_reaction_error.format(emoji))
        await message.reply(strings.incorrect_command_use)


@commands_router.message(Command(commands=['gif']), F.text)
async def create_and_send_gif(message: Message) -> None:
    """
    Создаёт гифку из текста и отправляет её (/gif <текст>)
    :param message: Сообщение в телеграмме
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text.split(' ')
    settings = await GifSettingManager.get_or_create_settings(user_id)
    strings = ResourceHandler.get_strings_resources()
    logger_strings = ResourceHandler.get_logger_strings_resources()

    await bot.send_chat_action(chat_id, ChatActions.UPLOAD_DOCUMENT)
    match message_text:
        case [_, *text]:
            text = ' '.join(text)
            gif_file = FSInputFile(GIFCreator.create_gif(text, settings.width, settings.height, settings.speed))
            await bot.send_document(chat_id, gif_file)

        case _:
            await message.reply(strings.incorrect_command_use)
            bot.get_logger().warn(logger_strings.command_error.format(message.text))

    GIFCreator.delete_gif()


@commands_router.message(Command(commands=['settings']))
async def gif_settings(message: Message) -> None:
    """
    Настройки для создания гифок (/settings). Работает только при личной переписке с ботом
    :param message: Сообщение в телеграмме
    """
    strings = ResourceHandler.get_strings_resources()
    if message.chat.type != ChatTypes.PRIVATE:
        await message.reply(strings.go_to_private)
    else:
        chat_id: int = message.chat.id
        user_id: int = message.from_user.id
        settings = await GifSettingManager.get_or_create_settings(user_id)
        await bot.send_message(chat_id, strings.gif_settings.format(settings.width, settings.height, settings.speed),
                               reply_markup=gif_settings_keyboard)


@commands_router.callback_query(F.data)
async def start_edit_settings(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Реакция на запрос поменять одну из настроек создателя гифок
    :param callback: Нажатие на кнопку
    :param state: Машина состояний
    """
    strings = ResourceHandler.get_strings_resources()
    logger_strings = ResourceHandler.get_logger_strings_resources()

    match callback.data:
        case GifSettingsCallBackData.WIDTH:
            await state.set_state(GifSettingsStateMachine.width)
            await callback.message.edit_text(strings.enter_width, reply_markup=None)

        case GifSettingsCallBackData.HEIGHT:
            await state.set_state(GifSettingsStateMachine.height)
            await callback.message.edit_text(strings.enter_height, reply_markup=None)

        case GifSettingsCallBackData.SPEED:
            await state.set_state(GifSettingsStateMachine.speed)
            await callback.message.edit_text(strings.enter_speed, reply_markup=None)

        case _:
            await callback.message.reply(strings.something_went_wrong)
            bot.get_logger().warn(logger_strings.callback_error.format(callback.message.text))


@commands_router.message(F.text, CustomFilters.is_any_state)
async def apply_settings(message: Message, state: FSMContext) -> None:
    """
    Применить введённое значение
    :param message: Сообщение в тг
    :param state: Машина состояний
    """
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id
    value: int = int(message.text)
    settings = await GifSettingManager.get_or_create_settings(user_id)
    strings = ResourceHandler.get_strings_resources()
    logger_strings = ResourceHandler.get_logger_strings_resources()

    if value > 0:
        match await state.get_state():
            case GifSettingsStateMachine.width:
                settings.width = value

            case GifSettingsStateMachine.height:
                # значение для высоты должно быть минимум 6
                if value >= 6:
                    settings.height = value
                else:
                    await message.reply(strings.incorrect_value)
                    bot.get_logger().warn(logger_strings.error_value.format(message.text))

            case GifSettingsStateMachine.speed:
                settings.speed = value

            case _:
                await message.reply(strings.something_went_wrong)
                bot.get_logger().warn(logger_strings.settings_update_error)
    else:
        await message.reply(strings.incorrect_value)
        bot.get_logger().warn(logger_strings.incorrect_value.format(message.text))

    await state.clear()
    await GifSettingManager.update_settings(settings)
    await bot.send_message(chat_id, strings.applied_successful)
