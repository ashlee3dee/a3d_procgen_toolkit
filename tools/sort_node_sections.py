#!/usr/bin/env python3
"""
sort_node_sections.py

Sorts the "### " node sections of a markdown document alphabetically by their
header text (e.g. each Geometry Nodes entry like "### A3D_Mirror"), within
each "## " category heading. Category headings keep their original order.

- Any content before the first "## " heading (a preamble) is kept at the top,
  unchanged.
- Documents with no "## " headings are treated as one uncategorized group.
- Each "### " section (header + everything up to the next "### " or "## "
  header) is treated as an atomic block and moved as a unit.
- Divider lines that only contain "---" are dropped.
- Sorting is case-insensitive, using the header text with the leading
  "### " stripped.

Usage:
    python tools/sort_node_sections.py input.md -o output.md
    python tools/sort_node_sections.py input.md       # prints to stdout
"""

import argparse
import re
import sys


HEADER_RE = re.compile(r"^### .+$", re.MULTILINE)
CATEGORY_RE = re.compile(r"^## .+$", re.MULTILINE)


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
    Strips divider-only lines ("---") and blank lines that trail a block
    (they sit between one section's content and the next header).
    """
    lines = block.splitlines()
    while lines and lines[-1].strip() in ("", "---"):
        lines.pop()
    return "\n".join(lines).rstrip() + "\n"


def sort_group(text: str) -> str:
    """Sort the "### " sections of one category's body."""
    preamble, sections = split_into_sections(text)

    cleaned = [(header, clean_block(block)) for header, block in sections]
    cleaned.sort(key=lambda pair: pair[0].lower())

    prefix = (preamble.rstrip() + "\n\n") if preamble.strip() else ""
    body = "\n".join(block for _, block in cleaned)
    return prefix + body


def sort_sections(text: str) -> str:
    matches = list(CATEGORY_RE.finditer(text))
    if not matches:
        return sort_group(text) + "\n"

    parts = []
    preamble = text[: matches[0].start()].rstrip()
    if preamble:
        parts.append(preamble)
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = sort_group(text[m.end():end])
        parts.append(m.group(0).rstrip() + "\n\n" + body)
    return "\n".join(parts) + "\n"


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
