#!/usr/bin/env python3
"""Generate the seven GCFPAD pages from one shell.

Why a generator rather than seven hand-written files: the navigation, the
footer and the head block are identical on every page, and the one certain way
to end up with a menu that is missing a link on exactly one page is to maintain
seven copies of it. The OUTPUT is plain static HTML with nothing clever in it -
open any file and it is readable.

⛔ NOTHING FACTUAL IS INVENTED. Everything on these pages is either taken
verbatim from Jeffery's brief or is clearly marked as a slot for content from
his 21-page document. No made-up statistics, no invented board members, no
"500 communities served". An institutional site that is caught with a
fabricated number is finished, and it would be my fabrication, not his.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [("Home", "index.html"), ("About", "about.html"),
       ("What We Do", "what-we-do.html"), ("Our Work", "our-work.html"),
       ("Partnerships", "partnerships.html"), ("Leadership", "leadership.html"),
       ("Contact", "contact.html")]

ORG = "Global Confederation for Promotion and Development"
# 🔑 The registered name on his logo artwork carries ", INC." - used where
# the legal entity is meant, not the display name.
ORG_LEGAL = "Global Confederation for Promotion and Development, Inc."
TAG = "Connecting Opportunities. Empowering Communities. Building Sustainable Futures."

# 🔑 HIS REAL LOGO, which arrived 11 Oct: a tree growing out of a globe of
# world flags with Haiti at the centre. It replaces the mark I drew as a
# placeholder.
#
# ⚠️ The white background was removed by flood-filling inward FROM THE EDGES
# only. A global "every white pixel becomes transparent" would have punched
# holes straight through the flags, most of which contain white. Checked on
# the navy header and on white - no box, flags intact.
#
# ⚠️ It is portrait (roughly 2:3), not square like the old mark, so the CSS
# sets a height and lets the width follow. Forcing it square would squash it.
MARK = ('<img class="mark" src="assets/img/logo.png" alt="" aria-hidden="true" '
        'width="512" height="779">')

def icon(name):
    """Line icons, 24x24, drawn here so the site loads no icon font."""
    p = {
        "growth": '<path d="M3 20h18M6 20V11M11 20V6M16 20v-7M21 20V9"/>',
        "learn":  '<path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M7 10.5V16c0 1.5 2.2 3 5 3s5-1.5 5-3v-5.5"/>',
        "build":  '<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M10 21v-6h4v6"/>',
        "rights": '<path d="M12 3l7.5 3v5.5c0 4.6-3.1 8-7.5 9.5-4.4-1.5-7.5-4.9-7.5-9.5V6L12 3z"/>'
                  '<path d="M9.3 12.2l1.9 1.9 3.6-3.8"/>',
        "globe":  '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 3 3.9 6 3.9 9s-1.3 6-3.9 9'
                  'c-2.6-3-3.9-6-3.9-9S9.4 6 12 3z"/>',
        "link":   '<path d="M10 13.5a4 4 0 005.7 0l3-3a4 4 0 10-5.7-5.7l-1.3 1.3"/>'
                  '<path d="M14 10.5a4 4 0 00-5.7 0l-3 3a4 4 0 105.7 5.7l1.3-1.3"/>',
        "gov":    '<path d="M3 21h18M4 21V10M20 21V10M12 3l9 5H3l9-5z"/><path d="M8 21V12M12 21V12M16 21V12"/>',
        "invest": '<path d="M12 2v20M17.5 6.5c0-2-2.3-3-5.5-3s-5.5 1.1-5.5 3S8 10 12 10.6s6 1.6 6 3.6'
                  '-2.7 3.3-6 3.3-6-1.3-6-3.3"/>',
        "biz":    '<path d="M3 9h18v11H3zM8 9V5h8v4"/><path d="M3 13h18"/>',
        "ngo":    '<path d="M12 20s-7-4.4-7-9.3A4 4 0 0112 8.4 4 4 0 0119 10.7c0 4.9-7 9.3-7 9.3z"/>',
        "people": '<circle cx="9" cy="8" r="3.2"/><path d="M2.5 20c0-3.6 2.9-5.6 6.5-5.6s6.5 2 6.5 5.6"/>'
                  '<path d="M16 5.2a3.2 3.2 0 010 5.9M18 14.9c2.1.7 3.5 2.4 3.5 5.1"/>',
        "intl":   '<circle cx="12" cy="12" r="9"/><path d="M12 3a14 14 0 000 18M3.6 9h16.8M3.6 15h16.8"/>',
        "dias":   '<path d="M4 18a4 4 0 014-4h8a4 4 0 014 4"/><circle cx="12" cy="7" r="3.4"/>'
                  '<path d="M2 21h20"/>',
        "shield": '<path d="M12 3l8 3.2v5.4c0 5-3.4 8.7-8 10.4-4.6-1.7-8-5.4-8-10.4V6.2L12 3z"/>',
        "node":   '<circle cx="5" cy="6" r="2.2"/><circle cx="19" cy="6" r="2.2"/>'
                  '<circle cx="12" cy="18" r="2.2"/><path d="M6.6 7.6L11 16M17.4 7.6L13 16M7.2 6h9.6"/>',
        "chart":  '<path d="M4 19V5M4 19h16"/><path d="M8 19v-6M12.7 19V8M17.3 19v-9"/>',
    }[name]
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % p)


ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def nav_html(current):
    links = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == current else '', t)
        for t, h in NAV)
    drawer = "".join('<a href="%s">%s</a>' % (h, t) for t, h in NAV)
    return f"""
