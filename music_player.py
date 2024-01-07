import sys
import pygame
import asyncio
import os

from enum import Enum
from typing import NoReturn

from src.queue import TrackQueue
from src.dataclasses import Track
from src.volume_controller import VolumeController
from src.utils import STATUS_PATH, TMP_PATH, get_status, set_status, track_queue


if TMP_PATH is None:
    sys.exit('ERROR: TMP_PATH not found in ".env" file')


class Status(Enum):
    PLAY = 0
    NEXT = 1
    TOAST = 4


class Player:
    def __init__(self, status_path: str, queue_path: str) -> None:
        self.status_path = status_path
        self.queue_path = queue_path
        self.volume = 50
        self.status: Status = Status.PLAY

        self.queue: TrackQueue = TrackQueue(self.queue_path)
        self.volume_controller = VolumeController()

    async def next(self) -> Track | None:
        return track_queue.get()

    def toast(self):
        pass

    def _get_status(self):
        if not os.path.exists(self.status_path):
            set_status("play")

        status = get_status().lower().split()
        match status[0]:
            case "next":
                self.status = Status.NEXT

            case "volume":
                self.volume = int(status[1])
                self.volume_controller.set_volume(self.volume)
                self.status = Status.PLAY
                set_status("play")

            case "toast":
                self.volume_controller.set_volume(10)
                self.status = Status.TOAST

            case "play":
                self.status = Status.PLAY
            case _:
                return NoReturn

    async def play(self):
        pygame.init()
        pygame.mixer.init()

        while True:
            track = await self.next()

            if track is None:
                await asyncio.sleep(1)
                continue
            pygame.mixer.music.load(
                os.path.join(TMP_PATH, f"tracks/{track.track_id}.mp3")
            )
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                await asyncio.sleep(1)

                self._get_status()
                print(self.status)

                if self.status == Status.NEXT:
                    pygame.mixer.music.stop()
                    self.status = Status.PLAY
                    set_status("play")
                    break

        return NoReturn


async def main():
    # 1. read queue
    # 4. If queue is empty start to play playlist (...)

    player = Player(
        status_path=STATUS_PATH,
        queue_path=os.path.join(TMP_PATH, "track.queue"),
    )
    await player.play()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
