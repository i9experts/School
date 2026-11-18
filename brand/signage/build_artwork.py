#!/usr/bin/env python3
"""Write the Adabury signage artwork as HTML pages (one per sign) for rendering to PNG.

Usage: python3 build_artwork.py <out-dir>
Then render each page at its pixel size (render_artwork.js) into brand/signage/artwork/.
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def svg(name, style=""):
    s = (ROOT / "logo" / name).read_text()
    s = re.sub(r'width="\d+" height="\d+"', f'style="{style}"', s, count=1)
    return s


CREST_REV = svg("adabury-crest-reverse.svg", "height:100%;width:auto;display:block")
GROUP = base64.b64encode((ROOT / "uniform/photos/web/10-group-campus.jpg").read_bytes()).decode()

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&'
         'family=Marcellus&family=Outfit:wght@400;500&family=Noto+Nastaliq+Urdu:wght@600&display=swap">')
BASE = """<style>*{box-sizing:border-box;margin:0}html,body{width:%dpx;height:%dpx;overflow:hidden}
body{font-family:Outfit,sans-serif}
.caps{font-family:Marcellus,serif}.ur{font-family:'Noto Nastaliq Urdu',serif}.disp{font-family:'Cormorant Garamond',serif}
</style>"""

pages = {}

# 1. Main gate sign: 3000 x 1000
pages["gate-sign"] = (3000, 1000, f"""
<div style="position:absolute;inset:0;background:#6E1F2F"></div>
<div style="position:absolute;inset:34px;border:6px solid #C9A962"></div>
<div style="position:absolute;inset:52px;border:2px solid rgba(201,169,98,.55)"></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:110px">
  <div style="height:640px">{CREST_REV}</div>
  <div style="width:4px;height:520px;background:#C9A962"></div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
    <div class="caps" style="color:#F5EEE6;font-size:190px;letter-spacing:.2em;line-height:1;padding-left:.2em">ADABURY</div>
    <div class="caps" style="color:#D7BB7A;font-size:78px;letter-spacing:.62em;line-height:1;padding-left:.62em;margin-top:18px">SCHOOL</div>
    <div class="ur" lang="ur" dir="rtl" style="color:#D7BB7A;font-size:120px;line-height:1.9;margin-top:4px">ادبری اسکول</div>
    <div style="color:#F5EEE6;opacity:.8;font-size:46px;letter-spacing:.5em;padding-left:.5em">FAISALABAD</div>
  </div>
</div>""")

# 2. Reception feature wall: 2400 x 1500
pages["reception-wall"] = (2400, 1500, f"""
<div style="position:absolute;inset:0;background:#6E1F2F"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
  <div style="height:560px">{CREST_REV}</div>
  <div class="caps" style="color:#E2C77E;font-size:150px;letter-spacing:.22em;padding-left:.22em;line-height:1;margin-top:40px">ADABURY</div>
  <div class="caps" style="color:#E2C77E;font-size:50px;letter-spacing:.5em;padding-left:.5em;margin-top:26px">ADAB · ILM · IHSAN</div>
  <div class="ur" lang="ur" dir="rtl" style="color:#F5EEE6;font-size:92px;line-height:2;margin-top:6px">ادب پہلا قرینہ ہے</div>
</div>""")

# 3. Admissions hoarding (roadside billboard 40 x 20 ft): 4000 x 2000
pages["hoarding"] = (4000, 2000, f"""
<div style="position:absolute;left:0;top:0;bottom:0;width:2050px;background:#6E1F2F"></div>
<div style="position:absolute;left:2050px;top:0;bottom:0;width:22px;background:#C9A962"></div>
<div style="position:absolute;left:2072px;right:0;top:0;bottom:0;background:url(data:image/jpeg;base64,{GROUP}) center/cover"></div>
<div style="position:absolute;left:150px;top:150px;width:1780px;display:flex;flex-direction:column;gap:0">
  <div style="display:flex;align-items:center;gap:56px">
    <div style="height:330px">{CREST_REV}</div>
    <div><div class="caps" style="color:#F5EEE6;font-size:120px;letter-spacing:.2em;line-height:1">ADABURY</div>
    <div style="color:#D7BB7A;font-size:44px;letter-spacing:.42em;margin-top:22px">SCHOOL · FAISALABAD</div></div>
  </div>
  <div class="disp" style="color:#F5EEE6;font-size:200px;line-height:1;margin-top:120px">Admissions open</div>
  <div style="color:#E2C77E;font-size:72px;margin-top:40px">Grade 3 to O Level · Session 2027–28</div>
  <div style="color:#F5EEE6;font-size:60px;margin-top:22px;opacity:.9">Cambridge curriculum · Character comes first</div>
  <div class="ur" lang="ur" dir="rtl" style="color:#E2C77E;font-size:84px;line-height:2.1;margin-top:20px;text-align:left">ادب پہلا قرینہ ہے</div>
  <div style="display:inline-block;margin-top:24px;background:#C9A962;color:#2A1418;font-size:66px;font-weight:500;padding:26px 56px;border-radius:12px;align-self:flex-start">+92 41 [number] · adabury.edu.pk</div>
</div>""")

# 4. Van side livery panel: 3000 x 900
pages["van-livery"] = (3000, 900, f"""
<div style="position:absolute;inset:0;background:#FFFFFF"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:#6E1F2F"></div>
<div style="position:absolute;left:0;right:0;bottom:300px;height:24px;background:#C9A962"></div>
<div style="position:absolute;left:180px;top:90px;height:470px;display:flex;align-items:center;gap:70px">
  <div style="height:470px">{svg("adabury-crest.svg", "height:100%;width:auto;display:block")}</div>
  <div><div class="caps" style="color:#6E1F2F;font-size:170px;letter-spacing:.2em;line-height:1">ADABURY</div>
  <div class="caps" style="color:#A8843E;font-size:58px;letter-spacing:.5em;margin-top:26px">SCHOOL · FAISALABAD</div></div>
</div>
<div class="ur" lang="ur" dir="rtl" style="position:absolute;right:200px;top:150px;color:#6E1F2F;font-size:130px;line-height:2">ادبری اسکول</div>
<div style="position:absolute;left:180px;right:180px;bottom:0;height:300px;display:flex;align-items:center;justify-content:space-between;color:#F5EEE6;font-size:70px">
  <span class="caps" style="letter-spacing:.3em;color:#E2C77E">ADAB · ILM · IHSAN</span><span>+92 41 [number]</span></div>""")

# 5. Building facade letters: 3600 x 900 (gold letters, transparent ground rendered on brick later)
pages["facade-letters"] = (3600, 900, f"""
<div style="position:absolute;inset:0;background:#8B3A2E"></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:110px">
  <div style="height:700px">{CREST_REV}</div>
  <div class="caps" style="color:#D9B35F;font-size:230px;letter-spacing:.18em;white-space:nowrap;line-height:1;text-shadow:0 10px 18px rgba(0,0,0,.35)">ADABURY SCHOOL</div>
</div>""")

for name, (w, h, body) in pages.items():
    (OUT / f"{name}.html").write_text(f'<!doctype html><meta charset="utf-8">{FONTS}{BASE % (w, h)}<body style="position:relative">{body}</body>')
    print(name, w, h)
