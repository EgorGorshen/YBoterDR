import sys
from aiogram.types import Video

from yandex_music import Album, Artist, ClientAsync, Playlist, Track

from src.utils import YANDEX_TOKEN
from src.dataclasses import Track as TrackDBType


if YANDEX_TOKEN is None:
    sys.exit('ERROR: YANDEX_API_TOKEN not found in ".env" file')


async def found_track(request: str):
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
