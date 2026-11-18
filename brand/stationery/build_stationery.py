#!/usr/bin/env python3
"""Build the Adabury School stationery proposal page (brand/adabury-stationery.html).

Every piece is drawn at its true print proportions in millimetres (scaled with container
query units), using the official outlined logo SVGs from brand/logo/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "logo"


def svg(name, cls="art", strip_ids_suffix=""):
    s = (LOGO / name).read_text()
    s = re.sub(r'width="\d+" height="\d+"', "", s, count=1)
    s = s.replace('role="img"', f'role="img" class="{cls}"')
    if strip_ids_suffix:  # make mask ids unique when a mono file is inlined twice
        s = re.sub(r'id="(\w+)"', rf'id="\1{strip_ids_suffix}"', s)
        s = re.sub(r'url\(#(\w+)\)', rf'url(#\1{strip_ids_suffix})', s)
    return s


H = svg("adabury-logo-horizontal.svg")
H_REV = svg("adabury-logo-horizontal-reverse.svg")
CREST = svg("adabury-crest.svg")
CREST_REV = svg("adabury-crest-reverse.svg")
PRIMARY = svg("adabury-logo-primary.svg")
PRIMARY_CLARET = svg("adabury-logo-primary-on-claret.svg")
WATERMARK = svg("adabury-crest.svg", "wm")

# Placeholder contact details: to be replaced with the real campus details.
ADDR = "[Campus address], Faisalabad"
PHONE = "+92 41 [number]"
WEB = "adabury.edu.pk"
MAIL = "info@adabury.edu.pk"

QR = "".join(
    f'<rect x="{x}" y="{y}" width="1" height="1"/>'
    for y in range(21) for x in range(21)
    if ((x < 7 and y < 7) or (x > 13 and y < 7) or (x < 7 and y > 13))
    and (x in (0, 6, 14, 20) or y in (0, 6, 14, 20) or (2 <= x % 14 <= 4 and 2 <= y % 14 <= 4))
    or (7 <= x <= 13 or 7 <= y <= 13) and ((x * 7 + y * 13 + x * y) % 5 < 2)
)
QR_SVG = f'<svg viewBox="-1 -1 23 23" class="qr" aria-hidden="true"><rect x="-1" y="-1" width="23" height="23" fill="#fff"/><g fill="#2A1418">{QR}</g></svg>'

PERSON = ('<svg viewBox="0 0 60 72" class="photo" aria-hidden="true"><rect width="60" height="72" fill="#EDE6DF"/>'
          '<path d="M30 10 C18 10 14 20 14 30 C14 40 17 46 10 56 Q30 70 50 56 C43 46 46 40 46 30 C46 20 42 10 30 10 Z" fill="#6E1F2F"/>'
          '<ellipse cx="30" cy="31" rx="9" ry="11" fill="#C9A385"/>'
          '<path d="M6 72 Q8 58 30 56 Q52 58 54 72 Z" fill="#6E1F2F"/></svg>')

CHARACTER = [
    ("Adab", "Good manners and respect", "Excellent"),
    ("Amanah", "Honesty and trustworthiness", "Excellent"),
    ("Ihsan", "Doing every task beautifully", "Very good"),
    ("Sabr", "Patience and self-control", "Good"),
    ("Shukr", "Gratitude", "Very good"),
    ("Khidmah", "Service to others", "Very good"),
]
SUBJECTS = [
    ("English Language", "88", "A"), ("Mathematics", "92", "A*"), ("Science", "84", "A"),
    ("Urdu", "79", "B"), ("Islamiyat", "90", "A*"), ("Pakistan Studies", "81", "A"),
    ("Computing", "86", "A"), ("Arabic", "74", "B"),
]
subj_rows = "".join(f"<tr><td>{s}</td><td class='n'>{m}</td><td class='n'><b>{g}</b></td></tr>" for s, m, g in SUBJECTS)
char_rows = "".join(f"<tr><td><b>{v}</b></td><td>{d}</td><td>{r}</td></tr>" for v, d, r in CHARACTER)

html = f'''<title>Adabury School Stationery</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Marcellus&family=Outfit:wght@300;400;500;600&family=Noto+Nastaliq+Urdu:wght@500&display=swap">
<style>
/* Layout: a print-desk presentation — each piece at true proportions on a soft ground, with a short spec beside it, then the approval panel. */
:root{{
  --bg:#EFEAE5; --surface:#FFFFFF; --fg:#2A1418; --muted:#6F5F60; --line:#DDD3CE; --accent:#6E1F2F;
  --claret:#6E1F2F; --gold:#C2A15A; --linen:#F5EEE6; --ink:#2A1418;
  --display:"Cormorant Garamond", Georgia, serif; --caps:"Marcellus", Georgia, serif;
  --sans:"Outfit","Segoe UI",system-ui,sans-serif; --urdu:"Noto Nastaliq Urdu","Noto Naskh Arabic",serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --bg:#1A1113; --surface:#241A1C; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }} }}
:root[data-theme="dark"]{{ --bg:#1A1113; --surface:#241A1C; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16px;line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 72px;display:flex;flex-direction:column;gap:64px}}
.eyebrow{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:var(--display);font-weight:600;font-size:clamp(38px,6vw,60px);line-height:1.02;margin:6px 0 10px}}
h2{{font-family:var(--display);font-weight:600;font-size:32px;margin:0 0 4px}}
.lede{{color:var(--muted);max-width:68ch;margin:0}}
.item{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:32px;align-items:start}}
.spec{{display:grid;gap:10px;position:sticky;top:20px}}
.spec dl{{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:6px 0 0;font-size:14px}}
.spec dt{{color:var(--muted)}} .spec dd{{margin:0}}
.spec p{{margin:0;font-size:14.5px;color:var(--muted)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}

/* ---- paper ---- */
.sheet{{container-type:inline-size;width:100%}}
.paper{{--mm:calc(100cqw / var(--w));position:relative;width:100%;aspect-ratio:var(--w)/var(--h);background:#FFFFFF;color:#2A1418;
  box-shadow:0 1px 2px rgba(42,20,24,.12),0 12px 28px rgba(42,20,24,.14);overflow:hidden;font-size:calc(var(--mm)*3.3);line-height:1.45}}
.paper .art{{display:block;width:100%;height:auto}}
.a4{{--w:210;--h:297}} .a4l{{--w:297;--h:210}} .bc{{--w:89;--h:51}} .id{{--w:54;--h:85.6}} .dl{{--w:220;--h:110}}

/* letterhead */
.lh .top{{position:absolute;left:calc(var(--mm)*18);right:calc(var(--mm)*18);top:calc(var(--mm)*14);display:flex;justify-content:space-between;align-items:flex-start}}
.lh .top .art{{width:calc(var(--mm)*72)}}
.lh .contact{{text-align:right;font-size:calc(var(--mm)*2.7);color:#6F5F60;line-height:1.6}}
.lh .rule{{position:absolute;left:calc(var(--mm)*18);right:calc(var(--mm)*18);top:calc(var(--mm)*42);height:calc(var(--mm)*.6);background:var(--claret)}}
.lh .rule::after{{content:"";position:absolute;left:0;right:0;top:calc(var(--mm)*1.2);height:calc(var(--mm)*.25);background:var(--gold)}}
.lh .wm{{position:absolute;width:calc(var(--mm)*120);left:calc(var(--mm)*45);top:calc(var(--mm)*95);opacity:.045}}
.lh .body{{position:absolute;left:calc(var(--mm)*22);right:calc(var(--mm)*22);top:calc(var(--mm)*54);font-size:calc(var(--mm)*3.2)}}
.lh .body p{{margin:0 0 calc(var(--mm)*3.2)}}
.lh .ref{{display:flex;justify-content:space-between;color:#6F5F60;font-size:calc(var(--mm)*2.8);margin-bottom:calc(var(--mm)*8)!important}}
.lh .subj{{font-weight:600;color:var(--claret)}}
.lh .sig{{margin-top:calc(var(--mm)*12)!important;line-height:1.35}}
.lh .sig b{{font-family:var(--display);font-size:calc(var(--mm)*4.4);font-weight:600}}
.lh .foot{{position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*20);background:var(--claret);color:#F5EEE6;display:flex;align-items:center;justify-content:space-between;padding:0 calc(var(--mm)*18)}}
.lh .foot::before{{content:"";position:absolute;left:0;right:0;top:0;height:calc(var(--mm)*1);background:var(--gold)}}
.lh .foot .m{{font-family:var(--caps);letter-spacing:.24em;font-size:calc(var(--mm)*2.8);color:#D7BB7A}}
.lh .foot .u{{font-family:var(--urdu);font-size:calc(var(--mm)*4.2);line-height:2;color:#F5EEE6}}
.lh .foot .a{{font-size:calc(var(--mm)*2.5);opacity:.85;text-align:right}}

/* business card */
.bc .front{{position:absolute;inset:0;background:var(--claret);display:flex;align-items:center;justify-content:center}}
.bc .front .art{{width:calc(var(--mm)*34)}}
.bc .front::after{{content:"";position:absolute;left:calc(var(--mm)*3);right:calc(var(--mm)*3);top:calc(var(--mm)*3);bottom:calc(var(--mm)*3);border:calc(var(--mm)*.25) solid rgba(201,169,98,.6)}}
.bc .back{{position:absolute;inset:0;padding:calc(var(--mm)*6) calc(var(--mm)*6);display:flex;flex-direction:column;justify-content:space-between}}
.bc .back .crest{{position:absolute;right:calc(var(--mm)*6);top:calc(var(--mm)*6);width:calc(var(--mm)*11)}}
.bc .nm{{font-family:var(--display);font-weight:600;font-size:calc(var(--mm)*5.4);line-height:1.1}}
.bc .tt{{font-size:calc(var(--mm)*2.7);color:var(--claret);letter-spacing:.08em;text-transform:uppercase;margin-top:calc(var(--mm)*1)}}
.bc .ct{{font-size:calc(var(--mm)*2.5);color:#4A3A3C;line-height:1.55}}
.bc .bar{{position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*1.6);background:var(--claret)}}
.bc .bar::before{{content:"";position:absolute;left:0;right:0;top:calc(var(--mm)*-.6);height:calc(var(--mm)*.6);background:var(--gold)}}

/* ID card */
.id .band{{position:absolute;left:0;right:0;top:0;height:calc(var(--mm)*17);background:var(--claret);display:flex;align-items:center;justify-content:center;padding:0 calc(var(--mm)*4)}}
.id .band .art{{width:calc(var(--mm)*40)}}
.id .band::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*.8);background:var(--gold)}}
.id .photo{{position:absolute;left:calc(var(--mm)*15.5);top:calc(var(--mm)*21);width:calc(var(--mm)*23);height:calc(var(--mm)*27.6);border:calc(var(--mm)*.6) solid var(--gold);border-radius:calc(var(--mm)*1)}}
.id .who{{position:absolute;left:0;right:0;top:calc(var(--mm)*51);text-align:center}}
.id .who .n{{font-family:var(--display);font-weight:600;font-size:calc(var(--mm)*4.4);line-height:1.1}}
.id .who .c{{font-size:calc(var(--mm)*2.4);color:var(--claret);letter-spacing:.1em;text-transform:uppercase;margin-top:calc(var(--mm)*.8)}}
.id .grid{{position:absolute;left:calc(var(--mm)*5);right:calc(var(--mm)*5);top:calc(var(--mm)*62);display:grid;grid-template-columns:1fr 1fr;gap:calc(var(--mm)*1) calc(var(--mm)*3);font-size:calc(var(--mm)*2.2)}}
.id .grid span{{color:#6F5F60;display:block;font-size:calc(var(--mm)*1.8);letter-spacing:.06em;text-transform:uppercase}}
.id .foot{{position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*8);background:var(--linen);display:flex;align-items:center;justify-content:space-between;padding:0 calc(var(--mm)*4);font-size:calc(var(--mm)*2)}}
.id .foot .yr{{font-family:var(--caps);letter-spacing:.12em;color:var(--claret)}}
.id .back{{position:absolute;inset:0;padding:calc(var(--mm)*5);display:flex;flex-direction:column;gap:calc(var(--mm)*2.2);font-size:calc(var(--mm)*2.2)}}
.id .back h4{{margin:0;font-family:var(--caps);letter-spacing:.14em;color:var(--claret);font-size:calc(var(--mm)*2.6);font-weight:400}}
.id .back ol{{margin:0;padding-left:calc(var(--mm)*3.5);display:grid;gap:calc(var(--mm)*.6)}}
.id .back .qr{{width:calc(var(--mm)*16);align-self:center}}
.id .back .ret{{margin-top:auto;border-top:calc(var(--mm)*.3) solid var(--gold);padding-top:calc(var(--mm)*1.5);text-align:center;color:#6F5F60}}
.id .back .crestwm{{position:absolute;width:calc(var(--mm)*30);left:calc(var(--mm)*12);top:calc(var(--mm)*26);opacity:.05}}

/* report card */
.rc .hd{{position:absolute;left:0;right:0;top:0;height:calc(var(--mm)*34);background:var(--claret);display:flex;align-items:center;justify-content:space-between;padding:0 calc(var(--mm)*14);color:#F5EEE6}}
.rc .hd::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*1);background:var(--gold)}}
.rc .hd .art{{width:calc(var(--mm)*66)}}
.rc .hd .t{{text-align:right}}
.rc .hd .t b{{display:block;font-family:var(--display);font-weight:600;font-size:calc(var(--mm)*7);line-height:1}}
.rc .hd .t span{{font-size:calc(var(--mm)*2.7);letter-spacing:.14em;text-transform:uppercase;color:#D7BB7A}}
.rc .in{{position:absolute;left:calc(var(--mm)*14);right:calc(var(--mm)*14);top:calc(var(--mm)*42);display:grid;gap:calc(var(--mm)*5)}}
.rc .stu{{display:grid;grid-template-columns:repeat(4,1fr);gap:calc(var(--mm)*2);font-size:calc(var(--mm)*2.9);background:var(--linen);padding:calc(var(--mm)*3.5) calc(var(--mm)*4)}}
.rc .stu span{{display:block;font-size:calc(var(--mm)*2.2);color:#6F5F60;letter-spacing:.08em;text-transform:uppercase}}
.rc h5{{margin:0 0 calc(var(--mm)*1.5);font-family:var(--caps);font-weight:400;letter-spacing:.16em;font-size:calc(var(--mm)*3.2);color:var(--claret);border-bottom:calc(var(--mm)*.4) solid var(--gold);padding-bottom:calc(var(--mm)*1)}}
.rc .cols{{display:grid;grid-template-columns:1fr 1fr;gap:calc(var(--mm)*6)}}
.rc table{{width:100%;border-collapse:collapse;font-size:calc(var(--mm)*3.1)}}
.rc td,.rc th{{padding:calc(var(--mm)*1.7) calc(var(--mm)*1);border-bottom:calc(var(--mm)*.2) solid #E6DEDA;text-align:left}}
.rc th{{font-weight:500;color:#6F5F60;font-size:calc(var(--mm)*2.3);letter-spacing:.06em;text-transform:uppercase}}
.rc .n{{text-align:right;font-variant-numeric:tabular-nums}}
.rc .quran{{display:grid;grid-template-columns:repeat(3,1fr);gap:calc(var(--mm)*2);font-size:calc(var(--mm)*2.8)}}
.rc .quran div{{border:calc(var(--mm)*.25) solid #E6DEDA;padding:calc(var(--mm)*2.6)}}
.rc .key{{font-size:calc(var(--mm)*2.3);color:#6F5F60;margin:calc(var(--mm)*1.5) 0 0}}
.rc .goals{{margin:0;padding-left:calc(var(--mm)*5);font-size:calc(var(--mm)*3);display:grid;gap:calc(var(--mm)*1)}}
.rc .quran span{{display:block;color:#6F5F60;font-size:calc(var(--mm)*2.2);text-transform:uppercase;letter-spacing:.06em}}
.rc .rem{{font-size:calc(var(--mm)*2.9);font-style:italic;font-family:var(--display);font-size:calc(var(--mm)*3.6);line-height:1.4;margin:0}}
.rc .sigs{{position:absolute;left:calc(var(--mm)*14);right:calc(var(--mm)*14);bottom:calc(var(--mm)*14);display:flex;justify-content:space-between;font-size:calc(var(--mm)*2.6);color:#6F5F60}}
.rc .sigs div{{border-top:calc(var(--mm)*.3) solid #2A1418;padding-top:calc(var(--mm)*1.2);width:calc(var(--mm)*50);text-align:center}}
.rc .sample{{position:absolute;right:calc(var(--mm)*14);bottom:calc(var(--mm)*5);font-size:calc(var(--mm)*2.2);color:#A0908F}}

/* certificate */
.ce{{background:#FFFDF9}}
.ce .b1{{position:absolute;inset:calc(var(--mm)*8);border:calc(var(--mm)*1.6) solid var(--claret)}}
.ce .b2{{position:absolute;inset:calc(var(--mm)*12);border:calc(var(--mm)*.4) solid var(--gold)}}
.ce .corner{{position:absolute;width:calc(var(--mm)*7);height:calc(var(--mm)*7);background:var(--gold);transform:rotate(45deg)}}
.ce .in{{position:absolute;inset:calc(var(--mm)*18);display:flex;flex-direction:column;align-items:center;text-align:center}}
.ce .in .art{{width:calc(var(--mm)*24)}}
.ce .sch{{font-family:var(--caps);letter-spacing:.3em;color:var(--claret);font-size:calc(var(--mm)*4.2);margin-top:calc(var(--mm)*2);padding-left:.3em}}
.ce .ttl{{font-family:var(--display);font-weight:600;font-size:calc(var(--mm)*13);line-height:1;margin-top:calc(var(--mm)*5);color:#2A1418}}
.ce .pres{{font-size:calc(var(--mm)*3.3);color:#6F5F60;margin-top:calc(var(--mm)*5);letter-spacing:.1em;text-transform:uppercase}}
.ce .nm{{font-family:var(--display);font-style:italic;font-weight:500;font-size:calc(var(--mm)*11);color:var(--claret);margin-top:calc(var(--mm)*2);border-bottom:calc(var(--mm)*.4) solid var(--gold);padding:0 calc(var(--mm)*14) calc(var(--mm)*1)}}
.ce .for{{font-size:calc(var(--mm)*3.6);max-width:calc(var(--mm)*170);margin-top:calc(var(--mm)*5);color:#2A1418}}
.ce .row{{position:absolute;left:calc(var(--mm)*34);right:calc(var(--mm)*34);bottom:calc(var(--mm)*24);display:flex;justify-content:space-between;align-items:flex-end;font-size:calc(var(--mm)*3)}}
.ce .row .s{{border-top:calc(var(--mm)*.3) solid #2A1418;width:calc(var(--mm)*62);padding-top:calc(var(--mm)*1.5);text-align:center;color:#6F5F60}}
.ce .seal{{width:calc(var(--mm)*30);height:calc(var(--mm)*30);border-radius:50%;background:radial-gradient(circle at 35% 30%,#E2C77E,#B48E43 70%);display:grid;place-items:center;box-shadow:0 0 0 calc(var(--mm)*1) #fff,0 0 0 calc(var(--mm)*1.5) #B48E43}}
.ce .seal .art{{width:calc(var(--mm)*14)}}

/* envelope */
.dlp .flap{{position:absolute;left:0;right:0;top:0;height:calc(var(--mm)*7);background:var(--claret)}}
.dlp .flap::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:calc(var(--mm)*.6);background:var(--gold)}}
.dlp .from{{position:absolute;left:calc(var(--mm)*12);top:calc(var(--mm)*16)}}
.dlp .from .art{{width:calc(var(--mm)*62)}}
.dlp .from p{{margin:calc(var(--mm)*2) 0 0;font-size:calc(var(--mm)*2.6);color:#6F5F60}}
.dlp .to{{position:absolute;left:calc(var(--mm)*110);top:calc(var(--mm)*58);font-size:calc(var(--mm)*3.6);line-height:1.6;color:#2A1418}}
.dlp .to span{{display:block;color:#A0908F;font-size:calc(var(--mm)*2.6);letter-spacing:.1em;text-transform:uppercase}}
.dlp .stamp{{position:absolute;right:calc(var(--mm)*12);top:calc(var(--mm)*16);width:calc(var(--mm)*22);height:calc(var(--mm)*26);border:calc(var(--mm)*.4) dashed #C9B9B5;display:grid;place-items:center;color:#B8A8A5;font-size:calc(var(--mm)*2.2)}}

.note{{font-size:13px;color:var(--muted);max-width:84ch;margin:0}}
.decide{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:28px max(20px,3vw);display:grid;gap:12px}}
.decide ol{{margin:0;padding-left:1.2em;display:grid;gap:8px;max-width:78ch}}
@media (max-width:900px){{ .item{{grid-template-columns:1fr}} .spec{{position:static}} }}
@media (max-width:520px){{ .pair{{grid-template-columns:1fr}} }}
</style>

<div class="wrap">
  <header>
    <span class="eyebrow">Adabury School · Design system · Stationery proposal</span>
    <h1>Adabury stationery</h1>
    <p class="lede">Seven core pieces, each shown at its real print proportions with the official logo, colours and fonts. Every piece shares the same claret band and thin gold line, so parents recognise an Adabury document before they read it.</p>
  </header>

  <section class="item" aria-labelledby="s1">
    <div class="sheet"><div class="paper a4 lh">
      {WATERMARK}
      <div class="top">{H}<div class="contact">{ADDR}<br>{PHONE}<br>{MAIL}<br>{WEB}</div></div>
      <div class="rule"></div>
      <div class="body">
        <p class="ref"><span>Ref: ADB/ADM/2027/0142</span><span>12 March 2027</span></p>
        <p>Dear [Parent name],</p>
        <p class="subj">Confirmation of admission: Grade 6, Session 2027–28</p>
        <p>Assalamu alaikum. We are delighted to confirm your child's admission to Adabury School. Our first term begins on 1 April 2027, and an orientation morning for parents will be held on 27 March.</p>
        <p>Please find enclosed the fee schedule, the uniform list and the parent handbook. Our admissions office is happy to answer any questions.</p>
        <p>We look forward to welcoming your family to Adabury.</p>
        <p class="sig">Warm regards,<br><b>[Name]</b><br>Principal, Adabury School</p>
      </div>
      <div class="foot"><span class="m">ADAB · ILM · IHSAN</span><span class="u" lang="ur" dir="rtl">ادبری اسکول</span><span class="a">{ADDR}<br>{WEB}</span></div>
    </div></div>
    <div class="spec">
      <h2 id="s1">1 · Letterhead</h2>
      <p>For admission letters, circulars, official correspondence. A faint crest watermark sits behind the text; the footer carries the motto and the Urdu name.</p>
      <dl><dt>Size</dt><dd>A4 (210 × 297 mm)</dd><dt>Paper</dt><dd>100 gsm white bond; also a Word template for daily use</dd><dt>Print</dt><dd>Claret + gold (2 spot colours) or full colour</dd></dl>
    </div>
  </section>

  <section class="item" aria-labelledby="s2">
    <div class="pair">
      <div class="sheet"><div class="paper bc"><div class="front">{PRIMARY_CLARET.replace('class="art"','class="art" style="width:auto;height:84%"')}</div></div></div>
      <div class="sheet"><div class="paper bc"><div class="back">
        <div class="crest-wrap">{CREST.replace('class="art"','class="art crest"')}</div>
        <div><div class="nm">[Full name]</div><div class="tt">Principal</div></div>
        <div class="ct">{PHONE}<br>[name]@adabury.edu.pk<br>{ADDR}</div>
        <div class="bar"></div>
      </div></div></div>
    </div>
    <div class="spec">
      <h2 id="s2">2 · Business card</h2>
      <p>Claret front with the full logo; white back with name, role and contact details. The same design is used for the principal, coordinators and admissions staff.</p>
      <dl><dt>Size</dt><dd>89 × 51 mm (standard Pakistan size)</dd><dt>Paper</dt><dd>350 gsm matt, soft-touch lamination</dd><dt>Finish</dt><dd>Gold foil on the front logo (optional)</dd></dl>
    </div>
  </section>

  <section class="item" aria-labelledby="s3">
    <div class="pair" style="max-width:520px">
      <div class="sheet"><div class="paper id">
        <div class="band">{H_REV}</div>
        {PERSON}
        <div class="who"><div class="n">[Student name]</div><div class="c">Grade 6 · Section B</div></div>
        <div class="grid"><div><span>GR No.</span>ADB-27-0142</div><div><span>Blood group</span>B+</div><div><span>House</span>[House]</div><div><span>Valid until</span>31 Mar 2028</div></div>
        <div class="foot"><span class="yr">SESSION 2027–28</span><span>{WEB}</span></div>
      </div></div>
      <div class="sheet"><div class="paper id"><div class="back">
        {CREST.replace('class="art"','class="art crestwm"')}
        <h4>SCHOOL RULES</h4>
        <ol><li>Wear this card at all times on campus.</li><li>The card is not transferable.</li><li>Report a lost card to the front office.</li></ol>
        <h4>EMERGENCY CONTACT</h4>
        <div>[Parent name]<br>[Mobile number]</div>
        {QR_SVG}
        <div class="ret">If found, please return to<br>Adabury School, {ADDR}<br>{PHONE}</div>
      </div></div></div>
    </div>
    <div class="spec">
      <h2 id="s3">3 · Student ID card</h2>
      <p>Portrait card with photo, GR number, blood group and house. The QR code on the back links to the student's record for gate attendance and van pick-up.</p>
      <dl><dt>Size</dt><dd>CR80 (54 × 85.6 mm), PVC</dd><dt>Print</dt><dd>Full colour both sides, printed in-house on a card printer</dd><dt>Lanyard</dt><dd>Claret with gold "ADABURY" text</dd></dl>
      <p>Staff cards use the same design, with a gold band instead of claret.</p>
    </div>
  </section>

  <section class="item" aria-labelledby="s4">
    <div class="sheet"><div class="paper a4 rc">
      <div class="hd">{H_REV}<div class="t"><b>Progress Report</b><span>Term 1 · 2027–28</span></div></div>
      <div class="in">
        <div class="stu"><div><span>Student</span>[Student name]</div><div><span>Grade</span>6 B</div><div><span>GR No.</span>ADB-27-0142</div><div><span>Attendance</span>96%</div></div>
        <div class="cols">
          <div><h5>ACADEMIC ACHIEVEMENT</h5><table><thead><tr><th>Subject</th><th class="n">%</th><th class="n">Grade</th></tr></thead><tbody>{subj_rows}</tbody></table></div>
          <div><h5>THE ADABURY CHARACTER RECORD</h5><table><thead><tr><th>Value</th><th>Meaning</th><th>Rating</th></tr></thead><tbody>{char_rows}</tbody></table></div>
        </div>
        <div><h5>QURAN AND ISLAMIC LEARNING</h5><div class="quran"><div><span>Nazra / Tajweed</span>Para 12 · Very good</div><div><span>Memorisation</span>Surah Al-Mulk complete</div><div><span>Daily duas and Seerah</span>Excellent</div></div></div>
        <div class="cols">
          <div><h5>CO-CURRICULAR AND HOUSE</h5><table><tbody><tr><td>Debating society</td><td>Inter-house finalist</td></tr><tr><td>Football</td><td>Junior team</td></tr><tr><td>Community service</td><td>6 hours</td></tr><tr><td>House points earned</td><td class="n">48</td></tr></tbody></table></div>
          <div><h5>GOALS FOR NEXT TERM</h5><ol class="goals"><li>Read one Urdu book each fortnight.</li><li>Complete Para 13 with Tajweed.</li><li>Lead one class assembly.</li></ol><p class="key">Character ratings: Excellent · Very good · Good · Developing</p></div>
        </div>
        <div><h5>CLASS TEACHER'S REMARKS</h5><p class="rem">"[Student name] is courteous and hard-working, and shows real kindness to younger pupils. Keep reading every evening to strengthen Urdu."</p></div>
      </div>
      <div class="sigs"><div>Class teacher</div><div>Principal</div><div>Parent</div></div>
      <div class="sample">Sample data for layout only</div>
    </div></div>
    <div class="spec">
      <h2 id="s4">4 · Report card</h2>
      <p>The report card is where the brand promise becomes visible to parents. Academic grades sit <b>side by side</b> with the <b>Adabury Character Record</b>, six values rated every term, followed by Quran and Islamic learning.</p>
      <dl><dt>Size</dt><dd>A4, printed or PDF from the school system</dd><dt>Grades</dt><dd>Cambridge-style A* to E</dd><dt>Values</dt><dd>Adab, Amanah, Ihsan, Sabr, Shukr, Khidmah</dd></dl>
      <p>The six values are a proposal for the academic model step, where we will finalise them.</p>
    </div>
  </section>

  <section class="item" aria-labelledby="s5">
    <div class="sheet"><div class="paper a4l ce">
      <div class="b1"></div><div class="b2"></div>
      <div class="corner" style="left:calc(var(--mm)*8.5);top:calc(var(--mm)*8.5);transform:translate(-50%,-50%) rotate(45deg)"></div>
      <div class="corner" style="right:calc(var(--mm)*8.5);top:calc(var(--mm)*8.5);transform:translate(50%,-50%) rotate(45deg)"></div>
      <div class="corner" style="left:calc(var(--mm)*8.5);bottom:calc(var(--mm)*8.5);transform:translate(-50%,50%) rotate(45deg)"></div>
      <div class="corner" style="right:calc(var(--mm)*8.5);bottom:calc(var(--mm)*8.5);transform:translate(50%,50%) rotate(45deg)"></div>
      <div class="in">
        {CREST}
        <div class="sch">ADABURY SCHOOL</div>
        <div class="ttl">Certificate of Excellence</div>
        <div class="pres">This certificate is proudly presented to</div>
        <div class="nm">[Student name]</div>
        <div class="for">for outstanding achievement in Mathematics and exemplary Adab throughout the academic session 2027–28.</div>
      </div>
      <div class="row"><div class="s">Class teacher</div><div class="seal">{CREST_REV}</div><div class="s">Principal</div></div>
    </div></div>
    <div class="spec">
      <h2 id="s5">5 · Certificate</h2>
      <p>One master design for every award: academic excellence, Hifz milestones, sports, character awards and graduation. Only the title and citation change.</p>
      <dl><dt>Size</dt><dd>A4 landscape</dd><dt>Paper</dt><dd>300 gsm textured ivory</dd><dt>Finish</dt><dd>Gold foil seal and border (optional)</dd></dl>
    </div>
  </section>

  <section class="item" aria-labelledby="s6">
    <div class="sheet"><div class="paper dl dlp">
      <div class="flap"></div>
      <div class="from">{H}<p>{ADDR}</p></div>
      <div class="stamp">Stamp</div>
      <div class="to"><span>To</span>[Parent name]<br>[Address line]<br>Faisalabad</div>
    </div></div>
    <div class="spec">
      <h2 id="s6">6 · Envelope</h2>
      <p>For admission letters and official mail. The claret flap edge carries the brand even when the envelope is seen from the back.</p>
      <dl><dt>Size</dt><dd>DL (220 × 110 mm); also A4 C4 for reports</dd><dt>Paper</dt><dd>100 gsm white, peel-and-seal</dd></dl>
    </div>
  </section>

  <section class="item" aria-labelledby="s7">
    <div class="sheet"><div class="paper a4 lh" style="--h:99">
      <div class="top" style="top:calc(var(--mm)*12)">{H}<div class="contact">{PHONE}<br>{WEB}</div></div>
      <div class="rule" style="top:calc(var(--mm)*38)"></div>
      <div class="body" style="top:calc(var(--mm)*48)"><p style="font-family:var(--display);font-size:calc(var(--mm)*6);font-style:italic;color:var(--claret);margin:0">With compliments</p></div>
      <div class="foot" style="height:calc(var(--mm)*12)"><span class="m">ADAB · ILM · IHSAN</span><span class="u" lang="ur" dir="rtl" style="font-size:calc(var(--mm)*3.6)">ادبری اسکول</span><span class="a">{WEB}</span></div>
    </div></div>
    <div class="spec">
      <h2 id="s7">7 · Compliment slip</h2>
      <p>For notes sent with books, fee receipts, gifts and documents. A third of an A4 sheet.</p>
      <dl><dt>Size</dt><dd>210 × 99 mm</dd><dt>Paper</dt><dd>100 gsm, same as the letterhead</dd></dl>
    </div>
  </section>

  <p class="note">Names, addresses, phone numbers, the GR number and the report card figures are placeholders. The domain adabury.edu.pk is a proposal: a .edu.pk address needs PKNIC approval for a registered school, so we should also secure adabury.pk and a .com as backups.</p>

  <section class="decide" aria-labelledby="ap">
    <h2 id="ap">Your approval</h2>
    <ol>
      <li><b>Overall look</b>: claret band, thin gold line, crest watermark. Approve or change?</li>
      <li><b>Report card</b>: are the six character values right (Adab, Amanah, Ihsan, Sabr, Shukr, Khidmah), or would you like different ones?</li>
      <li><b>Contact details</b>: send me the campus address, phone number and the principal's name when ready, and I will fill them in.</li>
      <li><b>After approval</b>, I will produce print-ready PDF files for the printer and Word templates for the office.</li>
    </ol>
  </section>
</div>
'''
(ROOT / "adabury-stationery.html").write_text(html)
print("wrote", len(html))
