import os
import sys
from aiogram.types import Video

from yandex_music import Album, Artist, ClientAsync, Playlist, Track
from yandex_music.utils.request_async import NotFoundError

from src.utils import YANDEX_TOKEN
from src.dataclasses import Track as TrackDBType


if YANDEX_TOKEN is None:
    sys.exit('ERROR: YANDEX_API_TOKEN not found in ".env" file')


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
    client = await ClientAsync(YANDEX_TOKEN).init()
    search_res = await client.tracks(track_id)

    if search_res is None:
        raise NotFoundError("ERROR: track not found")

    track = search_res.pop()

    if not os.path.exists("/tmp/y_boter_dr"):
        os.mkdir("/tmp/y_boter_dr")

    if not os.path.exists("/tmp/y_boter_dr/tracks"):
        os.mkdir("/tmp/y_boter_dr/tracks")

    if not os.path.exists("/tmp/y_boter_dr/cover"):
        os.mkdir("/tmp/y_boter_dr/cover")

    if not os.path.exists(f"/tmp/y_boter_dr/tracks/{id}.mp3"):
        await track.download_async(filename=f"/tmp/y_boter_dr/tracks/{id}.mp3")

    if not os.path.exists(f"/tmp/y_boter_dr/cover/{id}.png"):
        await track.download_cover_async(filename=f"/tmp/y_boter_dr/cover/{id}.png")


async def add_track_to_queue(track: TrackDBType):
    """add track to alise queue"""
    return track
