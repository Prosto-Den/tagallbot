from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards import ikb_confirm, cancel_kb, test_kb
from bot import bot, conn
from aiogram import Router, F
from settings import add_hashtags
from database import Meme
from filters import CustomFilters

# not sure if this is a good idea to place this var here
ARCHIVE_CHATS: set[int] = set()

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
                            ' (уверяю, мне можно доверить роль админа в твоём ламповом телеграм канале с мемами)', reply_markup=test_kb)
        await state.set_state(AddArchive.admin)
        ARCHIVE_CHATS.add(chat_id)
        await state.update_data(chat_id=chat_id)
        await state.set_state(AddArchive.ensure)
    else:
        await message.reply('йо, меня вообще нет в этом канале, давай ка по новой', reply_markup=cancel_kb)


@add_archive_router.message(AddArchive.ensure, Command(commands=['test']))
async def test_admin(message: Message, state: FSMContext) -> None:
    chat_id = await state.get_data()['chat_id']
    if message.from_user.id in bot.get_chat_administrators(chat_id):
        await message.reply('Ура, ты админ в канале, можно добавлять мемы в архив', reply_markup=[cancel_kb, test_kb])
        messages = await bot.get_chat_history(chat_id, limit=1000)
        max_attempts = 10
        for _ in range(max_attempts):
            random_msg = random.choice(messages)
            if random_msg.photo:
                random_photo = random.choice(random_msg.photo)
                await bot.send_photo(message.chat.id, random_photo.file_id)
                return
    else:
        await message.reply('Нету тебя в администрации этого канала, попробуй снова', reply_markup=[cancel_kb, test_kb])