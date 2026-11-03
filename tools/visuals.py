"""Animated SVG hero illustrations for service, solution and product pages.

Each scene is a small 'live console' in the site's Blueprint style. Animation
is pure CSS (classes v-*, defined in assets/css/v2.css) and switches off for
visitors who prefer reduced motion.
"""
B, T, G, L, M, W, N = "#1f8acb", "#1baa8f", "#6cb33f", "#2a5a8c", "#9fb3cc", "#e8f0fa", "#0a2240"


def hexp(cx, cy, r):
    k = 0.866 * r
    return f"{cx},{cy-r} {cx+k:.1f},{cy-r/2:.1f} {cx+k:.1f},{cy+r/2:.1f} {cx},{cy+r} {cx-k:.1f},{cy+r/2:.1f} {cx-k:.1f},{cy-r/2:.1f}"


def hexn(cx, cy, r, stroke=T, cls="", d=0, fill=N, style=""):
    st = style or f"--d:{d}s"
    return f'<polygon points="{hexp(cx, cy, r)}" fill="{fill}" stroke="{stroke}" stroke-width="1.8" class="{cls}" style="{st}"/>'


def txt(x, y, s, fill=M, size=9.5, anchor="start", cls="", d=0):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" text-anchor="{anchor}" class="{cls}" style="--d:{d}s">{s}</text>'


def frame(title, body, label):
    return f'''<svg class="viz" viewBox="0 0 480 360" role="img" aria-label="{label}">
  <defs><linearGradient id="vg" x1="0" x2="1"><stop offset="0" stop-color="{B}"/><stop offset=".5" stop-color="{T}"/><stop offset="1" stop-color="{G}"/></linearGradient></defs>
  <rect x="8" y="8" width="464" height="344" rx="16" fill="rgba(10,34,64,.72)" stroke="#16406e"/>
  <rect x="8" y="8" width="464" height="344" rx="16" fill="none" stroke="url(#vg)" stroke-width="1.2" class="v-edge"/>
  <g font-family="IBM Plex Mono, monospace" letter-spacing=".6">
    <text x="28" y="36" fill="{M}" font-size="10">{title}</text>
    <circle cx="442" cy="32" r="4" fill="{G}" class="v-glow" style="--t:2s"/>
    <text x="432" y="36" fill="{M}" font-size="9" text-anchor="end">LIVE</text>
    <line x1="28" y1="48" x2="452" y2="48" stroke="#16406e"/>
    {body}
  </g>
</svg>'''


# ------------------------------------------------------------------ scenes
def strategy():
    pts = [(60, 262), (170, 222), (290, 180), (420, 120)]
    labs = ["ASSESS", "DESIGN", "BUILD", "SCALE"]
    cards = ["BUSINESS CASE", "TARGET ARCH.", "LANDING ZONE", "OPERATING MODEL"]
    b = [f'<line x1="40" y1="306" x2="440" y2="306" stroke="{L}"/>']
    for i, q in enumerate(["Q1", "Q2", "Q3", "Q4"]):
        x = 60 + i * 120
        b.append(f'<line x1="{x}" y1="302" x2="{x}" y2="310" stroke="{L}"/>' + txt(x, 326, q, anchor="middle"))
    b.append(f'<path d="M60 262 L170 222 L290 180 L420 120" fill="none" stroke="url(#vg)" stroke-width="2.4" class="v-draw" style="--len:420;--t:7s"/>')
    for i, ((x, y), lab, card) in enumerate(zip(pts, labs, cards)):
        d = 0.5 + i * 0.9
        b.append(hexn(x, y, 15, stroke=[B, T, T, G][i], cls="v-pop", d=d, style="--t:7s;--d:%ss" % d))
        b.append(txt(x, y + 32, lab, fill=W, size=9, anchor="middle", cls="v-fade", d=d))
        cy = y - 78
        b.append(f'<g class="v-pop" style="--t:7s;--d:{d+0.3}s"><rect x="{x-48}" y="{cy}" width="96" height="40" rx="6" fill="{N}" stroke="#16406e"/>'
                 f'<text x="{x}" y="{cy+16}" fill="{M}" font-size="8" text-anchor="middle">{card}</text>'
                 f'<rect x="{x-36}" y="{cy+24}" width="72" height="4" rx="2" fill="{L}"/><rect x="{x-36}" y="{cy+24}" width="72" height="4" rx="2" fill="{T}" class="v-type" style="--t:7s;--d:{d+0.6}s"/></g>')
    return frame("TARGET ROADMAP · 12 MONTHS", "".join(b), "Animated cloud roadmap with four milestones over twelve months")


