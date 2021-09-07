from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
)

buttons = [
    KeyboardButton(text='Создать опрос'),
    KeyboardButton(text='Статистика'),
    KeyboardButton(text='Отмена')
]

start_keyboard.add(*buttons)
