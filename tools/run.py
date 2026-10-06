"""Single entry point for the toolkit scripts.

  python tools/run.py site                  rebuild docs/index.html
  python tools/run.py test                  run the unit tests
  python tools/run.py gifs [--lossy 40]     compress assets/node_images/*.gif
  python tools/run.py pull --blend X.blend  .blend -> Node Reference.md   (needs Blender)
  python tools/run.py push --blend X.blend  Node Reference.md -> .blend   (needs Blender)
  python tools/run.py export --blend X.blend  .blend -> nodegroups/*.py       (one-off migration)
  python tools/run.py build [--output X.blend]  nodegroups/*.py -> .blend      (needs Blender)

Anything after the subcommand's own options is passed to the underlying script,
e.g. `push --blend X.blend --dry-run` or `pull --blend X.blend --prefix A3D_`.
Blender is found via --blender, the BLENDER environment variable, or PATH;
the .blend via --blend or the A3D_BLEND environment variable.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent


def run(cmd):
    print("+ " + " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], cwd=ROOT).returncode


def blender_cmd(args, script):
    blender = args.blender or os.environ.get("BLENDER") or shutil.which("blender")
    blend = args.blend or os.environ.get("A3D_BLEND")
    if not blender:
        sys.exit("Blender not found: pass --blender, set BLENDER, or add it to PATH.")
    if not blend or not Path(blend).is_file():
        sys.exit(f"Blend file not found ({blend!r}): pass --blend or set A3D_BLEND.")
    return [blender, "-b", blend, "--python", TOOLS / script, "--", *args.extra]


def nodegroups_cmd(args):
    blender = args.blender or os.environ.get("BLENDER") or shutil.which("blender")
    if not blender:
        sys.exit("Blender not found: pass --blender, set BLENDER, or add it to PATH.")
    if args.command == "build":
        return [blender, "--factory-startup", "-b", "--python", TOOLS / "build_nodegroups.py", "--", *args.extra]
    blend = args.blend or os.environ.get("A3D_BLEND")
    if not blend or not Path(blend).is_file():
        sys.exit(f"Blend file not found ({blend!r}): pass --blend or set A3D_BLEND.")
    return [blender, "--factory-startup", "-b", blend, "--python", TOOLS / "export_nodegroups.py", "--", *args.extra]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text, script in (
        ("pull", "write Node Reference.md from the .blend", "node_to_markdown.py"),
        ("push", "apply Node Reference.md to the .blend", "markdown_to_node.py"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.set_defaults(script=script)
        p.add_argument("--blend", help="the .blend file (default: $A3D_BLEND)")
        p.add_argument("--blender", help="Blender executable (default: $BLENDER, then PATH)")
    for name, help_text in (
        ("export", "write nodegroups/*.py from the .blend (one-off migration)"),
        ("build", "build nodegroups/*.py into a .blend"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--blender", help="Blender executable (default: $BLENDER, then PATH)")
        if name == "export":
            p.add_argument("--blend", help="the .blend file (default: $A3D_BLEND)")
    sub.add_parser("site", help="rebuild docs/index.html")
    sub.add_parser("test", help="run the unit tests")
    sub.add_parser("gifs", help="compress node GIFs (options go to compress_gifs.py)")

    args, extra = parser.parse_known_args(argv)
    args.extra = extra

    if args.command in ("export", "build"):
        return run(nodegroups_cmd(args))
    if args.command in ("pull", "push"):
        return run(blender_cmd(args, args.script))
    if args.command == "site":
        return run([sys.executable, TOOLS / "build_site.py", *extra])
    if args.command == "gifs":
        return run([sys.executable, TOOLS / "compress_gifs.py", *extra])
    return run([sys.executable, "-m", "unittest", "discover", "-s", "tests", *extra])


if __name__ == "__main__":
    sys.exit(main())

