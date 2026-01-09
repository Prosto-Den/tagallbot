from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback_data import GifSettingsCallBackData, YesNoCallBackData


gif_settings_keyboard = InlineKeyboardMarkup(inline_keyboard= [[
    InlineKeyboardButton(text='↔️ Ширину', callback_data=GifSettingsCallBackData.WIDTH),
    InlineKeyboardButton(text='↕️ Высоту', callback_data=GifSettingsCallBackData.HEIGHT),
    InlineKeyboardButton(text='⏪ Скорость', callback_data=GifSettingsCallBackData.SPEED),
]])


ikb_confirm = InlineKeyboardMarkup(inline_keyboard = [[
    InlineKeyboardButton(text='Да', callback_data=YesNoCallBackData.YES),
    InlineKeyboardButton(text='Нет', callback_data=YesNoCallBackData.NO)
]])

