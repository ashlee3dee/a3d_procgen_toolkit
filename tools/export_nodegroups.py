"""
Export every A3D_ node group in the open .blend to nodegroups/<module>.py (nodebpy).

One module per group, defining one Custom*Group class; groups used by other groups
are imported from their own module instead of being redefined. Asset metadata
(catalog, description, tags, author) goes to nodegroups/assets.json. Node positions
are not kept. Existing generated files are overwritten.

  blender -b file.blend --python tools/export_nodegroups.py -- [--prefix A3D_]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import bpy

ROOT = Path(r"T:\Art\Blender Projects\Gumroad Products\a3d_procgen_toolkit")
sys.path.insert(0, str(ROOT / ".blender_libs"))
from nodebpy.export import to_python  # noqa: E402

OUT = ROOT / "nodegroups"


def class_name(name):
    return "".join(w[:1].upper() + w[1:] for w in re.split(r"[^0-9A-Za-z]+", name) if w) or "Group"


def module_name(name):
    return re.sub(r"[^0-9a-z]+", "_", name.lower()).strip("_")


def direct_deps(group):
    return sorted({n.node_tree.name for n in group.nodes
                   if getattr(n, "node_tree", None) is not None and n.node_tree is not group})


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="A3D_")
    prefix = ap.parse_args(argv).prefix

    groups = sorted((g for g in bpy.data.node_groups
                     if g.bl_idname == "GeometryNodeTree" and g.name.startswith(prefix)),
                    key=lambda g: g.name)
    names = {g.name for g in groups}
    classes = {n: class_name(n) for n in names}
    modules = {n: module_name(n) for n in names}
    assert len(set(modules.values())) == len(modules), "module name collision"

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.py"):
        if old.name != "__init__.py":
            old.unlink()
    (OUT / "__init__.py").write_text('"""Node groups as nodebpy source; see tools/build_nodegroups.py."""\n')

    assets = {}
    for g in groups:
        deps = [d for d in direct_deps(g) if d in names]
        code = to_python(g, top_level="class", group_class_names=classes,
                         external_groups=deps)
        imports = "".join(f"from .{modules[d]} import {classes[d]}\n" for d in deps)
        header, _, rest = code.partition("\n\n\n")
        if not rest:  # no preamble separation; fall back to prepending
            header, rest = "", code
        (OUT / f"{modules[g.name]}.py").write_text(
            f"{header}\n{imports}\n\n{rest}" if header else f"{imports}\n\n{rest}",
            encoding="utf-8")
        a = g.asset_data
        if a:
            assets[g.name] = {"catalog_id": a.catalog_id, "description": a.description,
                              "tags": [t.name for t in a.tags], "author": a.author,
                              "class": classes[g.name], "module": modules[g.name]}
        else:
            assets[g.name] = {"class": classes[g.name], "module": modules[g.name]}

    (OUT / "assets.json").write_text(json.dumps(assets, indent=2, ensure_ascii=False) + "\n",
                                     encoding="utf-8")
    print(f"exported {len(groups)} node groups to {OUT}")


main()
