import os
import platform
import time

from typing import Literal


class VolumeController:
    """class for sound control"""

    def __init__(self, duration=5):
        """
        init VolumeController
        :duration: smooth transition time of the sound
        """
        self.duration = duration

    def change_volume(self, value: int, action: Literal["louder"] | Literal["husher"]):
        """
        changing the sound depending on the operating system
        :volume: delta for volume
        :action: louder or husher
        """
        os_name = platform.system()

        match os_name:
            case "Darwin":
                self._change_volume_mac(value, action)
            case _:
                print("ERROR: OS не найдена")

    def _change_volume_mac(
        self, value: int, action: Literal["louder"] | Literal["husher"]
    ):
        """changing the sound on the mac"""
        steps = 50
        step_duration = self.duration / steps
        for i in range(steps + 1):
            volume_step = value * i / steps
            os.system(
                f"osascript -e \"set volume output volume ((output volume of (get volume settings))\
                        {'-' if action == 'husher' else '+'} {volume_step * 100})\""
            )
            time.sleep(step_duration)

    def louder(self, value: int):
        """wrapper for change_volume(..., 'louder')"""
        self.change_volume(value, "louder")

    def husher(self, value: int):
        """wrapper for change_volume(..., 'husher')"""
        self.change_volume(value, "husher")
