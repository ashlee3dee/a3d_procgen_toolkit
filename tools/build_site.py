"""Build the static GitHub Pages site (docs/index.html) from Node Reference.md.

Pages are generated straight from the parsed reference (see reference.py); the
page template, CSS, JS and colors live in tools/site/. No third-party packages.
"""
import html
import json
import re
import shutil
import sys
import unicodedata
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reference  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(__file__).resolve().parent / "site"
REFERENCE = ROOT / "Node Reference.md"
OUT = ROOT / "docs"
IMAGES_SRC = ROOT / "assets" / "node_images"

_CODE = re.compile(r"`([^`]+)`")


def esc(text):
    return html.escape(text, quote=False)


def css_name(text):
    return re.sub(r"\W", "", text)


def inline(text):
    """Escape text, turning `backtick` spans into <code>."""
    return "".join(
        f"<code>{esc(part)}</code>" if i % 2 else esc(part)
        for i, part in enumerate(_CODE.split(text))
    )


def make_slugger():
    """Heading -> unique anchor id (same scheme the old markdown toc used)."""
    seen = set()

    def slug(text):
        ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
        base = re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", ascii_text).strip().lower()) or "section"
        result, n = base, 0
        while result in seen:
            n += 1
            result = f"{base}_{n}"
        seen.add(result)
        return result

    return slug


def load_theme():
    data = json.loads((SITE / "theme.json").read_text(encoding="utf-8"))
    theme_css = ":root{" + ";".join(f"--{k}:{v}" for k, v in data["theme"].items()) + "}"
    socket_css = "".join(
        f"code.s-{css_name(name)}{{background:{bg};color:{fg};border:1px solid var(--socket-border)}}\n"
        for name, (bg, fg) in data["sockets"].items()
    )
    return theme_css, socket_css


def find_images(directory):
    """{node name (casefolded): [image paths]} for files named after nodes."""
    found = {}
    if directory.is_dir():
        for path in sorted(directory.iterdir(), key=lambda p: p.name.casefold()):
            if path.is_file() and path.name != ".gitkeep":
                found.setdefault(path.stem.casefold(), []).append(path)
    return found


def render_images(node, images):
    paths = images.get(node.name.casefold(), [])
    if not paths:
        return ""
    alt = html.escape(node.name, quote=True)
    imgs = "".join(
        f'<img src="images/{urllib.parse.quote(p.name)}" alt="{alt}" loading="lazy">'
        for p in paths
    )
    return f'<div class="node-imgs">{imgs}</div>'


def render_sockets(sockets):
    if not sockets:
        return ""
    rows = "".join(
        '<li class="socket-row">'
        f'<span class="socket-name">{inline(s.name)}</span>'
        f'<code class="s s-{css_name(s.type)}">{esc(s.type)}</code>'
        f'<span class="socket-description">{inline(s.description)}</span></li>'
        for s in sockets
    )
    return (
        '<ul class="socket-list"><li class="socket-header">'
        f"<span>Name</span><span>Type</span><span>Description</span></li>{rows}</ul>"
    )


def render_node(node, node_id, images):
    description = f"<p>{inline(node.description)}</p>" if node.description else ""
    return (
        f'<h3 id="{node_id}">{esc(node.name)}</h3>'
        f"{render_images(node, images)}"
        f'<p class="sec sec-Description">Description</p>{description}'
        f'<p class="sec sec-Inputs">Inputs</p>{render_sockets(node.inputs)}'
        f'<p class="sec sec-Outputs">Outputs</p>{render_sockets(node.outputs)}'
    )


def render_body_and_nav(ref, images):
    """-> (main content html, sidebar html). Nodes outside any category are listed first."""
    slug = make_slugger()
    body, loose_links, groups = [], [], []
    for category in ref.categories:
        links = []
        if category.name is not None:
            body.append(f'<h2 id="{slug(category.name)}">{esc(category.name)}</h2>')
        for node in category.nodes:
            node_id = slug(node.name)
            body.append(render_node(node, node_id, images))
            links.append(f'<a href="#{node_id}">{esc(node.name)}</a>')
        if category.name is None:
            loose_links += links
        else:
            groups.append(
                f"<details><summary>{esc(category.name)}<span>{len(category.nodes)}</span></summary>"
                f'{"".join(links)}</details>'
            )
    return "".join(body), "".join(loose_links) + "".join(groups)


def fill(template, **values):
    """Replace {{name}} placeholders; an unknown placeholder raises KeyError."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)


def build_page(ref, images):
    theme_css, socket_css = load_theme()
    body, nav = render_body_and_nav(ref, images)
    return fill(
        (SITE / "template.html").read_text(encoding="utf-8"),
        theme_css=theme_css,
        socket_css=socket_css,
        style=(SITE / "style.css").read_text(encoding="utf-8"),
        script=(SITE / "script.js").read_text(encoding="utf-8"),
        nav=nav,
        body=body,
    )


def main():
    ref = reference.parse(REFERENCE.read_text(encoding="utf-8"))
    for warning in ref.warnings:
        print(f"warning: {REFERENCE.name} {warning}", file=sys.stderr)

    OUT.mkdir(exist_ok=True)
    if IMAGES_SRC.is_dir():
        shutil.copytree(IMAGES_SRC, OUT / "images", dirs_exist_ok=True)
    # Without the (untracked) source images, fall back to the ones already published.
    images = find_images(OUT / "images")

    (OUT / "index.html").write_text(build_page(ref, images), encoding="utf-8", newline="\n")
    (OUT / ".nojekyll").touch()
    print(f"Wrote {OUT / 'index.html'} ({len(ref.nodes())} nodes)")


if __name__ == "__main__":
    main()
