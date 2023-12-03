from aiogram import Router

from src.dataclasses import User
from src.logger import Logger
from src.utils import ADMINS_IDS, bot


admin_router = Router()
admin_log = Logger("admin_log", "log/admin.log")


@admin_log.log_function_call
async def inform_the_admins_about_the_arrival(user: User):
    """inform admins about user comming"""
    for id in ADMINS_IDS:
        await bot.send_message(chat_id=id, text=f"Пользоваетль {user.name} приехал")
