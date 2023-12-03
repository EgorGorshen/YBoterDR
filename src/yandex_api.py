import sys

from yandex_music import ClientAsync

from src.utils import YANDEX_TOKEN


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

    match search_res.best.type:  # TODO:
        case "track":
            pass
        case _:
            pass
