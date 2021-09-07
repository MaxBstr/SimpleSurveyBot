from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import db_tools
from states import CreateSurveyStates
from keyboards.default import start_keyboard
from keyboards.inline import survey_keyboard
from handlers.users.start_survey import start_survey
from keyboards.inline.callback_data import survey_data


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    msg = message.text.split()
    if len(msg) == 2:
        survey_id = int(msg[1])
        await start_survey(message, survey_id)
        return

    await message.answer(
        text=(
            'Добро пожаловать!\n'
            'Данный бот предназначан для создания опросов.\n'
            'Выбери дальнейшую опцию :)\n'
        ),
        reply_markup=start_keyboard
    )


@dp.message_handler(text='Отмена', state="*")
async def cancel_call(message: types.Message, state: FSMContext):
    await message.answer(
        text="Меню скрыто",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(text='Создать опрос', state=None)
async def create_survey(message: types.Message):
    await message.answer(
        text=(
            "Кол-во вариантов ответа варьируется от 2 до 6.\n"
            "Введите вопрос:"
        )
    )
    await CreateSurveyStates.first()


@dp.message_handler(state=CreateSurveyStates.question, content_types=types.ContentTypes.TEXT)
async def get_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await message.answer('Введите 1 вариант ответа:')
    await CreateSurveyStates.next()


async def complete_survey(input_type: Union[types.CallbackQuery, types.Message], state: FSMContext):
    is_callback = True if isinstance(input_type, types.CallbackQuery) else False
    if len(await state.get_data()) < 3:
        text = "Кол-во вариантов должно быть больше 2"
        if is_callback:
            await input_type.message.answer(
                text=text,
            )
        else:
            await input_type.answer(text=text)
        return

    data = await state.get_data()
    survey_id = await db_tools.set_data(data)

    text_link = (
        f"Спасибо за создание опроса!\n"
        f"Ссылка на опрос: <a>https://t.me/survey_statistics_bot?start={survey_id}</a>"
    )

    if is_callback:
        await input_type.message.answer(text=text_link)
    else:
        await input_type.answer(text=text_link)

    await state.finish()


@dp.callback_query_handler(survey_data.filter(status="complete"), state=CreateSurveyStates.answers)
async def finish_survey(call: types.CallbackQuery, state: FSMContext):
    await complete_survey(call, state)


@dp.message_handler(state=CreateSurveyStates.answers, content_types=types.ContentTypes.TEXT)
async def get_answers(message: types.Message, state: FSMContext):
    answer = message.text
    state_data_len = len(await state.get_data())

    await state.update_data({f"answer{state_data_len}": answer})
    info = await state.get_data()
    print(info)

    if state_data_len == 6:
        await complete_survey(message, state)
        return

    if state_data_len == 5:
        text = "Введите последний вариант ответа!"
    else:
        text = (
            f"Вариант №{state_data_len} успешно сохранен!\n"
            f"Введите вариант ответа №{state_data_len + 1}"
            f"или закончите создание опроса"
        )
    await message.answer(
        text=text,
        reply_markup=survey_keyboard
    )
