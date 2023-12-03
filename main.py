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

from src.utils import dispatcher, bot, set_user_commands
from src.handlers.users import user_router
from src.handlers.admin import admin_router


async def init_routers():
    """Initialize routers"""

    # Include routers for handling user interactions
    dispatcher.include_router(user_router)
    dispatcher.include_router(admin_router)

    # set commands
    await set_user_commands()

    # Start polling bot
    await dispatcher.start_polling(bot)


def setup_logging():
    """Cofig base logging"""
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def main():
    """Main entry point for the bot."""
    setup_logging()
    asyncio.run(init_routers())


if __name__ == "__main__":
    main()
