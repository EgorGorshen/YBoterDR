from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.dataclasses import User


TRUE_FALSE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="true"),
            InlineKeyboardButton(text="❌", callback_data="false"),
        ]
    ]
)


def CHOOSE_TRACK_KEYBOARD(search_res):
    return InlineKeyboardMarkup(
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


def SELECT_USER_KEYBOARD(users: list[User]):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"{user.name} — {user.number_of_tracks}",
                callback_data=str(user.telegram_id),
            )
        ]
        for user in users
    ]

    inline_keyboard.append([InlineKeyboardButton(text="Отменить", callback_data="-1")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


SELECT_DELTA_TIME = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 minutes", callback_data="1m")],
        [InlineKeyboardButton(text="5 minutes", callback_data="5m")],
        [InlineKeyboardButton(text="10 minutes", callback_data="10m")],
        [InlineKeyboardButton(text="30 minutes", callback_data="30m")],
        [InlineKeyboardButton(text="1 hour", callback_data="1h")],
    ]
)
