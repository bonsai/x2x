"""Mock translation plugin."""
from __future__ import annotations
from typing import Any
from . import Plugin


class TranslatePlugin(Plugin):
    def __init__(self):
        super().__init__(name="translate", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        return f"[TRANSLATED] {data}" if isinstance(data, str) else data


def create_plugin() -> Plugin:
    return TranslatePlugin()