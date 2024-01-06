import os
import sys
from aiogram.types import Video

from yandex_music import Album, Artist, ClientAsync, Playlist, Track
from yandex_music.utils.request_async import NotFoundError
from src.logger import Logger

from src.utils import TMP_PATH, YANDEX_TOKEN
from src.dataclasses import Track as TrackDBType


yandex_api_log = Logger("yandex_api_log", "log/yandex_api.log")

if YANDEX_TOKEN is None:
    sys.exit('ERROR: YANDEX_API_TOKEN not found in ".env" file')


@yandex_api_log.log_function_call
async def find_track(request: str):
    """found tracks etc"""
    client = await ClientAsync(YANDEX_TOKEN).init()
    search_res = await client.search(request)

    if search_res is None:
        return None

    if search_res.best is None:
        return None

    if isinstance(search_res.best.result, Track):
        result = search_res.best.result
        track_id, name, auther = result.id, result.title, result.artists_name()[0]

        if track_id is None or name is None or auther is None:
            return None

        return TrackDBType(int(track_id), name, auther)

    if isinstance(search_res.best.result, Album):
        pass  # TODO:

    if isinstance(search_res.best.result, Artist):
        pass  # TODO:

    if isinstance(search_res.best.result, Playlist):
        pass  # TODO:

    if isinstance(search_res.best.result, Video):
        pass  # TODO:

    return None


async def save_img_and_sneapet_of_track(track_id: int):
    """save img and audio"""
    if TMP_PATH is None:
        sys.exit('ERROR: TMP_PATH not found in ".env" file')

    client = await ClientAsync(YANDEX_TOKEN).init()
    search_res = await client.tracks(track_id)

    if search_res is None:
        raise NotFoundError("ERROR: track not found")

    track = search_res.pop()
    audio_path = os.path.join(TMP_PATH, "tracks")  # /{track_id}.mp3
    photo_path = os.path.join(TMP_PATH, "cover")  # /{track_id}.png

    os.makedirs(audio_path, exist_ok=True)
    os.makedirs(photo_path, exist_ok=True)

    if not os.path.exists(os.path.join(audio_path, f"{track_id}.mp3")):
        await track.download_async(filename=os.path.join(audio_path, f"{track_id}.mp3"))

    if not os.path.exists(os.path.join(photo_path, f"{track_id}.png")):
        await track.download_cover_async(
            filename=os.path.join(photo_path, f"{track_id}.png")
        )

    return os.path.join(audio_path, f"{track_id}.mp3"), os.path.join(
        photo_path, f"{track_id}.png"
    )


async def get_track_by_id(track_id: int):
    """Get track by yandex id"""
    client = await ClientAsync(YANDEX_TOKEN).init()
    search_res = await client.tracks(track_id)

    if search_res is None:
        raise NotFoundError("ERROR: track not found")

    track = search_res.pop()

    return TrackDBType(
        track_id,
        track.title if track.title is not None else "(Без названия)",
        ", ".join(track.artists_name()),
    )
