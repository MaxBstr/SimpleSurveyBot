from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import survey_data

survey_keyboard = InlineKeyboardMarkup()
btn = InlineKeyboardButton(
    text="Закончить",
    callback_data=survey_data.new(
        status="complete",
        id="None"
    )
)
survey_keyboard.add(btn)