<header class="nav over-hero">
  <div class="nav-in">
    <a class="brand" href="index.html" aria-label="{ORG} — home">
      {MARK}
      <span class="brand-txt"><span class="b1">GCFPAD</span>
      <span class="b2">Promotion &amp; Development</span></span>
    </a>
    <nav aria-label="Primary"><ul class="nav-links">{links}</ul></nav>
    <div class="nav-cta">
      <a class="btn btn-primary" href="partnerships.html#partner">Partner With Us</a>
      <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
  {drawer}
  <a class="btn btn-primary" href="partnerships.html#partner">Partner With Us</a>
</div>"""


FOOT = f"""
<footer class="foot">
  <div class="wrap-wide">
    <div class="foot-top">
      <div>
        <a class="brand" href="index.html">{MARK}
          <span class="brand-txt"><span class="b1">GCFPAD</span>
          <span class="b2">Promotion &amp; Development</span></span></a>
        <p class="foot-tag">{TAG}</p>
      </div>
      <div>
        <h5>Organization</h5>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="what-we-do.html">What We Do</a></li>
          <li><a href="our-work.html">Our Work</a></li>
          <li><a href="leadership.html">Leadership</a></li>
        </ul>
      </div>
      <div>
        <h5>Engage</h5>
        <ul>
          <li><a href="partnerships.html">Partnerships</a></li>
          <li><a href="partnerships.html#partner">Partner With GCFPAD</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="contact.html#inquiry">Submit an Opportunity</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <div>&copy; <span id="yr">2026</span> {ORG_LEGAL} All Rights Reserved.</div>
      <ul>
        <li><a href="privacy.html">Privacy Policy</a></li>
        <li><a href="terms.html">Terms</a></li>
        <li><a href="contact.html">Social Media</a></li>
      </ul>
    </div>
  </div>
</footer>"""


def page(fname, title, desc, body, current=None):
    current = current or fname
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0B1F2A">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&family=Public+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{nav_html(current)}
{body}
{FOOT}
<script src="assets/site.js"></script>
</body>
</html>
"""
    open(os.path.join(ROOT, fname), "w").write(html)
    print("  %-22s %6d bytes" % (fname, len(html)))


# ══════════════════════════════════════════════════════════════════════════
# SHARED BLOCKS
# ══════════════════════════════════════════════════════════════════════════

def band(heading, text, primary=("Partner With GCFPAD", "partnerships.html#partner"),
         secondary=("Contact Us", "contact.html")):
    return f"""
<section class="band">
  <div class="wrap-wide band-in rv">
    <div>
      <h2>{heading}</h2>
      <p class="lede" style="color:rgba(246,242,236,.76);margin-top:16px">{text}</p>
    </div>
    <div class="btn-row" style="margin-top:0">
      <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
      <a class="btn btn-ghost" href="{secondary[1]}">{secondary[0]}</a>
    </div>
  </div>
</section>"""


