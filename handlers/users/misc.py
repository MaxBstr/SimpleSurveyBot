from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from keyboards.default import start_keyboard
from handlers.users.start_survey import start_survey


@dp.message_handler(CommandStart(), state=None)
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
    await message.answer(text="Скрыто", reply_markup=types.ReplyKeyboardRemove())
