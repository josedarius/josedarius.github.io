"""Build cropped web versions of the MyCloudSME logo from the vector PDF export.

Outputs (in ./out):
  mycloudsme-logo.svg               stacked, original colours (light backgrounds)
  mycloudsme-logo-white.svg         stacked, white text (dark backgrounds)
  mycloudsme-mark.svg               cloud mark only
  mycloudsme-logo-horizontal.svg    mark + wordmark side by side (header)
  mycloudsme-logo-horizontal-white.svg
"""
import re
from pathlib import Path

SRC = Path("logo.svg").read_text()
OUT = Path("out"); OUT.mkdir(exist_ok=True)

inner = re.search(r"<svg[^>]*>(.*)</svg>", SRC, re.S).group(1)

# Measured content boxes in page units (pt), from a 288 dpi render.
FULL = (616.75, 254.75, 1303.25, 825.25)
CLOUD = (658.75, 254.75, 1261.25, 653.0)
TEXT = (616.75, 695.25, 1303.25, 825.25)
PAD = 3


def near_black_to_white(s):
    def fix(m):
        r, g, b = (float(v) for v in m.groups())
        return 'fill="#ffffff"' if max(r, g, b) < 6 else m.group(0)
    return re.sub(r'fill="rgb\(([\d.]+)%, ([\d.]+)%, ([\d.]+)%\)"', fix, s)


def suffix_ids(s, suf):
    ids = re.findall(r'id="([^"]+)"', s)
    for i in ids:
        s = s.replace(f'id="{i}"', f'id="{i}{suf}"').replace(f"url(#{i})", f"url(#{i}{suf})")
    return s


def box(b, pad=PAD):
    x0, y0, x1, y1 = b
    return x0 - pad, y0 - pad, (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad


def single(name, content, b, title):
    x, y, w, h = box(b)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {w:.2f} {h:.2f}" '
           f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}"><title>{title}</title>{content}</svg>\n')
    (OUT / name).write_text(svg)
    return w, h


def horizontal(name, content, title):
    cx, cy, cw, ch = box(CLOUD, 2)
    tx, ty, tw, th = box(TEXT, 2)
    mark_h = 100.0
    mark_w = mark_h * cw / ch
    text_h = 50.0
    text_w = text_h * tw / th
    gap = 18.0
    W = mark_w + gap + text_w
    a = suffix_ids(content, "-m")
    t = suffix_ids(content, "-t")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {mark_h:.2f}" width="{W*2:.0f}" height="{mark_h*2:.0f}" '
           f'role="img" aria-label="{title}"><title>{title}</title>'
           f'<svg x="0" y="0" width="{mark_w:.2f}" height="{mark_h:.2f}" viewBox="{cx:.2f} {cy:.2f} {cw:.2f} {ch:.2f}">{a}</svg>'
           f'<svg x="{mark_w+gap:.2f}" y="{(mark_h-text_h)/2:.2f}" width="{text_w:.2f}" height="{text_h:.2f}" '
           f'viewBox="{tx:.2f} {ty:.2f} {tw:.2f} {th:.2f}">{t}</svg></svg>\n')
    (OUT / name).write_text(svg)
    return W, mark_h


T = "MyCloudSME Technologies Pvt Ltd"
white = near_black_to_white(inner)
_sil = '<path d="' + Path("silhouette.d").read_text() + '" fill="#ffffff"/>'
white = white.replace("</defs>", "</defs>" + _sil, 1)
print(single("mycloudsme-logo.svg", inner, FULL, T))
print(single("mycloudsme-logo-white.svg", white, FULL, T))
print(single("mycloudsme-mark.svg", inner, CLOUD, "MyCloudSME"))
print(horizontal("mycloudsme-logo-horizontal.svg", inner, T))
print(horizontal("mycloudsme-logo-horizontal-white.svg", white, T))
solid = inner.replace("</defs>", "</defs>" + _sil, 1)
print(single("mycloudsme-mark-solid.svg", solid, CLOUD, "MyCloudSME"))
