"""Rewrite root-absolute links (/assets/..., /about.html, /) to relative ones,
so the site works on mycloudsme.com, under a sub-path preview, and from disk."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
for p in list(root.glob("*.html")) + list(root.glob("*/*.html")):
    rel = p.relative_to(root)
    if rel.parts[0] == "partials": continue
    pre = "../" * (len(rel.parts) - 1)
    s = p.read_text(encoding="utf-8")
    def fix(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith("/"):            # protocol-relative, leave
            return m.group(0)
        if path == "" or path.startswith("#"):
            path = "index.html" + path
        return f'{attr}="{pre}{path}"'
    s = re.sub(r'\b(href|src)="/(?!/)([^"]*)"', fix, s)
    p.write_text(s, encoding="utf-8")
    print(rel)
