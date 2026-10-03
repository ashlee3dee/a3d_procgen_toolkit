import argparse
import os
import sys

import bpy

# ---------------------------------------------------------------------------
# Defaults (edit these, or override from the command line after "--", e.g.
#   blender -b file.blend --python write_node_data.py -- \
#       --exclude "Node A" "Node B" --out-dir //reports
# ---------------------------------------------------------------------------
EXCLUDE_NAMES = ['Node Group Container', 'Visual Scripting Editor', 'Compositing Node Tree']       # exact node group names to skip
OUTPUT_DIR = "T:\\Art\\Blender Projects\\Gumroad Products\\a3d_procgen_toolkit\\"        # "//" = folder of the .blend; absolute paths also work
# ---------------------------------------------------------------------------


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", nargs="*", default=None,
                        help="Node group names to filter out")
    parser.add_argument("--out-dir", default=None,
                        help="Directory to save the text file in")
    args = parser.parse_args(argv)
    exclude = set(args.exclude if args.exclude is not None else EXCLUDE_NAMES)
    out_dir = args.out_dir if args.out_dir is not None else OUTPUT_DIR
    return exclude, out_dir


def fmt_desc(text):
    """Return a printable description, flagging empty ones."""
    return repr(text) if text else "(none)"


exclude, out_dir = parse_args()
lines = []


def emit(text=""):
    print(text)
    lines.append(text)


node_groups = [ng for ng in bpy.data.node_groups if ng.name not in exclude]
skipped = len(bpy.data.node_groups) - len(node_groups)

#emit("=== Node Groups in File ===")
for ng in node_groups:
    emit(f"Name: {ng.name!r}")
    emit(f"  Type: {ng.type}")
    emit(f"  Description: {fmt_desc(ng.description)}")
    emit(f"  Users: {ng.users}")
    emit(f"  Fake user: {ng.use_fake_user}")
    emit(f"  Nodes: {len(ng.nodes)}")

    inputs = [s for s in ng.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'INPUT']
    outputs = [s for s in ng.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'OUTPUT']

    emit("  Inputs:")
    for s in inputs:
        emit(f"    - {s.name!r}: {s.socket_type}")
        emit(f"        Description: {fmt_desc(s.description)}")

    emit("  Outputs:")
    for s in outputs:
        emit(f"    - {s.name!r}: {s.socket_type}")
        emit(f"        Description: {fmt_desc(s.description)}")

    emit()

emit(f"Total: {len(node_groups)} node group(s) ({skipped} excluded)")

# Save to file
blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0] or "untitled"
out_path = os.path.join(bpy.path.abspath(out_dir), f"{blend_name}_node_data.txt")
try:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSaved to: {out_path}")
except OSError as e:
    print(f"\nFailed to save {out_path}: {e}")