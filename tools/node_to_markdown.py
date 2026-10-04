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

# Folder with this script and node_reference.py. Blender's text editor doesn't give
# a real __file__ for text blocks inside the .blend; set this path in that case.
TOOLS_DIR = r"T:\Art\Blender Projects\Gumroad Products\a3d_procgen_toolkit\tools"
_TOOLS = Path(TOOLS_DIR or Path(__file__).resolve().parent)
sys.path.insert(0, str(_TOOLS))
import reference
import node_reference
importlib.reload(reference)  # pick up edits when re-run in the same Blender session
importlib.reload(node_reference)
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


def sockets(group, in_out):
    return [
        reference.Socket(item.name, type_name(item.socket_type), item.description or "")
        for item in group.interface.items_tree
        if item.item_type == "SOCKET" and item.in_out == in_out
    ]


def description_of(group, previous=""):
    """A group has two descriptions: the node group's and (for assets) the asset's.
    If they disagree, use the one that differs from the previous reference text,
    i.e. the one that was just edited."""
    texts = [group.description or ""]
    if group.asset_data:
        texts.append(group.asset_data.description or "")
    for text in texts:
        if text.strip() and text.strip() != previous.strip():
            return text
    return texts[0]


def to_node(group, previous=""):
    return reference.Node(group.name, description_of(group, previous),
                          sockets(group, "INPUT"), sockets(group, "OUTPUT"))


def build(prefix, exclude, catalogs, previous_text, parent=node_reference.CATALOG_PARENT):
    """-> (markdown text, node group count, list of notes about categories)"""
    groups = [
        g for g in bpy.data.node_groups
        if g.bl_idname == "GeometryNodeTree"
        and g.name.startswith(prefix)
        and g.name not in exclude
    ]
    previous_ref = reference.parse(previous_text)
    previous = {n.name: c.name for c in previous_ref.categories for n in c.nodes}
    previous_desc = {n.name: n.description for c in previous_ref.categories for n in c.nodes}
    order = list(dict.fromkeys(c.name for c in previous_ref.categories if c.name))

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

    ref = reference.Reference([
        reference.Category(c, [to_node(g, previous_desc.get(g.name, "")) for g in sorted(by_category[c], key=lambda g: g.name.lower())])
        for c in ordered
    ])
    return reference.render(ref), len(groups), notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=OUTPUT_PATH)
    ap.add_argument("--prefix", default=PREFIX)
    ap.add_argument("--exclude", action="append", default=list(EXCLUDE_NAMES))
    node_reference.add_catalog_args(ap)
    args = ap.parse_args(node_reference.script_args())

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
