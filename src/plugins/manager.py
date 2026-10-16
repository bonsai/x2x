"""Plugin manager for pdf-ingest pipeline.

Allows registering arbitrary plugins that can transform PDF data
into additional structured outputs (e.g., Ronbun2x, summarization, etc.).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import Plugin


class PluginManager:
    """Manages plugin registration and execution."""

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._active: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin instance."""
        self._plugins[plugin.name] = plugin

    def activate(self, name: str) -> None:
        """Activate a registered plugin."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not registered")
        self._active[name] = self._plugins[name]

    def deactivate(self, name: str) -> None:
        """Deactivate a plugin."""
        self._active.pop(name, None)

    def load_from_file(self, file_path: Path, name: str) -> Plugin:
        """Load a plugin from a Python file."""
        spec = importlib.util.spec_from_file_location(name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load plugin from {file_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if not hasattr(module, "create_plugin"):
            raise AttributeError(f"Plugin file {file_path} missing create_plugin()")
        plugin = module.create_plugin()
        self.register(plugin)
        return plugin

    def load_from_module(self, module_path: str) -> Plugin:
        """Load a plugin from a module path (e.g. 'ronbun2x_plugin')."""
        module = importlib.import_module(module_path)
        if not hasattr(module, "create_plugin"):
            raise AttributeError(f"Module {module_path} missing create_plugin()")
        plugin = module.create_plugin()
        self.register(plugin)
        return plugin

    def run_active(self, data: Any) -> Dict[str, Any]:
        """Run all active plugins on the given data."""
        results: Dict[str, Any] = {}
        for name, plugin in self._active.items():
            if plugin.can_handle(data):
                try:
                    results[name] = plugin.process(data)
                except Exception as e:
                    results[name] = {"error": str(e)}
        return results

    def list_plugins(self) -> List[str]:
        """Return names of all registered plugins."""
        return list(self._plugins.keys())

    def list_active(self) -> List[str]:
        """Return names of all active plugins."""
        return list(self._active.keys())