def phero(title, lede, img, eyebrow):
    return f"""
<section class="phero">
  <img class="hero-img" src="assets/img/{img}" alt="" aria-hidden="true">
  <div class="wrap">
    <span class="eyebrow on-dark">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def tofill(label, what):
    return f'<div class="tofill"><b>{label}</b>{what}</div>'


WHAT_WE_DO = [
    ("growth", "Economic Development",
     "Entrepreneurship, investment, job creation, innovation, and stronger local economies."),
    ("learn", "Education &amp; Capacity Building",
     "Training, leadership development, technical assistance, knowledge exchange, and "
     "institutional strengthening."),
    ("build", "Infrastructure &amp; Community Development",
     "Connecting communities and partners to infrastructure and development opportunities."),
    ("rights", "Human Rights &amp; Inclusion",
     "Promoting dignity, protection, inclusion, youth opportunity, gender equality, and "
     "community well-being."),
    ("link", "Global Partnerships &amp; Investment",
     "Connecting governments, businesses, investors, development organizations, financial "
     "institutions, and diaspora networks."),
    ("globe", "Global Engagement",
     "Connecting local priorities with international institutions, dialogue, advocacy, and "
     "collaborative action."),
]

STEPS = [
    ("01", "Listen", "Understand community priorities and local realities."),
    ("02", "Connect", "Bring together people, institutions, expertise, capital, and resources."),
    ("03", "Build", "Strengthen local capacity and strategic partnerships."),
    ("04", "Advance", "Move opportunities toward implementation and measurable results."),
    ("05", "Sustain", "Build systems and partnerships capable of creating long-term value."),
]

IMPACT = [("chart", "Economic Opportunity"), ("people", "Human Development"),
          ("shield", "Community Resilience"), ("build", "Infrastructure &amp; Systems"),
          ("node", "Global Partnership")]

CATS = [("gov", "Government &amp; Public Institutions"), ("invest", "Investors &amp; Financial Partners"),
        ("biz", "Businesses"), ("ngo", "Development Organizations"),
        ("people", "Community Organizations"), ("intl", "International Institutions"),
        ("dias", "Diaspora Networks")]

VALUES = ["Dignity", "Partnership", "Inclusion", "Integrity", "Sustainability", "Action"]


def cards_grid(items, link="what-we-do.html"):
    out = []
    for i, (ic, t, d) in enumerate(items):
        out.append(f"""
      <article class="card rv" data-d="{(i % 3) * 90}">
        <span class="ico">{icon(ic)}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <a class="arrow-link" href="{link}">Learn More {ARROW}</a>
      </article>""")
    return '<div class="grid3">%s\n    </div>' % "".join(out)


def cats_grid():
    return '<div class="cats">%s\n    </div>' % "".join(
        f"""
      <div class="cat rv" data-d="{(i % 4) * 70}"><span class="ico">{icon(ic)}</span>
        <h4>{t}</h4></div>""" for i, (ic, t) in enumerate(CATS))


def values_strip():
    return '<ul class="values rv">%s</ul>' % "".join(
        f'<li>{v}</li>' for v in VALUES)


def inquiry_form():
    opts = ["", "Partnership", "Investment", "Project collaboration", "Technical assistance",
            "Community initiative", "Media or speaking", "Other"]
    o = "".join('<option%s>%s</option>' % (' value=""' if not x else '', x or 'Select an area')
                for x in opts)
    return f"""
    <form class="form rv" id="inquiry" novalidate>
      <div class="form-msg" role="status" aria-live="polite"></div>
      <div class="frow">
        <div class="field"><label for="f-name">Name</label>
          <input id="f-name" name="name" type="text" autocomplete="name" required>
          <span class="err">Please tell us your name.</span></div>
        <div class="field"><label for="f-org">Organization</label>
          <input id="f-org" name="organization" type="text" autocomplete="organization"></div>
        <div class="field"><label for="f-email">Email</label>
          <input id="f-email" name="email" type="email" autocomplete="email" required>
          <span class="err">Please enter an address we can reply to.</span></div>
        <div class="field"><label for="f-country">Country</label>
          <input id="f-country" name="country" type="text" autocomplete="country-name"></div>
        <div class="field full"><label for="f-int">Area of Interest</label>
          <select id="f-int" name="interest">{o}</select></div>
        <div class="field full"><label for="f-msg">Message</label>
          <textarea id="f-msg" name="message" required></textarea>
          <span class="err">Please tell us what you have in mind.</span></div>
      </div>
      <button class="btn btn-primary" type="submit">Send Inquiry</button>
      <p class="form-note">We read every inquiry. Partnership proposals are reviewed by the
        relevant team and answered directly.</p>
    </form>"""


# ══════════════════════════════════════════════════════════════════════════
# 1. HOME — the five sections
# ══════════════════════════════════════════════════════════════════════════
home = f"""
<main>

