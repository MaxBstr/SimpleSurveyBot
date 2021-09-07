from aiogram import types

from loader import dp
from keyboards.inline import get_statistics_keyboard
from keyboards.inline.callback_data import survey_data
from utils.db_api import get_statistics, get_survey_question_by_id, is_zero_surveys


@dp.message_handler(text="Статистика", state=None)
async def choose_survey_for_stats(message: types.Message):
    is_empty = await is_zero_surveys()
    if is_empty:
        await message.answer("На данный момент опросов нет!")
        return

    await message.answer(
        text="Выберите опрос, для которого хотите получить статистику:",
        reply_markup=await get_statistics_keyboard()
    )


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'page')
async def characters_page_callback(call: types.CallbackQuery):
    page = int(call.data.split('#')[1])
    chat_id = int(call.message.chat.id)
    await call.message.delete()

    await dp.bot.send_message(
        chat_id=chat_id,
        text="Выберите опрос, для которого хотите получить статистику:",
        reply_markup=await get_statistics_keyboard(page)
    )


@dp.callback_query_handler(survey_data.filter(status="show"), state=None)
async def show_statistics(call: types.CallbackQuery):
    await call.message.delete()

    survey_id = int(call.data.split(":")[-1])
    data = await get_statistics(survey_id)
    question = await get_survey_question_by_id(survey_id)

    text = f"Статистика по опросу <b><i>{question}</i></b>:\n"
    for answer, quantity, _ in data.values():
        text += f"Ответ <i>{answer}</i> был выбран <b>{quantity}</b> раз\n"

    await call.message.answer(text=text)
