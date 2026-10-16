"""Routing layer that covers both transformation and communication.

A router can chain together:
- Transformation steps (pure functions that mutate/convert data)
- Communication steps (functions that send/receive data over network/API)

Example usage:
    router = Router()
    router.add_transform(ir.json_to_ir)          # JSON -> IR
    router.add_transform(ast.ir_to_ast)          # IR -> AST
    router.add_transform(dsl.ast_to_dsl)         # AST -> DSL string
    router.add_communicator("vlm", vlm_communicator)  # send images to VLM, get description
    router.add_communicator("ronbun2x", ronbun2x_communicator)  # send JSON to ronbun2x
    result = router.run(initial_data)
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

# Import transformation functions from conversion layers
from .conversion import ir, ast, dsl

# Import communication functions (we'll define them below)
from . import vlm_processor  # for VLM communication
from .plugins import ronbun2x  # for ronbun2x communication


class Router:
    def __init__(self):
        self.transforms: List[Callable[[Any], Any]] = []
        self.communicators: List[tuple[str, Callable[[Any], Any]]] = []
        # Auto-add bullet normalization if requested (default: include)
        self.include_bullet_normalize = True

    def add_transform(self, func: Callable[[Any], Any]) -> None:
        """Add a transformation step."""
        self.transforms.append(func)

    def add_communicator(self, name: str, func: Callable[[Any], Any]) -> None:
        """Add a communication step identified by name."""
        self.communicators.append((name, func))

    def run(self, data: Any) -> Any:
        """Run all transforms then all communicators in order."""
        # Apply transformations
        for t in self.transforms:
            try:
                data = t(data)
            except Exception as e:
                raise RuntimeError(f"Transform {t.__name__} failed: {e}") from e

        # Apply communicators
        for name, func in self.communicators:
            try:
                # Communicators may return a dict with results; we'll store under a key
                result = func(data)
                # If result is a dict, merge; else store under name
                if isinstance(result, dict):
                    if not isinstance(data, dict):
                        data = {"_input": data}
                    data.update({f"{name}_{k}": v for k, v in result.items()})
                else:
                    data = {f"{name}_output": result, **(data if isinstance(data, dict) else {"_input": data})}
            except Exception as e:
                raise RuntimeError(f"Communicator '{name}' failed: {e}") from e

        return data


# Example communicator wrappers
def vlm_communicator(data: Any) -> Dict[str, Any]:
    """
    Expects data to contain image paths or similar.
    Uses vlm_processor.describe_image for each image.
    Returns dict with vlm_descriptions.
    """
    # For simplicity, assume data is a dict with key "image_paths" list of Paths
    # In real usage, adapt to your data structure.
    from pathlib import Path
    if isinstance(data, dict) and "image_paths" in data:
        image_paths = data["image_paths"]
        if not isinstance(image_paths, list):
            image_paths = [image_paths]
    else:
        # fallback: if data itself is a Path or str
        if isinstance(data, (Path, str)):
            image_paths = [Path(data)]
        else:
            image_paths = []

    descriptions = []
    for img_path in image_paths:
        try:
            desc = vlm_processor.describe_image(Path(img_path))
            descriptions.append({"image": str(img_path), "description": desc})
        except Exception as e:
            descriptions.append({"image": str(img_path), "error": str(e)})
    return {"vlm_descriptions": descriptions}


def ronbun2x_communicator(data: Any) -> Dict[str, Any]:
    """
    Expects data to contain arxiv_id or pdf_url.
    Calls ronbun2x API for each style.
    Returns dict with ronbun2x_results.
    """
    # Import inside to avoid circular if needed
    from .plugins.ronbun2x import create_plugin
    plugin = create_plugin()
    # The plugin's process method expects a dict
    if not isinstance(data, dict):
        data = {"pdf_url": str(data)} if isinstance(data, (str, Path)) else {"raw": data}
    return plugin.process(data)


# Convenience function to create a default router for pdf-ingest pipeline
def create_pdf_ingest_router() -> Router:
    router = Router()
    router.add_transform(ir.json_to_ir)      # JSON -> IR
    router.add_transform(ast.ir_to_ast)      # IR -> AST
    router.add_transform(dsl.ast_to_dsl)     # AST -> DSL
    router.add_communicator("vlm", vlm_communicator)
    router.add_communicator("ronbun2x", ronbun2x_communicator)
    return router
