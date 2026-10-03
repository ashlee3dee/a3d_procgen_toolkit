"""
Generate Node Reference.md from the node groups in the open .blend file.

Per node group it writes the group description plus every input/output socket
(name, type, description), in the same format apply_descriptions.py reads.

Run from Blender's Scripting tab, or headless:
  blender -b file.blend --python node_to_markdown.py -- \
      [--output "/path/Node Reference.md"] [--prefix A3D_] [--exclude "A3D_X"]
"""
import argparse
import sys
from pathlib import Path

import bpy

OUTPUT_PATH = r"T:\Art\Blender Projects\Gumroad Products\a3d_procgen_toolkit\Node Reference.md"
PREFIX = "A3D_"       # only node groups whose name starts with this ("" = all)
EXCLUDE_NAMES = []    # exact node group names to skip

TYPE_NAMES = {
    "NodeSocketBool": "Boolean",
    "NodeSocketInt": "Integer",
}


def type_name(socket_type):
    if socket_type in TYPE_NAMES:
        return TYPE_NAMES[socket_type]
    return socket_type.removeprefix("NodeSocket")


def one_line(text):
    return " ".join((text or "").split())


def socket_lines(group, in_out):
    lines = []
    for item in group.interface.items_tree:
        if item.item_type != "SOCKET" or item.in_out != in_out:
            continue
        desc = one_line(item.description)
        line = f"- {item.name} `{type_name(item.socket_type)}`"
        lines.append(f"{line} — {desc}" if desc else line)
    return lines


def node_section(group):
    parts = [f"### {group.name}", "", "**Description**", "", one_line(group.description), ""]
    for title, in_out in (("Inputs", "INPUT"), ("Outputs", "OUTPUT")):
        parts += [f"**{title}**", ""]
        lines = socket_lines(group, in_out)
        parts += lines + [""] if lines else []
    return "\n".join(parts).rstrip("\n") + "\n"


def build(prefix, exclude):
    groups = [
        g for g in bpy.data.node_groups
        if g.bl_idname == "GeometryNodeTree"
        and g.name.startswith(prefix)
        and g.name not in exclude
    ]
    groups.sort(key=lambda g: g.name.lower())
    return "\n\n".join(node_section(g) for g in groups), len(groups)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=OUTPUT_PATH)
    ap.add_argument("--prefix", default=PREFIX)
    ap.add_argument("--exclude", action="append", default=list(EXCLUDE_NAMES))
    args = ap.parse_args(argv)

    text, count = build(args.prefix, set(args.exclude))
    out = Path(bpy.path.abspath(args.output))
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {count} node groups to {out}")


main()
