from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.handlers.messages import START_MESSAGE
from src.logger import Logger


user_router = Router()
user_log = Logger("user_log", "log/user_handlers.log")


@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer(START_MESSAGE)
