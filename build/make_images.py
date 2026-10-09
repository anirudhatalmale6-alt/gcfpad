#!/usr/bin/env python3
"""The placeholder artwork.

Jeffery approved "professional placeholders" until the real photography
arrives. The temptation is to pull stock photographs off the internet; I will
not, for two reasons. An institutional site that shows a stock photograph of a
village it has no connection to is making a claim, and the licence on a hotlinked
image is somebody else's problem until it is suddenly ours.

So every image slot holds generated duotone artwork in the brand palette -
contour fields, graticules, halftone - which reads as a deliberate art
direction rather than a missing photograph. Each one is a single <img> with a
fixed aspect box behind it, so replacing it with a real photograph later is one
file swap and nothing moves.

Deterministic: seeded, so rebuilding does not churn the files.
"""
import math, os, random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
os.makedirs(OUT, exist_ok=True)

INK   = "#0B1F2A"
DEEP  = "#0E3B4A"
MID   = "#1C5B6B"
OCHRE = "#C8702A"
SAND  = "#E8DFD1"
BONE  = "#F6F2EC"


def contours(w, h, seed, lines=40, amp=0.055, step=None, phase=0.0):
    """A field of soft horizontal contours - the look of a relief map."""
    rnd = random.Random(seed)
    step = step or h / (lines - 2)
    out = []
    for i in range(lines):
        y0 = -step + i * step
        # three summed sines, randomised per line, so no two read the same
        a = [(rnd.uniform(0.35, 1.0) * amp * h,
              rnd.uniform(0.5, 1.8),
              rnd.uniform(0, math.tau)) for _ in range(3)]
        pts = []
        for x in range(0, w + 1, max(8, w // 90)):
            t = x / w
            y = y0 + sum(A * math.sin(f * math.tau * t + p + phase) for A, f, p in a)
            pts.append("%.1f,%.1f" % (x, y))
        out.append(" ".join(pts))
    return out


def svg_wrap(w, h, body, bg):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="%d" height="%d" preserveAspectRatio="xMidYMid slice" '
            'role="img" aria-label="Placeholder artwork">'
            '<rect width="%d" height="%d" fill="%s"/>%s</svg>') % (w, h, w, h, w, h, bg, body)


def relief(name, w, h, seed, base, line, accent, accent_at=None, graticule=True, dots=False):
    b = []
    b.append('<defs>'
             '<linearGradient id="g" x1="0" y1="0" x2="0.35" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity=".0"/>'
             '<stop offset="1" stop-color="%s" stop-opacity=".55"/>'
             '</linearGradient></defs>' % (INK, INK))
    if graticule:
        g = []
        for x in range(0, w + 1, w // 12):
            g.append('<line x1="%d" y1="0" x2="%d" y2="%d"/>' % (x, x, h))
        for y in range(0, h + 1, max(1, h // 8)):
            g.append('<line x1="0" y1="%d" x2="%d" y2="%d"/>' % (y, w, y))
        b.append('<g stroke="%s" stroke-opacity=".10" stroke-width="1">%s</g>'
                 % (line, "".join(g)))
    cs = contours(w, h, seed)
    paths = []
    for i, pts in enumerate(cs):
        op = 0.10 + 0.5 * (i / len(cs))
        sw = 1.1 if i % 4 else 2.0
        col = line
        if accent_at is not None and i in accent_at:
            col, op, sw = accent, 0.85, 2.4
        paths.append('<polyline points="%s" fill="none" stroke="%s" stroke-opacity="%.2f" '
                     'stroke-width="%.1f" stroke-linecap="round"/>' % (pts, col, op, sw))
    b.append("".join(paths))
    if dots:
        rnd = random.Random(seed + 77)
        d = []
        for _ in range(170):
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
            r = rnd.uniform(0.8, 2.6)
            d.append('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (x, y, r))
        b.append('<g fill="%s" fill-opacity=".22">%s</g>' % (accent, "".join(d)))
    b.append('<rect width="%d" height="%d" fill="url(#g)"/>' % (w, h))
    open(os.path.join(OUT, name), "w").write(svg_wrap(w, h, "".join(b), base))
    print("  " + name)


print("artwork ->", OUT)
# The hero carries the most weight, so it gets the accent ridge lines.
relief("hero.svg",       1920, 1080, 11, DEEP, SAND,  OCHRE, accent_at={9, 14, 19}, dots=True)
relief("approach.svg",   1920,  900, 23, INK,  MID,   OCHRE, accent_at={12})
relief("project.svg",    1600, 1100, 31, MID,  BONE,  OCHRE, accent_at={7, 16}, dots=True)
relief("about.svg",      1600,  900, 43, DEEP, SAND,  OCHRE, accent_at={11})
relief("work.svg",       1600,  900, 57, INK,  MID,   OCHRE, accent_at={6, 17}, dots=True)
relief("partners.svg",   1600,  900, 67, DEEP, BONE,  OCHRE, accent_at={13})
relief("leadership.svg", 1600,  900, 79, MID,  BONE,  OCHRE, accent_at={9})
relief("contact.svg",    1600,  900, 89, INK,  SAND,  OCHRE, accent_at={15}, dots=True)
relief("whatwedo.svg",   1600,  900, 97, DEEP, MID,   OCHRE, accent_at={8, 18})

# A square portrait slot for the leadership page.
# ⚠️ NOT the contour artwork. Six large abstract squares where six faces
# belong reads as a design choice nobody made; a plain, quiet portrait frame
# reads as "photograph to come", which is the truth. Two tones, a soft
# silhouette, and the brand rule at the foot.
def portrait(name, bg, fg, rule):
    body = (
        '<rect width="800" height="800" fill="%s"/>' % bg +
        '<g fill="%s" fill-opacity=".30">' % fg +
        '<circle cx="400" cy="318" r="104"/>' +
        '<path d="M196 640c0-112 91-182 204-182s204 70 204 182v60H196z"/></g>' +
        '<rect x="0" y="782" width="800" height="18" fill="%s"/>' % rule
    )
    open(os.path.join(OUT, name), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" '
        'height="800" preserveAspectRatio="xMidYMid slice" role="img" '
        'aria-label="Portrait placeholder">%s</svg>' % body)
    print("  " + name)


for i in range(6):
    portrait("person-%d.svg" % (i + 1),
             SAND if i % 2 else "#EFE8DC",
             "#9AA7AD" if i % 2 else "#A8B3B8",
             OCHRE if i == 0 else "#D8CCBB")
print("done")
