import os
import platform
import time

from src.utils import get_volume


class VolumeController:
    """class for sound control"""

    def __init__(self, duration=5):
        """
        init VolumeController
        :duration: smooth transition time of the sound
        """
        self.duration = duration

    def change_volume(self, value: int):
        """
        changing the sound to a specific volume depending on the operating system
        :value: target volume
        """
        os_name = platform.system()

        match os_name:
            case "Darwin":
                self._set_volume_mac(value)
            case _:
                print("ERROR: OS не найдена")

    def _set_volume_mac(self, value: int):
        """Set the sound on the Mac to a specific volume"""
        current_volume = self._get_current_volume_mac()
        steps = 10
        step_duration = self.duration / steps
        delta = (value - current_volume) / steps

        for i in range(1, steps + 1):
            volume_step = current_volume + delta * i
            os.system(f"osascript -e 'set volume output volume {volume_step}'")
            time.sleep(step_duration)

    def _get_current_volume_mac(self) -> int:
        """Get the current volume level on Mac"""
        return get_volume()

    def set_volume(self, value: int):
        """wrapper for change_volume"""
        self.change_volume(value)
