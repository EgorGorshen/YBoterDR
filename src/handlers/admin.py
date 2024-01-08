from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.dataclasses import User
from src.handlers.FSMachine import BlockUser
from src.handlers.keyboards import SELECT_DELTA_TIME, SELECT_USER_KEYBOARD
from src.utils import (
    ADMINS_IDS,
    bot,
    convert_to_timedelta,
    get_volume,
    set_status,
    data_base,
)


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


@admin_router.message(Command("block"))
async def block_user(message: Message, state: FSMContext):
    """blocking the user indefinitely"""
    if message.chat.id not in ADMINS_IDS:
        return

    users = data_base.get_users()

    if users is None:
        await message.answer("Нет зарегестрированных пользователей")
        return

    await message.answer(
        "Выберите польователя для блокировки:", reply_markup=SELECT_USER_KEYBOARD(users)
    )

    await state.set_state(BlockUser.choose_delta_time)


@admin_router.callback_query(BlockUser.choose_delta_time, F.data.as_("telegram_id"))
async def choose_delta_time_block_user(
    callback: CallbackQuery, state: FSMContext, telegram_id: str
):
    if callback.message is None:
        return

    if telegram_id == "-1":
        await callback.message.delete()
        await state.clear()
        return

    tg_id = int(telegram_id)
    await state.set_data({"tg_id": tg_id})

    await callback.message.edit_text(
        text="Теперь выберите на какой период заблокировать пользователя",
        reply_markup=SELECT_DELTA_TIME,
    )

    await state.set_state(BlockUser.add_to_db)


@admin_router.callback_query(F.data.as_("time"), BlockUser.add_to_db)
async def add_to_db_block_user(callback: CallbackQuery, state: FSMContext, time: str):
    if callback.message is None:
        return
    data = await state.get_data()
    delta = convert_to_timedelta(time)

    data_base.block_user(data["tg_id"], delta)

    await state.clear()

    await callback.message.edit_text("Пользователь заблокирован", reply_markup=None)
