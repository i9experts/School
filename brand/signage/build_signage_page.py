#!/usr/bin/env python3
"""Build the Adabury signage proposal page (brand/adabury-signage.html)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def svg(name, style=""):
    s = (ROOT / "logo" / name).read_text()
    return re.sub(r'width="\d+" height="\d+"', f'style="{style}"', s, count=1)


CREST = svg("adabury-crest.svg", "height:100%;width:auto;display:block")
CREST_REV = svg("adabury-crest-reverse.svg", "height:100%;width:auto;display:block")

MOCKS = [
    ("01-main-gate", "Main gate", "Illuminated claret panel above the gate, with the crest, English and Urdu names.",
     "gate-sign", [("Size", "3.0 × 1.0 m panel"), ("Build", "ACP box, acrylic face, LED backlight"), ("Est. cost", "PKR 250,000–450,000")]),
    ("02-building-facade", "Building facade", "Gold-finish 3D letters and crest fixed straight onto the brick, with no backing panel.",
     "facade-letters", [("Size", "about 6 m wide, letters 45 cm tall"), ("Build", "Stainless steel, gold PVD finish, halo-lit"), ("Est. cost", "PKR 400,000–700,000")]),
    ("03-reception-wall", "Reception feature wall", "Claret wall with brushed-gold crest, name, motto and the Urdu tagline. The first thing every parent sees.",
     "reception-wall", [("Size", "2.4 × 1.5 m artwork"), ("Build", "Brushed brass-finish 3D letters on painted claret wall"), ("Est. cost", "PKR 150,000–300,000")]),
    ("04-school-van", "School van livery", "White van, claret lower band, gold line. Easy to spot at pick-up and seen across the city every day.",
     "van-livery", [("Size", "Both sides plus rear door"), ("Build", "Cast vinyl wrap, 5-year outdoor grade"), ("Est. cost", "PKR 35,000–60,000 per van")]),
    ("05-admissions-billboard", "Admissions billboard", "The launch hoarding: crest, 'Admissions open', grades, the Urdu tagline and the uniform photo.",
     "hoarding", [("Size", "40 × 20 ft standard"), ("Build", "Star-flex print on existing structure"), ("Est. cost", "Print PKR 40,000–70,000; site rent varies by road")]),
]

WAY = [
    ("Principal's Office", "پرنسپل آفس", "door"),
    ("Admissions", "شعبۂ داخلہ", "door"),
    ("Library", "کتب خانہ", "door"),
    ("Prayer Hall", "مصلیٰ", "door"),
    ("Grade 6 · B", "جماعت ششم", "door"),
    ("Science Lab", "سائنس لیب", "door"),
]


def plate(en, ur):
    return (f'<div class="plate"><div class="pc">{CREST_REV}</div><div class="pt"><b>{en}</b>'
            f'<span lang="ur" dir="rtl">{ur}</span></div></div>')


plates = "".join(plate(e, u) for e, u, _ in WAY)


def mock_block(m):
    fn, title, desc, art, spec = m
    rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in spec)
    return f'''
  <section class="sg" aria-label="{title}">
    <button type="button" class="ph" data-full="signage/mockups/web/{fn}.jpg"><img src="signage/mockups/web/{fn}.jpg" alt="{title}: realistic visualisation" width="1400" height="792" loading="lazy"></button>
    <div class="info">
      <h2>{title}</h2>
      <p>{desc}</p>
      <dl>{rows}</dl>
      <figure class="art"><img src="signage/artwork/web/{art}.jpg" alt="{title} print artwork" loading="lazy"><figcaption>Exact print artwork</figcaption></figure>
    </div>
  </section>'''


blocks = "".join(mock_block(m) for m in MOCKS)

html = f'''<title>Adabury School Signage</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Marcellus&family=Outfit:wght@300;400;500;600&family=Noto+Nastaliq+Urdu:wght@500;600&display=swap">
<style>
/* Layout: one signage item per band (large photo + spec column with its exact print artwork), then the wayfinding system, cost summary and approval. */
:root{{
  --bg:#FAF8F5; --surface:#FFFFFF; --fg:#2A1418; --muted:#6F5F60; --line:#E6DEDA; --accent:#6E1F2F;
  --display:"Cormorant Garamond", Georgia, serif; --caps:"Marcellus", Georgia, serif;
  --sans:"Outfit","Segoe UI",system-ui,sans-serif; --urdu:"Noto Nastaliq Urdu","Noto Naskh Arabic",serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --bg:#140C0E; --surface:#1E1416; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }} }}
:root[data-theme="dark"]{{ --bg:#140C0E; --surface:#1E1416; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; color-scheme:dark }}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16px;line-height:1.55}}
.wrap{{max-width:1240px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 72px;display:flex;flex-direction:column;gap:56px}}
.eyebrow{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:var(--display);font-weight:600;font-size:clamp(38px,6vw,60px);line-height:1.02;margin:6px 0 10px}}
h2{{font-family:var(--display);font-weight:600;font-size:32px;margin:0}}
.lede{{color:var(--muted);max-width:70ch;margin:0}}
.sg{{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:28px;align-items:start;border-top:1px solid var(--line);padding-top:28px}}
.ph{{all:unset;cursor:zoom-in;display:block;border-radius:8px;overflow:hidden}}
.ph:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
.ph img{{width:100%;height:auto;display:block}}
.info{{display:grid;gap:10px}}
.info p{{margin:0;color:var(--muted)}}
.info dl{{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:4px 0 0;font-size:14px}}
.info dt{{color:var(--muted)}} .info dd{{margin:0}}
.art{{margin:8px 0 0;display:grid;gap:6px}}
.art img{{width:100%;height:auto;display:block;border-radius:4px;border:1px solid var(--line)}}
.art figcaption{{font-size:12px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}}
.way{{display:grid;gap:18px}}
.plates{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.plate{{background:#6E1F2F;border-radius:6px;display:flex;align-items:center;gap:16px;padding:18px 20px;box-shadow:inset 0 -5px 0 #C9A962}}
.plate .pc{{height:56px;flex:none}}
.pt{{display:grid;gap:0;min-width:0}}
.pt b{{font-family:var(--caps);font-weight:400;color:#F5EEE6;font-size:19px;letter-spacing:.08em}}
.pt span{{font-family:var(--urdu);color:#D7BB7A;font-size:20px;line-height:1.9;text-align:left}}
.dir{{background:#FFFFFF;border:1px solid var(--line);border-radius:6px;overflow:hidden;display:grid;max-width:640px}}
.dir .hd{{background:#6E1F2F;display:flex;align-items:center;gap:12px;padding:10px 18px;box-shadow:inset 0 -4px 0 #C9A962}}
.dir .hd .c{{height:34px}}
.dir .hd span{{font-family:var(--caps);color:#F5EEE6;letter-spacing:.2em;font-size:15px}}
.dir .r{{display:grid;grid-template-columns:44px 1fr auto;align-items:center;gap:12px;padding:12px 18px;border-top:1px solid #EDE6E1;color:#2A1418}}
.dir .r i{{font-style:normal;font-size:26px;color:#6E1F2F;text-align:center}}
.dir .r b{{font-weight:500;font-size:17px}}
.dir .r span{{font-family:var(--urdu);color:#6E1F2F;font-size:19px;line-height:1.9}}
.costs{{border:1px solid var(--line);border-radius:6px;overflow-x:auto;background:var(--surface)}}
table{{border-collapse:collapse;width:100%;min-width:560px;font-size:14px}}
th,td{{padding:10px 16px;border-bottom:1px solid var(--line);text-align:left}}
th{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:500}}
td.n,th.n{{text-align:right;font-variant-numeric:tabular-nums}}
tr.tot td{{font-weight:600;border-bottom:none}}
.note{{font-size:13px;color:var(--muted);max-width:86ch;margin:12px 0 0}}
.decide{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:28px max(20px,3vw);display:grid;gap:12px}}
.decide ol{{margin:0;padding-left:1.2em;display:grid;gap:8px;max-width:78ch}}
dialog{{border:none;padding:0;background:transparent;max-width:96vw;max-height:94vh}}
dialog::backdrop{{background:rgba(20,10,12,.88)}}
dialog img{{max-width:100%;max-height:90vh;display:block;border-radius:6px}}
dialog .x{{position:absolute;top:8px;right:8px;background:rgba(0,0,0,.55);color:#fff;border:none;border-radius:99px;width:36px;height:36px;font-size:20px;cursor:pointer}}
@media (max-width:900px){{ .sg{{grid-template-columns:1fr}} .plates{{grid-template-columns:1fr 1fr}} }}
@media (max-width:520px){{ .plates{{grid-template-columns:1fr}} }}
</style>

<div class="wrap">
  <header>
    <span class="eyebrow">Adabury School · Design system · Signage proposal</span>
    <h1>Adabury signage</h1>
    <p class="lede">From the road to the classroom door, every sign uses the same claret, gold and crest, with English and Urdu side by side. Each photo below shows the exact print artwork placed in a realistic setting.</p>
  </header>
{blocks}

  <section class="way" aria-labelledby="w">
    <div><h2 id="w">Wayfinding inside the campus</h2>
    <p class="lede">Door plates and corridor signs in English and Urdu, so every parent and visitor finds their way. Claret plate, gold crest and a gold base line.</p></div>
    <div class="plates">{plates}</div>
    <div class="dir" aria-label="Corridor direction sign">
      <div class="hd"><div class="c">{CREST_REV}</div><span>GROUND FLOOR</span></div>
      <div class="r"><i>←</i><b>Reception · Admissions</b><span lang="ur" dir="rtl">استقبالیہ · داخلہ</span></div>
      <div class="r"><i>↑</i><b>Prayer Hall</b><span lang="ur" dir="rtl">مصلیٰ</span></div>
      <div class="r"><i>→</i><b>Library · Science Labs</b><span lang="ur" dir="rtl">کتب خانہ · لیبز</span></div>
    </div>
    <p class="note" style="margin:0">Door plates: 300 × 100 mm, claret acrylic with gold vinyl or engraved brass, about PKR 3,000–6,000 each.</p>
  </section>

  <section aria-labelledby="c">
    <h2 id="c">Estimated signage budget</h2>
    <p class="lede" style="margin-bottom:18px">Rough Faisalabad market estimates for planning. I will collect real quotes for the financial model.</p>
    <div class="costs"><table>
      <thead><tr><th>Item</th><th>Qty</th><th class="n">Est. PKR (low)</th><th class="n">Est. PKR (high)</th></tr></thead>
      <tbody>
        <tr><td>Main gate sign, illuminated</td><td>1</td><td class="n">250,000</td><td class="n">450,000</td></tr>
        <tr><td>Building facade letters and crest</td><td>1</td><td class="n">400,000</td><td class="n">700,000</td></tr>
        <tr><td>Reception feature wall</td><td>1</td><td class="n">150,000</td><td class="n">300,000</td></tr>
        <tr><td>Van livery</td><td>4 vans</td><td class="n">140,000</td><td class="n">240,000</td></tr>
        <tr><td>Door plates and corridor signs</td><td>about 40</td><td class="n">120,000</td><td class="n">240,000</td></tr>
        <tr><td>Admissions billboard print (site rent extra)</td><td>2</td><td class="n">80,000</td><td class="n">140,000</td></tr>
        <tr class="tot"><td>Total, one-time</td><td></td><td class="n">1,140,000</td><td class="n">2,070,000</td></tr>
      </tbody>
    </table></div>
    <p class="note">The photos are AI-generated visualisations to agree the design. The buildings are illustrative, not your campus. Final sign sizes depend on the building you lease. Signs facing the road may need permission from the Faisalabad Development Authority (FDA) or the PHA, and the sign-maker usually handles this.</p>
  </section>

  <section class="decide" aria-labelledby="ap">
    <h2 id="ap">Your approval</h2>
    <ol>
      <li><b>Gate, facade and reception</b>: approve the look, or change anything?</li>
      <li><b>Vans</b>: white with a claret band as shown, or fully claret vans?</li>
      <li><b>Billboard</b>: approve the launch message "Admissions open · Grade 3 to O Level · Character comes first"?</li>
      <li><b>Next</b>: social media templates, then the business and financial feasibility for Faisalabad.</li>
    </ol>
  </section>
</div>

<dialog id="zoom" aria-label="Signage photo"><button class="x" type="button" aria-label="Close">×</button><img alt=""></dialog>
<script>
(() => {{
  const dlg = document.getElementById('zoom'), img = dlg.querySelector('img');
  document.querySelectorAll('button[data-full]').forEach(b => b.addEventListener('click', () => {{
    img.src = b.dataset.full; img.alt = b.querySelector('img').alt; if (dlg.showModal) dlg.showModal();
  }}));
  dlg.querySelector('.x').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => {{ if (e.target === dlg) dlg.close(); }});
}})();
</script>
'''
(ROOT / "adabury-signage.html").write_text(html)
print("wrote", len(html))
