from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


TRUE_FALSE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="true"),
            InlineKeyboardButton(text="❌", callback_data="false"),
        ]
    ]
)
