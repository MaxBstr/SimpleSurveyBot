from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tortoise import Tortoise

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def load_db():
    await Tortoise.init(
        db_url=config.DB_URL,
        modules={"models": ["utils.db_api.models"]}
    )
    await Tortoise.generate_schemas()
