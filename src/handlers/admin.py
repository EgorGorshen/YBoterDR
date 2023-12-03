from aiogram import Router

from src.dataclasses import User
from src.utils import ADMINS_IDS, bot


admin_router = Router()


async def inform_the_admins_about_the_com_t_or_left_f(user: User, com: bool):
    """inform admins about user comming"""
    for id in ADMINS_IDS:
        if com:
            await bot.send_message(chat_id=id, text=f"Пользоваетль {user.name} приехал")
        else:
            await bot.send_message(chat_id=id, text=f"Пользоваетль {user.name} уезжает")
