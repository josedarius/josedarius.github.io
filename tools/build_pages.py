"""Rebuild every MyCloudSME page into the v2 'Blueprint' template.

Usage: python3 build.py <site_dir>
Reads each legacy page, keeps its content, and wraps it in the shared header,
footer and section styles. about.html and contact.html are written from
templates in this file.
"""
import re, sys, html
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1])
DEMO_MAIL = "mailto:info@mycloudsme.com?subject=Product%20demo%20request"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet" />')

NAV = [("Services", "/services.html", "services"), ("Solutions", "/solutions.html", "solutions"),
       ("Case studies", "/#work", "work"), ("Products", "/products.html", "products"),
       ("About", "/about.html", "about"), ("Contact", "/contact.html", "contact")]


def header(active):
    links = "\n      ".join(
        f'<a href="{u}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for t, u, k in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>

<!-- ============ HEADER ============ -->
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/" aria-label="MyCloudSME home">
      <img src="/assets/images/mycloudsme-logo.png" alt="MyCloudSME Technologies" width="140" height="136" />
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      {links}
      <a class="btn btn-primary" href="/contact.html">Book a call</a>
    </nav>
  </div>
</header>
'''


FOOTER = '''<!-- ============ FOOTER ============ -->
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <a class="logo-chip" href="/"><img src="/assets/images/mycloudsme-logo.png" alt="MyCloudSME Technologies" width="41" height="40" /></a>
        <p style="margin-top:16px;max-width:34ch">Cloud migration, modernisation, security and FinOps. Headquartered in Chennai, working worldwide.</p>
      </div>
      <div><h4>Services</h4><ul><li><a href="/services/migration-modernization.html">Migration</a></li><li><a href="/services/cloud-security.html">Security</a></li><li><a href="/services/finops.html">FinOps</a></li><li><a href="/services/managed-operations.html">Managed ops</a></li><li><a href="/services.html">All services</a></li></ul></div>
      <div><h4>Products</h4><ul><li><a href="/products/myops.html">MyOps</a></li><li><a href="/products/tagops.html">TagOps</a></li><li><a href="/products.html">Academy OS</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="/about.html">About</a></li><li><a href="/#work">Case studies</a></li><li><a href="/solutions.html">Solutions</a></li><li><a href="/contact.html">Contact</a></li></ul></div>
    </div>
    <div class="base">
      <span>© <span id="yr">2026</span> MyCloudSME Technologies Private Limited</span>
      <span>DPIIT-recognised startup · Chennai, India</span>
    </div>
  </div>
</footer>

<script>
  const mb=document.querySelector('.menu-btn'),nav=document.getElementById('nav');
  mb.addEventListener('click',()=>{const o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o);mb.textContent=o?'Close':'Menu'});
  nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.textContent='Menu'}));
  const els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -40px 0px'});
    els.forEach(el=>io.observe(el));
  } else els.forEach(el=>el.classList.add('in'));
  document.getElementById('yr').textContent=new Date().getFullYear();
</script>
</body>
</html>
'''


def head(title, desc, path):
    url = "https://mycloudsme.com/" + ("" if path == "index.html" else path)
    t, d = html.escape(title), html.escape(desc)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t}</title>
  <meta name="description" content="{d}" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="MyCloudSME" />
  <meta property="og:title" content="{t}" />
  <meta property="og:description" content="{d}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://mycloudsme.com/assets/images/og/mycloudsme-og.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="/assets/favicon/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon/favicon-32x32.png" />
  <link rel="apple-touch-icon" href="/assets/favicon/apple-touch-icon.png" />
  <meta name="theme-color" content="#06152a" />
  {FONTS}
  <link rel="stylesheet" href="/assets/css/v2.css" />
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>
'''


def hero(crumb, crumb_url, h1, lede, cta=True):
    c = (f'<a href="/">Home</a><span aria-hidden="true">/</span><a href="{crumb_url}">{crumb}</a>'
         if crumb_url else '<a href="/">Home</a>')
    btns = ('\n    <div class="hero-ctas"><a class="btn btn-primary" href="/contact.html">Book a free 30-min call '
            '<span class="arr" aria-hidden="true">→</span></a><a class="btn btn-ghost" href="/#work">See our work</a></div>') if cta else ''
    return f'''<section class="navy grid-bg page-hero2">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{c}</nav>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>{btns}
  </div>
</section>
'''


SECTION_OF = {"services": ("Services", "/services.html", "services"),
              "solutions": ("Solutions", "/solutions.html", "solutions"),
              "products": ("Products", "/products.html", "products")}


