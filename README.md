# x2x — Generic Transformation & Communication Router

Converts any input through a configurable pipeline of **transforms** and **communicators**.

## Architecture

```
Input → [Transform Chain] → [Communicator Chain] → Output
```

- **Transforms**: pure functions that mutate/convert data
- **Communicators**: functions that send/receive data over network/API

## Layers

| Layer | File | Purpose |
|-------|------|---------|
| IR | `src/conversion/ir.py` | Normalized intermediate representation |
| AST | `src/conversion/ast.py` | Abstract syntax tree from IR |
| DSL | `src/conversion/dsl.py` | Domain-specific script from AST |
| Router | `src/routing.py` | Orchestrates transforms + communicators |
| Plugins | `src/plugins/` | Extensible transformation plugins |

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `char_replace` | Character replacement (●→□, etc.) |
| `translate` | Translation |
| `extension_convert` | File extension conversion |
| `voice_to_spectrum` | Voice to spectrum conversion |
| `abstract_to_class` | Intent to class definition |
| `bullet_normalizer` | Bullet character normalization |
| `generic_transformer` | Configurable multi-transform |
| `ronbun2x` | Ronbun2x API wrapper |

## Quick Start

```python
from x2x.src.routing import Router

router = Router()
router.add_transform(lambda x: x.replace("●", "□"))
router.add_transform(lambda x: x.upper())
router.add_communicator("mock", lambda x: {"result": x})

result = router.run("hello ● world")
print(result)
# → {'mock_result': 'HELLO □ WORLD'}
```

## JSON → IR → AST → DSL

```python
from x2x.src.conversion import ir, ast, dsl

raw_json = {"pdf_name": "test.pdf", "pages": [{"page_number": 1, "image_name": "fig.png", "diagram": {"diagram_type": "class", "caption": "UML", "elements": []}, "raw_text": "text"}]}

pdf_ir = ir.json_to_ir(raw_json)
ast_node = ast.ir_to_ast(pdf_ir)
dsl_script = dsl.ast_to_dsl(ast_node)
```