"""Compress every GIF in assets/node_images/ in place, keeping full resolution and frame rate.

Uses gifsicle: unchanged pixels between frames are stored as transparency and
each frame is cropped to the region that changed. Optional --lossy adds
palette-friendly dithering noise that shrinks files further.

Originals are kept in assets/node_images_originals/ (re-runs always compress from the
original, so changing settings never compounds quality loss).

Usage: python tools/compress_gifs.py [--lossy 0-200] [--colors 2-256]
Requires gifsicle on PATH (scoop install gifsicle / brew install gifsicle).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "node_images"
BACKUP = ROOT / "assets" / "node_images_originals"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lossy", type=int, default=0,
                   help="lossy level 0-200 (0 = lossless; ~30-80 is usually invisible)")
    p.add_argument("--colors", type=int, default=0, help="optional palette limit (2-256)")
    a = p.parse_args()

    exe = shutil.which("gifsicle")
    if not exe:
        sys.exit("gifsicle not found. Install it: scoop install gifsicle")

    BACKUP.mkdir(exist_ok=True)
    total_before = total_after = 0
    for gif in sorted(SRC.glob("*.gif")):
        orig = BACKUP / gif.name
        if not orig.exists():
            shutil.copy2(gif, orig)
        tmp = gif.with_name(gif.name + ".tmp")
        cmd = [exe, "-O3", "--no-warnings"]
        if a.lossy:
            cmd.append(f"--lossy={a.lossy}")
        if a.colors:
            cmd.append(f"--colors={a.colors}")
        cmd += [str(orig), "-o", str(tmp)]
        subprocess.run(cmd, check=True)
        before, after = orig.stat().st_size, tmp.stat().st_size
        if after < before:
            tmp.replace(gif)
        else:
            tmp.unlink()
            shutil.copy2(orig, gif)
            after = before
        total_before += before
        total_after += after
        print(f"{gif.name}: {before/1e6:.2f} MB -> {after/1e6:.2f} MB")
    print(f"Total: {total_before/1e6:.2f} MB -> {total_after/1e6:.2f} MB")


if __name__ == "__main__":
    main()
