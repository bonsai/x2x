"""Mock voice-to-spectrum plugin."""
from __future__ import annotations

from typing import Any

from . import Plugin


class VoiceToSpectrumPlugin(Plugin):
    def __init__(self):
        super().__init__(name="voice_to_spectrum", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        if isinstance(data, str):
            return f"spectrogram:mel:{data}"
        return data


def create_plugin() -> Plugin:
    return VoiceToSpectrumPlugin()