def migration():
    b = [f'<rect x="28" y="70" width="140" height="240" rx="8" fill="none" stroke="{L}" stroke-dasharray="4 4"/>', txt(42, 90, "SOURCE")]
    cols = [B, B, T, T, G, G]
    for r in range(6):
        for c in range(3):
            b.append(f'<rect x="{42+c*38}" y="{104+r*32}" width="32" height="20" rx="3" fill="{cols[r]}" fill-opacity=".22" stroke="{cols[r]}"/>')
    b.append(f'<rect x="312" y="70" width="140" height="240" rx="10" fill="{N}" stroke="url(#vg)" stroke-width="1.5"/>' + txt(326, 90, "TARGET CLOUD", fill=W))
    for i, (y1, y2, col) in enumerate([(124, 130, B), (190, 190, T), (256, 250, G)]):
        path = f"M170 {y1} C 240 {y1}, 250 {y2}, 312 {y2}"
        b.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="1.6" class="v-flow"/>')
        for k in range(2):
            b.append(f'<circle r="3.5" fill="{col}" class="v-move" style="offset-path:path(\'{path}\');--t:2.6s;--d:{-k*1.3 - i*0.4:.1f}s"/>')
        b.append(txt(214, y1 - 10 if i == 0 else y2 - 10, f"WAVE 0{i+1}", fill=W, size=9))
    for i, (x, y) in enumerate([(352, 132), (412, 132), (352, 200), (412, 200), (352, 268), (412, 268)]):
        b.append(hexn(x, y, 20, stroke=[B, B, T, T, G, G][i], cls="v-pop", d=0.4 * i, style=f"--t:6s;--d:{0.4*i}s"))
    return frame("MIGRATION FACTORY · WAVES", "".join(b), "Animated migration of workloads from a source environment to a target cloud in three waves")


