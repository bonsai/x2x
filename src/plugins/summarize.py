"""Summarization plugin: generates summaries from PDF text."""
from __future__ import annotations

from typing import Any, Dict

from . import Plugin


class SummarizePlugin(Plugin):
    def __init__(self):
        super().__init__(name="summarize", version="1.0.0")

    def can_handle(self, *args: Any) -> bool:
        return True

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        text = data.get("text", "")
        if not text:
            return {"error": "No text to summarize"}
        # Simple extractive summary (first N sentences)
        import re
        sentences = re.split(r"[。！？\n]+", text)
        summary = " ".join(s.strip() for s in sentences[:5] if s.strip())
        return {"summary": summary}


def create_plugin() -> Plugin:
    return SummarizePlugin()