<!-- SECTION 1 — HERO / GLOBAL MISSION -->
<section class="hero">
  <img class="hero-img" src="assets/img/hero.svg" alt="" aria-hidden="true">
  <div class="wrap">
    <span class="eyebrow on-dark">{ORG}</span>
    <h1>Advancing Sustainable Development.<br>Expanding Opportunity.<br>
      <em>Building Global Partnerships.</em></h1>
    <p class="lede">GCFPAD connects governments, investors, businesses, development
      organizations, civil society, and communities to advance sustainable development,
      inclusive growth, human dignity, and opportunity.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="our-work.html">Explore Our Work</a>
      <a class="btn btn-ghost" href="partnerships.html#partner">Partner With Us</a>
    </div>
    <div class="hero-strip">
      <span>Connecting Opportunities</span><span>Empowering Communities</span>
      <span>Building Sustainable Futures</span>
    </div>
  </div>
</section>

<!-- SECTION 2 — WHO WE ARE / VISION + MISSION -->
<section class="sec">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Who We Are</span>
      <h2>Building Sustainable Futures</h2>
      <p class="lede">GCFPAD connects people, resources, institutions, and ideas to help
        communities transform local priorities into sustainable initiatives and lasting
        opportunities.</p>
    </div>
    <div class="duo">
      <article class="bigcard rv">
        <span class="num">01</span>
        <h3>Our Vision</h3>
        <p>A world where every community has the opportunity to build a secure, dignified,
          and sustainable future.</p>
        <a class="arrow-link" href="about.html#vision">Learn More {ARROW}</a>
      </article>
      <article class="bigcard rv" data-d="110">
        <span class="num">02</span>
        <h3>Our Mission</h3>
        <p>Connecting people, resources, institutions, and ideas to advance sustainable and
          inclusive development.</p>
        <a class="arrow-link" href="about.html#mission">Learn More {ARROW}</a>
      </article>
    </div>
    {values_strip()}
  </div>
</section>

<!-- SECTION 3 — WHAT WE DO -->
<section class="sec sec-paper">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">What We Do</span>
      <h2>Turning Opportunity Into Action</h2>
      <p class="lede">We connect local priorities with global resources, expertise,
        investment, and strategic partnerships.</p>
    </div>
    {cards_grid(WHAT_WE_DO)}
  </div>
</section>

