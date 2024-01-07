import os
from aiogram import F, Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    Message,
)
from aiogram.fsm.context import FSMContext

from src.handlers.FSMachine import FindTrack, Toast
from src.handlers.admin import inform_the_admins_about_the_com_t_or_left_f
from src.handlers.keyboards import CHOOSE_TRACK_KEYBOARD, TRUE_FALSE_KEYBOARD
from src.handlers.messages import REGISTRATION_ERROR_MESSAGE, START_MESSAGE
from src.logger import Logger
from src.utils import (
    create_video,
    data_base,
    get_user_info_from_message,
    get_volume,
    set_status,
    track_queue,
)
from src.yandex_api import (
    find_track,
    get_track_by_id,
    save_img_and_sneapet_of_track,
)


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


@user_router.message(Command("help"))
async def help(message: Message):
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

    await inform_the_admins_about_the_com_t_or_left_f(user, True)


@user_router.message(Command("left"))
async def user_left(message: Message):
    from_user = await get_user_info_from_message(message)
    if from_user is None:
        return

    id, _ = from_user
    data_base.user_out(id)
    user = data_base.get_user(id)
    if user is None:
        await message.answer("Прежде чем начать пользование запустите команду /start")
        return

    await inform_the_admins_about_the_com_t_or_left_f(user, False)


@user_router.message(Command("find_track"))
async def find_track_tg(message: Message, state: FSMContext):
    if data_base.is_block(message.chat.id):
        await message.answer("Простите, но произошла ошибка, попробуйте чуть позже")
        return
    await message.answer("Введите запрос:")
    await state.set_state(FindTrack.get_request.state)


async def send_track_info(message, track, state, bot):
    """send track info (snipets)"""
    video_path = await create_video_for_track(track)
    if not os.path.exists(video_path):
        await message.answer(f"Добавить трэк [{track.name}({track.author})] в очередь?")
        return

    video = FSInputFile(path=video_path, filename=f"{track.name}.mp4")
    await state.set_data(track.__dict__)
    await state.set_state(FindTrack.set_track.state)
    await bot.send_video(
        message.chat.id,
        video=video,
        reply_markup=TRUE_FALSE_KEYBOARD,
        caption=f"Добавить трэк [{track.name}({track.author})] в очередь?",
    )


async def create_video_for_track(track):
    """create snipets"""
    audio_path, photo_path = await save_img_and_sneapet_of_track(track.track_id)
    return create_video(photo_path, audio_path, track.track_id, 20)


@user_router.message(FindTrack.get_request, F.text.as_("request"))
async def get_request(message: Message, state: FSMContext, request: str, bot: Bot):
    """Get request from request"""
    search_res = await find_track(request)
    if search_res is None:
        await message.answer("По вашему запросу ничего не найдено")
        await state.clear()
        return

    if isinstance(search_res, list):
        await message.answer(
            "Выберите трек:", reply_markup=CHOOSE_TRACK_KEYBOARD(search_res)
        )
        await state.set_data(search_res.__dict__)
        await state.set_state(FindTrack.choose_track)
        return

    await send_track_info(message, search_res, state, bot)


@user_router.callback_query(FindTrack.choose_track, F.data.as_("id_of_track"))
async def choose_track(
    callback: CallbackQuery, state: FSMContext, id_of_track: str, bot: Bot
):
    """choose track from list of tracks"""
    if callback.message is None:
        return

    if not id_of_track.isalnum():
        await callback.message.delete()
        await callback.message.answer(
            "Ошибка при получении трека... попробуйте по названию"
        )
        await state.clear()
        return

    track = await get_track_by_id(int(id_of_track))
    await send_track_info(callback.message, track, state, bot)


@user_router.callback_query(FindTrack.set_track)
async def set_track(callback: CallbackQuery, state: FSMContext):
    """ser track to queue"""
    data = await state.get_data()
    if callback.message is None:
        return

    await callback.message.delete()

    if callback.data == "true":
        data_base.add_track(data["track_id"], data["name"], data["author"])
        track = data_base.get_track(data["track_id"])
        if track is not None:
            track_queue.put(track)
        else:
            await callback.message.answer(
                "Простите произошла ошибка, попробуде найти трек ещё раз"
            )
            return

        await callback.message.answer(
            "Трек [{}({})] Добавлен".format(data["name"], data["author"])
        )

    if callback.data == "false":
        await callback.message.answer(
            "Ладно, попробуй ввести запрос по точней: /find_track"
        )

    await state.clear()


@user_router.message(Command("toast"))
async def toast(message: Message, state: FSMContext):
    set_status("toast")
    volume = get_volume()
    await state.set_state(Toast.toast)
    await state.set_data({"volume": volume})
    await message.answer("Когда закончишь отправь /done")


@user_router.message(Command("done"), Toast.toast)
async def finish_toast(message: Message, state: FSMContext):
    set_status(f"volume {(await state.get_data())['volume']}")

    await state.clear()
    await message.answer("Продолжаем трек")
