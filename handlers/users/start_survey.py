from aiogram import types
from aiogram.dispatcher.filters.builtin import Regexp

from loader import dp
from utils.db_api import db_tools
from keyboards.inline import get_start_survey_keyboard


async def start_survey(message: types.Message, survey_id: int):
    is_exist = await db_tools.check_survey_exists(survey_id)
    if not is_exist:
        await message.answer("Опроса с данным id не существует.")
        return

    is_answered = await db_tools.check_answered(
        user_id=int(message.from_user.id),
        survey_id=survey_id
    )
    if is_answered:
        await message.answer(text="Вы уже прошли данный опрос!")
        return

    data = await db_tools.get_statistics(survey_id)
    data["count"] = len(data)

    question = await db_tools.get_survey_question_by_id(survey_id)
    await message.answer(
        text=(
            f"Вопрос: {question}\n"
            f"Выберите вариант ответа:"
        ),
        reply_markup=get_start_survey_keyboard(data)
    )


@dp.callback_query_handler(Regexp(r'^answer:\d:\d+:\d+$'))
async def handle_survey_answer(call: types.CallbackQuery):
    data = call.data.split(':')
    answer_id = int(data[-1])
    user_id = int(call.from_user.id)

    await db_tools.update_data({'ans_id': answer_id, 'user_id': user_id})
    await call.message.edit_text(
        text="Спасибо за прохождение опроса!",
        reply_markup=types.InlineKeyboardMarkup()
    )
