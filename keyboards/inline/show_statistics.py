from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

from math import ceil

from keyboards.inline.callback_data import survey_data
from utils.db_api import get_surveys, get_surveys_count


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = 'Начало'
    previous_page_label = 'Назад'
    current_page_label = '-{}-'
    next_page_label = 'Вперед'
    last_page_label = 'Конец'

    def __init__(self, page_count, current_page=1, data_pattern='{page}'):
        super().__init__(page_count, current_page, data_pattern)


async def get_statistics_keyboard(page: int = 1) -> InlineKeyboardMarkup:
    limit = 1
    offset = limit * (page - 1)

    data = await get_surveys(offset, limit)
    page_count = ceil(await get_surveys_count() / limit)

    paginator = MyPaginator(page_count, page, "page#{page}")

    for survey_id, question in data.items():
        btn = InlineKeyboardButton(question, callback_data=survey_data.new(
            status="show",
            id=survey_id
        ))
        paginator.add_before(btn)

    paginator.add_after(InlineKeyboardButton("Скрыть", callback_data="close_stats"))
    return paginator.markup
