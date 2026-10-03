#!/usr/bin/env python3
"""
sort_node_sections.py

Sorts the "### " sub-header sections of a markdown document alphabetically
by their header text (e.g. each Geometry Nodes entry like "### A3D_Mirror").

- Any content before the first "### " header (a preamble) is kept at the top,
  unchanged, in its original position.
- Divider lines that only contain "---" and lines like "## New Nodes" are
  treated as separators between groups, not as content, and are dropped from
  the output (since sorting merges everything into one alphabetical list).
- Each "### " section (header + everything up to the next "### " header) is
  treated as an atomic block and moved as a unit.
- Sorting is case-insensitive, using the header text with the leading
  "### " stripped.

Usage:
    python sort_node_sections.py input.md -o output.md
    python sort_node_sections.py input.md            # prints to stdout
"""

import argparse
import re
import sys


HEADER_RE = re.compile(r"^### .+$", re.MULTILINE)


def split_into_sections(text: str):
    """
    Returns (preamble, sections) where sections is a list of
    (header_text, full_block_text) tuples. full_block_text includes the
    header line itself and everything up to (not including) the next
    "### " header.
    """
    matches = list(HEADER_RE.finditer(text))
    if not matches:
        return text, []

    preamble = text[: matches[0].start()]

    sections = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        header_text = m.group(0)[len("### "):].strip()
        sections.append((header_text, block))

    return preamble, sections


def clean_block(block: str) -> str:
    """
    Strips out divider-only lines ("---") and standalone "## ..." group
    headers (e.g. "## New Nodes") that may trail at the end of a block
    (they show up there because they sit between one section's content
    and the next "### " header). Also trims trailing whitespace.
    """
    lines = block.splitlines()
    # Drop trailing lines that are just "---" or a "## " heading or blank,
    # working backwards, but stop as soon as we hit real content.
    while lines and (
        lines[-1].strip() == ""
        or lines[-1].strip() == "---"
        or lines[-1].strip().startswith("## ")
    ):
        lines.pop()
    return "\n".join(lines).rstrip() + "\n"


def sort_sections(text: str) -> str:
    preamble, sections = split_into_sections(text)

    cleaned = [(header, clean_block(block)) for header, block in sections]
    cleaned.sort(key=lambda pair: pair[0].lower())

    prefix = (preamble.rstrip() + "\n\n") if preamble.strip() else ""
    body = "\n\n".join(block for _, block in cleaned)
    return prefix + body + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Path to the input markdown file")
    parser.add_argument(
        "-o", "--output",
        help="Path to write the sorted markdown (default: print to stdout)",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    result = sort_sections(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Wrote sorted document to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
