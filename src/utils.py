from datetime import timedelta
import os
import sys
import json
import dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from moviepy.editor import ImageClip, AudioFileClip

from src.database import DataBase
from src.queue import TrackQueue


# Load env from .env file
dotenv.load_dotenv()

TELEBOT_TOKEN = os.getenv("TELEBOT_TOKEN")
ADMINS_IDS = os.getenv("ADMINS_IDS")
YANDEX_TOKEN = os.getenv("YANDEX_API_TOKEN")
TMP_PATH = os.getenv("TMP_PATH")
DEVELOP = os.getenv("DEVELOP")

# Checkout if token exists in .env file
if TELEBOT_TOKEN is None:
    sys.exit('ERROR: TELEBOT_TOKEN not found in ".env" file')

if ADMINS_IDS is None:
    sys.exit('ERROR: ADMINS_IDS not found in ".env" file')

if YANDEX_TOKEN is None:
    sys.exit('ERROR: YANDEX_API_TOKEN not found in ".env" file')

if TMP_PATH is None:
    sys.exit('ERROR: TMP_PATH not found in ".env" file')


ADMINS_IDS = json.loads(ADMINS_IDS)

# Create bot and dispatcher instances
bot = Bot(TELEBOT_TOKEN)
dispatcher = Dispatcher()

track_queue = TrackQueue(os.path.join(TMP_PATH, "track.queue"))
STATUS_PATH = os.path.join(TMP_PATH, "status")

data_base = (
    DataBase("sqlite.db", False)
    if DEVELOP is None
    else (
        DataBase("sqlite.db", True)
        if DEVELOP.lower() == "true"
        else DataBase("sqlite.db", False)
    )
)


async def get_user_info_from_message(message: Message) -> tuple[int, str] | None:
    """
    get && checkout user info from message

    :param message: tg message
    :return: tuple with user id and his full name
    """
    from_user = message.from_user
    chat_id = message.chat.id
    if from_user is None:
        await message.answer("Информация о пользователе недоступна.")
        return

    if chat_id is None or from_user.full_name is None:
        await message.answer("Отсутствует идентификатор пользователя или полное имя.")
        return

    return chat_id, from_user.full_name


async def set_user_commands():
    """set menu commands"""
    command_list = [
        BotCommand(
            command="start",
            description="Начните своё путешествие с YBoterDR. Эта команда откроет главное меню.",
        ),
        BotCommand(command="help", description="Получите подсказки и инструкции."),
        BotCommand(command="delete", description="Удалите последний добавленный трек."),
        BotCommand(command="find_track", description="Найдите трек по названию."),
        BotCommand(command="toast", description="Сказать тост и затушить музыку."),
        BotCommand(command="left", description="Сообщите, что вы покидаете вечеринку."),
        BotCommand(
            command="arrived", description="Сообщите, что вы прибыли на вечеринку."
        ),
    ]

    await bot.set_my_commands(command_list, BotCommandScopeDefault())


def create_video(image_path, audio_path, track_id, duration):
    """
    Creates a video from a given image and audio track.

    :param image_path: Path to the image file.
    :param audio_path: Path to the audio file.
    :param track_id: Identifier for the track, used for naming the output file.
    :param duration: Duration of the video in seconds.
    :return: Path to the created video file.
    """
    # TODO: rewrite to ffmpeg
    output_path = os.path.join(TMP_PATH, f"snipet/{track_id}.mp4")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        return output_path
    image_clip = ImageClip(image_path).set_duration(duration)
    audio_clip = AudioFileClip(audio_path).subclip(0, duration)
    video_clip = image_clip.set_fps(24).set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec="libx264")

    return output_path


def set_status(staus: str):
    """set staus in STATUS_PATH file"""
    with open(STATUS_PATH, "w", encoding="utf-8") as file:
        file.write(staus)


def get_status() -> str:
    """get status from STATUS_PATH file"""
    if not os.path.exists(STATUS_PATH):
        return "play"
    with open(STATUS_PATH, "r", encoding="utf-8") as file:
        return file.read()


def get_volume() -> int:
    """
    Returns the current volume level on a Mac.
    """
    try:
        volume = (
            os.popen("osascript -e 'output volume of (get volume settings)'")
            .read()
            .strip()
        )
        return int(volume)
    except ValueError:
        # Handle the case where the volume could not be parsed to an integer
        return 30


def convert_to_timedelta(callback_data):
    """
    convert to time delta
    :callback_data:
        - <int>[m|h|]
    """
    if not callback_data or len(callback_data) < 2:
        raise ValueError("Invalid callback data")

    time_value = int(callback_data[:-1])
    time_unit = callback_data[-1]

    match time_unit:
        case "m":
            return timedelta(minutes=time_value)
        case "h":
            return timedelta(hours=time_value)
        case _:
            raise ValueError("Unsupported time unit")
