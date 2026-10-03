"""Build a static GitHub Pages site (docs/index.html) from Node Reference.md."""
import html
import re
import shutil
import urllib.parse
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"

# Page colors - tweak these. Each key becomes a CSS variable (--key).
THEME = {
    "page-bg": "#14121a",
    "text": "#e6e1ec",
    "header-start": "#2a1233",
    "header-end": "#e0457b",
    "header-text": "#ffffff",
    "header-shadow": "rgba(0,0,0,.6)",
    "nav-bg": "#1b1824",
    "nav-link": "#f0a6c4",
    "nav-link-hover": "#ff79b0",
    "input-bg": "#26222f",
    "input-text": "#e6e1ec",
    "input-border": "#4a3a55",
    "h1-bg": "#3a1530",
    "h1-text": "#ffd1e3",
    "h2-bg": "#c2185b",
    "h2-text": "#ffffff",
    "h3-bg": "#2b2236",
    "h3-text": "#ff8fbd",
    "h3-accent": "#ff4d94",
    "h4-bg": "#231d2c",
    "desc-bg": "#201c29",
    "desc-accent": "#9a8fab",
    "inputs-bg": "#1d2a2a",
    "inputs-accent": "#3fc49a",
    "outputs-bg": "#2d2230",
    "outputs-accent": "#ff6fa8",
    "code-bg": "#2f2a3a",
    "code-text": "#ffc2da",
    "socket-border": "rgba(255,255,255,.25)",
}
THEME_CSS = ":root{" + ";".join(f"--{k}:{v}" for k, v in THEME.items()) + "}"
# Blender socket colors: type -> (background, text color)
SOCKETS = {
    "Float": ("#a1a1a1", "#111"), "Integer": ("#598c5c", "#fff"),
    "Boolean": ("#cca6d6", "#111"), "Vector": ("#6363c7", "#fff"),
    "Color": ("#c7c729", "#111"), "Rotation": ("#a663c7", "#fff"),
    "Matrix": ("#c4207f", "#fff"), "String": ("#70b2ff", "#111"),
    "Object": ("#ed9e5c", "#111"), "Geometry": ("#00d6a3", "#111"),
    "Collection": ("#ffffff", "#111"), "Image": ("#5c3d5c", "#fff"),
    "Material": ("#f27585", "#111"), "Bundle": ("#3d6b6b", "#fff"),
    "Closure": ("#7a7a38", "#fff"), "Menu": ("#4a4a4a", "#fff"),
}
SOCKET_CSS = "".join(
    f"code.s-{k}{{background:{bg};color:{fg};border:1px solid var(--socket-border)}}\n"
    for k, (bg, fg) in SOCKETS.items()
)
SOCKET_RE = re.compile(r"(<li>[^<]*?)<code>(%s)</code>" % "|".join(SOCKETS))
SECTION_RE = re.compile(r"<p><strong>(Description|Inputs|Outputs)</strong></p>")
SOCKET_ROW_RE = re.compile(
    r'<li>([^<]*?)<code class="s s-([^"]+)">([^<]*)</code>(.*?)</li>'
)
SOCKET_LIST_RE = re.compile(
    r'(<p class="sec sec-(?:Inputs|Outputs)">(?:Inputs|Outputs)</p>\s*)<ul>'
)


def decorate(body):
    body = SOCKET_RE.sub(r'\1<code class="s s-\2">\2</code>', body)
    body = SECTION_RE.sub(r'<p class="sec sec-\1">\1</p>', body)

    def socket_row(match):
        name, socket_type, data_type, description = match.groups()
        description = re.sub(r"^\s*—\s*", "", description).strip()
        return (
            '<li class="socket-row">'
            f'<span class="socket-name">{name.strip()}</span>'
            f'<code class="s s-{socket_type}">{data_type}</code>'
            f'<span class="socket-description">{description}</span>'
            "</li>"
        )

    body = SOCKET_ROW_RE.sub(socket_row, body)
    return SOCKET_LIST_RE.sub(
        r'\1<ul class="socket-list"><li class="socket-header">'
        r"<span>Name</span><span>Type</span><span>Description</span></li>",
        body,
    )


