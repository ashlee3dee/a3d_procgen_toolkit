"""Build a static GitHub Pages site (site/index.html) from Node Reference.md."""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "site"

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
    f"code.s-{k}{{background:{bg};color:{fg};border:1px solid rgba(0,0,0,.25)}}\n"
    for k, (bg, fg) in SOCKETS.items()
)
SOCKET_RE = re.compile(r"(<li>[^<]*?)<code>(%s)</code>" % "|".join(SOCKETS))
SECTION_RE = re.compile(r"<p><strong>(Description|Inputs|Outputs)</strong></p>")


def decorate(body):
    body = SOCKET_RE.sub(r'\1<code class="s s-\2">\2</code>', body)
    return SECTION_RE.sub(r'<p class="sec sec-\1">\1</p>', body)


TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A3D Procgen Toolkit - Node Reference</title>
<style>
body{{margin:0;font:16px/1.6 system-ui,sans-serif;color:#222}}
header{{position:sticky;top:0;z-index:10;height:2.9rem;box-sizing:border-box;background:linear-gradient(90deg,#1f3a5f,#3b6ea5);color:#fff;padding:.5rem 1.5rem;font-size:1.25rem;font-weight:600;box-shadow:0 2px 6px rgba(0,0,0,.3)}}
.wrap{{display:flex}}
nav{{width:260px;height:calc(100vh - 2.9rem);overflow:auto;position:sticky;top:2.9rem;padding:1rem;background:#eaf0f8;box-sizing:border-box;flex:none}}
nav input{{width:100%;padding:.4rem;box-sizing:border-box;margin-bottom:.5rem}}
nav a{{display:block;padding:.15rem 0;color:#14304f;text-decoration:none;font-size:14px}}
nav a:hover{{text-decoration:underline}}
main{{max-width:800px;padding:1rem 2rem;flex:1}}
h1{{margin:.5rem 0 1rem;padding:.4rem .8rem;background:#1f3a5f;color:#fff;border-radius:6px}}
h2{{padding:.3rem .8rem;background:#3b6ea5;color:#fff;border-radius:6px}}
h3{{margin-top:2.5rem;padding:.35rem .8rem;background:#d6e4f5;color:#14304f;border-left:6px solid #3b6ea5;border-radius:4px;scroll-margin-top:3.5rem}}
h4{{padding:.2rem .7rem;background:#e8f0fa;border-radius:4px}}
.sec{{margin:1.2rem 0 .4rem;padding:.15rem .7rem;font-weight:700;border-radius:4px;border-left:4px solid}}
.sec-Description{{background:#eef0f3;border-color:#8a94a3}}
.sec-Inputs{{background:#e3f1e6;border-color:#4a9a5b}}
.sec-Outputs{{background:#fbebd9;border-color:#e08a2e}}
code{{background:#eee;padding:0 .35em;border-radius:3px}}
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
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(
        TEMPLATE.format(toc=toc, body=body, socket_css=SOCKET_CSS), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()

