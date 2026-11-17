#!/usr/bin/env python3
"""Build the official Adabury School logo files (all text outlined to vector paths).

Usage:  python3 build_logo.py <dir-with-Marcellus.ttf-and-Outfit.ttf>
Fonts:  Marcellus (wordmark, motto) and Outfit 500 (descriptor), both SIL Open Font License,
        from Google Fonts.
Output: SVG files next to this script.
"""
import math
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent
FONTDIR = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

# ---- Official palette -------------------------------------------------------
CLARET = "#6E1F2F"       # Adabury Claret (primary)
GOLD = "#C2A15A"         # Old Gold (secondary)
GOLD_LIGHT = "#C9A962"   # Gold for use on claret
LINEN = "#F5EEE6"        # Linen (paper / light ground)
CLARET_DEEP = "#4E1420"  # ribbon fold shadow on light grounds
GOLD_DEEP = "#A8843E"    # ribbon fold shadow on claret grounds

MOTTO = "ADAB · ILM · IHSAN"
NAME = "ADABURY"
DESCRIPTOR = "SCHOOL · FAISALABAD"


class Font:
    def __init__(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.hmtx = self.f["hmtx"]

    def glyph(self, ch):
        name = self.cmap.get(ord(ch)) or self.cmap.get(ord("·"))
        return name, self.hmtx[name][0]

    def width(self, text, size, track):
        s = size / self.upm
        total = sum(self.glyph(c)[1] * s for c in text)
        return total + track * size * (len(text) - 1)

    def draw(self, ch, matrix):
        name, _ = self.glyph(ch)
        pen = SVGPathPen(self.gs)
        self.gs[name].draw(TransformPen(pen, matrix))
        return pen.getCommands()

    def line(self, text, size, track, cx, baseline):
        """Outline a straight line of text centred on cx."""
        s = size / self.upm
        x = cx - self.width(text, size, track) / 2
        d = []
        for ch in text:
            d.append(self.draw(ch, (s, 0, 0, -s, x, baseline)))
            x += self.glyph(ch)[1] * s + track * size
        return " ".join(d)

    def line_left(self, text, size, track, x, baseline):
        return self.line(text, size, track, x + self.width(text, size, track) / 2, baseline)

    def on_quad(self, text, size, track, p0, p1, p2):
        """Outline text centred along a quadratic Bezier curve."""
        n = 400
        pts = [quad(p0, p1, p2, i / n) for i in range(n + 1)]
        cum = [0.0]
        for a, b in zip(pts, pts[1:]):
            cum.append(cum[-1] + math.dist(a, b))
        total = cum[-1]
        s = size / self.upm

        def at(L):
            for i in range(1, len(cum)):
                if cum[i] >= L:
                    t = (i - 1 + (L - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)) / n
                    return quad(p0, p1, p2, t), quad_tangent(p0, p1, p2, t)
            return pts[-1], quad_tangent(p0, p1, p2, 1)

        pos = (total - self.width(text, size, track)) / 2
        d = []
        for ch in text:
            adv = self.glyph(ch)[1] * s
            (mx, my), ang = at(pos + adv / 2)
            c, si = math.cos(ang), math.sin(ang)
            ox, oy = mx - c * adv / 2, my - si * adv / 2
            d.append(self.draw(ch, (s * c, s * si, s * si, -s * c, ox, oy)))
            pos += adv + track * size
        return " ".join(d)


def quad(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def quad_tangent(p0, p1, p2, t):
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    return math.atan2(dy, dx)


MARCELLUS = Font(FONTDIR / "Marcellus.ttf")
OUTFIT = Font(FONTDIR / "Outfit.ttf")


# ---- Crest (100 x 104 units) ------------------------------------------------
def crest(P, S):
    """P = shield field colour, S = charge colour (tower, star, olive, border)."""
    leaves_l = [(34.2, 79.5, -50), (31.3, 72, -70), (30.2, 64.5, -85), (30.6, 57.5, -100)]
    leaves = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="4.6" ry="2" transform="rotate({a} {x} {y})"/>'
        f'<ellipse cx="{100 - x}" cy="{y}" rx="4.6" ry="2" transform="rotate({-a} {100 - x} {y})"/>'
        for x, y, a in leaves_l)
    return f'''
<path fill="{P}" d="M14 12 Q50 2 86 12 L86 50 C86 76 69 91 50 99 C31 91 14 76 14 50 Z"/>
<path fill="none" stroke="{S}" stroke-width="1.4" d="M20 15.5 Q50 7 80 15.5 L80 50 C80 72 66 85 50 92 C34 85 20 72 20 50 Z"/>
<g fill="{S}">
  <rect x="46.5" y="13.5" width="7" height="7"/>
  <rect x="46.5" y="13.5" width="7" height="7" transform="rotate(45 50 17)"/>
</g>
<circle fill="{P}" cx="50" cy="17" r="1.8"/>
<g fill="none" stroke="{S}" stroke-width="1.3" stroke-linecap="round">
  <path d="M38 85 Q29 75 30 56"/><path d="M62 85 Q71 75 70 56"/>
</g>
<g fill="{S}">{leaves}
  <rect x="49.4" y="22.5" width="1.2" height="4.5"/>
  <path d="M44.5 36 Q44.5 29.5 50 26.5 Q55.5 29.5 55.5 36 Z"/>
  <path d="M41.5 36 L41.5 32.5 L42.75 30 L44 32.5 L44 36 Z"/>
  <path d="M56 36 L56 32.5 L57.25 30 L58.5 32.5 L58.5 36 Z"/>
  <rect x="40.5" y="36" width="19" height="3"/>
  <rect x="43.5" y="39" width="13" height="8"/>
  <rect x="41.5" y="47" width="17" height="3"/>
  <rect x="43" y="50" width="14" height="28"/>
  <rect x="39" y="78" width="22" height="5"/>
  <rect x="36" y="83" width="28" height="3"/>
</g>
<g fill="{P}">
  <path d="M48.6 45.5 L48.6 42.5 Q50 40.6 51.4 42.5 L51.4 45.5 Z"/>
  <circle cx="50" cy="57" r="4.4"/>
  <path d="M46.8 78 L46.8 70 Q50 65.5 53.2 70 L53.2 78 Z"/>
</g>
<g fill="none" stroke="{S}" stroke-width="1.1" stroke-linecap="round">
  <line x1="50" y1="57" x2="50" y2="54.2"/><line x1="50" y1="57" x2="52.3" y2="58.2"/>
</g>'''


# ---- Motto ribbon (240 x 44 units) ------------------------------------------
RIBBON_TEXT = MARCELLUS.on_quad(MOTTO, 11, 0.27, (32, 25.5), (120, 15.5), (208, 25.5))


def ribbon(BAND, TAIL, TEXT):
    return f'''
<path fill="{TAIL}" d="M28 13 L3 13 L13 23 L3 33 L28 33 Z"/>
<path fill="{TAIL}" d="M212 13 L237 13 L227 23 L237 33 L212 33 Z"/>
<path fill="{BAND}" d="M22 9 Q120 -1 218 9 L218 33 Q120 23 22 33 Z"/>
<path fill="{TEXT}" d="{RIBBON_TEXT}"/>'''


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def place(inner, x, y, scale):
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({scale:.4f})">{inner}</g>'


# ---- Lockups ----------------------------------------------------------------
W = 300


def stacked(cP, cS, band, tail, rtext, name, desc, bg=None):
    body = ""
    if bg:
        body += f'<rect width="{W}" height="262" fill="{bg}"/>'
        y0 = 8
    else:
        y0 = 0
    body += place(crest(cP, cS), 75, y0, 1.5)
    body += place(ribbon(band, tail, rtext), 35, y0 + 126, 230 / 240)
    body += f'<path fill="{name}" d="{MARCELLUS.line(NAME, 40, 0.22, W / 2, y0 + 214)}"/>'
    body += f'<path fill="{desc}" d="{OUTFIT.line(DESCRIPTOR, 11, 0.32, W / 2, y0 + 238)}"/>'
    return body, (262 if bg else 246)


def horizontal(cP, cS, name, desc):
    nw = MARCELLUS.width(NAME, 36, 0.2)
    dw = OUTFIT.width(DESCRIPTOR, 10.5, 0.3)
    tx = 122
    body = place(crest(cP, cS), 0, 0, 1.0)
    body += f'<path fill="{name}" d="{MARCELLUS.line_left(NAME, 36, 0.2, tx, 56)}"/>'
    body += f'<path fill="{desc}" d="{OUTFIT.line_left(DESCRIPTOR, 10.5, 0.3, tx + 1, 78)}"/>'
    return body, tx + max(nw, dw) + 2, 104


def mono_crest(colour, uid):
    return (f'<defs><mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="104">'
            f'{crest("#fff", "#000")}</mask></defs>'
            f'<rect width="100" height="104" fill="{colour}" mask="url(#m{uid})"/>')


def mono_ribbon(colour, uid):
    return (f'<defs><mask id="r{uid}" maskUnits="userSpaceOnUse" x="0" y="-2" width="240" height="46">'
            f'{ribbon("#fff", "#fff", "#000")}</mask></defs>'
            f'<rect y="-2" width="240" height="46" fill="{colour}" mask="url(#r{uid})"/>')


def mono_stacked(colour, uid):
    # One stencil for crest + ribbon, so the ribbon's letter cut-outs show the ground,
    # not the crest behind the ribbon.
    stencil = (place(crest("#fff", "#000"), 75, 0, 1.5)
               + place(ribbon("#fff", "#fff", "#000"), 35, 126, 230 / 240))
    body = (f'<defs><mask id="s{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="180">'
            f'{stencil}</mask></defs>'
            f'<rect width="{W}" height="180" fill="{colour}" mask="url(#s{uid})"/>')
    body += f'<path fill="{colour}" d="{MARCELLUS.line(NAME, 40, 0.22, W / 2, 214)}"/>'
    body += f'<path fill="{colour}" d="{OUTFIT.line(DESCRIPTOR, 11, 0.32, W / 2, 238)}"/>'
    return body


def write(name, content):
    (OUT / name).write_text(content)
    print("wrote", name)


T = "Adabury School"

# 1. Crest only
write("adabury-crest.svg", svg(100, 104, crest(CLARET, GOLD), T + " crest"))
write("adabury-crest-reverse.svg", svg(100, 104, crest(GOLD_LIGHT, CLARET), T + " crest, reverse"))

# 2. Primary stacked logo
b, h = stacked(CLARET, GOLD, GOLD, CLARET_DEEP, CLARET, CLARET, CLARET)
write("adabury-logo-primary.svg", svg(W, h, b, T))
b, h = stacked(GOLD_LIGHT, CLARET, GOLD_LIGHT, GOLD_DEEP, CLARET, LINEN, GOLD_LIGHT, bg=CLARET)
write("adabury-logo-primary-on-claret.svg", svg(W, h, b, T))

# 3. Horizontal logo
b, w, h = horizontal(CLARET, GOLD, CLARET, CLARET)
write("adabury-logo-horizontal.svg", svg(w, h, b, T))
b, w, h = horizontal(GOLD_LIGHT, CLARET, LINEN, GOLD_LIGHT)
write("adabury-logo-horizontal-reverse.svg", svg(w, h, b, T))

# 4. Single-colour versions (stamps, embroidery in one thread, engraving, fax/photocopy)
write("adabury-logo-mono-claret.svg", svg(W, 246, mono_stacked(CLARET, "c"), T))
write("adabury-logo-mono-black.svg", svg(W, 246, mono_stacked("#111111", "k"), T))
write("adabury-logo-mono-white.svg", svg(W, 246, mono_stacked("#FFFFFF", "w"), T))

# 5. App icon / social avatar (square, claret ground)
icon = f'<rect width="512" height="512" fill="{CLARET}"/>' + place(crest(GOLD_LIGHT, CLARET), 106, 100, 3.0)
write("adabury-app-icon.svg", svg(512, 512, icon, T + " app icon"))
