"""Generic transformer plugin: apply a series of configurable transformations.

Can be configured to handle character replacement, translation, extension conversion,
voice-to-spectrum, abstract-to-class, and any other transformation types.
"""
from __future__ import annotations

import re
from typing import Any

from . import Plugin


class GenericTransformerPlugin(Plugin):
    def __init__(self):
        super().__init__(name="generic_transformer", version="1.0.0")
        self.transforms = []

    def add_transform(self, name: str, func: Callable[[Any], Any]) -> None:
        self.transforms.append((name, func))

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        result = data
        for name, func in self.transforms:
            try:
                result = func(result)
            except Exception as e:
                print(f"[generic_transformer] Transform '{name}' failed: {e}")
        return result

    def configure(self, config: list) -> None:
        """Configure transforms from a config list.

        Example config:
        [
            {"type": "replace_char", "old": "●", "new": "□"},
            {"type": "translate", "target_lang": "en"},
            {"type": "convert_extension", "target": "json"},
            {"type": "voice_to_spectrum", "method": "mel"},
            {"type": "abstract_to_class", "model": "gpt-4"}
        ]
        """
        # Clear existing transforms
        self.transforms.clear()
        for entry in config:
            self._apply_entry(entry)

    def _apply_entry(self, entry: dict):
        etype = entry.get("type")
        if etype == "replace_char":
            self.add_transform("replace_char", lambda txt: txt.replace(entry.get("old", ""), entry.get("new", "")))
        elif etype == "translate":
            # mock translation: prepend [LANG]
            lang = entry.get("target_lang", "en")
            self.add_transform("translate", lambda txt: f"[{lang}] {txt}")
        elif etype == "convert_extension":
            target = entry.get("target", "json")
            self.add_transform("convert_extension", lambda path: f"{path}.{target}" if isinstance(path, str) and "." not in path.split("|")[-1] else path)
        elif etype == "voice_to_spectrum":
            method = entry.get("method", "mel")
            self.add_transform("voice_to_spectrum", lambda audio: f"spectrogram:{method}:{audio}")
        elif etype == "abstract_to_class":
            model = entry.get("model", "gpt-4")
            self.add_transform("abstract_to_class", lambda intent: f"class GeneratedFromIntent: # {intent} # model={model}")
        else:
            print(f"[generic_transformer] Unknown transform type: {etype}")


def create_plugin() -> Plugin:
    return GenericTransformerPlugin()