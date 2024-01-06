import sys
import pygame
import asyncio
import os

from enum import Enum
from typing import NoReturn

from src.queue import TrackQueue
from src.dataclasses import Track
from src.volume_controller import VolumeController

from src.utils import TMP_PATH, track_queue


if TMP_PATH is None:
    sys.exit('ERROR: TMP_PATH not found in ".env" file')


class Status(Enum):
    PLAY = 0
    NEXT = 1
    LOUDER = 2
    HUSHER = 3
    TOAST = 4


class Player:
    def __init__(self, status_path: str, queue_path: str) -> None:
        self.status_path = status_path
        self.queue_path = queue_path
        self.volume = 50
        self.status: Status = Status.PLAY

        self.queue: TrackQueue = TrackQueue(self.queue_path)
        self.volume_controller = VolumeController()

    async def next(self) -> Track:
        return await track_queue.get()

    def toast(self):
        pass

    def _get_status(self):
        with open(self.status_path, "r") as file:
            status = file.read().lower().split()
            match status:
                case "next", _:
                    self.status = Status.NEXT

                case "louder", int(volume), _:
                    self.volume = volume
                    self.volume_controller.louder(volume)

                case "husher", int(volume), _:
                    self.volume_controller.husher(volume)

                case "toast", _:
                    self.volume_controller.husher(10)
                    self.status = Status.TOAST

                case "play", _:
                    self.status = Status.PLAY
                case _:
                    return NoReturn

    async def play(self):
        pygame.init()
        pygame.mixer.init()

        while True:
            track = await self.next()

            pygame.mixer.music.load(
                os.path.join(TMP_PATH, f"/track/{track.track_id}.mp3")
            )
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                await asyncio.sleep(1)

                self._get_status()

                if self.status == Status.NEXT:
                    pygame.mixer.music.stop()
                    self.status = Status.PLAY
                    break

        return NoReturn


async def main():
    # 1. read queue
    # 2. play queue
    # 3. get signals from y_boter_bot (|<< / || / |> / >>|)
    # 4. If queue is empty start to play playlist (...)
    # pygame.mixer.init()
    # pygame.mixer.music.load("/Users/gorsenkovegor/Downloads/mp3/Nirvana.mp3")
    #
    # pygame.mixer.music.play()
    #
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

    player = Player(
        status_path=os.path.join(TMP_PATH, "status"),
        queue_path=os.path.join(TMP_PATH, "track.queue"),
    )
    await player.play()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
