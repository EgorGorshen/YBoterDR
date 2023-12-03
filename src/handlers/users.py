from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.handlers.messages import REGISTRATION_ERROR_MESSAGE, START_MESSAGE
from src.logger import Logger
from src.utils import data_base


user_router = Router()
user_log = Logger("user_log", "log/user_handlers.log")


@user_router.message(CommandStart())
async def start(message: Message):
    from_user = message.from_user
    if from_user is None:
        await message.answer("Информация о пользователе недоступна.")
        return

    if from_user.id is None or from_user.full_name is None:
        await message.answer("Отсутствует идентификатор пользователя или полное имя.")
        return

    # Call the user_reg method without await if it is a synchronous method
    if not data_base.user_reg(from_user.id, from_user.full_name):
        await message.answer(REGISTRATION_ERROR_MESSAGE)
        return  # If registration fails, do not proceed to send START_MESSAGE

    await message.answer(START_MESSAGE)
