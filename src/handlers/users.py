from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from src.handlers.admin import inform_the_admins_about_the_arrival

from src.handlers.messages import REGISTRATION_ERROR_MESSAGE, START_MESSAGE
from src.logger import Logger
from src.utils import data_base, get_user_info_from_message


user_router = Router()
user_log = Logger("user_log", "log/user_handlers.log")


@user_router.message(CommandStart())
async def start(message: Message):
    """start mesage && reg user"""
    from_user = await get_user_info_from_message(message)
    if from_user is None:
        return

    id, full_name = from_user

    if not data_base.user_reg(id, full_name):
        await message.answer(REGISTRATION_ERROR_MESSAGE)
        return

    await message.answer(START_MESSAGE)


@user_router.message(Command("arrived"))
async def user_com(message: Message):
    from_user = await get_user_info_from_message(message)
    if from_user is None:
        return

    id, _ = from_user
    data_base.user_in(id)
    user = data_base.get_user(id)
    if user is None:
        await message.answer("Прежде чем начать пользование запустите команду /start")
        return

    await inform_the_admins_about_the_arrival(user)
