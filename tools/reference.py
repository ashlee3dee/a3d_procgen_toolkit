"""
The one place that knows the Node Reference.md format. Pure stdlib (no bpy), so
the Blender scripts, the site builder and the tests all share it.

Layout:
  ## Category name
  ### A3D_Node Name
  **Description**
  One paragraph of text.
  **Inputs**
  - Socket name `Type`: description
  **Outputs**
  - Socket name `Type`: description

Nodes that appear before any "## " heading go in a Category whose name is None.
"""
import re
from dataclasses import dataclass, field

SEP = ": "

_CATEGORY = re.compile(r"^## (.+?)\s*$")
_NODE = re.compile(r"^### (.+?)\s*$")
_SECTION = re.compile(r"^\*\*(Description|Inputs|Outputs):?\*\*\s*$")
_SOCKET = re.compile(
    r"^[-*+] (?P<name>.*?)(?: `(?P<type>[^`]*)`)?(?:" + re.escape(SEP) + r"(?P<desc>.*))?\s*$"
)


@dataclass
class Socket:
    name: str
    type: str = ""
    description: str = ""


@dataclass
class Node:
    name: str
    description: str = ""
    inputs: list = field(default_factory=list)
    outputs: list = field(default_factory=list)


@dataclass
class Category:
    name: "str | None"
    nodes: list = field(default_factory=list)


@dataclass
class Reference:
    categories: list = field(default_factory=list)
    warnings: list = field(default_factory=list)   # lines the parser could not place

    def nodes(self):
        return [n for c in self.categories for n in c.nodes]


def one_line(text):
    return " ".join((text or "").split())


def parse(text):
    ref = Reference()
    category = node = section = None
    desc = []

    def flush():
        if node is not None and desc:
            node.description = one_line(" ".join(desc))

    for number, line in enumerate(text.splitlines(), 1):
        if m := _CATEGORY.match(line):
            flush()
            category, node, section, desc = Category(m.group(1)), None, None, []
            ref.categories.append(category)
        elif m := _NODE.match(line):
            flush()
            if category is None:
                category = Category(None)
                ref.categories.append(category)
            node, section, desc = Node(m.group(1)), None, []
            category.nodes.append(node)
        elif node is None or not line.strip():
            continue
        elif m := _SECTION.match(line):
            flush()
            section, desc = m.group(1), []
        elif section == "Description":
            desc.append(line.strip())
        elif section in ("Inputs", "Outputs") and (m := _SOCKET.match(line)):
            socket = Socket(m.group("name").strip(), m.group("type") or "", one_line(m.group("desc")))
            (node.inputs if section == "Inputs" else node.outputs).append(socket)
        else:
            ref.warnings.append(f"line {number}: ignored {line.strip()!r}")
    flush()
    return ref


def render_socket(socket):
    line = f"- {socket.name}" + (f" `{socket.type}`" if socket.type else "")
    return f"{line}{SEP}{one_line(socket.description)}" if socket.description else line


def render_node(node):
    parts = [f"### {node.name}", "", "**Description**", "", one_line(node.description), ""]
    for title, sockets in (("Inputs", node.inputs), ("Outputs", node.outputs)):
        parts += [f"**{title}**", ""]
        if sockets:
            parts += [render_socket(s) for s in sockets] + [""]
    return "\n".join(parts).rstrip("\n") + "\n"


def render(ref):
    chunks = []
    for category in ref.categories:
        body = "\n".join(render_node(n) for n in category.nodes)
        chunks.append(body if category.name is None else f"## {category.name}\n\n{body}")
    return "\n".join(chunks)
