"""Build a static GitHub Pages site (site/index.html) from Node Reference.md."""
import html
import json
import re
import shutil
import urllib.parse
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
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


def decorate(body):
    body = SOCKET_RE.sub(r'\1<code class="s s-\2">\2</code>', body)
    return SECTION_RE.sub(r'<p class="sec sec-\1">\1</p>', body)


IMAGES_SRC = ROOT / "node_images"  # folder of images/gifs
IMAGES_MAP = ROOT / "node_images.json"  # {"Node Name": "file.gif" | ["a.png", "b.gif"]}
H3_RE = re.compile(r'(<h3 id="([^"]+)">.*?</h3>)(.*?)(?=<h3 id=|\Z)', re.S)


def add_images(body, names):
    """Insert images above each mapped node's Description."""
    if not IMAGES_MAP.exists():
        return body
    lookup = json.loads(IMAGES_MAP.read_text(encoding="utf-8"))

    def repl(m):
        head, hid, rest = m.groups()
        files = lookup.get(names.get(hid, ""), [])
        if isinstance(files, str):
            files = [files]
        files = [f for f in files if (IMAGES_SRC / f).is_file()]
        if not files:
            return m.group(0)
        imgs = '<div class="node-imgs">' + "".join(
            f'<img src="images/{urllib.parse.quote(f)}" alt="{html.escape(names[hid])}" loading="lazy">'
            for f in files) + "</div>"
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
main{{max-width:800px;padding:1rem 2rem;flex:1}}
h1{{margin:.5rem 0 1rem;padding:.4rem .8rem;background:var(--h1-bg);color:var(--h1-text);border-radius:6px}}
h2{{padding:.3rem .8rem;background:var(--h2-bg);color:var(--h2-text);border-radius:6px}}
h3{{margin-top:2.5rem;padding:.35rem .8rem;background:var(--h3-bg);color:var(--h3-text);border-left:6px solid var(--h3-accent);border-radius:4px;scroll-margin-top:3.5rem}}
h4{{padding:.2rem .7rem;background:var(--h4-bg);border-radius:4px}}
.sec{{margin:1.2rem 0 .4rem;padding:.15rem .7rem;font-weight:700;border-radius:4px;border-left:4px solid}}
.sec-Description{{background:var(--desc-bg);border-color:var(--desc-accent)}}
.sec-Inputs{{background:var(--inputs-bg);border-color:var(--inputs-accent)}}
.sec-Outputs{{background:var(--outputs-bg);border-color:var(--outputs-accent)}}
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
document.getElementById('q').addEventListener('input',e=>{{
const v=e.target.value.toLowerCase();
document.querySelectorAll('nav a').forEach(a=>a.style.display=a.textContent.toLowerCase().includes(v)?'':'none');
}});
</script></body></html>
"""


def main():
    text = (ROOT / "Node Reference.md").read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["toc", "tables", "fenced_code"],
                           extension_configs={"toc": {"toc_depth": "3"}})
    body = decorate(md.convert(text))
    toc = "".join(
        f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>'
        for t in md.toc_tokens if t["level"] == 3
    )
    names = {t["id"]: t["name"] for t in md.toc_tokens if t["level"] == 3}
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

