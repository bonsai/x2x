"""Intermediate Representation (IR): normalized schema from raw JSON plugin output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class ElementIR:
    name: str
    type: str
    attributes: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)


@dataclass
class RelationshipIR:
    relationship: str
    source: str
    target: str
    extra: dict = field(default_factory=dict)


@dataclass
class DiagramIR:
    diagram_type: str
    caption: str
    elements: List[ElementIR] = field(default_factory=list)
    relationships: List[RelationshipIR] = field(default_factory=list)


@dataclass
class PageIR:
    page_number: int
    image_name: str
    diagram: Optional[DiagramIR]
    raw_text: str


@dataclass
class PDFIR:
    pdf_name: str
    pages: List[PageIR]


def json_to_ir(data: dict) -> PDFIR:
    """Convert raw plugin JSON into normalized PDFIR."""
    pages = []
    for i, page in enumerate(data.get("pages", []), 1):
        desc = page.get("description", {})
        elements = [
            ElementIR(
                name=e.get("name", ""),
                type=e.get("type", ""),
                attributes=e.get("attributes", []),
                methods=e.get("methods", []),
                extra={k: v for k, v in e.items() if k not in ("name", "type", "attributes", "methods")},
            )
            for e in desc.get("elements", [])
        ]
        relationships = [
            RelationshipIR(
                relationship=r.get("relationship", ""),
                source=r.get("source", ""),
                target=r.get("target", ""),
                extra={k: v for k, v in r.items() if k not in ("relationship", "source", "target")},
            )
            for r in desc.get("elements", []) if "relationship" in r
        ]
        diagram = DiagramIR(
            diagram_type=desc.get("diagram_type", "other"),
            caption=desc.get("caption", ""),
            elements=elements,
            relationships=relationships,
        )
        pages.append(PageIR(
            page_number=i,
            image_name=page.get("image", ""),
            diagram=diagram,
            raw_text=page.get("text", ""),
        ))
    return PDFIR(pdf_name=data.get("pdf_name", ""), pages=pages)
