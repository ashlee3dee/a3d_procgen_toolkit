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
  - "- Name `Type` — description" bullets      -> interface socket .description
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
import re
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
from node_reference import RE_CATEGORY, UNCATEGORIZED

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

# Node groups whose name in the .blend differs from their heading in the
# reference: {name in .blend: heading in reference}. Remove once the typo is fixed.
NAME_ALIASES = {}

# Separator between a socket's name/type and its description in a bullet.
SEP = " — "

# Node heading: "### Name" ("## Name" is a category, see node_reference).
RE_NODE = re.compile(r"^### (.+?)\s*$")

# Section marker: either "**Description**" style or "### Description" style
# (colon optional). Group 1 or 2 holds the section name.
RE_SECTION = re.compile(
    r"^(?:\*\*(Description|Inputs|Outputs):?\*\*|#{1,6}\s*(Description|Inputs|Outputs):?)\s*$"
)

# Any markdown list bullet ("-", "*" or "+").
RE_BULLET = re.compile(r"^[-*+] ")

# A socket bullet: "- Name `Type` — description"
# (the `Type` part and the description are both optional).
RE_SOCKET = re.compile(
    r"^[-*+] (?P<name>.*?)(?: `(?P<type>[^`]*?)`?)?(?:" + re.escape(SEP) + r"(?P<desc>.*))?\s*$"
)


def parse_args():
    """Read CLI args (everything after "--"), falling back to the defaults above."""
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--reference", default=REFERENCE_PATH)
    p.add_argument("--exclude", nargs="*", default=None, help="Node group names to skip")
    p.add_argument("--catalogs", default=None,
                   help="blender_assets.cats.txt to use (default: nearest to the .blend, "
                        "else a new one beside it)")
    p.add_argument("--catalog-parent", default=node_reference.CATALOG_PARENT,
                   help="existing library catalog the categories are nested under "
                        "('' = top level)")
    p.add_argument("--no-mark", action="store_true",
                   help="don't mark node groups as assets; only categorize ones that already are")
    p.add_argument("--only-empty", action="store_true", default=ONLY_EMPTY)
    p.add_argument("--dry-run", action="store_true", default=DRY_RUN)
    p.add_argument("--save", action="store_true", default=SAVE)
    p.add_argument("--verbose", action="store_true", default=False,
                   help="print node group/asset descriptions as parsed and as read back")
    a = p.parse_args(argv)
    # Use the command-line exclude list if given, otherwise the default list.
    a.exclude = set(a.exclude if a.exclude is not None else EXCLUDE_NAMES)
    return a


def parse_reference(text):
    """-> {node: {"category": str|None, "description": str|None,
                  "Inputs": {sock: [desc|None]}, "Outputs": {...}}}

    Socket descriptions are stored as a list per socket name so that sockets
    sharing a name (e.g. duplicates) can be matched up in order later.
    """
    ref = {}
    category = None         # current "## " category heading
    node = section = None   # current node heading / current section within it
    desc_lines = []         # accumulates lines of the current Description block

    def flush_desc():
        """Store the accumulated Description lines on the current node, joined
        into one line with whitespace collapsed."""
        if node is not None and desc_lines:
            ref[node]["description"] = " ".join(" ".join(desc_lines).split()) or None

    for line in text.splitlines():
        if m := RE_CATEGORY.match(line):
            # Category heading: finish the previous node; nodes below belong to it.
            flush_desc()
            category, node, section, desc_lines = m.group(1), None, None, []
            continue
        if m := RE_NODE.match(line):
            # New node heading: finish the previous node and start a fresh entry.
            flush_desc()
            node, section, desc_lines = m.group(1), None, []
            ref[node] = {"category": category, "description": None,
                         "Inputs": defaultdict(list), "Outputs": defaultdict(list)}
        elif node is None:
            # Anything before the first node heading is ignored.
            continue
        elif m := RE_SECTION.match(line):
            # New section marker (Description / Inputs / Outputs).
            flush_desc()
            section, desc_lines = (m.group(1) or m.group(2)), []

        if section == "Description":
            # Collect description text, skipping blanks and heading/section lines.
            if line.strip() and not RE_NODE.match(line) and not RE_SECTION.match(line):
                desc_lines.append(line.strip())
        elif section in ("Inputs", "Outputs") and RE_BULLET.match(line):
            # Socket bullet: record its description (None if it has none).
            m = RE_SOCKET.match(line)
            if m:
                desc = (m.group("desc") or "").strip() or None
                ref[node][section][m.group("name")].append(desc)

    # Don't forget the last node's description.
    flush_desc()
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
                if args.verbose and kind != "socket description":
                    print(f"[{kind}] {label}\n    parsed   ({len(new)}): {new!r}\n"
                          f"    read back({len(target.description)}): {target.description!r}")
                # Verify the write actually took effect.
                if target.description != new:
                    report["write did not stick (property ignored the value)"].append(f"{kind}: {label}")
                    return
            stats[f"{kind}: " + ("replaced" if old else "set")] += 1

    # Node groups in the file, minus any excluded by name.
    groups = {ng.name: ng for ng in bpy.data.node_groups if ng.name not in args.exclude}

    # Reference headings that are covered by an alias shouldn't be reported as missing.
    aliased = {ref_name for blend_name, ref_name in NAME_ALIASES.items() if blend_name in groups}
    for name in ref:
        if name not in groups and name not in aliased and name not in args.exclude:
            report["in reference, not in file"].append(name)

    for name, ng in groups.items():
        # Look up by file name first, then by its aliased reference heading.
        entry = ref.get(name) or ref.get(NAME_ALIASES.get(name))
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