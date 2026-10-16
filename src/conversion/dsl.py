"""DSL generator: render AST into a domain-specific script text.

DSL grammar (example):

    PDF <name>
      PAGE <n> IMAGE <file>
        DIAGRAM <type>
          CAPTION "<text>"
          ELEMENT <name> <type> [attr1, attr2] [m1, m2]
          REL <rel> <source> -> <target>
"""

from __future__ import annotations

from .ast import ASTNode


def escape_str(s: str) -> str:
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def render(ast: ASTNode) -> str:
    lines: list[str] = []

    def walk(node: ASTNode, indent: int = 0) -> None:
        pad = "  " * indent
        kind = node.kind
        val = node.value or {}

        if kind == "program":
            lines.append(f'PDF "{escape_str(str(val))}"')
        elif kind == "pdf":
            pass  # metadata handled by program
        elif kind == "page":
            lines.append(
                f'{pad}PAGE {val.get("page_number")} IMAGE "{escape_str(val.get("image_name",""))}"'
            )
        elif kind == "diagram":
            lines.append(f'{pad}  DIAGRAM {val.get("diagram_type","other")}')
            if val.get("caption"):
                lines.append(f'{pad}    CAPTION "{escape_str(val.get("caption"))}"')
        elif kind == "elements":
            pass
        elif kind == "element":
            attrs = ", ".join(val.get("attributes", []))
            methods = ", ".join(val.get("methods", []))
            lines.append(
                f'{pad}    ELEMENT "{escape_str(val.get("name"))}" {escape_str(val.get("type"))}'
                f' [{attrs}] [{methods}]'
            )
        elif kind == "relationships":
            pass
        elif kind == "relationship":
            lines.append(
                f'{pad}    REL {val.get("relationship")} {escape_str(val.get("source"))} -> {escape_str(val.get("target"))}'
            )

        for child in node.children:
            walk(child, indent + 1)

    walk(ast)
    return "\n".join(lines)


def ast_to_dsl(ast: ASTNode) -> str:
    return render(ast)
