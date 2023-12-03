import os
import sys
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import dotenv
from src.database import DataBase


data_base = DataBase("sqlite.db")
# Load env from .env file
dotenv.load_dotenv()
TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")
ADMINS_IDS = os.getenv("ADMINS_IDS")

# Checkout if token exists in .env file
if TELEBOT_TOKEN is None:
    sys.exit('ERROR: TELEBOT_TOKEN not found in ".env" file')

if ADMINS_IDS is None:
    sys.exit('ERROR: ADMINS_IDS not found in ".env" file')

ADMINS_IDS = json.loads(ADMINS_IDS)

# Create bot and dispatcher instances
bot = Bot(TELEBOT_TOKEN)
dispatcher = Dispatcher()


async def get_user_info_from_message(message: Message) -> tuple[int, str] | None:
    """get && checkout user info from message"""
    from_user = message.from_user
    chat_id = message.chat.id
    if from_user is None:
        await message.answer("Информация о пользователе недоступна.")
        return

    if chat_id is None or from_user.full_name is None:
        await message.answer("Отсутствует идентификатор пользователя или полное имя.")
        return

    return chat_id, from_user.full_name
