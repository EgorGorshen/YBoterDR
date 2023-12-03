import os
import sys
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
import dotenv
from src.database import DataBase


data_base = DataBase("sqlite.db")
# Load env from .env file
dotenv.load_dotenv()

TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")
ADMINS_IDS = os.getenv("ADMINS_IDS")
YANDEX_TOKEN = os.getenv("YANDEX_API_TOKEN")

# Checkout if token exists in .env file
if TELEBOT_TOKEN is None:
    sys.exit('ERROR: TELEBOT_TOKEN not found in ".env" file')

if ADMINS_IDS is None:
    sys.exit('ERROR: ADMINS_IDS not found in ".env" file')

if YANDEX_TOKEN is None:
    sys.exit('ERROR: YANDEX_API_TOKEN not found in ".env" file')

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


async def set_user_commands():
    """set menu commands"""
    command_list = [
        BotCommand(
            command="start",
            description="Начните своё путешествие с YBoterDR. Эта команда откроет главное меню.",
        ),
        BotCommand(command="help", description="Получите подсказки и инструкции."),
        BotCommand(command="add_track_queue", description="Добавьте трек в очередь."),
        BotCommand(command="like", description="Отметьте понравившийся трек."),
        BotCommand(command="delete", description="Удалите последний добавленный трек."),
        BotCommand(command="find_track", description="Найдите трек по названию."),
        BotCommand(command="toast", description="Сказать тост и затушить музыку."),
        BotCommand(
            command="next_tracks", description="Посмотрите следующие треки в очереди."
        ),
        BotCommand(command="left", description="Сообщите, что вы покидаете вечеринку."),
        BotCommand(
            command="arrived", description="Сообщите, что вы прибыли на вечеринку."
        ),
    ]

    await bot.set_my_commands(command_list, BotCommandScopeDefault())
