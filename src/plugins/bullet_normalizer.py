"""Bullet normalization plugin: convert ● to □ in prompts/text."""
from __future__ import annotations

from typing import Any

from . import Plugin


class BulletNormalizerPlugin(Plugin):
    def __init__(self):
        super().__init__(name="bullet_normalizer", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        # Handles any data (text, dict, list) that contains string fields
        return True

    def process(self, data: Any) -> Any:
        # Recursively replace bullet characters with check boxes
        return self._normalize_recursive(data)

    def _normalize_recursive(self, obj: Any) -> Any:
        if isinstance(obj, str):
            # Replace fullwidth bullet (U+25A0) and Japanese dot
            return obj.replace('\u25A0', '□').replace('・', '□')
        elif isinstance(obj, dict):
            return {k: self._normalize_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._normalize_recursive(v) for v in obj]
        else:
            return obj


def create_plugin() -> Plugin:
    return BulletNormalizerPlugin()