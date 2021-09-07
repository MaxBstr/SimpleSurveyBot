from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import answer_data


def get_start_survey_keyboard(data: dict) -> InlineKeyboardMarkup:
    start_survey_keyboard = InlineKeyboardMarkup(row_width=1)
    answer_quantity = data["count"]

    for i in range(1, answer_quantity + 1):
        answer = data[f"answer{i}"]
        btn = InlineKeyboardButton(
            text=f"{answer[0]}",
            callback_data=answer_data.new(
                number=i,
                quantity=answer[1],
                id=answer[2]
            )
        )
        start_survey_keyboard.add(btn)

    return start_survey_keyboard