<!-- SECTION 4 — OUR APPROACH + IMPACT -->
<section class="sec sec-dark">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow on-dark">Our Approach</span>
      <h2>From Dialogue to Sustainable Impact</h2>
    </div>
    <div class="steps">
      {"".join(f'''
      <div class="step rv" data-d="{i*90}">
        <div class="dot">{n}</div>
        <h4>{t}</h4>
        <p>{d}</p>
      </div>''' for i, (n, t, d) in enumerate(STEPS))}
    </div>

    <div class="impact">
      {"".join(f'''
      <div class="rv" data-d="{i*70}"><span class="ico">{icon(ic)}</span><h4>{t}</h4></div>'''
               for i, (ic, t) in enumerate(IMPACT))}
    </div>

    <div class="btn-row rv"><a class="btn btn-primary" href="our-work.html">Explore Our Projects</a></div>

    <!-- FEATURED PROJECT -->
    <div class="feature rv">
      <div class="feature-img">
        <img src="assets/img/project.svg" alt="" aria-hidden="true">
      </div>
      <div class="feature-body">
        <div class="tag">Featured Project</div>
        <h3>Saint Francis Mission &amp; Foundation for Caring</h3>
        <p class="quote">From Compassion to Opportunity. From Assistance to Sustainable
          Development.</p>
        <a class="arrow-link" href="our-work.html#saint-francis">View Project {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 5 — GLOBAL PARTNERSHIPS / GET INVOLVED / CONTACT -->
<section class="sec" id="partner">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Global Partnerships</span>
      <h2>Let's Build What Comes Next.</h2>
      <p class="lede">Development happens when people work together. Whether you represent a
        government, investor, business, development organization, community, international
        institution, or diaspora network, GCFPAD welcomes opportunities for meaningful
        collaboration.</p>
    </div>
    {cats_grid()}
    <div class="btn-row rv">
      <a class="btn btn-dark" href="partnerships.html#partner">Partner With GCFPAD</a>
      <a class="btn btn-outline" href="contact.html">Contact Us</a>
      <a class="btn btn-outline" href="contact.html#inquiry">Submit an Opportunity</a>
    </div>
    <div style="margin-top:clamp(48px,5vw,72px);max-width:860px">
      {inquiry_form()}
    </div>
  </div>
</section>

</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 2. ABOUT
# ══════════════════════════════════════════════════════════════════════════
about = f"""
<main>
{phero("Who We Are",
       "GCFPAD connects people, resources, institutions, and ideas to help communities "
       "transform local priorities into sustainable initiatives and lasting opportunities.",
       "about.svg", "About GCFPAD")}

<section class="sec">
  <div class="wrap-wide split">
    <div class="rv prose">
      <span class="eyebrow">Our Purpose</span>
      <h2 style="margin-bottom:22px">Building Sustainable Futures</h2>
      <p>GCFPAD exists to close the distance between a community that knows what it needs and
        the institutions, expertise and capital that can help it get there. We are a
        confederation: we convene rather than replace, and we work through partners already
        rooted where the work happens.</p>
      {tofill("Content to add", "The full organizational background, history and legal "
              "status from the 21-page document belongs here. Send me that section and it "
              "goes in as written.")}
    </div>
    <div class="split-img rv" data-d="120">
      <img src="assets/img/whatwedo.svg" alt="" aria-hidden="true">
    </div>
  </div>
</section>

<section class="sec sec-paper">
  <div class="wrap-wide">
    <div class="duo">
      <article class="bigcard rv" id="vision">
        <span class="num">01</span>
        <h3>Our Vision</h3>
        <p>A world where every community has the opportunity to build a secure, dignified,
          and sustainable future.</p>
      </article>
      <article class="bigcard rv" data-d="110" id="mission">
        <span class="num">02</span>
        <h3>Our Mission</h3>
        <p>Connecting people, resources, institutions, and ideas to advance sustainable and
          inclusive development.</p>
      </article>
    </div>
    {values_strip()}
  </div>
</section>

<section class="sec">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Our Values</span>
      <h2>Six commitments that decide how we work</h2>
    </div>
    <div class="grid3">
      {"".join(f'''
      <article class="card rv" data-d="{(i%3)*90}">
        <span class="ico">{icon(ic)}</span>
        <h3>{v}</h3>
        <p>{d}</p>
      </article>''' for i, (v, ic, d) in enumerate([
        ("Dignity", "rights", "Every person we work with is treated as the author of their own "
         "future, not the subject of someone else's plan."),
        ("Partnership", "node", "We do not arrive with the answer. We convene the people who "
         "already hold most of it."),
        ("Inclusion", "people", "Youth, women, and communities at the margin are part of the "
         "design, not an afterthought in the report."),
        ("Integrity", "shield", "Transparent governance, honest reporting, and a clear line "
         "between what is promised and what is delivered."),
        ("Sustainability", "growth", "Work that survives our departure. Capacity first, "
         "systems second, headlines last."),
        ("Action", "build", "Dialogue is where development starts, not where it finishes."),
      ]))}
    </div>
  </div>
</section>

{band("Work with a confederation, not a contractor.",
      "GCFPAD is built to convene. Tell us what you are trying to move and we will tell you "
      "honestly whether we can help.")}
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 3. WHAT WE DO
# ══════════════════════════════════════════════════════════════════════════
whatwedo = f"""
<main>
{phero("Turning Opportunity Into Action",
       "We connect local priorities with global resources, expertise, investment, and "
       "strategic partnerships.", "whatwedo.svg", "What We Do")}

<section class="sec sec-paper">
  <div class="wrap-wide">
    {cards_grid(WHAT_WE_DO, link="contact.html#inquiry")}
    {tofill("Content to add", "Each of these six areas has detail in the 21-page document - "
            "programmes, criteria, who to approach. Send me those sections and each card "
            "gets its own full page beneath this grid.")}
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow on-dark">Our Approach</span>
      <h2>From Dialogue to Sustainable Impact</h2>
      <p class="lede" style="color:rgba(246,242,236,.72)">The same five steps apply whether
        the work is a single community initiative or a multi-country partnership.</p>
    </div>
    <div class="steps">
      {"".join(f'''
      <div class="step rv" data-d="{i*90}"><div class="dot">{n}</div><h4>{t}</h4><p>{d}</p></div>'''
               for i, (n, t, d) in enumerate(STEPS))}
    </div>
  </div>
</section>

{band("Have an opportunity that fits?",
      "Submit it and the relevant team will look at it properly.",
      ("Submit an Opportunity", "contact.html#inquiry"), ("Our Work", "our-work.html"))}
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 4. OUR WORK
# ══════════════════════════════════════════════════════════════════════════
ourwork = f"""
<main>
{phero("Our Work",
       "Projects and partnerships carried out with and through the institutions and "
       "communities closest to the work.", "work.svg", "Our Work")}

<section class="sec">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Featured</span>
      <h2>Saint Francis Mission &amp; Foundation for Caring</h2>
    </div>
    <div class="split" id="saint-francis">
      <div class="split-img rv"><img src="assets/img/project.svg" alt="" aria-hidden="true"></div>
      <div class="rv prose" data-d="120">
        <p style="font-family:var(--serif);font-size:1.3rem;line-height:1.45;color:var(--deep);
           font-style:italic;margin-bottom:24px">From Compassion to Opportunity. From
           Assistance to Sustainable Development.</p>
        {tofill("Content to add", "The project description, location, partners, timeline and "
                "results belong here. I have deliberately written nothing about this project "
                "beyond the tagline you supplied - inventing detail about a real foundation "
                "is not something I will do.")}
        <div class="btn-row" style="margin-top:28px">
          <a class="btn btn-dark" href="contact.html#inquiry">Support This Project</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-paper">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Impact Areas</span>
      <h2>Where the work shows up</h2>
      <p class="lede">Five areas that every GCFPAD project is measured against.</p>
    </div>
    <div class="grid3">
      {"".join(f'''
      <article class="card rv" data-d="{(i%3)*90}">
        <span class="ico">{icon(ic)}</span><h3>{t}</h3>
        <p>{d}</p>
      </article>''' for i, (ic, t, d) in enumerate([
        ("chart", "Economic Opportunity", "Enterprise, employment and investment that stays in "
         "the local economy."),
        ("people", "Human Development", "Education, skills, health and the capacity of people "
         "to act on their own priorities."),
        ("shield", "Community Resilience", "The ability of a community to absorb a shock and "
         "keep functioning."),
        ("build", "Infrastructure &amp; Systems", "The physical and institutional systems "
         "development depends on."),
        ("node", "Global Partnership", "Relationships that outlast a single project cycle."),
      ]))}
      <article class="card rv" data-d="90" style="justify-content:center">
        <h3 style="margin-bottom:14px">Add a project</h3>
        <p>New projects slot into this grid without touching the homepage. Send the details
          and the photograph and it appears here.</p>
        <a class="arrow-link" href="contact.html">Get in touch {ARROW}</a>
      </article>
    </div>
  </div>
</section>

{band("Bring us a project.", "Communities, governments and foundations all come to GCFPAD "
      "the same way: with something specific they are trying to move.",
      ("Submit an Opportunity", "contact.html#inquiry"))}
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 5. PARTNERSHIPS
# ══════════════════════════════════════════════════════════════════════════
partnerships = f"""
<main>
{phero("Let's Build What Comes Next.",
       "Development happens when people work together. GCFPAD welcomes opportunities for "
       "meaningful collaboration.", "partners.svg", "Global Partnerships")}

<section class="sec" id="partner">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Who We Partner With</span>
      <h2>Seven kinds of partner, one way of working</h2>
      <p class="lede">Whether you represent a government, investor, business, development
        organization, community, international institution, or diaspora network, the
        conversation starts the same way: what are you trying to make happen, and who else
        needs to be in the room.</p>
    </div>
    {cats_grid()}
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow on-dark">How It Works</span>
      <h2>From first conversation to signed partnership</h2>
    </div>
    <div class="steps">
      {"".join(f'''
      <div class="step rv" data-d="{i*90}"><div class="dot">{n}</div><h4>{t}</h4><p>{d}</p></div>'''
               for i, (n, t, d) in enumerate([
        ("01", "Enquire", "Tell us who you are and what you are trying to move."),
        ("02", "Scope", "We map the partners, resources and constraints with you."),
        ("03", "Agree", "Roles, contributions and what success will be measured against."),
        ("04", "Deliver", "Implementation through partners rooted where the work happens."),
        ("05", "Report", "Honest reporting against what was agreed, not against what looks best."),
      ]))}
    </div>
  </div>
</section>

<section class="sec sec-paper">
  <div class="wrap-wide" style="max-width:900px">
    <div class="sec-head rv center">
      <span class="eyebrow">Start Here</span>
      <h2>Partner With GCFPAD</h2>
      <p class="lede">One form. It reaches the team that handles your kind of partnership.</p>
    </div>
    {inquiry_form()}
  </div>
</section>
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 6. LEADERSHIP
# ══════════════════════════════════════════════════════════════════════════
leadership = f"""
<main>
{phero("Leadership &amp; Governance",
       "The people and the structure accountable for how GCFPAD works.",
       "leadership.svg", "Leadership")}

<section class="sec">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Governance</span>
      <h2>Accountable by design</h2>
      <p class="lede">A confederation only works if it is clear who decides what. This page
        sets out the governing bodies, the leadership team, and how decisions are made.</p>
    </div>
    {tofill("Content to add — I will not invent this",
            "Names, titles, photographs and biographies must come from you. I have left six "
            "placeholder cards below so you can see the layout, but I have not written a "
            "single person into this organization. Send the leadership section of the "
            "document and the photographs, and these become real.")}
    <div class="people" style="margin-top:38px">
      {"".join(f'''
      <article class="person rv" data-d="{(i%3)*90}">
        <div class="person-img"><img src="assets/img/person-{i+1}.svg" alt="" aria-hidden="true"></div>
        <h4>Name to be supplied</h4>
        <div class="role">Title to be supplied</div>
      </article>''' for i in range(6))}
    </div>
  </div>
</section>

<section class="sec sec-paper">
  <div class="wrap-wide">
    <div class="sec-head rv">
      <span class="eyebrow">Structure</span>
      <h2>How GCFPAD is organized</h2>
    </div>
    <div class="grid3">
      {"".join(f'''
      <article class="card rv" data-d="{(i%3)*90}">
        <span class="ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p>
      </article>''' for i, (ic, t, d) in enumerate([
        ("intl", "General Assembly", "The members of the confederation, meeting to set "
         "direction and approve the programme of work."),
        ("gov", "Executive Board", "Responsible for strategy, oversight and the appointment of "
         "the executive leadership."),
        ("node", "Secretariat", "Day-to-day coordination, partnerships and programme delivery."),
        ("people", "Advisory Council", "Independent expertise across the areas GCFPAD works in."),
        ("shield", "Audit &amp; Integrity", "Financial controls, safeguarding and conflict of "
         "interest."),
        ("globe", "Regional Chapters", "Representation close to where the work is carried out."),
      ]))}
    </div>
    {tofill("Confirm before publishing", "These six bodies are the conventional structure for "
            "a confederation of this kind. Confirm or correct them against your statutes "
            "before this page goes live - I would rather you change six headings than have a "
            "partner read something that is not how you are actually governed.")}
  </div>
</section>

{band("Questions about governance?", "We answer them directly.",
      ("Contact Us", "contact.html"), ("Partnerships", "partnerships.html"))}
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# 7. CONTACT
# ══════════════════════════════════════════════════════════════════════════
contact = f"""
<main>
{phero("Contact GCFPAD",
       "Partnership proposals, project opportunities, media and general enquiries.",
       "contact.svg", "Contact")}

<section class="sec">
  <div class="wrap-wide split" style="align-items:start">
    <div class="rv">
      <span class="eyebrow">Send an Inquiry</span>
      <h2 style="margin-bottom:26px">Tell us what you are trying to make happen</h2>
      {inquiry_form()}
    </div>
    <div class="rv prose" data-d="120" style="padding-top:8px">
      <h3 style="margin-top:0">Where to find us</h3>
      {tofill("Content to add", "Registered address, telephone, general inbox and social "
              "media accounts. I have left these out rather than putting a plausible-looking "
              "address on the page - a wrong address on a contact page is worse than none.")}
      <h3>Partnership proposals</h3>
      <p>Use the form and choose <b>Partnership</b> as the area of interest. Tell us who you
        represent, where you work and what you need from a partner. Proposals are reviewed by
        the team responsible for that sector.</p>
      <h3>Submitting an opportunity</h3>
      <p>Communities, local organizations and governments can submit an opportunity directly.
        You do not need a completed proposal - a clear description of the priority and who is
        already involved is enough to start.</p>
      <h3>Media</h3>
      <p>Choose <b>Media or speaking</b> in the form and include your outlet and deadline.</p>
    </div>
  </div>
</section>
</main>"""

# ══════════════════════════════════════════════════════════════════════════
# PRIVACY + TERMS — linked from the footer, so they must exist
# ══════════════════════════════════════════════════════════════════════════
def legal(title, intro, blocks):
    inner = "".join(f"<h3>{h}</h3><p>{b}</p>" for h, b in blocks)
    return f"""
<main>
{phero(title, intro, "about.svg", "Legal")}
<section class="sec">
  <div class="wrap" style="max-width:820px">
    <div class="prose rv">
      {tofill("Review before publishing", "This is a plain-language starting point, not legal "
              "advice. Have it checked against the law of the country GCFPAD is registered in "
              "before the site goes live, and tell me the registered entity name and address "
              "so they can be named here.")}
      {inner}
    </div>
  </div>
</section>
</main>"""


privacy = legal(
    "Privacy Policy",
    "What we collect when you contact us, and what we do with it.",
    [("What we collect", "When you send an inquiry we receive the name, organization, email "
      "address, country, area of interest and message you type into the form. We do not "
      "collect anything else through this website."),
     ("Why we hold it", "To answer your inquiry and, where it leads to a partnership, to "
      "carry out that work. We do not sell it and we do not use it for unrelated marketing."),
     ("How long", "Inquiries are kept for as long as the relationship is active, and then "
      "deleted."),
     ("Cookies", "This website sets no tracking cookies and runs no advertising or analytics "
      "scripts. The only external request it makes is for the typefaces."),
     ("Your rights", "You can ask us what we hold about you, ask for it to be corrected, or "
      "ask for it to be deleted. Use the contact form and say so.")])

terms = legal(
    "Terms of Use",
    "The terms on which this website is made available.",
    [("The content", "The material on this website is published for information. It is not an "
      "offer, a commitment to fund, or professional advice."),
     ("Accuracy", "We take care that what is published is accurate at the time of publication. "
      "Projects, partnerships and figures change."),
     ("Inquiries", "Sending an inquiry does not create a partnership or any obligation on "
      "either side. Partnerships are established in writing."),
     ("Intellectual property", "The name, logo and content of this website belong to the "
      "organization unless stated otherwise."),
     ("Links", "Where we link to another organization we are not responsible for what is "
      "published there.")])


print("pages ->", ROOT)
page("index.html", f"{ORG} — GCFPAD",
     "GCFPAD connects governments, investors, businesses, development organizations, civil "
     "society and communities to advance sustainable development, inclusive growth, human "
     "dignity and opportunity.", home)
page("about.html", f"About — GCFPAD",
     "Who GCFPAD is: vision, mission and the six values that decide how we work.", about)
page("what-we-do.html", "What We Do — GCFPAD",
     "Economic development, education and capacity building, infrastructure, human rights and "
     "inclusion, global partnerships and investment, and global engagement.", whatwedo)
page("our-work.html", "Our Work — GCFPAD",
     "Projects and partnerships, including the Saint Francis Mission & Foundation for Caring.",
     ourwork)
page("partnerships.html", "Partnerships — GCFPAD",
     "Partner with GCFPAD: governments, investors, businesses, development organizations, "
     "communities, international institutions and diaspora networks.", partnerships)
page("leadership.html", "Leadership & Governance — GCFPAD",
     "The governing bodies and leadership accountable for how GCFPAD works.", leadership)
page("contact.html", "Contact — GCFPAD",
     "Partnership proposals, project opportunities, media and general enquiries.", contact)
page("privacy.html", "Privacy Policy — GCFPAD",
     "What GCFPAD collects when you make contact, and what we do with it.", privacy)
page("terms.html", "Terms of Use — GCFPAD",
     "The terms on which the GCFPAD website is made available.", terms)

# favicon - the mark on its own
open(os.path.join(ROOT, "assets", "img", "favicon.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
    '<rect width="40" height="40" rx="7" fill="#0B1F2A"/>'
    '<g transform="translate(5,5) scale(0.75)" fill="none">'
    '<circle cx="20" cy="20" r="18.4" stroke="#E8DFD1" stroke-width="1.6"/>'
    '<path d="M20 1.6c5 5.6 7.6 11.7 7.6 18.4S25 32.8 20 38.4" stroke="#C8702A" stroke-width="2"/>'
    '<path d="M20 1.6c-5 5.6-7.6 11.7-7.6 18.4S15 32.8 20 38.4" stroke="#C8702A"'
    ' stroke-width="2" stroke-opacity=".45"/>'
    '<path d="M2.4 13.6h35.2M2.4 26.4h35.2" stroke="#E8DFD1" stroke-width="1.3" stroke-opacity=".5"/>'
    '</g></svg>')
print("  favicon.svg")
print("done")
