#!/usr/bin/env python3
"""Build the Adabury School uniform proposal page (brand/adabury-uniform.html).

Figures are drawn as flat fashion illustrations from shared garment parts.
Run from anywhere:  python3 build_uniform.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREST_SVG = (ROOT / "logo" / "adabury-crest.svg").read_text()
CREST_INNER = re.sub(r"^.*?<title>.*?</title>", "", CREST_SVG, flags=re.S).replace("</svg>", "")

CLARET, CLARET_D, GOLD, WHITE = "#6E1F2F", "#561522", "#C2A15A", "#FBFAF7"
CHARCOAL, INK, HAIR = "#3E4249", "#2A1418", "#2B1D17"
OL = f'stroke="{INK}" stroke-opacity=".28" stroke-width="1" stroke-linejoin="round"'
SKINS = ["#C68E6B", "#B07A5A", "#D9A882", "#A86F50"]


def mirror(d):
    """Mirror a path made only of absolute M/L/Q/C/Z commands around x = 80."""
    out = []
    for tok in re.findall(r"[MLQCZ]|-?\d+\.?\d*", d):
        out.append(tok)
    res, i, is_x = [], 0, True
    for tok in out:
        if tok in "MLQCZ":
            res.append(tok); is_x = True
        else:
            v = float(tok)
            res.append(f"{160 - v:g}" if is_x else f"{v:g}")
            is_x = not is_x
    return " ".join(res)


def pair(d, fill, extra=""):
    attrs = extra or OL  # explicit stroke settings replace the default outline
    return f'<path d="{d}" fill="{fill}" {attrs}/><path d="{mirror(d)}" fill="{fill}" {attrs}/>'


# ---- body parts -------------------------------------------------------------
def neck(skin):
    return f'<rect x="74.5" y="52" width="11" height="16" fill="{skin}"/>'


def face(skin):
    return f'<circle cx="80" cy="40" r="17" fill="{skin}"/>'


def hair_boy():
    return f'<path d="M62.5 38 C61 21 71 14 80 14 C90 14 99 21 97.5 38 C95 29 88 25.5 80 25.5 C72 25.5 65 29 62.5 38 Z" fill="{HAIR}"/>'


def hair_girl(band=CLARET):
    return (f'<path d="M62 42 C60 21 71 13 80 13 C89 13 100 21 98 42 C96 31 88 25 80 25 C72 25 64 31 62 42 Z" fill="{HAIR}"/>'
            f'<path d="M64 30 Q80 15 96 30" fill="none" stroke="{band}" stroke-width="3.2" stroke-linecap="round"/>')


def hair_girl_back():
    return f'<path d="M61 40 Q59 58 63 66 L70 66 L68 44 Z" fill="{HAIR}"/><path d="M99 40 Q101 58 97 66 L90 66 L92 44 Z" fill="{HAIR}"/>'


def hijab(colour, skin, trim=None):
    t = (f'<path d="M58 70 Q80 90 102 70" fill="none" stroke="{trim}" stroke-width="1.6"/>' if trim else "")
    return (f'<path d="M80 16 C61 16 57 32 57 46 C57 58 60 66 51 77 Q80 97 109 77 C100 66 103 58 103 46 C103 32 99 16 80 16 Z" fill="{colour}" {OL}/>'
            f'{t}<ellipse cx="80" cy="44" rx="12.5" ry="15" fill="{skin}"/>')


def hands(skin, y=168):
    return f'<circle cx="38.5" cy="{y}" r="6" fill="{skin}"/><circle cx="121.5" cy="{y}" r="6" fill="{skin}"/>'


# ---- garments ----------------------------------------------------------------
def shirt(colour=WHITE, sleeves="long", length=172, skin="#C68E6B"):
    s = f'<path d="M54 68 Q80 62 106 68 L110 {length} L50 {length} Z" fill="{colour}" {OL}/>'
    if sleeves == "long":
        s += pair("M54 68 L42 74 L33 162 L44.5 164 L51 104 Z", colour)
    else:
        s += pair("M38 104 L49 106 L45 162 L33 160 Z", skin, 'stroke-opacity="0"')
        s += pair("M54 68 L41 75 L36 106 L51 108 Z", colour)
    s += pair("M72 63 L80 73 L76 79 L67 68 Z", colour)
    return s


def tunic(colour=WHITE, trim=CLARET, length=250):
    s = f'<path d="M54 68 Q80 62 106 68 L114 {length} L46 {length} Z" fill="{colour}" {OL}/>'
    s += pair("M54 68 L42 74 L33 162 L44.5 164 L51 104 Z", colour)
    s += f'<line x1="47" y1="{length - 2}" x2="113" y2="{length - 2}" stroke="{trim}" stroke-width="3"/>'
    s += f'<path d="M50 {length - 34} L48.5 {length}" stroke="{INK}" stroke-opacity=".35" stroke-width="1"/><path d="M110 {length - 34} L111.5 {length}" stroke="{INK}" stroke-opacity=".35" stroke-width="1"/>'
    s += f'<path d="M73 64 Q80 76 87 64" fill="none" stroke="{trim}" stroke-width="2.2"/>'
    return s


def trousers(colour=CHARCOAL, top=170, stripe=None):
    d = f"M51 {top} L109 {top} L106 330 L85 330 L80 {top + 32} L75 330 L54 330 Z"
    s = f'<path d="{d}" fill="{colour}" {OL}/>'
    if stripe:
        s += f'<path d="M52 {top + 4} L54.5 330 M108 {top + 4} L105.5 330" stroke="{stripe}" stroke-width="2.4"/>'
    return s


def slim_trousers(colour=CHARCOAL, top=244):
    return f'<path d="M58 {top} L102 {top} L101 330 L84 330 L80 {top + 20} L76 330 L59 330 Z" fill="{colour}" {OL}/>'


def shoes(colour="#1A1A1A"):
    return pair("M54 329 L76 329 L77 338 L48 338 Q48 331 54 329 Z", colour)


def tie(stripe=GOLD, ground=CLARET):
    return (f'<path d="M78.3 72 L81.7 72 L84.5 78 L83 118 L80 123 L77 118 L75.5 78 Z" fill="url(#tie-{stripe[1:]})" {OL}/>'
            f'<path d="M76.5 65.5 L83.5 65.5 L82.3 73 L77.7 73 Z" fill="{ground}"/>')


def crest(x, y, w=14):
    return f'<use href="#crest" x="{x}" y="{y}" width="{w}" height="{w * 1.04:.1f}"/>'


def sweater(colour=CLARET, length=178, tip=GOLD):
    body = f"M53 66 Q66 62 72 64 L80 94 L88 64 Q94 62 107 66 L111 {length} L49 {length} Z"
    s = f'<path d="{body}" fill="{colour}" {OL}/>'
    s += pair("M53 66 L41 73 L33 160 L45 162 L51 104 Z", colour)
    s += f'<path d="M72 64 L80 94 L88 64" fill="none" stroke="{tip}" stroke-width="2"/>'
    s += f'<rect x="49" y="{length - 9}" width="62" height="9" fill="{CLARET_D}"/>'
    s += f'<line x1="49" y1="{length - 9}" x2="111" y2="{length - 9}" stroke="{tip}" stroke-width="1.6"/>'
    s += pair("M33.6 152 L45 154 L44.8 162 L33 160 Z", CLARET_D, 'stroke-opacity="0"')
    s += crest(91, 86, 13)
    return s


def blazer(colour=CLARET, length=184, piping=None):
    body = f"M50 64 Q63 60 71 62 L80 121 L89 62 Q97 60 110 64 L114 {length} L46 {length} Z"
    s = f'<path d="{body}" fill="{colour}" {OL}/>'
    s += pair("M50 64 L38 71 L31 160 L45 162 L51 104 Z", colour)
    s += pair("M71 62 L76 96 L72 100 L80 121", "none", f'stroke="{CLARET_D}" stroke-width="1.6"')
    if piping:
        s += f'<path d="M71 62 L80 121 L89 62 M46 {length - 1} L114 {length - 1}" fill="none" stroke="{piping}" stroke-width="2"/>'
        s += pair("M31.4 152 L45 154", "none", f'stroke="{piping}" stroke-width="2"')
    s += f'<circle cx="80" cy="134" r="2" fill="{GOLD}"/><circle cx="80" cy="152" r="2" fill="{GOLD}"/>'
    s += f'<path d="M58 150 L70 150" stroke="{CLARET_D}" stroke-width="1.6"/><path d="M90 150 L102 150" stroke="{CLARET_D}" stroke-width="1.6"/>'
    s += f'<path d="M89 99 L103 99" stroke="{CLARET_D}" stroke-width="1.4"/>'
    s += crest(89.5, 82, 14)
    return s


def polo(colour=CLARET, collar=GOLD, skin="#C68E6B", long=False):
    s = f'<path d="M54 68 Q80 62 106 68 L110 176 L50 176 Z" fill="{colour}" {OL}/>'
    if long:
        s += pair("M54 68 L42 74 L33 162 L44.5 164 L51 104 Z", colour)
        s += pair("M33.4 156 L44.8 158", "none", f'stroke="{collar}" stroke-width="2"')
    else:
        s += pair("M38 104 L49 106 L45 162 L33 160 Z", skin, 'stroke-opacity="0"')
        s += pair("M54 68 L41 75 L36 106 L51 108 Z", colour)
        s += pair("M36.4 102 L51 104", "none", f'stroke="{collar}" stroke-width="2.4"')
    s += pair("M72 63 L80 72 L77 78 L67 68 Z", collar)
    s += f'<path d="M80 72 L80 92" stroke="{CLARET_D}" stroke-width="1.4"/>'
    s += f'<path d="M50 120 L110 120" stroke="{collar}" stroke-width="2.4"/>'
    s += crest(91, 84, 12)
    return s


# ---- outfits -------------------------------------------------------------------
def figure(parts):
    return f'<svg viewBox="0 0 160 344" class="fig" aria-hidden="true">{parts}</svg>'


def junior_boy_winter(sk=SKINS[0]):
    return figure(neck(sk) + trousers(top=168) + shoes() + shirt(skin=sk) + tie() + sweater() + hands(sk) + face(sk) + hair_boy())


def junior_girl_winter(sk=SKINS[2]):
    return figure(hair_girl_back() + neck(sk) + slim_trousers() + shoes() + tunic() + sweater(length=182) + hands(sk) + face(sk) + hair_girl())


def senior_boy_winter(sk=SKINS[1]):
    return figure(neck(sk) + trousers(top=168) + shoes() + shirt(skin=sk) + tie() + blazer() + hands(sk) + face(sk) + hair_boy())


def senior_girl_winter(sk=SKINS[3]):
    return figure(neck(sk) + slim_trousers() + shoes() + tunic() + blazer(length=192) + hands(sk) + hijab(CLARET, sk, GOLD))


def olevel_boy_winter(sk=SKINS[2]):
    return figure(neck(sk) + trousers(top=168) + shoes() + shirt(skin=sk) + tie(stripe=WHITE) + blazer(piping=GOLD) + hands(sk) + face(sk) + hair_boy())


def olevel_girl_winter(sk=SKINS[0]):
    return figure(hair_girl_back() + neck(sk) + slim_trousers() + shoes() + tunic() + blazer(length=192, piping=GOLD) + hands(sk) + face(sk) + hair_girl(band=GOLD))


def boy_summer(sk=SKINS[3]):
    return figure(neck(sk) + trousers(top=168) + shoes() + shirt(sleeves="short", skin=sk) + crest(90, 86, 13) + hands(sk, 166) + face(sk) + hair_boy())


def girl_summer_hijab(sk=SKINS[1]):
    return figure(neck(sk) + slim_trousers() + shoes() + tunic() + crest(90, 92, 13) + hands(sk) + hijab(WHITE, sk, CLARET))


def girl_summer(sk=SKINS[2]):
    return figure(hair_girl_back() + neck(sk) + slim_trousers() + shoes() + tunic() + crest(90, 88, 13) + hands(sk) + face(sk) + hair_girl())


def boy_pe(sk=SKINS[0]):
    return figure(neck(sk) + trousers(colour=CHARCOAL, top=170, stripe=GOLD) + shoes("#F2F2F2") + polo(skin=sk) + hands(sk, 166) + face(sk) + hair_boy())


def girl_pe_hijab(sk=SKINS[3]):
    return figure(neck(sk) + trousers(colour=CHARCOAL, top=170, stripe=GOLD) + shoes("#F2F2F2") + polo(skin=sk, long=True) + hands(sk) + hijab(CLARET, sk))


def girl_pe(sk=SKINS[2]):
    return figure(hair_girl_back() + neck(sk) + trousers(colour=CHARCOAL, top=170, stripe=GOLD) + shoes("#F2F2F2") + polo(skin=sk, long=True) + hands(sk) + face(sk) + hair_girl(band=GOLD))


def tie_pattern(stripe):
    return (f'<pattern id="tie-{stripe[1:]}" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(-40)">'
            f'<rect width="7" height="7" fill="{CLARET}"/><rect width="7" height="1.6" fill="{stripe}"/></pattern>')


DEFS = (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        f'<symbol id="crest" viewBox="0 0 100 104">{CREST_INNER}</symbol>'
        f'{tie_pattern(GOLD)}{tie_pattern(WHITE)}</defs></svg>')


def card(svg, title, who, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<article class="look"><div class="stage">{svg}</div><h3>{title}</h3><p class="who">{who}</p><ul>{lis}</ul></article>'


def big_tie(stripe, label, note):
    svg = (f'<svg viewBox="70 60 20 66" class="tiebig" aria-hidden="true">'
           f'<path d="M78.3 72 L81.7 72 L84.5 78 L83 118 L80 123 L77 118 L75.5 78 Z" fill="url(#tie-{stripe[1:]})"/>'
           f'<path d="M76.5 65.5 L83.5 65.5 L82.3 73 L77.7 73 Z" fill="{CLARET}"/></svg>')
    return f'<div class="detail">{svg}<div><h4>{label}</h4><p>{note}</p></div></div>'


winter = "".join([
    card(junior_boy_winter(), "Junior boys", "Grade 3 to 5", [
        "White cotton shirt", "Claret clip-on tie, gold stripe", "Claret V-neck sweater, gold tipping, crest", "Charcoal trousers, black shoes"]),
    card(junior_girl_winter(), "Junior girls", "Grade 3 to 5", [
        "White knee-length tunic, claret piping", "Claret V-neck sweater, gold tipping, crest", "Charcoal straight trousers", "Claret hairband"]),
    card(senior_boy_winter(), "Senior boys", "Grade 6 to 8", [
        "Claret blazer with embroidered crest", "White shirt, claret tie with gold stripe", "Charcoal trousers, black shoes"]),
    card(senior_girl_winter(), "Senior girls", "Grade 6 to 8 · shown with optional hijab", [
        "Claret blazer with embroidered crest", "White tunic, claret piping", "Charcoal straight trousers", "Optional hijab: claret with gold edge"]),
    card(olevel_boy_winter(), "O Level boys", "Grade 9 to 11", [
        "Claret blazer with <b>gold piping</b>", "Senior tie: claret with white stripe", "White shirt, charcoal trousers"]),
    card(olevel_girl_winter(), "O Level girls", "Grade 9 to 11 · shown without hijab", [
        "Claret blazer with <b>gold piping</b>", "White tunic, claret piping", "Charcoal trousers, gold hairband"]),
])

summer = "".join([
    card(boy_summer(), "Boys", "All grades", [
        "White short-sleeve cotton shirt, crest on pocket", "No tie, no blazer", "Charcoal trousers in lighter cotton-blend"]),
    card(girl_summer_hijab(), "Girls", "All grades · optional white hijab", [
        "White cotton-lawn tunic, long sleeves, crest", "Claret piping at neck and hem", "Optional hijab: white with claret edge"]),
    card(girl_summer(), "Girls", "All grades · without hijab", [
        "Same tunic and trousers", "Hair neatly tied, claret hairband", "Breathable fabrics only"]),
])

pe = "".join([
    card(boy_pe(), "Boys PE kit", "All grades", [
        "Claret polo, gold collar and chest band", "Charcoal track trousers, gold side stripe", "White trainers"]),
    card(girl_pe_hijab(), "Girls PE kit", "With optional sports hijab", [
        "Claret long-sleeve sports top, gold collar", "Charcoal track trousers, gold side stripe", "Optional jersey sports hijab in claret"]),
    card(girl_pe(), "Girls PE kit", "Without hijab", [
        "Same long-sleeve top and track trousers", "Gold hairband", "White trainers"]),
])

ties = big_tie(GOLD, "Junior and senior tie", "Claret with diagonal gold stripes. Clip-on for Grades 3 to 5.") + \
       big_tie(WHITE, "O Level tie", "Claret with white stripes. Earned on entering Grade 9, a visible step up.")

html = f'''<title>Adabury School Uniform</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Marcellus&family=Outfit:wght@300;400;500;600&display=swap">
<style>
/* Layout: a lookbook — principles, then winter / summer / PE runways of figure cards, then details, costs and the approval panel. */
:root{{
  --bg:#FAF8F5; --surface:#FFFFFF; --stage:#F3ECE4; --fg:#2A1418; --muted:#6F5F60; --line:#E6DEDA; --accent:#6E1F2F;
  --display:"Cormorant Garamond", Georgia, serif; --caps:"Marcellus", Georgia, serif; --sans:"Outfit","Segoe UI",system-ui,sans-serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --bg:#140C0E; --surface:#1E1416; --stage:#EFE7DE; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }} }}
:root[data-theme="dark"]{{ --bg:#140C0E; --surface:#1E1416; --stage:#EFE7DE; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16px;line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 72px;display:flex;flex-direction:column;gap:60px}}
.eyebrow{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:var(--display);font-weight:600;font-size:clamp(38px,6vw,60px);line-height:1.02;margin:6px 0 10px}}
h2{{font-family:var(--display);font-weight:600;font-size:34px;margin:0}}
.lede{{color:var(--muted);max-width:66ch;margin:0}}
.shead{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 16px;margin-bottom:6px}}
.season{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:500}}
section > .lede{{margin-bottom:22px}}
.principles{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.pr{{border-top:2px solid var(--accent);padding-top:12px}}
.pr h3{{margin:0 0 4px;font-size:16px;font-weight:500}}
.pr p{{margin:0;font-size:14px;color:var(--muted)}}
.runway{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}
.runway.three{{grid-template-columns:repeat(3,1fr);max-width:760px}}
.look{{display:grid;grid-template-rows:auto auto auto 1fr;gap:4px;min-width:0}}
.stage{{background:var(--stage);border-radius:6px;padding:18px 8px 10px;display:flex;justify-content:center}}
.fig{{width:100%;max-width:150px;height:auto}}
.look h3{{margin:10px 0 0;font-size:16px;font-weight:500}}
.who{{margin:0;font-size:12.5px;color:var(--accent)}}
.look ul{{margin:6px 0 0;padding-left:16px;font-size:13.5px;color:var(--muted);display:grid;gap:3px}}
.details{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.detail{{display:flex;gap:16px;align-items:center;border:1px solid var(--line);border-radius:6px;background:var(--surface);padding:18px;min-width:0}}
.detail h4{{margin:0 0 4px;font-size:15px;font-weight:500}}
.detail p{{margin:0;font-size:13.5px;color:var(--muted)}}
.tiebig{{width:40px;height:132px;flex:none}}
.crestbig{{width:64px;height:67px;flex:none}}
.hj{{display:flex;gap:6px;flex:none}}
.hj i{{width:26px;height:40px;border-radius:13px 13px 6px 6px;border:1px solid var(--line)}}
.fabrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.fab{{border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--surface)}}
.fab .sw{{height:70px}}
.fab .m{{padding:12px 14px;display:grid;gap:3px;font-size:13.5px}}
.fab b{{font-weight:500;font-size:14.5px}} .fab span{{color:var(--muted)}}
.calendar{{display:grid;grid-template-columns:repeat(12,1fr);gap:3px;margin-top:6px}}
.calendar div{{padding:8px 2px;text-align:center;font-size:11.5px;border-radius:3px;font-variant-numeric:tabular-nums}}
.calendar .w{{background:#6E1F2F;color:#F5EEE6}} .calendar .s{{background:#F3ECE4;color:#2A1418}} .calendar .t{{background:#C2A15A;color:#2A1418}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--muted);margin-top:10px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:-1px;margin-right:6px}}
.costs{{border:1px solid var(--line);border-radius:6px;overflow-x:auto;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;min-width:560px;font-size:14px}}
th,td{{padding:10px 16px;border-bottom:1px solid var(--line);text-align:left}}
th{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
tr.tot td{{font-weight:600;border-bottom:none}}
.note{{font-size:13px;color:var(--muted);max-width:80ch;margin:12px 0 0}}
.decide{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:28px max(20px,3vw);display:grid;gap:12px}}
.decide ol{{margin:0;padding-left:1.2em;display:grid;gap:8px;max-width:76ch}}
@media (max-width:1000px){{ .runway{{grid-template-columns:repeat(3,1fr)}} .principles,.fabrics{{grid-template-columns:1fr 1fr}} .details{{grid-template-columns:1fr}} }}
@media (max-width:560px){{ .runway,.runway.three{{grid-template-columns:1fr 1fr}} .principles,.fabrics{{grid-template-columns:1fr}} }}
</style>
{DEFS}
<div class="wrap">
  <header>
    <span class="eyebrow">Adabury School · Design system · Uniform proposal</span>
    <h1>The Adabury uniform</h1>
    <p class="lede">A claret-and-white uniform that looks like a leading Cambridge school, keeps every child modestly dressed, and is comfortable in Faisalabad's heat. The hijab is offered in official school colours and is optional.</p>
  </header>

  <section aria-label="Principles">
    <div class="principles">
      <div class="pr"><h3>Modest by design</h3><p>Long sleeves for girls in every season, knee-length tunics over straight trousers, and loose cuts for everyone. Modesty is built into the garments, not added on top.</p></div>
      <div class="pr"><h3>Hijab: offered, not imposed</h3><p>Official hijabs in claret and white so girls who wear one look fully part of the uniform. No girl is required to wear it.</p></div>
      <div class="pr"><h3>Made for 45 °C</h3><p>Cotton next to the skin, no blazer or tie in summer, and lighter fabrics from April to October.</p></div>
      <div class="pr"><h3>Made in Faisalabad</h3><p>Shirting and tunic fabric from Faisalabad mills: a local story for parents, and easier reordering.</p></div>
    </div>
  </section>

  <section aria-labelledby="w">
    <div class="shead"><h2 id="w">Winter uniform</h2><span class="season">1 November to 31 March</span></div>
    <p class="lede">Juniors wear the claret sweater. The blazer marks the move to senior school in Grade 6. O Level students earn gold piping and the senior tie, a visible sign of progress that children look forward to.</p>
    <div class="runway">{winter}</div>
  </section>

  <section aria-labelledby="s">
    <div class="shead"><h2 id="s">Summer uniform</h2><span class="season">1 April to 31 October</span></div>
    <p class="lede">White and claret only, with the crest on every top. No blazer, sweater or tie. Girls keep long sleeves in light cotton lawn.</p>
    <div class="runway three">{summer}</div>
  </section>

  <section aria-labelledby="p">
    <div class="shead"><h2 id="p">PE and sports kit</h2><span class="season">All year, on PE days</span></div>
    <p class="lede">Full-length track trousers for everyone and a long-sleeve top for girls, so modest dress never stops a child from playing sport.</p>
    <div class="runway three">{pe}</div>
  </section>

  <section aria-labelledby="d">
    <h2 id="d">Details</h2>
    <p class="lede">The small items that make the uniform look premium and hard to copy.</p>
    <div class="details">
      {ties}
      <div class="detail"><svg viewBox="0 0 100 104" class="crestbig" aria-hidden="true"><use href="#crest"/></svg><div><h4>Embroidered crest</h4><p>Gold and claret thread on the blazer pocket (65 mm tall), smaller on sweaters, shirts and PE tops.</p></div></div>
      <div class="detail"><div class="hj"><i style="background:#6E1F2F;box-shadow:inset 0 -4px 0 #C2A15A"></i><i style="background:#FBFAF7;box-shadow:inset 0 -4px 0 #6E1F2F"></i></div><div><h4>Official hijabs (optional)</h4><p>Winter: claret with a gold edge. Summer: white with a claret edge. PE: claret jersey, pull-on.</p></div></div>
      <div class="detail"><svg viewBox="40 55 80 50" style="width:80px;height:50px;flex:none" aria-hidden="true"><path d="M53 66 Q66 62 72 64 L80 94 L88 64 Q94 62 107 66 L109 104 L51 104 Z" fill="#6E1F2F"/><path d="M72 64 L80 94 L88 64" fill="none" stroke="#C2A15A" stroke-width="2"/></svg><div><h4>Gold tipping</h4><p>A thin gold line on sweater necks, cuffs and hems: a detail that market copies rarely get right.</p></div></div>
      <div class="detail"><svg viewBox="0 0 60 40" style="width:60px;height:40px;flex:none" aria-hidden="true"><rect width="60" height="40" rx="4" fill="#6E1F2F"/><path d="M0 34 H60" stroke="#C2A15A" stroke-width="3"/><use href="#crest" x="22" y="6" width="16" height="17"/></svg><div><h4>School bag</h4><p>Claret backpack with crest and a gold band. Optional, but it makes children recognisable on the street.</p></div></div>
    </div>
  </section>

  <section aria-labelledby="f">
    <h2 id="f">Fabrics and colours</h2>
    <p class="lede">Every colour matches the official logo palette.</p>
    <div class="fabrics">
      <div class="fab"><div class="sw" style="background:#6E1F2F"></div><div class="m"><b>Blazer and sweater</b><span>Adabury Claret #6E1F2F</span><span>Poly-viscose suiting (cooler and easier to wash than wool); acrylic-cotton knit for sweaters</span></div></div>
      <div class="fab"><div class="sw" style="background:#FBFAF7;border-bottom:1px solid var(--line)"></div><div class="m"><b>Shirts and tunics</b><span>White</span><span>100% cotton, Faisalabad mill. Winter: cotton twill. Summer: cotton lawn.</span></div></div>
      <div class="fab"><div class="sw" style="background:#3E4249"></div><div class="m"><b>Trousers</b><span>Charcoal #3E4249</span><span>Poly-cotton twill, hides dust better than black or grey</span></div></div>
      <div class="fab"><div class="sw" style="background:#C2A15A"></div><div class="m"><b>Trims</b><span>Old Gold #C2A15A</span><span>Tie stripes, tipping, piping, PE collars. Never a main colour.</span></div></div>
    </div>
    <div class="calendar" aria-label="Uniform calendar">
      <div class="w">Jan</div><div class="w">Feb</div><div class="t">Mar</div><div class="s">Apr</div><div class="s">May</div><div class="s">Jun</div><div class="s">Jul</div><div class="s">Aug</div><div class="s">Sep</div><div class="s">Oct</div><div class="t">Nov</div><div class="w">Dec</div>
    </div>
    <div class="legend"><span><i style="background:#6E1F2F"></i>Winter, blazer or sweater required</span><span><i style="background:#C2A15A"></i>Winter, blazer optional (changeover month)</span><span><i style="background:#F3ECE4;border:1px solid var(--line)"></i>Summer</span></div>
  </section>

  <section aria-labelledby="c">
    <h2 id="c">Estimated cost per child</h2>
    <p class="lede">Rough Faisalabad market estimates for planning only. Real prices come from supplier quotes, which I will include in the financial model.</p>
    <div class="costs"><table>
      <thead><tr><th>Item</th><th>Qty per year</th><th class="n">Est. PKR each</th><th class="n">Est. PKR total</th></tr></thead>
      <tbody>
        <tr><td>Blazer (Grade 6+) or sweater (Grade 3–5)</td><td>1</td><td class="n">3,000–7,500</td><td class="n">3,000–7,500</td></tr>
        <tr><td>White shirts or tunics</td><td>3</td><td class="n">1,300–2,000</td><td class="n">3,900–6,000</td></tr>
        <tr><td>Trousers</td><td>2</td><td class="n">1,500–2,200</td><td class="n">3,000–4,400</td></tr>
        <tr><td>Tie</td><td>1</td><td class="n">500–800</td><td class="n">500–800</td></tr>
        <tr><td>PE kit (top and track trousers)</td><td>1</td><td class="n">3,000–4,500</td><td class="n">3,000–4,500</td></tr>
        <tr><td>Hijab (optional)</td><td>2</td><td class="n">600–900</td><td class="n">1,200–1,800</td></tr>
        <tr class="tot"><td>Full set, excluding shoes and bag</td><td></td><td class="n"></td><td class="n">13,400–25,000</td></tr>
      </tbody>
    </table></div>
    <p class="note">Selling uniforms through one appointed supplier (or a school shop) keeps quality consistent and can add a small margin to school income. I will model both options in the financial feasibility.</p>
  </section>

  <section class="decide" aria-labelledby="ap">
    <h2 id="ap">Your approval</h2>
    <ol>
      <li><b>Overall direction</b>: claret and white, with sweaters for juniors, a blazer from Grade 6 and gold piping for O Level. Approve or change?</li>
      <li><b>Girls</b>: knee-length tunic over straight trousers, long sleeves all year. Would you prefer a longer tunic (to mid-calf) or a different cut?</li>
      <li><b>Hijab</b>: optional, in official colours. Keep it optional, or make it compulsory from a certain grade?</li>
      <li><b>Trousers</b>: charcoal, or would you prefer claret, navy or grey?</li>
      <li><b>Sections</b>: will boys and girls study together in all grades, or separately from a certain grade? This affects the uniform and the campus plan.</li>
    </ol>
  </section>
</div>
'''
(ROOT / "adabury-uniform.html").write_text(html)
print("wrote", ROOT / "adabury-uniform.html", len(html))
