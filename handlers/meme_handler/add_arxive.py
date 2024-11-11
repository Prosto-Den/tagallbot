from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards import ikb_confirm, cancel_kb, test_cancel_kb
from bot import bot, conn
from aiogram import Router, F
from settings import add_hashtags
from database import Meme
from filters import CustomFilters


class AddArchive(StatesGroup):
    channel = State()
    admin = State()
    ensure = State()

add_archive_router = Router()

@add_archive_router.message(Command(commands=['add_arxive']))
async def add_archive(message: Message, state: FSMContext) -> None:
    await state.set_state(AddArchive.channel)
    if message.chat.type == 'private':
        await message.reply('Перешли мне мем из канала, который должен стать архивом для мемов', reply_markup = cancel_kb)

@add_archive_router.message(AddArchive.channel)
async def set_channel(message: Message, state: FSMContext) -> None:
    if not message.forward_from_chat:
        await message.reply('Да просто перешли мне ченить из канала', reply_markup=cancel_kb)
        return
    chat_id = message.forward_from_chat.id
    if bot.get_chat(chat_id):
        await message.reply('Okей, ты добавил меня в канал, но будь уверен что ты дал мне админские права'
                            ' (уверяю, мне можно доверить роль админа в твоём ламповом телеграм канале с мемами)\n\n'
                            'P.S. я смогу отправлять только новые сообщения из твоего архива')
        await state.set_state(AddArchive.admin)
        bot.push_archive(message)
        # await state.update_data(chat_id=chat_id)
        await state.clear()
    else:
        await message.reply('йо, меня вообще нет в этом канале, давай ка по новой', reply_markup=cancel_kb)


@add_archive_router.message(F.photo)
async def add_archive_photo(message: Message, state: FSMContext) -> None:
    print("add_archive_photo", message.message_id, message.chat.id)
    bot.add_meme(message)