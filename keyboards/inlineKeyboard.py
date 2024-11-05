from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikb_confirm = InlineKeyboardMarkup(inline_keyboard = [[
    InlineKeyboardButton(text = 'Да', callback_data = 'con_yes'),
    InlineKeyboardButton(text = 'Нет', callback_data = 'con_no')
]])

