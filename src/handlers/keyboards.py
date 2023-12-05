from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


TRUE_FALSE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="true"),
            InlineKeyboardButton(text="❌", callback_data="false"),
        ]
    ]
)

CHOOSE_TRACK_KEYBOARD = lambda search_res: InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="{} — {}".format(track.name, track.author),
                callback_data="{}".format(track.track_id),
            )
        ]
        for track in search_res
    ]
)