def fix_inner(node):
    """Map legacy classes to v2 classes inside a section."""
    for el in node.select(".lifecycle-icon"):
        el.decompose()
    for el in node.find_all(True):
        cls = el.get("class") or []
        new = []
        for c in cls:
            if c == "container": new.append("wrap")
            elif c == "reveal": new.append("rv")
            elif c == "section-title": new.append("h2")
            elif c == "section-subtitle": new.append("lede")
            elif c == "btn-primary": new += ["btn", "btn-primary"]
            else: new.append(c)
        if new: el["class"] = list(dict.fromkeys(new))
        if el.name == "h2" and "h2" not in (el.get("class") or []):
            el["class"] = (el.get("class") or []) + ["h2"]
    # live demo links -> request a demo
    for a in node.find_all("a", href=re.compile(r"myops\.mycloudsme\.com")):
        a["href"] = DEMO_MAIL
        a.attrs.pop("target", None)
        a.string = "Request a demo"
    for a in node.find_all("a", href=True):
        a["href"] = re.sub(r"^(\.\./)+", "/", a["href"])
        if a["href"] in ("contact.html", "/contact.html") and "btn" in (a.get("class") or []):
            a.string = "Book a free 30-min call"
    return node


def convert(path):
    rel = path.relative_to(ROOT).as_posix()
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "MyCloudSME"
    md = soup.find("meta", attrs={"name": "description"})
    sections = [s for s in soup.find_all("section") if s.find_parent("section") is None]

    folder = rel.split("/")[0] if "/" in rel else rel.replace(".html", "")
    crumb, crumb_url, active = SECTION_OF.get(folder, ("", "", folder))
    if "/" not in rel:  # overview page: breadcrumb is just Home
        crumb_url = ""

    out, desc = [], None
    paper_next = False
    for s in sections:
        cls = s.get("class") or []
        if "page-hero" in cls:
            h1 = s.find("h1").decode_contents().strip()
            ps = [p.get_text(" ", strip=True) for p in s.find_all("p")]
            lede = " ".join(ps)
            desc = re.sub(r"\s+", " ", lede)[:300]
            out.append(hero(crumb, crumb_url, h1, html.escape(desc)))
            continue
        fix_inner(s)
        inner = s.decode_contents()
        if "cta-band" in cls:
            out.append(f'<section class="navy grid-bg cta lg cta-simple">{inner}</section>\n')
            continue
        if "how-we-deliver" in cls:
            out.append(f'<section class="sec navy grid-bg lg">{inner}</section>\n')
            paper_next = False
            continue
        is_paper = any(c in cls for c in ("bg-soft", "alt-bg", "light", "soft-bg"))
        out.append(f'<section class="sec lg{" paper" if is_paper else ""}">{inner}</section>\n')

    if md and md.get("content"):
        desc = md["content"]
    page = head(title, desc or title, rel) + header(active) + '\n<main id="main">\n' + "".join(out) + "</main>\n\n" + FOOTER
    path.write_text(page, encoding="utf-8")
    return rel, len(sections)


# ---------------- hand-written pages ----------------
CTA = '''<section class="navy grid-bg cta lg cta-simple">
  <div class="wrap rv">
    <h2 class="h2">Tell us what you run today. We'll tell you what it takes to move it.</h2>
    <p class="lede">A free 30-minute call with an engineer, not a salesperson.</p>
    <a class="btn btn-primary" href="/contact.html">Book a free 30-min call</a>
  </div>
</section>
'''

