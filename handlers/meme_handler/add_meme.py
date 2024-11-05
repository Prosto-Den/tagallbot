from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import ikb_confirm
from bot import bot, conn
from aiogram import Router, F
from settings import add_hashtags
from database import Meme


# машина состояний
class AddMeme(StatesGroup):
    picture = State()
    name = State()
    tags = State()
    confirm = State()


# роутер для отслеживания сообщений
add_meme_router = Router()


@add_meme_router.message(Command(commands=['add']))
async def add_meme(message: Message, state: FSMContext) -> None:
    await state.set_state(AddMeme.picture)

    if message.chat.type in ('group', 'supergroup'):
        user_id: int = message.from_user.id
        await message.delete()
        await bot.send_message(user_id, 'Отправь мне мем')

    elif message.chat.type == 'private':
        await message.reply('Отправь мне мем')


@add_meme_router.message(AddMeme.picture, F.photo)
async def save_picture(message: Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id

    photo_id: str = message.photo[0].file_id

    await state.update_data(photo_id=photo_id)

    await bot.send_message(user_id, "Введи название мема")

    await state.set_state(AddMeme.name)


@add_meme_router.message(AddMeme.name)
async def set_name(message: Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id

    name: str = message.text

    await state.update_data(name=name)

    await state.set_state(AddMeme.tags)

    await bot.send_message(user_id, 'Добавить теги к мему?', reply_markup=ikb_confirm)


@add_meme_router.callback_query(F.data.startswith('con_'), AddMeme.tags)
async def add_tags(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()

    user_id: int = call.from_user.id

    match call.data.replace('con_', ''):
        case 'yes':
            await call.message.edit_text("Добавьте теги без значка #. "
                                         "Теги указывай через пробел, запятые можешь не ставить :)")
        case 'no':
            data: dict = await state.get_data()
            meme = Meme(data['photo_id'], data['name'])

            await check_data(user_id, meme, state)


@add_meme_router.message(AddMeme.tags, F.text)
async def set_tags(message: Message, state: FSMContext) -> None:
    hashtags: str = add_hashtags(message.text)
    data: dict = await state.get_data()

    meme = Meme(data['photo_id'], data['name'], hashtags)

    await check_data(message.from_user.id, meme, state)


@add_meme_router.callback_query(F.data.startswith('con_'), AddMeme.confirm)
async def save_meme(call: CallbackQuery, state: FSMContext) -> None:
    data: dict = await state.get_data()
    meme: Meme = data['meme']

    match call.data.replace('con_', ''):
        case 'yes':
            await conn.add_meme(meme)
            await call.message.edit_text('Мем успешно сохранён :)')

        case 'no':
            await call.message.edit_text('Мем не сохранён :(')

    await state.clear()


async def check_data(user_id: int, meme: Meme, state: FSMContext) -> None:
    caption = (f'Название: {meme.name}\n'
               f'Теги: {meme.tags}')

    await bot.send_message(user_id, "Проверим введённую информацию")
    await bot.send_photo(chat_id=user_id, photo=meme.id, caption=caption)
    await bot.send_message(user_id, 'Сохранить мем?', reply_markup=ikb_confirm)

    await state.set_data({'meme': meme})
    await state.set_state(AddMeme.confirm)