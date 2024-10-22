from aiogram import Bot, Dispatcher, F
from aiogram.methods import DeleteWebhook
from aiogram.filters import Command
from aiogram.types import Message
from chatMembers import get_chat_members
from settings.settings import TOKEN, MESSAGE_SYMBOLS_LIMIT, MAX_MESSAGES_PER_MINUTE
import asyncio


bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command(commands = ['spam']))
async def spam(message: Message) -> None:
    chat_id: int = message.chat.id

    message: list = message.text.split(' ')

    match message:
        case [_, number, *word]: 
            try:
                number = int(number)
                if number <= 0:
                    raise ValueError

                text: str = (' '.join(word) + ' ') * number

                """Ограничение на кол-во символов в сообщение - 2048.
                Этим алгоритмом разрываем сообщение на несколько таким образом, чтобы разрыв не оказался посреди слов"""
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
            
        case _:
            await bot.send_message(chat_id, 'Неправильно команду используешь')


@dp.message(Command(commands = ['all']))
async def tag_all(message: Message) -> None:
    chat_id: int = message.chat.id

    usernames: list = await get_chat_members(chat_id)
    text: str = ''.join(usernames)


    await message.reply(text)


@dp.message(F.text)
async def mention(message: Message) -> None:
    data = await bot.me()

    if f'@{data.username}' in message.text:
        await tag_all(message)


async def main():
    await bot(DeleteWebhook(drop_pending_updates = True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())