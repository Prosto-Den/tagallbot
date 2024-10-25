from bot import bot
from aiogram.filters import Command
from settings import COMMANDS, MAX_MESSAGES_PER_MINUTE
from aiogram import Router
from getChatMembers import get_chat_members
from getMeme import get_random_meme
from aiogram.types import Message, FSInputFile
from aiogram import F


messages_router = Router(name ='messages')


@messages_router.message(Command(commands=['help']))
async def help(message: Message) -> None:
    text = '\n'.join([f'{key} - {value}' for key, value in COMMANDS.items()])

    await message.reply(text)


@messages_router.message(Command(commands=['spam']))
async def spam(message: Message) -> None:
    def check_values(number: int, lst: list) -> None:
        if number < 0:
            raise ValueError

        if len(lst) == 0:
            raise SyntaxError

    chat_id: int = message.chat.id

    message: list = message.text.split(' ')

    match message:
        case [_, number, *word]:
            try:
                number: int = int(number)

                check_values(number, word)

                text: str = (' '.join(word) + ' ') * number

                """Ограничение на кол-во символов в сообщение - 2048.
                Этим алгоритмом разрываем сообщение на несколько таким образом, чтобы разрыв не оказался посреди слова"""
                message_counter = 0
                while text:
                    index = 2048

                    if len(text) > 2048 and text[index] not in (' ', '\n'):
                        for i in range(2048, 0, -1):
                            if text[i] in (' ', '\n'):
                                index = i
                                break

                    await bot.send_message(chat_id, text[:index])
                    text = text[index:]

                    message_counter += 1
                    if message_counter >= MAX_MESSAGES_PER_MINUTE:
                        break

            except ValueError:
                await bot.send_message(chat_id, 'Нормально кол-во сообщений укажи')

            except SyntaxError:
                await bot.send_message(chat_id, 'Нормально команду напиши')
        case _:
            await bot.send_message(chat_id, 'Неправильно команду используешь')


@messages_router.message(Command(commands = ['all']))
async def tag_all(message: Message) -> None:
    chat_id: int = message.chat.id

    usernames: list = await get_chat_members(chat_id)
    text: str = ''.join(usernames)

    await message.reply(text)


@messages_router.message(Command(commands=['meme']))
async def send_meme(message: Message) -> None:
    chat_id = message.chat.id

    text = message.text.split(' ')
    text.pop(0)

    text = ' '.join(text)

    meme = FSInputFile(get_random_meme())

    match meme.filename.split('.')[-1]:
        case 'gif':
            await bot.send_animation(chat_id, meme, caption=text)

        case 'mp4':
            await bot.send_video(chat_id, meme, caption=text)

        case _:
            await bot.send_photo(chat_id, meme, caption=text)


@messages_router.message(F.text)
async def mention(message: Message) -> None:
    data = await bot.me()

    if f'@{data.username}' in message.text:
        await tag_all(message)