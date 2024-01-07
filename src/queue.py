import functools
import os
import pickle

from src.dataclasses import Track
from src.logger import Logger


track_log = Logger("track_log", "log/track.log")


def _save_load_dec(func):
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        cls._load()
        result = func(cls, *args, **kwargs)
        cls._save()
        return result

    return wrapper


class Queue:
    """Queue class"""

    def __init__(self) -> None:
        """init queue"""
        self._queue = []

    def get(self):
        """get object from queue"""
        if len(self._queue) == 0:
            return None
        return self._queue.pop(0)

    def put(self, obj):
        """put object to queue"""
        self._queue.append(obj)

    def __str__(self) -> str:
        if len(self._queue) == 0:
            return "Queue<None>(len=0)"

        return f"Queue{type(self._queue[0])}(len={len(self._queue)})"


@track_log.class_log
class TrackQueue:
    """Track queue"""

    def __init__(self, queue_path: str) -> None:
        """
        init track queue
        :queue_path: tmp path to queue
        """
        self.queue = Queue()
        self.queue_path = queue_path
        self._load()

    def _save(self):
        """
        save queue to tmp file
        """
        with open(self.queue_path, "wb") as f:
            pickle.dump(self.queue, f)

    def _load(self):
        """
        save queue to tmp file
        """
        if os.path.exists(self.queue_path):
            with open(self.queue_path, "rb") as f:
                loaded_queue_contents = pickle.load(f)
                self.queue = loaded_queue_contents

    @_save_load_dec
    def get(self):
        """
        get next track
        """
        return self.queue.get()

    @_save_load_dec
    def put(self, track: Track):
        """
        put next track to queue
        """
        self.queue.put(track)

    def empty(self):
        """
        make queue empty
        """
        self.queue = Queue()
