"""Build a static GitHub Pages site (site/index.html) from Node Reference.md."""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "site"

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A3D Procgen Toolkit - Node Reference</title>
<style>
body{{margin:0;font:16px/1.6 system-ui,sans-serif;color:#222;display:flex}}
nav{{width:260px;height:100vh;overflow:auto;position:sticky;top:0;padding:1rem;background:#f4f4f6;box-sizing:border-box}}
nav input{{width:100%;padding:.4rem;box-sizing:border-box;margin-bottom:.5rem}}
nav a{{display:block;padding:.15rem 0;color:#333;text-decoration:none;font-size:14px}}
nav a:hover{{text-decoration:underline}}
main{{max-width:800px;padding:1rem 2rem;flex:1}}
h3{{margin-top:2.5rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}}
code{{background:#eee;padding:0 .25em;border-radius:3px}}
@media(max-width:700px){{body{{display:block}}nav{{width:auto;height:auto;position:static}}}}
</style></head><body>
<nav><input id="q" placeholder="Filter nodes..." aria-label="Filter nodes">{toc}</nav>
<main><h1>A3D Procgen Toolkit - Node Reference</h1>{body}</main>
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
    body = md.convert(text)
    toc = "".join(
        f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>'
        for t in md.toc_tokens if t["level"] == 3
    )
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(TEMPLATE.format(toc=toc, body=body), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
