"""Character replacement plugin: replace characters in text."""
from __future__ import annotations

from typing import Any

from . import Plugin


class CharReplacePlugin(Plugin):
    def __init__(self):
        super().__init__(name="char_replace", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Any) -> Any:
        return self._replace_recursive(data, {
            "old": "●",
            "new": "□",
            "old_jp_dot": "・",
            "new_jp_dot": "□",
        })

    def _replace_recursive(self, obj: Any, mapping: dict) -> Any:
        if isinstance(obj, str):
            result = obj
            for old, new in [(mapping["old"], mapping["new"]), (mapping["old_jp_dot"], mapping["new_jp_dot"])]:
                result = result.replace(old, new)
            return result
        elif isinstance(obj, dict):
            return {k: self._replace_recursive(v, mapping) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_recursive(v, mapping) for v in obj]
        else:
            return obj


def create_plugin() -> Plugin:
    return CharReplacePlugin()