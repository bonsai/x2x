"""File extension conversion plugin."""
from __future__ import annotations

from typing import Any

from . import Plugin


class ExtensionConvertPlugin(Plugin):
    def __init__(self):
        super().__init__(name="extension_convert", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        if isinstance(data, str):
            return data.replace(".pdf", ".md")
        return data


def create_plugin() -> Plugin:
    return ExtensionConvertPlugin()