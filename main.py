import asyncio
import logging
import sys
import dotenv
import os

from aiogram import Bot, Dispatcher

from src.handlers.users import user_router

dotenv.load_dotenv()


TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")
if TELEBOT_TOKEN is None:
    exit('ERROR: TELEBOT_TOKEN not found in ".env" file')


async def main() -> None:
    bot = Bot(TELEBOT_TOKEN)
    disp = Dispatcher()

    disp.include_router(user_router)

    await disp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
