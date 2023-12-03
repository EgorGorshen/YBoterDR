"""
dP    dP  888888ba             dP                     888888ba   888888ba
Y8.  .8P  88    `8b            88                     88    `8b  88    `8b
 Y8aa8P  a88aaaa8P' .d8888b. d8888P .d8888b. 88d888b. 88     88 a88aaaa8P'
   88     88   `8b. 88'  `88   88   88ooood8 88'  `88 88     88  88   `8b.
   88     88    .88 88.  .88   88   88.  ... 88       88    .8P  88     88
   dP     88888888P `88888P'   dP   `88888P' dP       8888888P   dP     dP 

telegram bot for parties, its functionality can be found in the README file
"""
import asyncio
import logging
import sys
import os
import dotenv
from aiogram import Bot, Dispatcher
from src.handlers.users import user_router

# Load env from .env file
dotenv.load_dotenv()
TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")

# Checkout if token exists in .env file
if TELEBOT_TOKEN is None:
    sys.exit('ERROR: TELEBOT_TOKEN not found in ".env" file')


async def run_bot():
    """Initialize and run the telegram bot."""
    # Create bot and dispatcher instances
    bot = Bot(TELEBOT_TOKEN)
    dispatcher = Dispatcher()

    # Include routers for handling user interactions
    dispatcher.include_router(user_router)

    # Start polling bot
    await dispatcher.start_polling(bot)


def setup_logging():
    """Cofig base logging"""
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def main():
    """Main entry point for the bot."""
    setup_logging()
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
