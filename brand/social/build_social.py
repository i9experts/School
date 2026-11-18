#!/usr/bin/env python3
"""Write the Adabury social media templates as HTML pages at exact platform sizes.

Usage: python3 build_social.py <html-out-dir>
Render them with ../signage/render_artwork.js <html-out-dir> png
Placeholders in [square brackets] are replaced per post (in Canva, Photoshop or by regenerating).
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def svg(name, style="height:100%;width:auto;display:block"):
    s = (ROOT / "logo" / name).read_text()
    return re.sub(r'width="\d+" height="\d+"', f'style="{style}"', s, count=1)


def photo(name):
    return "data:image/jpeg;base64," + base64.b64encode((ROOT / "uniform/photos/web" / name).read_bytes()).decode()


CREST = svg("adabury-crest.svg")
CREST_REV = svg("adabury-crest-reverse.svg")
H_REV = svg("adabury-logo-horizontal-reverse.svg", "width:100%;height:auto;display:block")
H = svg("adabury-logo-horizontal.svg", "width:100%;height:auto;display:block")

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,500&'
         'family=Marcellus&family=Outfit:wght@400;500;600&family=Noto+Nastaliq+Urdu:wght@600&family=Amiri:wght@700&display=swap">')
CSS = """<style>*{box-sizing:border-box;margin:0}html,body{width:%dpx;height:%dpx;overflow:hidden}
body{position:relative;font-family:Outfit,sans-serif;color:#2A1418}
.caps{font-family:Marcellus,serif}.disp{font-family:'Cormorant Garamond',serif;font-weight:600}
.ur{font-family:'Noto Nastaliq Urdu',serif}.ar{font-family:Amiri,serif}
.claret{background:#6E1F2F}.gold{color:#E2C77E}.linen{color:#F5EEE6}
.rule{height:6px;background:#C9A962}
.frame{position:absolute;border:3px solid rgba(201,169,98,.7)}
.pill{display:inline-block;background:#C9A962;color:#2A1418;font-weight:500;border-radius:999px}
</style>"""

T = {}

# 1. Instagram / Facebook post, portrait 4:5 — Admissions open
T["01-post-admissions"] = (1080, 1350, f"""
<div class="claret" style="position:absolute;inset:0"></div>
<div style="position:absolute;left:0;right:0;top:0;height:720px;background:url({photo('10-group-campus.jpg')}) center 30%/cover"></div>
<div style="position:absolute;left:0;right:0;top:600px;height:120px;background:linear-gradient(transparent,#6E1F2F)"></div>
<div class="rule" style="position:absolute;left:0;right:0;top:716px"></div>
<div style="position:absolute;left:80px;right:80px;top:770px">
  <div class="caps gold" style="font-size:30px;letter-spacing:.3em">SESSION 2027–28</div>
  <div class="disp linen" style="font-size:118px;line-height:1;margin-top:18px">Admissions open</div>
  <div class="linen" style="font-size:36px;margin-top:22px;opacity:.92">Grade 3 to O Level · Cambridge curriculum</div>
  <div class="ur gold" lang="ur" dir="rtl" style="font-size:46px;line-height:2;text-align:left;margin-top:6px">ادب پہلا قرینہ ہے</div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px">
    <span class="pill" style="font-size:30px;padding:16px 34px">+92 41 [number]</span>
    <div style="width:330px">{H_REV}</div>
  </div>
</div>""")

# 2. Square post — Value of the month
T["02-post-value-of-month"] = (1080, 1080, f"""
<div class="claret" style="position:absolute;inset:0"></div>
<div class="frame" style="inset:40px"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:110px 120px 0">
  <div style="height:120px">{CREST_REV}</div>
  <div class="caps gold" style="font-size:28px;letter-spacing:.34em;margin-top:34px;padding-left:.34em">VALUE OF THE MONTH</div>
  <div class="disp linen" style="font-size:170px;line-height:1;margin-top:20px">Adab</div>
  <div class="ur gold" lang="ur" dir="rtl" style="font-size:54px;line-height:1.9">ادب</div>
  <div class="linen" style="font-size:34px;line-height:1.45;margin-top:14px;opacity:.92">Good manners and respect: in how we speak, listen and treat every person.</div>
  <div class="ar gold" lang="ar" dir="rtl" style="font-size:52px;margin-top:34px">وَقُولُوا لِلنَّاسِ حُسْنًا</div>
  <div class="linen" style="font-size:26px;margin-top:8px;opacity:.8">"And speak to people good words." · Al-Baqarah 2:83</div>
</div>""")

# 3. Portrait post — Student achievement
T["03-post-achievement"] = (1080, 1350, f"""
<div style="position:absolute;inset:0;background:#F5EEE6"></div>
<div style="position:absolute;left:80px;top:80px;width:560px;height:840px;background:url({photo('04-olevel-boy-winter.jpg')}) center 12%/cover;border-radius:8px"></div>
<div style="position:absolute;left:80px;top:80px;width:560px;height:840px;border:4px solid #C9A962;border-radius:8px;transform:translate(22px,22px)"></div>
<div style="position:absolute;left:700px;top:96px;width:300px">
  <div style="height:150px">{CREST}</div>
  <div class="caps" style="font-size:24px;letter-spacing:.28em;color:#6E1F2F;margin-top:40px">PROUD MOMENT</div>
  <div class="disp" style="font-size:76px;line-height:1;margin-top:18px;color:#6E1F2F">Mabrook!</div>
  <div class="disp" style="font-size:44px;line-height:1.15;margin-top:30px;color:#2A1418">[Student name]</div><div style="font-size:30px;margin-top:10px;color:#4A3A3C">Grade [ ]</div>
</div>
<div class="claret" style="position:absolute;left:0;right:0;bottom:0;height:330px"></div>
<div class="rule" style="position:absolute;left:0;right:0;bottom:330px"></div>
<div style="position:absolute;left:80px;right:80px;bottom:70px">
  <div class="disp linen" style="font-size:64px;line-height:1.08">[Achievement, e.g. First place, Inter-school Science Olympiad]</div>
  <div class="caps gold" style="font-size:24px;letter-spacing:.3em;margin-top:24px">ADABURY SCHOOL · FAISALABAD</div>
</div>""")

# 4. Square post — Event
T["04-post-event"] = (1080, 1080, f"""
<div style="position:absolute;left:0;top:0;bottom:0;width:470px;background:url({photo('08-boy-pe.jpg')}) center 20%/cover"></div>
<div class="claret" style="position:absolute;left:470px;top:0;right:0;bottom:0"></div>
<div class="rule" style="position:absolute;left:470px;top:0;bottom:0;width:8px;height:auto"></div>
<div style="position:absolute;left:540px;right:70px;top:90px">
  <div style="height:96px">{CREST_REV}</div>
  <div class="caps gold" style="font-size:26px;letter-spacing:.3em;margin-top:40px">YOU ARE INVITED</div>
  <div class="disp linen" style="font-size:104px;line-height:.98;margin-top:16px">[Annual Sports Day]</div>
  <div style="margin-top:44px;display:grid;gap:22px">
    <div><div class="caps gold" style="font-size:20px;letter-spacing:.24em">DATE</div><div class="linen" style="font-size:36px">[Saturday, 12 February]</div></div>
    <div><div class="caps gold" style="font-size:20px;letter-spacing:.24em">TIME</div><div class="linen" style="font-size:36px">[9:00 am]</div></div>
    <div><div class="caps gold" style="font-size:20px;letter-spacing:.24em">VENUE</div><div class="linen" style="font-size:36px">[School grounds]</div></div>
  </div>
</div>""")

# 5. Square post — Notice (bilingual, linen)
T["05-post-notice"] = (1080, 1080, f"""
<div style="position:absolute;inset:0;background:#F5EEE6"></div>
<div class="claret" style="position:absolute;left:0;right:0;top:0;height:190px"></div>
<div class="rule" style="position:absolute;left:0;right:0;top:190px"></div>
<div style="position:absolute;left:70px;top:48px;width:400px">{H_REV}</div>
<div class="caps gold" style="position:absolute;right:70px;top:78px;font-size:30px;letter-spacing:.3em">NOTICE</div>
<div style="position:absolute;left:90px;right:90px;top:280px">
  <div class="disp" style="font-size:96px;line-height:1;color:#6E1F2F">[School closed for Eid-ul-Adha]</div>
  <div style="font-size:38px;margin-top:34px;color:#2A1418">[Day, date] to [day, date]</div>
  <div style="font-size:34px;margin-top:10px;color:#4A3A3C">Classes resume on [day, date].</div>
  <div style="height:3px;background:#C9A962;margin:48px 0 18px;width:180px"></div>
  <div class="ur" lang="ur" dir="rtl" style="font-size:44px;line-height:2;color:#6E1F2F">عید الاضحیٰ کی تعطیلات</div>
  <div class="ur" lang="ur" dir="rtl" style="font-size:34px;line-height:2;color:#4A3A3C">تاریخ ____ سے ____ تک</div>
</div>
<div style="position:absolute;left:90px;bottom:60px;font-size:26px;color:#6F5F60">adabury.edu.pk · +92 41 [number]</div>""")

# 6. Story / WhatsApp status 9:16 — Admissions
T["06-story-admissions"] = (1080, 1920, f"""
<div class="claret" style="position:absolute;inset:0"></div>
<div style="position:absolute;left:0;right:0;top:300px;bottom:0;background:url({photo('03-senior-girl-winter-hijab.jpg')}) center 8%/cover"></div>
<div class="rule" style="position:absolute;left:0;right:0;top:294px"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:1150px;background:linear-gradient(transparent,#6E1F2F 34%)"></div>
<div style="position:absolute;left:0;right:0;top:80px;display:flex;justify-content:center"><div style="width:520px">{H_REV}</div></div>
<div style="position:absolute;left:90px;right:90px;bottom:180px">
  <div class="caps gold" style="font-size:32px;letter-spacing:.3em">SESSION 2027–28</div>
  <div class="disp linen" style="font-size:150px;line-height:.95;margin-top:20px">Admissions<br>open</div>
  <div class="linen" style="font-size:42px;margin-top:30px;line-height:1.4;opacity:.95">Grade 3 to O Level<br>Cambridge curriculum · Character comes first</div>
  <div class="ur gold" lang="ur" dir="rtl" style="font-size:58px;line-height:2;text-align:left;margin-top:10px">ادب پہلا قرینہ ہے</div>
  <span class="pill" style="font-size:38px;padding:22px 46px;margin-top:20px">Book a campus visit</span>
</div>""")

# 7. Facebook cover 1640 x 624 (safe area centred)
T["07-facebook-cover"] = (1640, 624, f"""
<div class="claret" style="position:absolute;inset:0"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:900px;background:url({photo('10-group-campus.jpg')}) center 35%/cover"></div>
<div style="position:absolute;right:900px;top:0;bottom:0;width:240px;background:linear-gradient(90deg,#6E1F2F,transparent);transform:translateX(240px)"></div>
<div class="rule" style="position:absolute;left:0;right:0;bottom:0;height:10px"></div>
<div style="position:absolute;left:300px;top:150px;width:520px">
  <div style="width:460px">{H_REV}</div>
  <div class="disp linen" style="font-size:58px;line-height:1.05;margin-top:40px">Character comes first.</div>
  <div class="ur gold" lang="ur" dir="rtl" style="font-size:38px;line-height:2;text-align:left">ادب پہلا قرینہ ہے</div>
</div>""")

# 8. YouTube thumbnail 1280 x 720
T["08-youtube-thumbnail"] = (1280, 720, f"""
<div style="position:absolute;inset:0;background:url({photo('10-group-campus.jpg')}) center 40%/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#6E1F2F 0%,rgba(110,31,47,.92) 42%,rgba(110,31,47,0) 72%)"></div>
<div style="position:absolute;left:64px;top:60px;height:110px">{CREST_REV}</div>
<div style="position:absolute;left:64px;top:220px;width:640px">
  <div class="disp linen" style="font-size:112px;line-height:.95">[A day at Adabury]</div>
  <div class="caps gold" style="font-size:28px;letter-spacing:.28em;margin-top:28px">[CAMPUS TOUR · 4 MIN]</div>
</div>
<div class="rule" style="position:absolute;left:0;right:0;bottom:0;height:12px"></div>""")

for name, (w, h, body) in T.items():
    (OUT / f"{name}.html").write_text(f'<!doctype html><meta charset="utf-8">{FONTS}{CSS % (w, h)}<body>{body}</body>')
    print(name, w, h)
