from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateSurveyStates(StatesGroup):
    question = State()
    answers = State()