def engineering():
    b = [f'<rect x="28" y="66" width="200" height="262" rx="8" fill="#071a33" stroke="#16406e"/>']
    kw = ["module", "resource", "resource", "policy", "output", "module", "resource", "policy"]
    for i, k in enumerate(kw):
        y = 90 + i * 28
        b.append(txt(42, y, k, fill=T, size=9.5))
        w = [110, 90, 120, 70, 100, 115, 85, 95][i]
        b.append(f'<rect x="{100 if len(k) < 7 else 106}" y="{y-8}" width="{w-30}" height="8" rx="3" fill="{L}" class="v-type" style="--t:8s;--d:{i*0.35:.2f}s"/>')
    b.append(f'<path d="M236 196 H292" stroke="{T}" stroke-width="1.6" class="v-flow"/><circle r="4" fill="{T}" class="v-move" style="offset-path:path(\'M236 196 H292\');--t:1.6s"/>')
    b.append(txt(264, 184, "APPLY", fill=W, size=9, anchor="middle"))
    names = ["VNET", "AKS", "SQL", "VAULT", "LOGS", "POLICY"]
    for i, n in enumerate(names):
        x, y = 336 + (i % 2) * 76, 104 + (i // 2) * 80
        d = 0.9 + i * 0.45
        b.append(f'<g class="v-pop" style="--t:8s;--d:{d:.2f}s">{hexn(x, y, 26, stroke=[B, T, G][i % 3])}{txt(x, y + 3.5, n, fill=W, size=8.6, anchor="middle")}</g>')
    return frame("INFRASTRUCTURE AS CODE", "".join(b), "Animated infrastructure-as-code: code lines are written and cloud resources appear")


def devops():
    xs = [64, 152, 240, 328, 416]
    labs = ["COMMIT", "BUILD", "TEST", "SCAN", "DEPLOY"]
    b = [f'<line x1="64" y1="140" x2="416" y2="140" stroke="{L}" stroke-width="2"/>',
         f'<line x1="64" y1="140" x2="416" y2="140" stroke="url(#vg)" stroke-width="2.4" class="v-draw" style="--len:352;--t:5s"/>']
    for i, (x, l) in enumerate(zip(xs, labs)):
        d = i * 1.0 * (352 / 352) * (5 * 0.6 / 4)
        b.append(hexn(x, 140, 20, stroke=[B, B, T, T, G][i]))
        b.append(hexn(x, 140, 20, stroke="none", fill=T, cls="v-glow", d=round(i * 0.75, 2), style=f"--t:5s;--d:{i*0.75:.2f}s;fill-opacity:.55"))
        b.append(txt(x, 178, l, fill=W, size=9, anchor="middle"))
    b.append(f'<circle r="6" fill="#fff" class="v-move" style="offset-path:path(\'M64 140 H416\');--t:5s;filter:drop-shadow(0 0 6px {T})"/>')
    for r in range(4):
        y = 214 + r * 30
        b.append(f'<rect x="40" y="{y}" width="400" height="22" rx="5" fill="{N}" stroke="#16406e"/>')
        b.append(txt(52, y + 15, f"run {['main', 'feature/api', 'main', 'release'][r]}", size=9))
        for k in range(5):
            b.append(f'<circle cx="{250+k*38}" cy="{y+11}" r="5" fill="{G}" class="v-pop" style="--t:6s;--d:{r*0.5+k*0.25:.2f}s"/>')
    return frame("CI/CD PIPELINE", "".join(b), "Animated CI/CD pipeline moving a change from commit to deploy")


def kubernetes():
    b = [f'<rect x="28" y="64" width="424" height="230" rx="12" fill="none" stroke="url(#vg)" stroke-width="1.4"/>', txt(44, 84, "CLUSTER · AKS / EKS / GKE", fill=W)]
    for n in range(3):
        x0 = 44 + n * 138
        b.append(f'<rect x="{x0}" y="98" width="124" height="180" rx="8" fill="{N}" stroke="#16406e"/>' + txt(x0 + 12, 116, f"NODE {n+1}", size=9))
        for i in range(9):
            cx, cy = x0 + 26 + (i % 3) * 36, 146 + (i // 3) * 42
            col = [B, T, G][(i + n) % 3]
            if i < 4:
                b.append(hexn(cx, cy, 13, stroke=col))
            else:
                b.append(hexn(cx, cy, 13, stroke=col, cls="v-pop", style=f"--t:7s;--d:{(i-4)*0.4+n*0.25:.2f}s"))
    b.append(txt(44, 320, "REPLICAS", size=9))
    b.append(f'<rect x="110" y="312" width="330" height="8" rx="4" fill="{L}"/><rect x="110" y="312" width="330" height="8" rx="4" fill="url(#vg)" class="v-type" style="--t:7s;--d:.2s"/>')
    return frame("AUTOSCALING WORKLOADS", "".join(b), "Animated Kubernetes cluster scaling pods across three nodes")


def security():
    rows = ["MFA FOR ADMINS", "PRIVATE ENDPOINTS", "ENCRYPTION AT REST", "LOGGING ENABLED", "ALLOWED REGIONS", "TAG POLICY"]
    b = []
    for i, r in enumerate(rows):
        y = 82 + i * 40
        b.append(f'<rect x="28" y="{y-16}" width="232" height="30" rx="6" fill="{N}" stroke="#16406e"/>' + txt(62, y + 3, r, fill=W, size=9))
        b.append(f'<circle cx="44" cy="{y-1}" r="6" fill="{L}"/><circle cx="44" cy="{y-1}" r="6" fill="{G}" class="v-pop" style="--t:7s;--d:{0.5+i*0.5:.1f}s"/>')
    shield = "M370 80 L430 104 V170 C430 222 404 256 370 276 C336 256 310 222 310 170 V104 Z"
    b.append(f'<path d="{shield}" fill="rgba(27,170,143,.08)" stroke="url(#vg)" stroke-width="2.4" class="v-draw" style="--len:560;--t:7s"/>')
    b.append(f'<path d="M346 176 L364 194 L398 156" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" class="v-draw" style="--len:80;--t:7s;--d:3.4s"/>')
    b.append(txt(370, 306, "COMPLIANT", fill=W, size=10, anchor="middle", cls="v-fade", d=3.6))
    b.append(f'<rect x="20" y="60" width="440" height="2" fill="{T}" opacity=".7" class="v-scan"/>')
    return frame("SECURITY BASELINE · POLICY AS CODE", "".join(b), "Animated security baseline: policies are checked and the environment becomes compliant")


def finops():
    hs = [150, 168, 180, 176, 128, 104, 92, 86]
    b = [f'<line x1="40" y1="300" x2="444" y2="300" stroke="{L}"/>',
         f'<line x1="40" y1="120" x2="444" y2="120" stroke="#b0452f" stroke-dasharray="5 5"/>', txt(444, 112, "BUDGET", fill="#e0866f", size=9, anchor="end")]
    for i, h in enumerate(hs):
        x = 56 + i * 49
        col = B if i < 4 else T if i < 6 else G
        b.append(f'<rect x="{x}" y="{300-h}" width="30" height="{h}" rx="3" fill="{col}" fill-opacity=".85" class="v-grow" style="--t:7s;--d:{i*0.18:.2f}s"/>')
        b.append(txt(x + 15, 318, ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"][i], anchor="middle", size=8.5))
    b.append(f'<line x1="244" y1="70" x2="244" y2="300" stroke="{T}" stroke-dasharray="3 4"/>' + txt(250, 78, "OPTIMISATION STARTS", fill=T, size=8.5))
    b.append(f'<path d="M71 148 L120 130 L169 118 L218 122 L267 170 L316 194 L365 206 L414 212" fill="none" stroke="#fff" stroke-width="2" class="v-draw" style="--len:420;--t:7s;--d:1.2s"/>')
    b.append(f'<g class="v-pop" style="--t:7s;--d:2.8s"><rect x="330" y="232" width="104" height="26" rx="13" fill="{G}"/>{txt(382, 249, "SAVINGS ↓", fill="#06152a", size=10, anchor="middle")}</g>')
    return frame("MONTHLY CLOUD SPEND", "".join(b), "Animated cloud spend chart that falls below budget after optimisation starts")


def observability():
    b = [f'<clipPath id="vc"><rect x="28" y="64" width="300" height="130"/></clipPath>',
         f'<rect x="28" y="64" width="300" height="130" rx="8" fill="{N}" stroke="#16406e"/>']
    beat = "".join(f"L{x} 140 L{x+10} 140 L{x+16} 98 L{x+24} 176 L{x+30} 130 L{x+36} 140 " for x in range(0, 640, 80))
    b.append(f'<g clip-path="url(#vc)"><path d="M28 140 {beat}" transform="translate(28 0)" fill="none" stroke="{T}" stroke-width="2" class="v-ticker"/></g>')
    b.append(txt(40, 82, "LATENCY · P95", size=9))
    # gauge
    b.append(f'<circle cx="396" cy="130" r="48" fill="none" stroke="{L}" stroke-width="10"/>'
             f'<circle cx="396" cy="130" r="48" fill="none" stroke="url(#vg)" stroke-width="10" stroke-linecap="round" class="v-gauge" transform="rotate(-90 396 130)"/>'
             + txt(396, 128, "SLO", fill=W, size=11, anchor="middle") + txt(396, 144, "ON TRACK", size=8.5, anchor="middle"))
    for i, (lab, col) in enumerate([("CPU", B), ("ERRORS", G), ("REQUESTS", T)]):
        x = 28 + i * 146
        b.append(f'<rect x="{x}" y="214" width="132" height="110" rx="8" fill="{N}" stroke="#16406e"/>' + txt(x + 12, 234, lab, size=9))
        pts = " ".join(f"{x+12+k*13},{300-((k*37+i*17) % 45)}" for k in range(9))
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" class="v-draw" style="--len:200;--t:6s;--d:{i*0.4}s"/>')
    b.append(f'<circle cx="300" cy="80" r="5" fill="#e3a008" class="v-glow" style="--t:1.6s"/>')
    return frame("OBSERVABILITY · SERVICE HEALTH", "".join(b), "Animated monitoring dashboard with a live latency trace and an SLO gauge")


def operations():
    b = []
    cols = [("NEW", 40), ("IN PROGRESS", 186), ("RESOLVED", 332)]
    for name, x in cols:
        b.append(f'<rect x="{x}" y="64" width="128" height="262" rx="8" fill="{N}" stroke="#16406e"/>' + txt(x + 12, 84, name, fill=W, size=9))
    # cards travelling across the board
    for k in range(3):
        b.append(f'<g class="v-ticket" style="--d:{-k*2.6:.1f}s"><rect x="52" y="{102+k*70}" width="104" height="52" rx="6" fill="#0f2d52" stroke="{[B,T,G][k]}"/>'
                 f'<rect x="62" y="{114+k*70}" width="60" height="6" rx="3" fill="{M}"/><rect x="62" y="{128+k*70}" width="80" height="5" rx="2.5" fill="{L}"/>'
                 f'<circle cx="142" cy="{142+k*70}" r="5" fill="{[B,T,G][k]}"/></g>')
    return frame("OPERATIONS BOARD", "".join(b), "Animated operations board with tickets moving from new to resolved")


def software():
    b = [f'<rect x="28" y="64" width="210" height="262" rx="8" fill="#071a33" stroke="#16406e"/>']
    for i in range(9):
        y = 86 + i * 26
        ind = [0, 12, 24, 24, 12, 0, 12, 24, 12][i]
        w = [120, 140, 90, 110, 70, 130, 100, 80, 60][i]
        b.append(f'<rect x="{44+ind}" y="{y}" width="{w}" height="8" rx="3" fill="{[T, B, L, L, B, T, L, G, B][i]}" class="v-type" style="--t:8s;--d:{i*0.3:.1f}s"/>')
    b.append(f'<rect x="262" y="64" width="190" height="262" rx="14" fill="{N}" stroke="url(#vg)" stroke-width="1.4"/>')
    parts = [(276, 82, 162, 26), (276, 120, 76, 70), (362, 120, 76, 70), (276, 202, 162, 50), (276, 264, 162, 44)]
    for i, (x, y, w, h) in enumerate(parts):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0f2d52" stroke="{[B, T, G, T, B][i]}" class="v-pop" style="--t:8s;--d:{1+i*0.45:.2f}s"/>')
    return frame("BUILD · CLOUD-NATIVE APP", "".join(b), "Animated code editor building a cloud-native application screen")


def opsme():
    b = []
    for i, (lab, col) in enumerate([("SPEND", B), ("FORECAST", T), ("RISK", "#e3a008"), ("SAVED", G)]):
        x = 28 + i * 108
        b.append(f'<rect x="{x}" y="62" width="98" height="58" rx="8" fill="{N}" stroke="#16406e"/>' + txt(x + 10, 80, lab, size=8.5))
        b.append(f'<rect x="{x+10}" y="92" width="70" height="12" rx="3" fill="{col}" class="v-type" style="--t:8s;--d:{i*0.25:.2f}s"/>')
    b.append(f'<rect x="28" y="132" width="250" height="194" rx="8" fill="{N}" stroke="#16406e"/>' + txt(40, 152, "COST BY APPLICATION", size=8.5))
    for i, h in enumerate([90, 120, 70, 140, 60, 100]):
        x = 48 + i * 36
        b.append(f'<rect x="{x}" y="{306-h}" width="22" height="{h}" rx="3" fill="{[B, T, G][i % 3]}" class="v-grow" style="--t:8s;--d:{0.4+i*0.15:.2f}s"/>')
    b.append(f'<rect x="290" y="132" width="162" height="194" rx="8" fill="{N}" stroke="#16406e"/>' + txt(302, 152, "ACTION QUEUE", size=8.5))
    chips = [("NEW", B), ("ASSIGNED", T), ("VERIFIED", G), ("OVERDUE", "#e0866f"), ("RESOLVED", G)]
    for i, (c, col) in enumerate(chips):
        y = 166 + i * 30
        b.append(f'<g class="v-pop" style="--t:8s;--d:{1+i*0.4:.1f}s"><rect x="302" y="{y}" width="138" height="22" rx="5" fill="#0f2d52"/>'
                 f'<rect x="310" y="{y+8}" width="50" height="6" rx="3" fill="{M}"/><rect x="370" y="{y+4}" width="62" height="14" rx="7" fill="{col}" fill-opacity=".25" stroke="{col}"/>'
                 f'<text x="401" y="{y+14}" fill="{W}" font-size="7.5" text-anchor="middle">{c}</text></g>')
    return frame("OPSME · EXECUTIVE VIEW", "".join(b), "Animated OpsME dashboard showing spend, forecast, risk, savings, cost by application and an action queue")


def tagsme():
    b = [f'<rect x="28" y="62" width="300" height="214" rx="8" fill="{N}" stroke="#16406e"/>' + txt(40, 82, "RESOURCE GROUPS", size=8.5)]
    tags = ["owner", "cost", "env", "app"]
    for r in range(5):
        y = 96 + r * 34
        b.append(f'<rect x="40" y="{y}" width="92" height="22" rx="4" fill="#0f2d52"/><rect x="48" y="{y+8}" width="{60-r*6}" height="6" rx="3" fill="{M}"/>')
        for k, t in enumerate(tags[: 4 - (r % 2)]):
            x = 140 + k * 46
            b.append(f'<g class="v-pop" style="--t:8s;--d:{0.3+r*0.3+k*0.15:.2f}s"><rect x="{x}" y="{y+2}" width="42" height="18" rx="9" fill="{G}" fill-opacity=".2" stroke="{G}"/>'
                     f'<text x="{x+21}" y="{y+14}" fill="{W}" font-size="7" text-anchor="middle">{t}</text></g>')
    # compliance ring
    b.append(f'<circle cx="396" cy="150" r="44" fill="none" stroke="{L}" stroke-width="9"/>'
             f'<circle cx="396" cy="150" r="44" fill="none" stroke="url(#vg)" stroke-width="9" stroke-linecap="round" class="v-gauge" transform="rotate(-90 396 150)"/>'
             + txt(396, 148, "TAG", fill=W, size=10, anchor="middle") + txt(396, 162, "COVERAGE", size=8, anchor="middle"))
    steps = [("SNAPSHOT", 60), ("EXPORT", 150), ("PREVIEW", 240), ("APPLY", 330), ("RESTORE", 420)]
    b.append(f'<line x1="60" y1="310" x2="420" y2="310" stroke="{L}" stroke-width="2"/>')
    for i, (s, x) in enumerate(steps):
        b.append(hexn(x, 310, 12, stroke=[B, B, T, T, G][i]) + txt(x, 336, s, fill=W, size=8, anchor="middle"))
    b.append(f'<circle r="5" fill="#fff" class="v-move" style="offset-path:path(\'M60 310 H420\');--t:5s;filter:drop-shadow(0 0 6px {T})"/>')
    return frame("TAGSME · SNAPSHOT-FIRST", "".join(b), "Animated TagsME view: tags are applied to resource groups, coverage rises, with snapshot and restore steps")


SCENES = {
    "services/cloud-strategy.html": strategy, "services/migration-modernization.html": migration,
    "services/cloud-engineering.html": engineering, "services/devops-platform.html": devops,
    "services/kubernetes.html": kubernetes, "services/cloud-security.html": security,
    "services/finops.html": finops, "services/observability-sre.html": observability,
    "services/managed-operations.html": operations, "services/software-development.html": software,
    "solutions/datacenter-exit.html": migration, "solutions/landing-zone.html": engineering,
    "solutions/kubernetes-platform.html": kubernetes, "solutions/finops-cost-reduction.html": finops,
    "solutions/secure-cloud-blueprint.html": security, "solutions/cicd-factory.html": devops,
    "services.html": None, "solutions.html": None,
    "products/opsme.html": opsme, "products/tagsme.html": tagsme,
}

if __name__ == "__main__":
    import re, sys
    from pathlib import Path
    root = Path(sys.argv[1])
    for rel, fn in SCENES.items():
        if not fn:
            continue
        p = root / rel
        s = p.read_text(encoding="utf-8")
        m = re.search(r'<section class="navy grid-bg page-hero2[^"]*">\s*<div class="wrap">(.*?)</div>\s*</section>', s, re.S)
        if not m:
            print("skip", rel); continue
        inner = m.group(1)
        inner = re.sub(r'<div class="ph-viz">.*?</div><!--/viz-->', "", inner, flags=re.S)
        inner = re.sub(r'^\s*<div class="ph-text">(.*)</div>\s*$', r"\1", inner, flags=re.S)
        new = (f'<section class="navy grid-bg page-hero2 has-viz">\n  <div class="wrap">\n    <div class="ph-text">{inner}</div>\n'
               f'    <div class="ph-viz">{fn()}</div><!--/viz-->\n  </div>\n</section>')
        s = s[:m.start()] + new + s[m.end():]
        p.write_text(s, encoding="utf-8")
        print("ok", rel)
