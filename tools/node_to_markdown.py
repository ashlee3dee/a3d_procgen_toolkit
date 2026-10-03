"""
Generate Node Reference.md from the node groups in the open .blend file.

Node groups are grouped under "## <category>" headings taken from their asset
catalog (blender_assets.cats.txt); each group is a "### <name>" section with its
description and every input/output socket (name, type, description), in the
same format markdown_to_node.py reads.

A group with no catalog keeps the category it already has in the existing
reference; otherwise it goes under "## Uncategorized". Category order follows
the existing reference, with new categories appended alphabetically.

Run from Blender's Scripting tab, or headless:
  blender -b file.blend --python tools/node_to_markdown.py -- \
      [--output "/path/Node Reference.md"] [--prefix A3D_] [--exclude "A3D_X"] \
      [--catalogs "/path/blender_assets.cats.txt"] [--catalog-parent "A3D_Procgen Toolkit"]
"""
import argparse
import importlib
import sys
from collections import defaultdict
from pathlib import Path

import bpy

# Folder containing this script and node_reference.py. Only needed when the
# script is run from a text block inside the .blend (where __file__ is not a
# real path); set it to e.g. r"T:\...\a3d_procgen_toolkit\tools".
TOOLS_DIR = ""


def _find_tools_dir():
    candidates = [TOOLS_DIR, str(Path(__file__).resolve().parent)]
    text = bpy.data.texts.get(Path(__file__).name)  # text block linked to an external file
    if text is not None and text.filepath:
        candidates.append(str(Path(bpy.path.abspath(text.filepath)).resolve().parent))
    for c in candidates:
        if c and (Path(c) / "node_reference.py").is_file():
            return Path(c)
    raise FileNotFoundError(
        "Can't find node_reference.py. Set TOOLS_DIR at the top of this script to the repo's tools folder."
    )


_TOOLS = _find_tools_dir()
sys.path.insert(0, str(_TOOLS))
import node_reference
importlib.reload(node_reference)  # pick up edits when re-run in the same Blender session
from node_reference import UNCATEGORIZED

ROOT = _TOOLS.parent
OUTPUT_PATH = str(ROOT / "Node Reference.md")
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


def build(prefix, exclude, catalogs, previous_text, parent=node_reference.CATALOG_PARENT):
    """-> (markdown text, node group count, list of notes about categories)"""
    groups = [
        g for g in bpy.data.node_groups
        if g.bl_idname == "GeometryNodeTree"
        and g.name.startswith(prefix)
        and g.name not in exclude
    ]
    previous, order = node_reference.parse_categories(previous_text)

    notes = []
    by_category = defaultdict(list)
    for g in groups:
        asset = g.asset_data
        catalog_id = asset.catalog_id if asset else None
        category = node_reference.category_from_catalog(catalogs.get(catalog_id, ""), parent)
        if category is None:
            category = previous.get(g.name) or UNCATEGORIZED
            if asset and catalog_id and catalog_id != "00000000-0000-0000-0000-000000000000":
                notes.append(f"{g.name}: catalog {catalogs.get(catalog_id, catalog_id)!r} "
                             f"is not directly under {parent!r}; kept previous category")
        by_category[category].append(g)

    known = [c for c in order if c in by_category and c != UNCATEGORIZED]
    new = sorted((c for c in by_category if c not in known and c != UNCATEGORIZED), key=str.casefold)
    ordered = known + new + ([UNCATEGORIZED] if UNCATEGORIZED in by_category else [])

    chunks = []
    for category in ordered:
        members = sorted(by_category[category], key=lambda g: g.name.lower())
        chunks.append(f"## {category}\n\n" + "\n".join(node_section(g) for g in members))
    return "\n".join(chunks), len(groups), notes


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=OUTPUT_PATH)
    ap.add_argument("--prefix", default=PREFIX)
    ap.add_argument("--exclude", action="append", default=list(EXCLUDE_NAMES))
    ap.add_argument("--catalogs", default=None,
                    help="blender_assets.cats.txt (default: nearest to the .blend)")
    ap.add_argument("--catalog-parent", default=node_reference.CATALOG_PARENT,
                    help="library catalog the categories are nested under ('' = top level)")
    args = ap.parse_args(argv)

    out = Path(bpy.path.abspath(args.output))
    previous_text = out.read_text(encoding="utf-8") if out.is_file() else ""

    catalogs_path = node_reference.find_catalogs_file(bpy.data.filepath, args.catalogs)
    if catalogs_path is None:
        print("No blender_assets.cats.txt found; categories come from the existing reference only.")
    else:
        print(f"Using catalogs file {catalogs_path}")
    catalogs = node_reference.read_catalogs(catalogs_path)

    text, count, notes = build(args.prefix, set(args.exclude), catalogs, previous_text,
                               args.catalog_parent)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {count} node groups to {out}")
    for note in notes:
        print(f"  warning: {note}")


main()
