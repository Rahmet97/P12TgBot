import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
storage = MemoryStorage()
bot = Bot(bot_token)
dp = Dispatcher(bot, storage=storage)