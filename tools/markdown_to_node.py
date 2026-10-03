"""
Apply node group and socket descriptions from Node_Reference.md onto the node
groups in the open .blend file.

Reads, per "### <node group name>" section:
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
      [--dry-run] [--save]
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import bpy

# ---------------------------------------------------------------------------
# Defaults (edit these, or override from the command line after "--")
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
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

# Node heading: "## Name", "### Name" or "#### Name".
RE_NODE = re.compile(r"^#{2,4} (.+?)\s*$")

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
    """-> {node: {"description": str|None, "Inputs": {sock: [desc|None]}, "Outputs": {...}}}

    Socket descriptions are stored as a list per socket name so that sockets
    sharing a name (e.g. duplicates) can be matched up in order later.
    """
    ref = {}
    node = section = None   # current node heading / current section within it
    desc_lines = []         # accumulates lines of the current Description block

    def flush_desc():
        """Store the accumulated Description lines on the current node, joined
        into one line with whitespace collapsed."""
        if node is not None and desc_lines:
            ref[node]["description"] = " ".join(" ".join(desc_lines).split()) or None

    for line in text.splitlines():
        if m := RE_NODE.match(line):
            # New node heading: finish the previous node and start a fresh entry.
            flush_desc()
            node, section, desc_lines = m.group(1), None, []
            ref[node] = {"description": None, "Inputs": defaultdict(list), "Outputs": defaultdict(list)}
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


def apply(ref, args, report):
    """Write the parsed descriptions onto the node groups; returns a stats dict."""
    stats = defaultdict(int)

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

    stats = apply(ref, args, report)

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