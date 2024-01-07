from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from src.dataclasses import User
from src.utils import ADMINS_IDS, bot, get_volume, set_status


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


@admin_router.message(Command("volume"), F.text.split()[1].isnumeric())
async def volume(message: Message):
    """change volume"""
    if message.chat.id not in ADMINS_IDS:
        return

    if message.text is None:
        return

    text = message.text.strip().strip("/")

    if len(text.split()) != 2:
        await message.answer(
            "Не правильный запрос нужно ввести /volume [уровень звука не превышающий 100]"
        )

    _, volume = text

    volume = int(volume) if 10 < int(volume) < 100 else get_volume()

    set_status(f"volume {volume}")

    await message.answer(f"Меняем звук на {volume}")
