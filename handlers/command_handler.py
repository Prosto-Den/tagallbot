from bot import bot, memory
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReactionTypeEmoji, FSInputFile
from settings.settings import Settings
from utils.chat_utils import ChatUtils
from typing import NoReturn, Sequence
from sys import getsizeof
from aiogram.exceptions import TelegramBadRequest
from filters.custom_filters import CustomFilters
from utils.gif_creator import GIFCreator
from database.gif_settings_manager import GifSettingManager
from models.database_models import GifSettingsModel


commands_router = Router()


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

    #TODO хочу вынести парсинг отсюда
    match message_text:
        case [_, number, *word]:
            try:
                number = int(number)
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
    async def __prepare_and_send(words: list[str], model: GifSettingsModel) -> None:
        words = ' '.join(words)
        gif_file = FSInputFile(GIFCreator.create_gif(words, model.width, model.height, model.speed))
        await bot.send_document(chat_id, gif_file)

    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text.split(' ')
    settings = await GifSettingManager.get_or_create_settings(user_id)

    await bot.send_chat_action(chat_id, 'upload_document')
    print(message_text)
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
    if message.chat.type != 'private':
        await message.reply('Пойдём в лс пообщаемся')
