"""Mock abstract-to-class plugin: convert an intent into a class definition."""
from __future__ import annotations

from typing import Any

from . import Plugin


class AbstractToClassPlugin(Plugin):
    def __init__(self):
        super().__init__(name="abstract_to_class", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        if isinstance(data, str):
            return f"class GeneratedFromIntent:\n    ''' {data} '''\n    pass"
        return data


def create_plugin() -> Plugin:
    return AbstractToClassPlugin()