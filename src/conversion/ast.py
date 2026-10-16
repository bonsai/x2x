"""Abstract Syntax Tree (AST): pipeline processing tree built from IR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .ir import PDFIR


@dataclass
class ASTNode:
    kind: str
    value: Any = None
    children: List["ASTNode"] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_child(self, child: "ASTNode") -> None:
        self.children.append(child)

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "value": self.value,
            "metadata": self.metadata,
            "children": [c.to_dict() for c in self.children],
        }


def ir_to_ast(pdf_ir: PDFIR) -> ASTNode:
    """Build an AST from PDFIR.

    Root: program
      ├─ pdf (metadata)
      └─ pages[]
          ├─ page (page_number, image_name)
          ├─ diagram (diagram_type, caption)
          ├─ elements[]
          │   └─ element (name, type, attributes, methods)
          └─ relationships[]
              └─ relationship (relationship, source, target)
    """
    root = ASTNode(kind="program", value=pdf_ir.pdf_name)
    pdf_node = ASTNode(kind="pdf", value={"name": pdf_ir.pdf_name})
    root.add_child(pdf_node)

    for page_ir in pdf_ir.pages:
        page_node = ASTNode(
            kind="page",
            value={"page_number": page_ir.page_number, "image_name": page_ir.image_name},
        )

        if page_ir.diagram:
            dia_node = ASTNode(
                kind="diagram",
                value={
                    "diagram_type": page_ir.diagram.diagram_type,
                    "caption": page_ir.diagram.caption,
                },
            )

            elem_parent = ASTNode(kind="elements")
            for el in page_ir.diagram.elements:
                elem_node = ASTNode(
                    kind="element",
                    value={
                        "name": el.name,
                        "type": el.type,
                        "attributes": el.attributes,
                        "methods": el.methods,
                    },
                    metadata=el.extra,
                )
                elem_parent.add_child(elem_node)
            dia_node.add_child(elem_parent)

            rel_parent = ASTNode(kind="relationships")
            for rel in page_ir.diagram.relationships:
                rel_node = ASTNode(
                    kind="relationship",
                    value={
                        "relationship": rel.relationship,
                        "source": rel.source,
                        "target": rel.target,
                    },
                    metadata=rel.extra,
                )
                rel_parent.add_child(rel_node)
            dia_node.add_child(rel_parent)

            page_node.add_child(dia_node)

        pdf_node.add_child(page_node)

    return root


def ast_to_json(ast: ASTNode) -> dict:
    return ast.to_dict()