ABOUT = hero("", "", "About MyCloudSME",
             "An engineering-led cloud and software company. Headquartered in Chennai, working with clients worldwide.", cta=False) + '''
<section class="sec lg">
  <div class="wrap two-col">
    <div class="rv">
      <span class="eyebrow">Who we are</span>
      <h2 class="h2" style="margin-top:14px">Engineers who design, build and stay to run it.</h2>
    </div>
    <div class="rv">
      <p>MyCloudSME Technologies Private Limited is a cloud and software engineering company. We help organisations move to the cloud, modernise the applications that hold them back, secure their environments and keep costs under control.</p>
      <p>We work as a core team in Chennai together with a network of experienced specialist engineers in Germany, the United States, the Philippines and Australia. For each engagement we bring together the people with the right skills, working in your time zone.</p>
      <p>Our work covers the whole lifecycle: strategy, architecture, migration, software delivery and day-to-day operations. That way what we design is also what works in production.</p>
    </div>
  </div>
</section>

<section class="sec paper lg">
  <div class="wrap">
    <div class="sec-head rv"><span class="eyebrow">Track record</span><h2 class="h2">What we've delivered so far.</h2></div>
    <ul class="stat-row rv">
      <li><b>250+</b><span>Projects delivered</span></li>
      <li><b>600+</b><span>Workloads moved in one VMware-to-Azure programme</span></li>
      <li><b>20+</b><span>Legacy apps modernised for one client</span></li>
      <li><b>6×</b><span>Faster apps after modernisation</span></li>
    </ul>
    <p class="rv" style="margin-top:28px"><a href="/#work">Read the case studies →</a></p>
  </div>
</section>

<section class="sec lg">
  <div class="wrap">
    <div class="sec-head rv"><span class="eyebrow">How we operate</span><h2 class="h2">Four principles behind every project.</h2></div>
    <div class="pillars-grid">
      <div class="pillar-card rv"><h3>Engineering first</h3><p>The people who design your platform are hands-on engineers who build and run it, not slide writers.</p></div>
      <div class="pillar-card rv"><h3>Security by default</h3><p>Identity, policy, logging and compliance are part of every platform from the first day.</p></div>
      <div class="pillar-card rv"><h3>Everything as code</h3><p>Infrastructure, policies and pipelines are versioned and repeatable, so nothing depends on one person's memory.</p></div>
      <div class="pillar-card rv"><h3>Measurable outcomes</h3><p>We agree on what success looks like up front: cost, performance, reliability or audit readiness.</p></div>
    </div>
  </div>
</section>

<section class="sec paper lg">
  <div class="wrap team">
    <div class="rv">
      <span class="eyebrow">The team</span>
      <h2 class="h2" style="margin-top:14px">Senior specialists, assembled for each engagement.</h2>
      <p>Our engineers bring experience across:</p>
      <ul class="bullet-list one">
        <li>Cloud architecture on Azure, AWS and Google Cloud</li>
        <li>Large migrations, datacentre exits and landing zones</li>
        <li>Kubernetes and container platforms (AKS, EKS, GKE)</li>
        <li>DevOps, CI/CD and platform engineering</li>
        <li>Cloud security, identity and governance</li>
        <li>FinOps and cost optimisation</li>
        <li>Observability, SRE and managed operations</li>
        <li>Custom software and cloud-native applications</li>
      </ul>
    </div>
    <div class="rv">
      <div class="map">
        <span class="eyebrow">Where we work</span>
        <ul class="locs">
          <li><span class="r">Chennai</span><span>Headquarters and delivery centre</span></li>
          <li><span class="r">Germany</span><span>Specialist engineers · European time zone</span></li>
          <li><span class="r">United States</span><span>Specialist engineers</span></li>
          <li><span class="r">Philippines</span><span>Specialist engineers</span></li>
          <li><span class="r">Australia</span><span>Specialist engineers</span></li>
        </ul>
      </div>
      <div class="dpiit"><img src="/assets/images/DPIIT.jpeg" alt="DPIIT Startup India" width="120" height="40" /><span>Recognised startup by DPIIT, Government of India</span></div>
    </div>
  </div>
</section>

<section class="sec lg">
  <div class="wrap two-col">
    <div class="rv"><span class="eyebrow">Our mission</span></div>
    <div class="rv"><p class="mission">Help organisations adopt cloud and modern software with confidence: security, governance and cost discipline from day one, and teams that can move fast.</p></div>
  </div>
</section>
''' + CTA

CONTACT = hero("", "", "Let's talk about your cloud",
               "Tell us what you run today and where you want to be. You'll speak with an engineer, not a salesperson.", cta=False) + '''
<section class="sec lg">
  <div class="wrap contact-wrap">
    <div class="rv">
      <span class="eyebrow">Book a free 30-min call</span>
      <h2 class="h2" style="margin-top:14px">Send us a few lines. We'll set up a call.</h2>
      <p>Email us and mention what's most useful for a first conversation:</p>
      <ul class="bullet-list one">
        <li>What you run today (for example VMware, Azure, AWS, or a mix)</li>
        <li>Roughly how many servers or applications are involved</li>
        <li>What's driving the change: cost, a contract end, performance, security or an audit</li>
        <li>Any deadline you're working towards</li>
      </ul>
      <div class="hero-ctas"><a class="btn btn-primary" href="mailto:info@mycloudsme.com?subject=Book%20a%2030-min%20call">Email us to book a call <span class="arr" aria-hidden="true">→</span></a></div>
      <p class="small">Not sure where to start? Our fixed-scope <a href="/#packages">starter packages</a> are a low-risk first step.</p>
    </div>
    <div class="rv">
      <div class="contact-card light-card">
        <dl>
          <div><dt>Email</dt><dd><a href="mailto:info@mycloudsme.com">info@mycloudsme.com</a></dd></div>
          <div><dt>India</dt><dd><a href="tel:+919176200251">+91 91762 00251</a></dd></div>
          <div><dt>Germany</dt><dd><a href="tel:+491772585993">+49 177 258 5993</a></dd></div>
          <div><dt>Headquarters</dt><dd>Chennai, Tamil Nadu, India</dd></div>
          <div><dt>Delivery network</dt><dd>Germany · United States · Philippines · Australia</dd></div>
          <div><dt>Clients</dt><dd>Worldwide, in your time zone</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>
'''


def write_custom(rel, title, desc, active, body):
    (ROOT / rel).write_text(head(title, desc, rel) + header(active) + '\n<main id="main">\n' + body + "</main>\n\n" + FOOTER, encoding="utf-8")


if __name__ == "__main__":
    skip = {"index.html", "about.html", "contact.html"}
    for p in sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("*/*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel in skip or rel.startswith("partials/"):
            continue
        print(convert(p))
    write_custom("about.html", "About Us | MyCloudSME Technologies",
                 "MyCloudSME is an engineering-led cloud and software company headquartered in Chennai, with specialist engineers across Europe, the US and Asia-Pacific.",
                 "about", ABOUT)
    write_custom("contact.html", "Contact | MyCloudSME Technologies",
                 "Book a free 30-minute call with a MyCloudSME cloud engineer. Email info@mycloudsme.com or call our India and Germany numbers.",
                 "contact", CONTACT)
    print("about, contact written")
