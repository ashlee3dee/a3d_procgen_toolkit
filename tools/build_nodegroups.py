"""
Build the node groups in nodegroups/ into a .blend (the .blend is a build product).

Runs every group's create_group(), marks it as an asset with the metadata from
nodegroups/assets.json, keeps it alive with a fake user, and saves the file.

  blender --factory-startup -b --python tools/build_nodegroups.py -- [--output X.blend]
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
sys.path.insert(0, str(ROOT / ".blender_libs"))
sys.path.insert(0, str(ROOT))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=str(ROOT / "A3D_Procgen Toolkit_Generated.blend"))
    out = Path(ap.parse_args(argv).output)

    assets = json.loads((ROOT / "nodegroups" / "assets.json").read_text(encoding="utf-8"))
    for name, meta in assets.items():
        module = importlib.import_module(f"nodegroups.{meta['module']}")
        group = getattr(module, meta["class"]).create_group()
        group.use_fake_user = True
        if "catalog_id" in meta:
            group.asset_mark()
            data = group.asset_data
            data.catalog_id = meta["catalog_id"]
            data.description = meta["description"]
            data.author = meta["author"]
            for tag in meta["tags"]:
                data.tags.new(tag, skip_if_exists=True)

    missing = [n for n in assets if n not in bpy.data.node_groups]
    if missing:
        raise SystemExit(f"groups not built: {missing}")
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    print(f"built {len(assets)} node groups -> {out}")


main()
