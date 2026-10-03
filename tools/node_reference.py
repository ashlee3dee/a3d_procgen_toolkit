"""
Blender asset catalog helpers for the Node Reference.md <-> Blender round trip.

The markdown format itself lives in reference.py. Layout:
  ## Category name          -> Blender asset catalog "<CATALOG_PARENT>/<Category name>"
  ### A3D_Node Name         -> node group

No bpy import here, so this can be used (and tested) outside Blender.
"""
import sys
import uuid
from pathlib import Path

CATALOGS_FILENAME = "blender_assets.cats.txt"
CATALOG_PARENT = "A3D_Procgen Toolkit"   # existing library catalog the categories nest under
UNCATEGORIZED = "Uncategorized"   # heading for node groups with no catalog

_CATALOGS_HEADER = """\
# This is an Asset Catalog Definition file for Blender.
#
# Empty lines and lines starting with `#` will be ignored.
# The first non-ignored line should be the version indicator.
# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"

VERSION 1
"""


def find_catalogs_file(blend_filepath, override=None):
    """Path of an existing catalogs file: the override, else the nearest one
    in the .blend's folder or any parent folder. None if there isn't one."""
    if override:
        return Path(override)
    if not blend_filepath:
        return None
    folder = Path(blend_filepath).resolve().parent
    for candidate in (folder, *folder.parents):
        path = candidate / CATALOGS_FILENAME
        if path.is_file():
            return path
    return None


def read_catalogs(path):
    """-> {uuid: catalog path} from a catalogs file ({} if it doesn't exist)."""
    catalogs = {}
    if path is None or not Path(path).is_file():
        return catalogs
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("VERSION"):
            continue
        parts = line.split(":", 2)
        if len(parts) == 3:
            catalogs[parts[0]] = parts[1]
    return catalogs


def simple_name(catalog_path):
    """Blender's 'simple name' convention: the path with '/' replaced by '-'."""
    return catalog_path.replace("/", "-")


def catalog_path(category, parent=CATALOG_PARENT):
    """Full catalog path for a category: '<parent>/<category>' (or just the category)."""
    return f"{parent}/{category}" if parent else category


def category_from_catalog(path, parent=CATALOG_PARENT):
    """Inverse of catalog_path; None if `path` isn't directly under `parent`."""
    if not parent:
        return path
    prefix = parent + "/"
    if path.startswith(prefix) and "/" not in path[len(prefix):]:
        return path[len(prefix):]
    return None


def ensure_catalogs(path, categories, parent=CATALOG_PARENT, write=True):
    """-> ({category: uuid}, [catalog paths that had to be created]).

    Each category lives at '<parent>/<category>'. Existing catalogs are matched
    by path; the parent catalog and any missing categories get a new UUID and,
    when `write` is true, are appended to the catalogs file (created if absent).
    """
    path = Path(path)
    existing = {cat_path: cat_id for cat_id, cat_path in read_catalogs(path).items()}
    wanted = ([parent] if parent else []) + [catalog_path(c, parent) for c in categories]
    new_ids, created = {}, []
    for cat_path in wanted:
        if cat_path not in existing:
            new_ids[cat_path] = str(uuid.uuid4())
            created.append(cat_path)
    if created and write:
        text = path.read_text(encoding="utf-8") if path.is_file() else _CATALOGS_HEADER
        if not text.endswith("\n"):
            text += "\n"
        text += "".join(f"{new_ids[c]}:{c}:{simple_name(c)}\n" for c in created)
        path.write_text(text, encoding="utf-8", newline="\n")
    ids = {c: existing.get(catalog_path(c, parent)) or new_ids[catalog_path(c, parent)]
           for c in categories}
    return ids, created


def script_args():
    """Arguments after "--" on a `blender ... --python script.py -- args` command line."""
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def add_catalog_args(parser):
    parser.add_argument("--catalogs", default=None,
                        help="blender_assets.cats.txt to use (default: nearest to the .blend)")
    parser.add_argument("--catalog-parent", default=CATALOG_PARENT,
                        help="existing library catalog the categories are nested under ('' = top level)")
