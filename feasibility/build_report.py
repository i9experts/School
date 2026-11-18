#!/usr/bin/env python3
"""Build the Adabury School Faisalabad feasibility report (HTML; PDF rendered separately).

Reads results exported from the Excel model (model.json) so every figure matches the model.
Usage: python3 build_report.py <model.json>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND = ROOT.parent / "brand"
D = json.load(open(sys.argv[1]))
B, W, BE = D["rows"]["base"], D["rows"]["worst"], D["rows"]["best"]
K = D["kpi"]


def m(v, dp=1):  # PKR -> million string
    v = float(v) / 1e6
    s = f"{abs(v):,.{dp}f}"
    return f"({s})" if v < 0 else s


def cr(v):  # PKR -> crore string
    return f"{float(v) / 1e7:,.1f}"


def kp(label, i):
    return K[label][i]


crest = re.sub(r'width="\d+" height="\d+"', 'class="crest"', (BRAND / "logo/adabury-crest-reverse.svg").read_text(), count=1)
hlogo = re.sub(r'width="\d+" height="\d+"', 'class="hlogo"', (BRAND / "logo/adabury-logo-horizontal-reverse.svg").read_text(), count=1)

years = ["Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"]
yl = ["2027-28", "2028-29", "2029-30", "2030-31", "2031-32", "2032-33", "2033-34", "2034-35", "2035-36", "2036-37", "2037-38"]
other_costs = [B["Total other operating costs"][t] - B["Building rent"][t] for t in range(11)]
tbl_rows = [
    ("Students", [f"{int(v):,}" for v in B["Total students"]], False),
    ("Capacity used", [f"{v * 100:.0f}%" for v in B["Capacity used"]], False),
    ("Revenue", [m(v) for v in B["Total revenue"]], True),
    ("Payroll", [m(-v) for v in B["Total payroll"]], False),
    ("Rent", [m(-v) for v in B["Building rent"]], False),
    ("Other running costs", [m(-v) for v in other_costs], False),
    ("EBITDA", [m(v) for v in B["EBITDA (operating profit before depreciation)"]], True),
    ("Net profit after tax", [m(v) for v in B["Net profit after tax"]], True),
    ("Free cash flow", [m(v) for v in B["Free cash flow (before owner's investment)"]], False),
    ("Cash balance with PKR 10 crore invested", [m(v) for v in B["Cash balance at year end"]], True),
]
year_table = "<tr><th>PKR million</th>" + "".join(f"<th>{y}<small>{l}</small></th>" for y, l in zip(years, yl)) + "</tr>"
for lab, vals, bold in tbl_rows:
    cls = ' class="b"' if bold else ""
    year_table += f"<tr{cls}><td>{lab}</td>" + "".join(f'<td class="{"neg" if v.startswith("(") else ""}">{v}</td>' for v in vals) + "</tr>"

capex_rows = "".join(f"<tr><td>{n}</td><td class='n'>{m(v)}</td></tr>" for n, v in D["capex"][:-3])
capex_total = D["capex"][-1][1]
capex_cont = D["capex"][-2][1]

scen_labels = [
    ("Students in Y1", "Students in Y1", "int"), ("Students in Y5", "Students in Y5", "int"),
    ("Revenue in Y5 (PKR million)", "Revenue in Y5, PKR million", "m"),
    ("Net profit in Y5 (PKR million)", "Net profit in Y5, PKR million", "m"),
    ("EBITDA margin in Y5", "EBITDA margin in Y5", "pct"),
    ("First year with a net profit", "First year with a net profit", "txt"),
    ("Payback (cumulative cash turns positive)", "Payback year (cumulative cash flow turns positive)", "txt"),
    ("Peak funding need (PKR million)", "Peak funding need (lowest cumulative cash flow), PKR million", "m"),
    ("Extra funding beyond PKR 10 crore (PKR million)", "Extra funding needed beyond the owner's investment, PKR million", "m"),
    ("10-year return (IRR)", "10-year internal rate of return", "pct"),
]


def fmtk(v, kind):
    if kind == "int":
        return f"{int(v):,}"
    if kind == "m":
        v = float(v)
        return f"({abs(v):,.1f})" if v < 0 else f"{v:,.1f}"
    if kind == "pct":
        return f"{float(v) * 100:.1f}%" if isinstance(v, (int, float)) or re.match(r"^-?[\d.]+(e-?\d+)?$", str(v)) else str(v)
    return str(v)


scen_table = "<tr><th>Measure</th><th>Worst</th><th>Base</th><th>Best</th></tr>"
for lab, key, kind in scen_labels:
    scen_table += f"<tr><td>{lab}</td>" + "".join(f"<td class='n'>{fmtk(kp(key, i), kind)}</td>" for i in range(3)) + "</tr>"

peak_base = float(kp("Peak funding need (lowest cumulative cash flow), PKR million", 1))
gap_base = float(kp("Extra funding needed beyond the owner's investment, PKR million", 1))
ni5 = float(kp("Net profit in Y5, PKR million", 1))
rev5 = float(kp("Revenue in Y5, PKR million", 1))
irr = float(kp("10-year internal rate of return", 1))
pay = kp("Payback year (cumulative cash flow turns positive)", 1)
first = kp("First year with a net profit", 1)
ni10 = float(B["Net profit after tax"][10]) / 1e6
teachers_y1, teachers_y5 = B["Teachers (full-time equivalent)"][1], B["Teachers (full-time equivalent)"][5]
sections_y1, sections_y5 = B["Total sections (classes)"][1], B["Total sections (classes)"][5]
startup = float(kp("Start-up investment needed (capex + deposit + Y0 costs), PKR million", 1))

# simple bar chart of base revenue vs costs (SVG, drawn to scale)
rev = [float(v) / 1e6 for v in B["Total revenue"]]
cost = [float(v) / 1e6 for v in B["Total operating costs (payroll + other)"]]
ni = [float(v) / 1e6 for v in B["Net profit after tax"]]
cash = [float(v) / 1e6 for v in B["Cash balance at year end"]]
vmax = 500
CW, CH, PL, PT, PB = 760, 300, 52, 16, 40
plot_h = CH - PT - PB
x0 = PL
bw = (CW - PL - 10) / 11


def y(v):
    return PT + plot_h * (1 - v / vmax)


bars = ""
for i in range(11):
    bx = x0 + i * bw
    bars += f'<rect x="{bx + bw * .14:.1f}" y="{y(rev[i]):.1f}" width="{bw * .34:.1f}" height="{y(0) - y(rev[i]):.1f}" fill="var(--claret)"/>'
    bars += f'<rect x="{bx + bw * .5:.1f}" y="{y(cost[i]):.1f}" width="{bw * .34:.1f}" height="{y(0) - y(cost[i]):.1f}" fill="var(--gold)"/>'
    bars += f'<text x="{bx + bw / 2:.1f}" y="{CH - 18}" text-anchor="middle" class="ax">{years[i]}</text>'
grid = "".join(f'<line x1="{PL}" x2="{CW - 6}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="gr"/><text x="{PL - 8}" y="{y(v) + 4:.1f}" text-anchor="end" class="ax">{v}</text>' for v in range(0, 501, 100))
chart1 = f'<svg viewBox="0 0 {CW} {CH}" class="chart" role="img" aria-label="Base case revenue and operating costs by year, PKR million">{grid}{bars}</svg>'

# cash balance line chart
cmin, cmax = -150, 300
def yc(v):
    return PT + plot_h * (1 - (v - cmin) / (cmax - cmin))
pts = " ".join(f"{x0 + i * bw + bw / 2:.1f},{yc(cash[i]):.1f}" for i in range(11))
grid2 = "".join(f'<line x1="{PL}" x2="{CW - 6}" y1="{yc(v):.1f}" y2="{yc(v):.1f}" class="gr{" zero" if v == 0 else ""}"/><text x="{PL - 8}" y="{yc(v) + 4:.1f}" text-anchor="end" class="ax">{v}</text>' for v in range(-150, 301, 50))
dots = "".join(f'<circle cx="{x0 + i * bw + bw / 2:.1f}" cy="{yc(cash[i]):.1f}" r="4" fill="{"var(--neg)" if cash[i] < 0 else "var(--claret)"}"/>' for i in range(11))
labels2 = "".join(f'<text x="{x0 + i * bw + bw / 2:.1f}" y="{CH - 18}" text-anchor="middle" class="ax">{years[i]}</text>' for i in range(11))
low_i = min(range(11), key=lambda i: cash[i])
ann = f'<text x="{x0 + low_i * bw + bw / 2 + 10:.1f}" y="{yc(cash[low_i]) + 18:.1f}" class="ann">Lowest point: PKR {cash[low_i]:,.0f} million</text>'
chart2 = f'<svg viewBox="0 0 {CW} {CH}" class="chart" role="img" aria-label="Base case cash balance by year with PKR 10 crore invested">{grid2}<polyline points="{pts}" fill="none" stroke="var(--claret)" stroke-width="2.5"/>{dots}{labels2}{ann}</svg>'

html = f'''<title>Adabury Feasibility Study</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Marcellus&family=Outfit:wght@300;400;500;600&display=swap">
<style>
/* Layout: a report — claret cover band, a sticky contents rail on wide screens, numbered chapters (the order is the argument), tables and two to-scale charts. */
:root{{
  --bg:#FAF8F5; --surface:#FFFFFF; --fg:#2A1418; --muted:#6F5F60; --line:#E6DEDA; --accent:#6E1F2F; --chip:#F3ECE4;
  --claret:#6E1F2F; --gold:#C2A15A; --neg:#B3261E; --pos:#2E6B3F;
  --display:"Cormorant Garamond", Georgia, serif; --caps:"Marcellus", Georgia, serif; --sans:"Outfit","Segoe UI",system-ui,sans-serif;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{ --bg:#140C0E; --surface:#1E1416; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; --chip:#2A1D20; --claret:#C9677C; --gold:#E2BE76; --neg:#FF8A80; --pos:#7FCF95; color-scheme:dark }} }}
:root[data-theme="dark"]{{ --bg:#140C0E; --surface:#1E1416; --fg:#F2E9E6; --muted:#B4A3A3; --line:#3A2A2D; --accent:#E2BE76; --chip:#2A1D20; --claret:#C9677C; --gold:#E2BE76; --neg:#FF8A80; --pos:#7FCF95; color-scheme:dark }}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16px;line-height:1.6}}
.cover{{background:#6E1F2F;color:#F5EEE6;box-shadow:inset 0 -6px 0 #C9A962}}
.cover .in{{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 48px;display:grid;gap:18px}}
.hlogo{{width:260px;height:auto;display:block}}
.cover h1{{font-family:var(--display);font-weight:600;font-size:clamp(36px,6vw,62px);line-height:1.03;margin:10px 0 0;max-width:18ch;text-wrap:balance}}
.cover p{{margin:0;max-width:70ch;color:#EADBD3}}
.meta{{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#D7BB7A}}
.wrap{{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 80px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:48px}}
nav{{position:sticky;top:20px;align-self:start;font-size:14px}}
nav ol{{margin:0;padding-left:20px;display:grid;gap:6px;color:var(--muted)}}
nav a{{color:var(--muted);text-decoration:none}} nav a:hover{{color:var(--accent)}}
main{{display:flex;flex-direction:column;gap:56px;min-width:0}}
section > h2{{font-family:var(--display);font-weight:600;font-size:34px;line-height:1.1;margin:0 0 6px}}
.num{{font-family:var(--caps);font-size:13px;letter-spacing:.2em;color:var(--accent)}}
h3{{font-size:17px;font-weight:600;margin:24px 0 6px}}
p{{margin:0 0 12px;max-width:72ch}}
ul,ol.l{{margin:0 0 12px;padding-left:20px;max-width:72ch;display:grid;gap:4px}}
.verdict{{background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--claret);border-radius:6px;padding:22px 24px;display:grid;gap:10px}}
.verdict p{{margin:0}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}}
.kpi{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:14px 16px}}
.kpi b{{display:block;font-family:var(--display);font-size:30px;font-weight:600;line-height:1.1;font-variant-numeric:tabular-nums}}
.kpi span{{font-size:13px;color:var(--muted)}}
.kpi.warn b{{color:var(--neg)}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--surface);margin:12px 0}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{padding:8px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:12px;font-weight:500;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}}
th small{{display:block;text-transform:none;letter-spacing:0;font-size:11px}}
td.n,.yt td:not(:first-child){{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
.yt{{min-width:900px}}
.yt tr.b td{{font-weight:600}}
td.neg{{color:var(--neg)}}
.chart{{width:100%;height:auto;display:block;margin:8px 0 4px}}
.chart .gr{{stroke:var(--line);stroke-width:1}} .chart .gr.zero{{stroke:var(--muted)}}
.chart .ax{{fill:var(--muted);font-size:12px;font-family:var(--sans)}}
.chart .ann{{fill:var(--neg);font-size:13px;font-family:var(--sans)}}
.legend{{display:flex;gap:18px;font-size:13px;color:var(--muted)}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}}
.cards{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:12px 0}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:16px 18px}}
.card h4{{margin:0 0 6px;font-size:16px;font-weight:600}}
.card p{{margin:0;font-size:14.5px;color:var(--muted)}}
.card .eff{{display:block;margin-top:8px;font-size:13px;color:var(--accent);font-weight:500}}
.org{{display:grid;gap:10px;justify-items:center;margin:16px 0}}
.org .row{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
.org .box{{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--claret);border-radius:4px;padding:8px 14px;font-size:14px;text-align:center;min-width:150px}}
.org .box small{{display:block;color:var(--muted);font-size:12px}}
.org .box.top{{border-top-color:var(--gold)}}
.org .ar{{color:var(--muted);font-size:18px;line-height:1}}
.tl{{display:grid;gap:0;border-left:2px solid var(--gold);margin:12px 0 12px 6px}}
.tl div{{position:relative;padding:0 0 14px 22px}}
.tl div::before{{content:"";position:absolute;left:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--claret)}}
.tl b{{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}}
.risk td:first-child{{font-weight:500}}
.pill{{display:inline-block;font-size:12px;padding:2px 9px;border-radius:99px;background:var(--chip)}}
.pill.h{{background:#F6D6D3;color:#7A1A12}} .pill.mid{{background:#F5E7C6;color:#6A4A0A}} .pill.l{{background:#DDEBDD;color:#1F4A2A}}
.note{{font-size:13px;color:var(--muted)}}
.src{{font-size:13px;color:var(--muted)}} .src a{{color:var(--muted)}}
@media (max-width:900px){{ .wrap{{grid-template-columns:1fr}} nav{{position:static}} .kpis{{grid-template-columns:1fr 1fr}} .cards{{grid-template-columns:1fr}} }}
@media print{{
  nav{{display:none}} .wrap{{grid-template-columns:1fr;padding-block:20px}} body{{background:#fff;font-size:11pt}}
  .num{{display:block;break-after:avoid}} section{{break-inside:auto}} .tw,.verdict,.kpis,.card,.org,table,svg{{break-inside:avoid}} section > h2{{break-after:avoid}}
  .cover{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
}}
</style>

<header class="cover"><div class="in">
  {hlogo}
  <div class="meta"><span>Feasibility study</span><span>Faisalabad campus</span><span>November 2026</span></div>
  <h1>Adabury School, Faisalabad: feasibility study</h1>
  <p>A Cambridge school, Grade 3 to O Level, with separate girls' and boys' blocks on the Canal Road belt, opening April 2028. Prepared for the founder and the future Board of Governors.</p>
</div></header>

<div class="wrap">
<nav aria-label="Contents"><ol>
  <li><a href="#s1">Summary and verdict</a></li><li><a href="#s2">The opportunity</a></li><li><a href="#s3">Competition and pricing</a></li>
  <li><a href="#s4">Location and building</a></li><li><a href="#s5">Academic and Tarbiyah model</a></li><li><a href="#s6">Governance</a></li>
  <li><a href="#s7">Students and staff</a></li><li><a href="#s8">Investment</a></li><li><a href="#s9">Financial projections</a></li>
  <li><a href="#s10">Scenarios</a></li><li><a href="#s11">Closing the funding gap</a></li><li><a href="#s12">Risks</a></li>
  <li><a href="#s13">Licences and approvals</a></li><li><a href="#s14">Launch timeline</a></li><li><a href="#s15">Decisions needed</a></li>
</ol></nav>
<main>

<section id="s1"><span class="num">01</span><h2>Summary and verdict</h2>
  <div class="verdict">
    <p><b>The school works as a business once it is established, but it needs about twice the planned start-up money.</b></p>
    <p>In the base case Adabury reaches {int(B['Total students'][5]):,} students by Year 5, makes its first net profit in {first.lower()}, and earns about PKR {ni5:,.0f} million a year by Year 5 (about PKR {ni10:,.0f} million by Year 10). The cash invested is paid back in {pay.lower()}.</p>
    <p>However, losses in the first two years, together with the fit-out, mean the school is up to <b>PKR {peak_base / 10:,.1f} crore</b> down before it turns the corner. With PKR 10 crore invested, about <b>PKR {gap_base / 10:,.1f} crore more</b> is needed. Section 11 shows how to close most of that gap.</p>
    <p><b>Recommendation:</b> go ahead to the site search and registration stage, but sign a lease only once the funding plan in Section 11 is agreed. The worst case (20% fewer students and 5% lower fees) does not make a profit within 10 years, so a strong first intake is essential.</p>
  </div>
  <div class="kpis">
    <div class="kpi"><b>{int(B['Total students'][1]):,} → {int(B['Total students'][5]):,}</b><span>Students, Year 1 to Year 5</span></div>
    <div class="kpi"><b>PKR {rev5 / 10:,.1f} cr</b><span>Revenue in Year 5</span></div>
    <div class="kpi"><b>{first}</b><span>First year with a net profit</span></div>
    <div class="kpi warn"><b>PKR {peak_base / 10:,.1f} cr</b><span>Peak funding need (budget: PKR 8–12 crore)</span></div>
  </div>
  <p class="note">All money in Pakistani rupees, in prices of the year shown. 1 crore = 10 million. Figures come from the Excel model (Adabury_Faisalabad_Financial_Model.xlsx), base case unless stated.</p>
</section>

<section id="s2"><span class="num">02</span><h2>The opportunity</h2>
  <p>Over 13 years of running The Deenway School, the founder has seen a large group of parents who want strong character and an Islamic environment for their children, but who will not choose a school that looks strictly traditional. They want a <b>world-class school that also builds character</b>.</p>
  <p>In Faisalabad, these middle and upper-middle income families currently choose between two kinds of school:</p>
  <ul>
    <li><b>Premium chains</b> (Beaconhouse, LGS, Roots and others): strong academics and facilities, but values and Islamic learning are not the core promise.</li>
    <li><b>Islamic schools</b>: strong on Quran and values, but rarely seen as offering Cambridge-level academics or a modern, premium experience.</li>
  </ul>
  <p>Adabury sits between them: <b>Cambridge academics, with character first</b> ("Adab is the first grace"). It is priced below the premium chains and looks and feels like a leading school, with a crest rooted in Faisalabad's Clock Tower.</p>
  <h3>Target families</h3>
  <ul>
    <li>Business, textile and professional families on and around the Canal Road belt.</li>
    <li>Parents moving their child after Grade 2 from a pre-school or a general private school, looking for stronger values and stronger academics.</li>
    <li>Families who want Quran, Arabic and good manners taught seriously, alongside O Levels.</li>
  </ul>
</section>

<section id="s3"><span class="num">03</span><h2>Competition and pricing</h2>
  <p>Published fee information for Faisalabad comes only from third-party guides. They disagree with each other and must be checked by calling each school's admissions office before the fees are finalised.</p>
  <div class="tw"><table>
    <tr><th>School (Faisalabad)</th><th>Reported monthly tuition</th><th>Position</th></tr>
    <tr><td>Beaconhouse</td><td>About PKR 30,000–40,000 (primary and secondary); O Level reported at PKR 35,000–40,000</td><td>National premium chain</td></tr>
    <tr><td>Lahore Grammar School (LGS)</td><td>Reported between PKR 17,000 and 45,000 depending on the source</td><td>Premium, strong academics</td></tr>
    <tr><td>Roots (IVY and other Roots schools)</td><td>About PKR 35,000–45,000 (primary and secondary)</td><td>Premium chain</td></tr>
    <tr><td><b>Adabury (proposed, April 2028)</b></td><td><b>PKR 19,500 (Grades 3–5) · 23,000 (6–8) · 27,500 (O Level)</b></td><td><b>Premium look, character first, priced below the chains</b></td></tr>
  </table></div>
  <p>The Adabury fees are within the founder's PKR 15,000–25,000 band in today's money; they equal about PKR 16,700–23,600 in 2026 prices. In 2028 they sit roughly 25–40% below the premium chains, which gives a clear value story: <i>"Cambridge quality and real character education, for less."</i></p>
  <p>Fees then rise 7% a year. Punjab rules have been reported to allow 5% a year normally, and up to 8% with approval for fees above PKR 4,000 a month. The current rule must be confirmed before launch, because it limits how fast fees can keep pace with salaries.</p>
  <p class="src">Sources: <a href="https://theeducationtrailblazer.com/best-schools-in-faisalabad/">The Education Trailblazer, Best Schools in Faisalabad</a>; <a href="https://blog.foriedu.com/top-10-schools-in-pakistan/">Foriedu, Top 10 Schools in Pakistan</a>; <a href="https://mixthometutors.com/best-schools-in-faisalabad/">Mixtho Me Tutors</a>; <a href="https://www.dawn.com/news/1307682">Dawn, Punjab fee ordinance</a>; <a href="https://arynews.tv/punjab-govt-bars-private-schools-from-raising-tuition-fee">ARY News</a>.</p>
</section>

<section id="s4"><span class="num">04</span><h2>Location and building</h2>
  <p><b>Area: the Canal Road belt</b> (Canal Road, Gulberg, Kohinoor City, Eden Valley and nearby). This is where the target families live, it is easy to reach, and it signals a premium school. The trade-off is higher rent and more competition, which the model reflects.</p>
  <h3>What the building must have</h3>
  <ul>
    <li>About 6–8 kanal, with room for <b>36 classrooms</b> at full size (9 grades × 2 blocks × 2 sections).</li>
    <li><b>Two fully separate blocks</b>, girls' and boys', each with its own entrance, prayer hall, washrooms, staff room, library, science lab and computer lab.</li>
    <li>A safe drop-off area for vans and cars off the main road, which matters on busy Canal Road.</li>
    <li>Permission for school use from the Faisalabad Development Authority, and room for solar panels on the roof.</li>
  </ul>
  <h3>Rent</h3>
  <p>The model assumes <b>PKR 20 lakh a month</b> from April 2028, rising 10% a year, with 6 months' deposit and 4 months' rent during fit-out. Canal Road listings show 1–2 kanal buildings at roughly PKR 3.5–8 lakh, so a two-block school building is scaled up from those. <b>Rent is the single biggest cost to negotiate.</b> A 10-year lease with rent increases capped at 10%, two rent-free months for fit-out, and a first right to buy are the targets.</p>
  <p class="src">Source: <a href="https://www.zameen.com/Property/faisalabad_canal_road_building_for_rent-53842513-1140-4.html">Zameen.com Canal Road building listings</a> (asking prices, 2025).</p>
</section>

<section id="s5"><span class="num">05</span><h2>Academic and Tarbiyah model</h2>
  <h3>Academic pathway: Cambridge International</h3>
  <div class="tw"><table>
    <tr><th>Stage</th><th>Grades</th><th>Programme</th></tr>
    <tr><td>Junior</td><td>3–5</td><td>Cambridge Primary: English, Maths, Science, Global Perspectives, Computing, plus Urdu and Islamiyat to the Punjab curriculum</td></tr>
    <tr><td>Middle</td><td>6–8</td><td>Cambridge Lower Secondary, with Cambridge Checkpoint tests in Grade 8</td></tr>
    <tr><td>O Level</td><td>9–11</td><td>Cambridge O Level: about 8 subjects, including the compulsory Islamiyat, Pakistan Studies and Urdu</td></tr>
  </table></div>
  <h3>The Adabury Tarbiyah programme (the difference parents pay for)</h3>
  <ul>
    <li><b>Quran every day</b>: Nazra and Tajweed, with selected surahs memorised, plus an optional Hifz track in the afternoon.</li>
    <li><b>Arabic</b> from Grade 3, focused on understanding the Quran and daily duas.</li>
    <li><b>Seerah and Islamic studies</b> taught through stories and projects.</li>
    <li><b>Six character values</b>, rated every term on the report card: Adab, Amanah, Ihsan, Sabr, Shukr and Khidmah. A "Value of the month" is shared with families.</li>
    <li><b>Zuhr prayer in congregation</b> in each block. A mentor teacher meets each small group of students every week.</li>
    <li>Service learning, debating and leadership roles, so students become confident and kind.</li>
  </ul>
  <h3>A typical day</h3>
  <p>7:45 assembly and Quran → 8:15–13:15 Cambridge lessons (with a break) → 13:15 Zuhr → 13:35–14:15 Tarbiyah, clubs or Hifz track. Fridays end after Jumu'ah preparation.</p>
  <h3>Uniform</h3>
  <p>The approved claret-and-white uniform, with no tie. The school hijab is compulsory for girls. See the uniform page.</p>
</section>

<section id="s6"><span class="num">06</span><h2>Governance</h2>
  <p><b>Legal form:</b> a separate private limited company registered with SECP, which owns the Adabury brand. It should be fully separate from The Deenway School, as decided. The Adabury name and crest should be registered as trademarks with IPO Pakistan before launch. A tax adviser should confirm whether a company, an association of persons or a Section 42 non-profit structure works best.</p>
  <h3>Board of Governors (5–7 members)</h3>
  <ul>
    <li><b>Chair:</b> the founder.</li>
    <li><b>Two independent education experts</b>, ideally with Cambridge school leadership experience.</li>
    <li><b>One finance and audit expert</b> (a chartered accountant).</li>
    <li><b>One Shariah and Tarbiyah scholar</b>, who also chairs the advisory council below.</li>
    <li><b>One parent representative</b>, from Year 2.</li>
    <li><b>The Principal</b>, attending without a vote.</li>
  </ul>
  <p>The Board meets every quarter and has three committees: <b>Academic and Tarbiyah</b>, <b>Finance and Audit</b>, and <b>People and Safeguarding</b>. An <b>advisory Shariah and Tarbiyah Council</b> of two or three scholars approves the Tarbiyah curriculum and policies once a year.</p>
  <h3>Organisation chart</h3>
  <div class="org" role="img" aria-label="Organisation chart">
    <div class="row"><div class="box top">Board of Governors<small>with the Shariah and Tarbiyah Council</small></div></div>
    <div class="ar">↓</div>
    <div class="row"><div class="box">Principal</div></div>
    <div class="ar">↓</div>
    <div class="row">
      <div class="box">Head of Girls' Block<small>female teachers and staff</small></div>
      <div class="box">Head of Boys' Block<small>teachers and staff</small></div>
      <div class="box">Head of Tarbiyah<small>Quran, Arabic, Islamic studies</small></div>
      <div class="box">Bursar<small>finance, HR, admin</small></div>
      <div class="box">Admissions and marketing</div>
    </div>
    <div class="ar">↓</div>
    <div class="row">
      <div class="box">Cambridge coordinators (2)</div><div class="box">Class and subject teachers</div><div class="box">IT and exams</div><div class="box">Nurses, security, facilities</div>
    </div>
  </div>
  <h3>Key policies needed before opening</h3>
  <p>Admissions and fees, child safeguarding and protection, student conduct (built on Adab), staff code and recruitment, the uniform including the hijab, health and safety, data protection, and a complaints procedure.</p>
</section>

<section id="s7"><span class="num">07</span><h2>Students and staff</h2>
  <div class="tw"><table>
    <tr><th></th><th>Year 1 (2028-29)</th><th>Year 5 (2032-33)</th><th>Full size</th></tr>
    <tr><td>Students</td><td class="n">{int(B['Total students'][1]):,}</td><td class="n">{int(B['Total students'][5]):,}</td><td class="n">900 seats</td></tr>
    <tr><td>Classes (sections)</td><td class="n">{int(sections_y1)}</td><td class="n">{int(sections_y5)}</td><td class="n">about 41</td></tr>
    <tr><td>Teachers (full-time equivalent)</td><td class="n">{teachers_y1:,.0f}</td><td class="n">{teachers_y5:,.0f}</td><td class="n">about 64</td></tr>
    <tr><td>Leadership and support staff</td><td class="n">{int(D['staff_total'])}</td><td class="n">{int(D['staff_total'])}</td><td class="n">{int(D['staff_total'])}</td></tr>
  </table></div>
  <p>Year 1 opens Grades 3 to 9 in both blocks. Grades 10 and 11 open as the first O Level students move up, because few families switch schools in the middle of O Level. No class goes above 25 students; a new section opens when classes average 22.</p>
  <p>Teachers are budgeted at an average of <b>PKR 75,000 a month</b> in 2028, plus 10% employer costs and an Eid bonus, rising 8% a year. Recruiting experienced Cambridge-trained teachers, especially women for the girls' block, is the biggest hiring challenge. The Principal and core team join in November 2027, five months before opening.</p>
  <p class="src">Salary benchmarks: Lahore O Level teacher posts advertised at PKR 50,000–70,000 for early-career teachers (<a href="https://jobs.taraki.co/jobs/ao-levels-teacher-mathematics--physics-hex-solutions">Taraki listing</a>); Punjab minimum wage PKR 40,000 from July 2025 (<a href="https://propakistani.pk/2025/09/10/punjab-increases-minimum-wage-to-rs-40000/">ProPakistani</a>).</p>
</section>

<section id="s8"><span class="num">08</span><h2>Investment</h2>
  <p>Total fit-out and equipment is <b>PKR {m(capex_total)} million</b> (PKR {cr(capex_total)} crore), including a 10% contingency. 70% is spent before opening and the rest in Years 1–2 as the higher grades open. Transport is outsourced to a contractor using Adabury-branded vans and paid for by parents, which avoids about PKR 5 crore of van purchases.</p>
  <div class="tw"><table>
    <tr><th>Item</th><th class="n">PKR million</th></tr>
    {capex_rows}
    <tr><td>Contingency (10%)</td><td class="n">{m(capex_cont)}</td></tr>
    <tr class="b"><td><b>Total capital investment</b></td><td class="n"><b>{m(capex_total)}</b></td></tr>
  </table></div>
  <p>Before the first student arrives, the school also pays the rent deposit, 4 months' rent during fit-out, 5 months of leadership salaries, teacher training, a PKR 1.5 crore launch campaign and registration costs. In total, about <b>PKR {startup / 10:,.1f} crore</b> is spent before opening day.</p>
</section>

<section id="s9"><span class="num">09</span><h2>Financial projections (base case)</h2>
  <div class="legend"><span><i style="background:var(--claret)"></i>Revenue</span><span><i style="background:var(--gold)"></i>Operating costs</span></div>
  {chart1}
  <p class="note">PKR million. Revenue passes operating costs in Year 3, and the gap widens as the school fills up.</p>
  <div class="tw"><table class="yt">{year_table}</table></div>
  <p>Fees are about 90% of revenue. Payroll is the largest cost, at about 53–55% of revenue once the school is full, which is normal for a quality school. Rent falls from 26% of revenue in Year 1 to about 12% by Year 5, so filling seats matters more than anything else.</p>
  <h3>Cash: why extra funding is needed</h3>
  {chart2}
  <p class="note">Cash balance at each year end with PKR 10 crore invested in Year 0 (PKR million). Below zero means more money is needed.</p>
</section>

<section id="s10"><span class="num">10</span><h2>Scenarios</h2>
  <p>The worst case assumes 20% fewer students, fees 5% lower, salaries 5% higher and rent 15% higher. The best case assumes 12% more students (up to the 900-seat capacity), fees 5% higher and rent 5% lower.</p>
  <div class="tw"><table>{scen_table}</table></div>
  <p>The difference between the cases comes almost entirely from <b>how quickly the seats fill</b>. Every extra 50 students in Year 1 improves the funding need by roughly PKR 1.5–2 crore over the first three years. Pre-launch admissions, open days and the first-intake offer are therefore the most valuable money the school spends.</p>
</section>

<section id="s11"><span class="num">11</span><h2>Closing the funding gap</h2>
  <p>The base case needs about PKR {peak_base / 10:,.1f} crore at its lowest point (Year 2) against PKR 10 crore budgeted. These measures can be combined. The savings shown are approximate and should be tested in the model before a lease is signed.</p>
  <div class="cards">
    <div class="card"><h4>1. Islamic bank lease (Ijarah) for equipment</h4><p>Lease the air conditioning, solar system, IT and smart boards (about PKR 4 crore) instead of buying them. Monthly rentals replace a large upfront payment.</p><span class="eff">Reduces start-up cash by about PKR 3–4 crore</span></div>
    <div class="card"><h4>2. Landlord-funded fit-out</h4><p>Choose a landlord who builds the partitions, washrooms and prayer halls to the school's design, in return for a somewhat higher rent over a 10-year lease.</p><span class="eff">Reduces start-up cash by about PKR 2–3 crore</span></div>
    <div class="card"><h4>3. Softer rent in the first two years</h4><p>Negotiate a stepped rent: for example 60% in Year 1 and 80% in Year 2, recovered later in the lease.</p><span class="eff">Reduces early losses by about PKR 1–1.5 crore</span></div>
    <div class="card"><h4>4. Strong first intake</h4><p>Target 350 or more students in Year 1 through early admissions from September 2027, founding-family discounts and open days.</p><span class="eff">Every 50 extra students: about PKR 1.5–2 crore better</span></div>
    <div class="card"><h4>5. A partner or a bank facility for the rest</h4><p>A minority investor, or a running-finance line from an Islamic bank secured on fee income, covering Years 1–2 only.</p><span class="eff">Covers whatever remains, likely PKR 1–3 crore</span></div>
    <div class="card"><h4>6. Fallback: a smaller first phase</h4><p>Open Grades 3–8 only in Year 1 and add O Level from Year 2. This means fewer labs and teachers at the start, but delays O Level income.</p><span class="eff">Reduces Year 1 costs; test in the model</span></div>
  </div>
  <p>With measures 1–3 together, the gap shrinks to roughly PKR 3–5 crore, which brings the total close to the PKR 12 crore upper end of the founder's range. Measure 5 can then cover the rest.</p>
</section>

<section id="s12"><span class="num">12</span><h2>Risks and how to manage them</h2>
  <div class="tw"><table class="risk">
    <tr><th>Risk</th><th>Level</th><th>How to manage it</th></tr>
    <tr><td>Slow first intake</td><td><span class="pill h">High</span></td><td>Start admissions in September 2027, run open days and a founding-family offer, and let the Deenway network make referrals informally.</td></tr>
    <tr><td>Funding gap (Years 0–2)</td><td><span class="pill h">High</span></td><td>Agree the funding plan in Section 11 before signing the lease.</td></tr>
    <tr><td>Hiring Cambridge-trained teachers, especially women</td><td><span class="pill mid">Medium</span></td><td>Recruit early (from November 2027), pay above market for key posts, run training with Cambridge, and recruit from Lahore with a relocation allowance.</td></tr>
    <tr><td>Fee increases capped below cost inflation</td><td><span class="pill mid">Medium</span></td><td>Confirm the Punjab rule, set the launch fees correctly from day one, and keep payroll at or below 55% of revenue.</td></tr>
    <tr><td>Rent increases and lease security</td><td><span class="pill mid">Medium</span></td><td>Sign a 10-year lease with capped increases, a renewal option and a first right to buy.</td></tr>
    <tr><td>Approvals delay (FDA, education registration, Cambridge)</td><td><span class="pill mid">Medium</span></td><td>Start registration as soon as the building is chosen and use an experienced consultant.</td></tr>
    <tr><td>Brand confusion with Deenway</td><td><span class="pill l">Low</span></td><td>Keep a separate company, name, website and social media, as decided.</td></tr>
    <tr><td>Electricity costs in summer</td><td><span class="pill l">Low</span></td><td>Solar system, efficient inverter ACs, and timetables that use cooler morning hours.</td></tr>
  </table></div>
</section>

<section id="s13"><span class="num">13</span><h2>Licences and approvals</h2>
  <p>These need to be confirmed with a local consultant, because requirements change.</p>
  <ul>
    <li>Company registration with SECP, and NTN and tax registration with FBR.</li>
    <li>Trademark registration of the name and crest with IPO Pakistan.</li>
    <li>Building approval for school use from the Faisalabad Development Authority.</li>
    <li>Registration of the private school with the Punjab school education authorities (District Education Authority, Faisalabad).</li>
    <li>Approval as a Cambridge International school (Cambridge Assessment International Education), which can take several months.</li>
    <li>Fire safety, building safety and health certificates. Staff registered with EOBI and Punjab social security.</li>
  </ul>
</section>

<section id="s14"><span class="num">14</span><h2>Launch timeline to April 2028</h2>
  <div class="tl">
    <div><b>Dec 2026 – Feb 2027</b>Approve this study and the funding plan. Register the company and trademarks. Reserve the web domain and social media handles.</div>
    <div><b>Mar – Jun 2027</b>Search for a building on the Canal Road belt and sign the lease (with the fit-out and rent terms in Section 11). Apply to Cambridge and start registration.</div>
    <div><b>Jul – Oct 2027</b>Fit-out and signage. Recruit the Principal and both block heads. Launch the website. Admissions open in September with open days and billboards.</div>
    <div><b>Nov 2027 – Jan 2028</b>Core team in place. Recruit teachers. Build the Tarbiyah curriculum and policies. Hold entry assessments and the first admissions round.</div>
    <div><b>Feb – Mar 2028</b>Teacher training and induction. Uniform and books supply. Parent orientation. Final inspections.</div>
    <div><b>April 2028</b>Adabury School opens: Grades 3–9 in both blocks.</div>
  </div>
</section>

<section id="s15"><span class="num">15</span><h2>Decisions needed from the founder</h2>
  <ol class="l">
    <li>Approve going ahead to the site search and registration stage.</li>
    <li>Choose the funding approach for the gap (Section 11): Ijarah, landlord fit-out, stepped rent, a partner or bank facility, or a smaller first phase.</li>
    <li>Confirm the fee levels (PKR 19,500 / 23,000 / 27,500 a month in 2028), or set different ones.</li>
    <li>Review the model's assumptions, especially salaries from your Karachi branches and real rent quotes, and update the blue cells.</li>
    <li>Nominate the first Board of Governors and the Shariah and Tarbiyah Council.</li>
  </ol>
  <p class="note">Prepared with publicly available information in November 2026. Fee, rent and salary figures come from listings and guides and must be verified with quotes. This study is a planning tool, not legal, tax or investment advice.</p>
</section>
</main></div>
'''
(ROOT / "adabury-feasibility-report.html").write_text(html)
print("wrote", len(html))
