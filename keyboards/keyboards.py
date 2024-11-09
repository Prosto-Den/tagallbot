from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

cancel_kb = ReplyKeyboardMarkup(keyboard = [
    [
        KeyboardButton(text = '/cancel')
    ]
], resize_keyboard = True) 

# only used to make sure bot can access telegram archive and send photos
test_cancel_kb = ReplyKeyboardMarkup(keyboard = [
    [
        KeyboardButton(text = '/test'),
        KeyboardButton(text = '/cancel')
    ]
], resize_keyboard = True)
