import asyncio
import functools
import os
import pickle

from src.dataclasses import Track


def _save_load_dec(func):
    @functools.wraps(func)
    async def wrapper(cls, *args, **kwargs):
        cls._load()
        result = await func(cls, *args, **kwargs)
        cls._save()
        return result

    return wrapper


class TrackQueue:
    """Track queue"""

    def __init__(self, queue_path: str) -> None:
        """
        init track queue
        :queue_path: tmp path to queue
        """
        self.queue = asyncio.Queue()
        self.queue_path = queue_path
        self._load()

    def _save(self):
        """
        save queue to tmp file
        """
        with open(self.queue_path, "wb") as f:
            print(self.queue)
            pickle.dump(self.queue, f)

    def _load(self):
        """
        save queue to tmp file
        """
        if os.path.exists(self.queue_path):
            with open(self.queue_path, "rb") as f:
                loaded_queue_contents = pickle.load(f)
                print(loaded_queue_contents, "Done")
                self.queue = loaded_queue_contents

    @_save_load_dec
    async def get(self):
        """
        get next track
        """
        return await self.queue.get()

    @_save_load_dec
    async def put(self, track: Track):
        """
        put next track to queue
        """
        await self.queue.put(track)
