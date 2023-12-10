import asyncio
import os
import pickle

from src.dataclasses import Track


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

    def _load(self):
        """
        load queue from tmp file
        """
        if os.path.exists(self.queue_path):
            with open(self.queue_path, "rb") as f:
                loaded_queue = pickle.load(f)
                for item in loaded_queue:
                    self.queue.put_nowait(item)

    def _save(self):
        """
        save queue
        """
        with open(self.queue_path, "wb") as f:
            pickle.dump(self.queue, f)

    async def get(self):
        """
        get next track
        """
        return await self.queue.get()

    async def put(self, track: Track):
        """
        put next track to queue
        """
        await self.queue.put(track)
