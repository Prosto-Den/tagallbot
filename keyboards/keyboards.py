from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

cancel_kb = ReplyKeyboardMarkup(keyboard = [
    [
        KeyboardButton(text = '/cancel')
    ]
], resize_keyboard = True)
