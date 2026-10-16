"""Plugin framework for pdf-ingest pipeline."""
from abc import ABC, abstractmethod
from typing import Any


class Plugin(ABC):
    """Base class for all pipeline plugins."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version

    @abstractmethod
    def can_handle(self, *args: Any) -> bool:
        ...

    @abstractmethod
    def process(self, *args: Any) -> Any:
        ...

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        pass
