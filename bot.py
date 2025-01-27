from aiogram import Bot
import os
from dotenv import load_dotenv
load_dotenv()

# Инициализация бота
bot = Bot(os.environ['BOT_API'])