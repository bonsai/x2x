"""Ronbun2x plugin: converts PDF data into Ronbun2x handoff format.

Supports: rakugo, yonkoma, two_line, screenshot
"""
from __future__ import annotations

import os
from typing import Any, Dict

from . import Plugin


class Ronbun2xPlugin(Plugin):
    """Plugin that wraps ronbun2x API for PDF ingestion."""

    def __init__(self):
        super().__init__(name="ronbun2x", version="1.0.0")
        self.base_url = os.getenv("RONBUN2X_URL", "http://localhost:8000")

    def can_handle(self, *args: Any) -> bool:
        # Accept any PDF-derived data
        return True

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        import requests

        # data should have 'pdf_url' or 'arxiv_id'
        arxiv_id = data.get("arxiv_id")
        pdf_url = data.get("pdf_url")
        if not arxiv_id and not pdf_url:
            return {"error": "No arxiv_id or pdf_url in data"}

        results: Dict[str, Any] = {}
        for x in ["rakugo", "yonkoma", "two_line", "screenshot"]:
            url = f"{self.base_url}/api"
            params = {"x": x}
            if arxiv_id:
                params["url"] = f"https://arxiv.org/abs/{arxiv_id}"
            else:
                params["url"] = pdf_url
            try:
                resp = requests.get(url, params=params, timeout=60)
                resp.raise_for_status()
                results[x] = resp.json()
            except Exception as e:
                results[x] = {"error": str(e)}
        return results


def create_plugin() -> Plugin:
    return Ronbun2xPlugin()