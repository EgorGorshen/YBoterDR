import os
import platform
import time

from typing import Literal
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import pulsectl


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
            case "Windows":
                self._change_volume_win(value, action)
            case "Darwin":
                # self._change_volume_mac(value, action)
                self._change_volume_mac(value)
            case "Linux":
                self._change_volume_linux(value, action)
            case _:
                print("ERROR: OS не найдена")

    def _change_volume_mac(self, value: int):
        """changing the sound on the mac"""
        steps = 50
        step_duration = self.duration / steps
        for i in range(steps + 1):
            volume_step = value * i / steps
            os.system(f"osascript -e 'set volume output volume {volume_step * 100}'")
            time.sleep(step_duration)

    def _change_volume_win(self, value: int, action: str):
        """sound change on windows"""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume_db = volume.GetMasterVolumeLevel()
        max_volume_db = volume.GetVolumeRange()[1]
        target_volume_db = max_volume_db * value

        steps = 50
        step_duration = self.duration / steps
        volume_step = (target_volume_db - current_volume_db) / steps

        if action == "husher":
            volume_step = -volume_step

        for _ in range(steps):
            current_volume_db += volume_step
            volume.SetMasterVolumeLevel(current_volume_db, None)
            time.sleep(step_duration)

    def _change_volume_linux(self, value: int, action: str):
        """changing the sound to Linux"""
        if "pulsectl" not in globals():
            print("PulseAudio не поддерживается на этой ОС")
            return

        with pulsectl.Pulse("volume-changer") as pulse:
            for sink in pulse.sink_list():
                current_volume = pulse.volume_get_all_chans(sink)
                steps = 50
                step_duration = self.duration / steps
                volume_step = (value - current_volume) / steps

                if action == "husher":
                    volume_step = -volume_step

                for _ in range(steps):
                    current_volume += volume_step
                    pulse.volume_set_all_chans(sink, current_volume)
                    time.sleep(step_duration)

    def louder(self, value: int):
        """wrapper for change_volume(..., 'louder')"""
        self.change_volume(value, "louder")

    def husher(self, value: int):
        """wrapper for change_volume(..., 'husher')"""
        self.change_volume(value, "husher")
