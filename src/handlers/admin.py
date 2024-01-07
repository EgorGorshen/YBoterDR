from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.dataclasses import User
from src.utils import ADMINS_IDS, bot, set_status


admin_router = Router()


async def inform_the_admins_about_the_com_t_or_left_f(user: User, com: bool):
    """inform admins about user comming"""
    for id in ADMINS_IDS:
        if com:
            await bot.send_message(chat_id=id, text=f"Пользоваетль {user.name} приехал")
        else:
            await bot.send_message(chat_id=id, text=f"Пользоваетль {user.name} уезжает")


@admin_router.message(Command("next"))
async def next_track(message: Message):
    if message.chat.id not in ADMINS_IDS:
        return

    set_status("next")

    await message.answer("Переключили")