IMAGES_SRC = ROOT / "assets" / "node_images"
H3_RE = re.compile(r'(<h3 id="([^"]+)">.*?</h3>)(.*?)(?=<h[23] id=|\Z)', re.S)


def add_images(body, names):
    """Insert matching node images above each node's Description."""
    if not IMAGES_SRC.is_dir():
        return body
    media_by_name = {}
    for path in IMAGES_SRC.iterdir():
        if path.is_file():
            media_by_name.setdefault(path.stem.casefold(), []).append(path)
    for paths in media_by_name.values():
        paths.sort(key=lambda path: path.name.casefold())

    def repl(m):
        head, hid, rest = m.groups()
        node_name = names.get(hid, "")
        files = media_by_name.get(node_name.casefold(), [])
        if not files:
            return m.group(0)
        imgs = '<div class="node-imgs">' + "".join(
            f'<img src="images/{urllib.parse.quote(path.name)}" '
            f'alt="{html.escape(node_name, quote=True)}" loading="lazy">'
            for path in files) + "</div>"
        marker = '<p class="sec sec-Description">'
        if marker in rest:
            rest = rest.replace(marker, imgs + marker, 1)
        else:
            rest = imgs + rest
        return head + rest

    return H3_RE.sub(repl, body)


TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A3D Procgen Toolkit - Node Reference</title>
<style>
{theme_css}
body{{margin:0;font:16px/1.6 system-ui,sans-serif;color:var(--text);background:var(--page-bg)}}
header{{position:sticky;top:0;z-index:10;height:2.9rem;box-sizing:border-box;background:linear-gradient(90deg,var(--header-start),var(--header-end));color:var(--header-text);padding:.5rem 1.5rem;font-size:1.25rem;font-weight:600;box-shadow:0 2px 6px var(--header-shadow)}}
.wrap{{display:flex}}
nav{{width:260px;height:calc(100vh - 2.9rem);overflow:auto;position:sticky;top:2.9rem;padding:1rem;background:var(--nav-bg);box-sizing:border-box;flex:none}}
nav input{{background:var(--input-bg);color:var(--input-text);border:1px solid var(--input-border);border-radius:4px;width:100%;padding:.4rem;box-sizing:border-box;margin-bottom:.5rem}}
nav a{{display:block;padding:.15rem 0;color:var(--nav-link);text-decoration:none;font-size:14px}}
nav a:hover{{color:var(--nav-link-hover);text-decoration:underline}}
nav details{{margin:.15rem 0}}
nav summary{{cursor:pointer;padding:.25rem .4rem;border-radius:4px;background:var(--h3-bg);color:var(--h3-text);font-size:14px;font-weight:600}}
nav summary:hover{{color:var(--nav-link-hover)}}
nav summary span{{opacity:.6;font-weight:400;margin-left:.3em}}
nav details a{{padding-left:1rem}}
main{{max-width:800px;padding:1rem 2rem;flex:1}}
h1{{margin:.5rem 0 1rem;padding:.4rem .8rem;background:var(--h1-bg);color:var(--h1-text);border-radius:6px}}
h2{{margin-top:3rem;padding:.3rem .8rem;background:var(--h2-bg);color:var(--h2-text);border-radius:6px;scroll-margin-top:3.5rem}}
h3{{margin-top:2.5rem;padding:.35rem .8rem;background:var(--h3-bg);color:var(--h3-text);border-left:6px solid var(--h3-accent);border-radius:4px;scroll-margin-top:3.5rem}}
h4{{padding:.2rem .7rem;background:var(--h4-bg);border-radius:4px}}
.sec{{margin:1.2rem 0 .4rem;padding:.15rem .7rem;font-weight:700;border-radius:4px;border-left:4px solid}}
.sec-Description{{background:var(--desc-bg);border-color:var(--desc-accent)}}
.sec-Inputs{{background:var(--inputs-bg);border-color:var(--inputs-accent)}}
.sec-Outputs{{background:var(--outputs-bg);border-color:var(--outputs-accent)}}
.socket-list{{list-style:none;padding:0;margin:.35rem 0 1rem}}
.socket-row,.socket-header{{display:grid;grid-template-columns:minmax(8rem,1.2fr) minmax(6.5rem,auto) minmax(0,3fr);column-gap:.75rem;align-items:start}}
.socket-row{{padding:.35rem .7rem;border-bottom:1px solid var(--socket-border)}}
.socket-header{{padding:.2rem .7rem;color:var(--desc-accent);font-size:.8em;font-weight:700}}
.socket-name,.socket-description{{overflow-wrap:anywhere}}
.node-imgs{{margin:1rem 0;display:flex;flex-wrap:wrap;gap:.75rem}}
.node-imgs img{{max-width:100%;border-radius:6px;border:1px solid var(--input-border)}}
code{{background:var(--code-bg);color:var(--code-text);padding:0 .35em;border-radius:3px}}
code.s{{font-size:.85em;font-weight:600;padding:.05em .45em;border-radius:10px}}
{socket_css}@media(max-width:700px){{.wrap{{display:block}}nav{{width:auto;height:auto;position:static}}}}
</style></head><body>
<header>A3D Procgen Toolkit</header>
<div class="wrap">
<nav><input id="q" placeholder="Filter nodes..." aria-label="Filter nodes">{toc}</nav>
<main><h1>A3D Procgen Toolkit - Node Reference</h1>{body}</main>
</div>
<script>
const q=document.getElementById('q');
const groups=[...document.querySelectorAll('nav details')];
let filtering=false;
q.addEventListener('input',e=>{{
const v=e.target.value.trim().toLowerCase();
if(v&&!filtering)groups.forEach(d=>d.dataset.wasOpen=d.open?'1':'');
document.querySelectorAll('nav a').forEach(a=>a.style.display=a.textContent.toLowerCase().includes(v)?'':'none');
groups.forEach(d=>{{
const hit=[...d.querySelectorAll('a')].some(a=>a.style.display!=='none');
d.style.display=hit?'':'none';
d.open=v?hit:d.dataset.wasOpen==='1';
}});
filtering=!!v;
}});
function openCurrent(){{
const a=document.querySelector('nav a[href="'+decodeURIComponent(location.hash)+'"]');
const d=a&&a.closest('details');
if(d)d.open=true;
}}
window.addEventListener('hashchange',openCurrent);
openCurrent();
</script></body></html>
"""


def nav_html(tree):
    """Sidebar: one dropdown per category listing its nodes."""
    parts = []
    for category, nodes in tree:
        links = "".join(
            f'<a href="#{html.escape(nid)}">{html.escape(name)}</a>' for nid, name in nodes
        )
        if category is None:
            parts.append(links)
            continue
        cid, cname = category
        parts.append(
            f'<details><summary>{html.escape(cname)}<span>{len(nodes)}</span></summary>{links}</details>'
        )
    return "".join(parts)


def nav_tree(toc_tokens):
    """-> [((id, name) | None, [(node id, node name)])]: h2 categories with
    their h3 nodes; h3 nodes outside any category go in a leading None group."""
    loose = [(t["id"], html.unescape(t["name"])) for t in toc_tokens if t["level"] == 3]
    tree = [(None, loose)] if loose else []
    for t in toc_tokens:
        if t["level"] == 2:
            nodes = [(c["id"], html.unescape(c["name"])) for c in t["children"] if c["level"] == 3]
            tree.append(((t["id"], html.unescape(t["name"])), nodes))
    return tree


def main():
    text = (ROOT / "Node Reference.md").read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["toc", "tables", "fenced_code"],
                           extension_configs={"toc": {"toc_depth": "3"}})
    body = decorate(md.convert(text))
    tree = nav_tree(md.toc_tokens)
    toc = nav_html(tree)
    names = {nid: name for _, nodes in tree for nid, name in nodes}
    body = add_images(body, names)
    OUT.mkdir(exist_ok=True)
    if IMAGES_SRC.is_dir():
        shutil.copytree(IMAGES_SRC, OUT / "images", dirs_exist_ok=True)
    (OUT / "index.html").write_text(
        TEMPLATE.format(toc=toc, body=body, theme_css=THEME_CSS, socket_css=SOCKET_CSS), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
