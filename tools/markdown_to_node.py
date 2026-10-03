"""
Apply node group and socket descriptions from Node_Reference.md onto the node
groups in the open .blend file.

Reads, per "### <node group name>" section (under a "## <category>" heading):
  - the "## <category>" heading                -> asset catalog "A3D_Procgen Toolkit/<category>"
                                                  (the parent must already be your library
                                                  catalog; subcatalogs are created in
                                                  blender_assets.cats.txt if missing;
                                                  the group is marked as an asset
                                                  unless --no-mark). "## Uncategorized"
                                                  leaves the catalog untouched.
  - the text under **Description**             -> node_group.description
                                                  (and asset_data.description if the
                                                  group is marked as an asset)
  - "- Name `Type`: description" bullets      -> interface socket .description
    (matched by node group + Inputs/Outputs + socket name)

Entries with no description in the reference are skipped, so existing
descriptions in the file are never blanked out.

The markdown is assumed to be well-formed: every node has a Description
section followed by explicit Inputs / Outputs headings.

Run from Blender's Scripting tab, or headless:
  blender -b file.blend --python tools/markdown_to_node.py -- \
      --reference "/path/Node Reference.md" [--exclude "A3D_X"] [--only-empty] \
      [--catalogs "/path/blender_assets.cats.txt"] [--catalog-parent "A3D_Procgen Toolkit"] \
      [--no-mark] [--dry-run] [--save]

After running, refresh the asset library (or reopen the file) so the Asset
Browser picks up newly written catalogs.
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

# ---------------------------------------------------------------------------
# Defaults (edit these, or override from the command line after "--")
# ---------------------------------------------------------------------------
ROOT = _TOOLS.parent
REFERENCE_PATH = str(ROOT / "Node Reference.md")  # "//" = folder of the .blend
EXCLUDE_NAMES = []     # exact node group names to skip
ONLY_EMPTY = False     # True = never overwrite a description that already exists
DRY_RUN = False        # True = report only, change nothing
SAVE = False           # True = save the .blend when done
# ---------------------------------------------------------------------------

def parse_args():
    """Read CLI args (everything after "--"), falling back to the defaults above."""
    p = argparse.ArgumentParser()
    p.add_argument("--reference", default=REFERENCE_PATH)
    p.add_argument("--exclude", nargs="*", default=None, help="Node group names to skip")
    node_reference.add_catalog_args(p)
    p.add_argument("--no-mark", action="store_true",
                   help="don't mark node groups as assets; only categorize ones that already are")
    p.add_argument("--only-empty", action="store_true", default=ONLY_EMPTY)
    p.add_argument("--dry-run", action="store_true", default=DRY_RUN)
    p.add_argument("--save", action="store_true", default=SAVE)
    a = p.parse_args(node_reference.script_args())
    # Use the command-line exclude list if given, otherwise the default list.
    a.exclude = set(a.exclude if a.exclude is not None else EXCLUDE_NAMES)
    return a


def parse_reference(text):
    """-> {node: {"category": str|None, "description": str|None,
                  "Inputs": {sock: [desc|None]}, "Outputs": {...}}}

    Socket descriptions are stored as a list per socket name so that sockets
    sharing a name (e.g. duplicates) can be matched up in order later.
    """
    parsed = reference.parse(text)
    for warning in parsed.warnings:
        print(f"warning: reference {warning}")
    ref = {}
    for category in parsed.categories:
        for node in category.nodes:
            entry = {"category": category.name, "description": node.description or None,
                     "Inputs": defaultdict(list), "Outputs": defaultdict(list)}
            for section, sockets in (("Inputs", node.inputs), ("Outputs", node.outputs)):
                for socket in sockets:
                    entry[section][socket.name].append(socket.description or None)
            ref[node.name] = entry
    return ref

def set_category(ng, category, catalog_ids, args, stats, report):
    """Assign the group to the catalog for `category`, marking it as an asset
    first if needed. Does nothing for Uncategorized / missing categories."""
    if not category or category == UNCATEGORIZED:
        return
    if ng.asset_data is None:
        if args.no_mark:
            report["not an asset (category not applied)"].append(ng.name)
            return
        if not args.dry_run:
            ng.asset_mark()
        stats["marked as assets"] += 1
    asset = ng.asset_data
    catalog_id = catalog_ids[category]
    if asset is not None and asset.catalog_id == catalog_id:
        stats["category: unchanged"] += 1
        return
    if asset is not None and not args.dry_run:
        asset.catalog_id = catalog_id
        if asset.catalog_id != catalog_id:
            report["write did not stick (property ignored the value)"].append(f"category: {ng.name}")
            return
    stats["category: set"] += 1


def apply(ref, args, report, catalog_ids=None):
    """Write the parsed categories and descriptions onto the node groups; returns a stats dict."""
    stats = defaultdict(int)
    catalog_ids = catalog_ids or {}

    def set_desc(target, new, kind, label):
        """Set target.description to `new` (node group, asset or socket), honoring
        --only-empty / --dry-run, and record the outcome in stats."""
        if not new:
            return  # nothing in the reference: never blank an existing description
        old = target.description
        if old == new:
            stats[f"{kind}: unchanged"] += 1
        elif old and args.only_empty:
            stats[f"{kind}: skipped (already has description)"] += 1
        else:
            if not args.dry_run:
                target.description = new
                # Verify the write actually took effect.
                if target.description != new:
                    report["write did not stick (property ignored the value)"].append(f"{kind}: {label}")
                    return
            stats[f"{kind}: " + ("replaced" if old else "set")] += 1

    # Node groups in the file, minus any excluded by name.
    groups = {ng.name: ng for ng in bpy.data.node_groups if ng.name not in args.exclude}

    for name in ref:
        if name not in groups and name not in args.exclude:
            report["in reference, not in file"].append(name)

    for name, ng in groups.items():
        entry = ref.get(name)
        if entry is None:
            report["in file, not in reference"].append(name)
            continue

        # Category first, so a freshly marked asset also gets its asset description below.
        if entry["category"]:
            set_category(ng, entry["category"], catalog_ids, args, stats, report)
        else:
            report["reference entry has no category"].append(name)

        # Node group description (plus the asset description if it's an asset).
        if entry["description"]:
            set_desc(ng, entry["description"], "node group description", name)
            asset = getattr(ng, "asset_data", None)
            if asset is not None:
                stats["node groups marked as assets"] += 1
                set_desc(asset, entry["description"], "asset description", name)
        else:
            report["reference has no description text"].append(name)

        # Copy each socket's description list into a queue keyed by
        # (section, socket name); duplicates are consumed in order.
        queues = {}
        for sec in ("Inputs", "Outputs"):
            for sock_name, descs in entry[sec].items():
                queues[(sec, sock_name)] = list(descs)

        # Walk the group's interface and apply descriptions to matching sockets.
        seen = set()
        for item in ng.interface.items_tree:
            if item.item_type != 'SOCKET':
                continue  # skip panels
            sec = "Inputs" if item.in_out == 'INPUT' else "Outputs"
            key = (sec, item.name)
            seen.add(key)
            descs = queues.get(key)
            if descs is None:
                report["socket in file, not in reference"].append(f"{name} / {sec} / {item.name}")
            elif descs:
                set_desc(item, descs.pop(0), "socket description", f"{name} / {item.name}")

        # Anything left in the reference that never matched a socket in the file.
        for (sec, sock_name) in queues:
            if (sec, sock_name) not in seen:
                report["socket in reference, not in file"].append(f"{name} / {sec} / {sock_name}")

    return stats


def main():
    args = parse_args()
    path = bpy.path.abspath(args.reference)  # resolves "//" relative to the .blend
    print(f"Using {path}")
    report = defaultdict(list)  # category -> list of problem entries

    with open(path, encoding="utf-8") as f:
        ref = parse_reference(f.read())

    categories = sorted({e["category"] for e in ref.values()
                         if e["category"] and e["category"] != UNCATEGORIZED})
    catalogs_path = (node_reference.find_catalogs_file(bpy.data.filepath, args.catalogs)
                     or Path(bpy.data.filepath).resolve().parent / node_reference.CATALOGS_FILENAME)
    print(f"Using catalogs file {catalogs_path}")
    catalog_ids, created = node_reference.ensure_catalogs(
        catalogs_path, categories, args.catalog_parent, write=not args.dry_run)
    if created:
        print(f"{'Would create' if args.dry_run else 'Created'} catalogs: {', '.join(created)}")

    stats = apply(ref, args, report, catalog_ids)

    # Print mismatches/problems found along the way.
    for key, items in report.items():
        print(f"\n{key} ({len(items)}):")
        for item in items:
            print(f"  - {item}")

    # Print counts of what was changed/skipped.
    print("\n=== Summary" + (" (dry run, nothing changed)" if args.dry_run else "") + " ===")
    for key in sorted(stats):
        print(f"  {key}: {stats[key]}")

    if args.save and not args.dry_run:
        bpy.ops.wm.save_mainfile()
        print(f"Saved {bpy.data.filepath}")


main()