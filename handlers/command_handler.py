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
    text = '\n'.join([f'{key} - {value}' for key, value in Settings.get_settings().AVAILABLE_COMMANDS.items()])
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

    #TODO хочу вынести парсинг отсюда
    match message_text:
        case [_, number, *word]:
            try:
                number = int(number)
                if number > 1_000_000:
                    await message.reply('В штангу дал?')
                    return
                __check_values(number, word)

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
                bot.get_logger().warn(f"Неправильное кол-во сообщений: {message.text}")
                await message.reply('Нормально кол-во сообщений укажи')

            except SyntaxError:
                bot.get_logger().warn(f"Неправильное использование команды: {message.text}")
                await message.reply('Нормально команду напиши')
        case _:
            bot.get_logger().warn(f"Неправильное использование команды: {message.text}")
            await message.reply('Нормально команду напиши')


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
    try:
        bot.get_logger().info(f'Пробуем поставить реакцию: {emoji}')
        await message.reply_to_message.react([reaction])
    except TelegramBadRequest:
        bot.get_logger().error(f'Ошибка при попытке поставить реакцию: {emoji}')
        await message.reply('Нормально команду используй')


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

    await bot.send_chat_action(chat_id, 'upload_document')
    match message_text:
        case [_, *text]:
            text = ' '.join(text)
            gif_file = FSInputFile(GIFCreator.create_gif(text, settings.width, settings.height, settings.speed))
            await bot.send_document(chat_id, gif_file)

        case _:
            await message.reply('Нормально команду используй')
            bot.get_logger().warn(f'Не удалось выполнить команду {message.text}')

    GIFCreator.delete_gif()


@commands_router.message(Command(commands=['settings']))
async def gif_settings(message: Message) -> None:
    """
    Настройки для создания гифок (/settings). Работает только при личной переписке с ботом
    :param message: Сообщение в телеграмме
    """
    if message.chat.type != 'private':
        await message.reply('Пойдём в лс пообщаемся')
    else:
        chat_id: int = message.chat.id
        user_id = message.from_user.id
        settings = await GifSettingManager.get_or_create_settings(user_id)
        text = ("🛠Текущие настройки🛠:\n"
                "↔️ Ширина гифки: {}\n"
                "↕️ Высота гифки: {}\n"
                "⏪ Скорость гифки: {}\n"
                "Что хочешь поменять?")
        await bot.send_message(chat_id, text.format(settings.width, settings.height, settings.speed),
                               reply_markup=gif_settings_keyboard)


@commands_router.callback_query(F.data)
async def start_edit_settings(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Реакция на запрос поменять одну из настроек создателя гифок
    :param callback: Нажатие на кнопку
    :param state: Машина состояний
    """
    match callback.data:
        case GifSettingsCallBackData.WIDTH:
            await state.set_state(GifSettingsStateMachine.width)
            await callback.message.edit_text('Введите ширину гифки', reply_markup=None)

        case GifSettingsCallBackData.HEIGHT:
            await state.set_state(GifSettingsStateMachine.height)
            await callback.message.edit_text('Введите высоту гифки', reply_markup=None)

        case GifSettingsCallBackData.SPEED:
            await state.set_state(GifSettingsStateMachine.speed)
            await callback.message.edit_text('Введите скорость гифки', reply_markup=None)

        case _:
            await callback.message.reply('Что-то пошло не так :(')
            bot.get_logger().warn(f'Не удалось обработать запрос: {callback.message.text}')


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

    if value > 0:
        match await state.get_state():
            case GifSettingsStateMachine.width:
                settings.width = value

            case GifSettingsStateMachine.height:
                # значение для высоты должно быть минимум 6
                if value >= 6:
                    settings.height = value
                else:
                    await message.reply('Недопустимо')
                    bot.get_logger().warn(f'Не удалось применить значение: {message.text}')

            case GifSettingsStateMachine.speed:
                settings.speed = value

            case _:
                await message.reply('Что-то пошло не так :(')
                bot.get_logger().warn('Не удалось обновить настройки пользователя')
    else:
        await message.reply('Недопустимо')
        bot.get_logger().warn(f'Введено недопустимое значение для параметра: {message.text}')

    await state.clear()
    await GifSettingManager.update_settings(settings)
    await bot.send_message(chat_id, 'Настройки успешно применены!')
