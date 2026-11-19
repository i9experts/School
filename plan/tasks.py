#!/usr/bin/env python3
"""Master launch plan for Adabury School, Faisalabad: every task to open well in April 2028
and run a strong first year. Writes tasks.json (seed data for the tracker's database).

Fields: id, ws (workstream), title, note, owner, due (YYYY-MM), pri (High/Medium/Low),
status (Not started / In progress / Done / Blocked), claude (True if Claude can draft it).
"""
import json
from pathlib import Path

WS = [
    ("strategy", "Strategy and funding"),
    ("legal", "Legal and governance"),
    ("site", "Site and building"),
    ("reg", "Registration and accreditation"),
    ("acad", "Academics and Tarbiyah"),
    ("people", "People and HR"),
    ("brand", "Brand rollout"),
    ("admit", "Admissions and marketing"),
    ("tech", "Technology and systems"),
    ("ops", "Operations and safety"),
    ("parents", "Parents and community"),
    ("year1", "First year and growth"),
]

T = []


def t(ws, title, owner, due, pri="Medium", note="", status="Not started", claude=False):
    n = sum(1 for x in T if x["ws"] == ws) + 1
    T.append(dict(id=f"{ws}-{n:02d}", ws=ws, title=title, note=note, owner=owner, due=due, pri=pri,
                  status=status, claude=claude))


# 1 Strategy and funding
t("strategy", "Brand name, logo and identity", "Founder", "2026-11", "High", "Adabury School; Ghanta Ghar crest approved.", "Done", True)
t("strategy", "Feasibility study, financial model and investor deck", "Founder", "2026-11", "High", "Base case: profit from Year 3, payback Year 8, peak need PKR 20.8 crore.", "Done", True)
t("strategy", "Update the model with real salaries from the Karachi branches", "Founder", "2026-12", "High", "Replace the assumed PKR 75,000 average teacher salary.", claude=True)
t("strategy", "Confirm competitor fees by calling Beaconhouse, LGS and Roots Faisalabad", "Founder", "2026-12", "High", "Published figures come from unofficial guides.")
t("strategy", "Approve the 2028 fee schedule", "Founder", "2027-01", "High", "Proposed PKR 19,500 / 23,000 / 27,500 a month, plus admission and annual charges.", claude=True)
t("strategy", "Choose the funding plan for the PKR 10.8 crore gap", "Founder", "2027-01", "High", "Ijarah for equipment, landlord fit-out, stepped rent, partner or bank facility.")
t("strategy", "Get Ijarah quotes for AC, solar and IT from two Islamic banks", "Bursar", "2027-03", "High")
t("strategy", "Open the school's bank accounts and a fee-collection account", "Founder", "2027-02", "Medium")
t("strategy", "Set the year-by-year budget and approval limits", "Bursar", "2027-04", "Medium", claude=True)
t("strategy", "Choose an accounting system and chart of accounts", "Bursar", "2027-06", "Medium", claude=True)
t("strategy", "Insurance: property, public liability, student accident", "Bursar", "2028-02", "Medium")

# 2 Legal and governance
t("legal", "Confirm the legal structure with a tax adviser", "Founder", "2026-12", "High", "Private limited company, AOP or Section 42 non-profit.")
t("legal", "Register the company with SECP, NTN with FBR", "Founder", "2027-01", "High")
t("legal", "File trademarks for the Adabury name and crest with IPO Pakistan", "Founder", "2027-01", "High", "Name and crest, in classes for education and printed matter.")
t("legal", "Register domains (adabury.pk, adabury.com) and apply for adabury.edu.pk", "Founder", "2026-12", "High", ".edu.pk needs PKNIC approval once registered.")
t("legal", "Reserve @adaburyschool on Instagram, Facebook, YouTube, TikTok, WhatsApp Business", "Admissions", "2026-12", "High")
t("legal", "Appoint the Board of Governors", "Founder", "2027-03", "High", "Founder (chair), 2 educators, a chartered accountant, a Shariah scholar; parent from Year 2.")
t("legal", "Appoint the Shariah and Tarbiyah advisory council", "Founder", "2027-04", "Medium")
t("legal", "Board charter, committee terms and meeting calendar", "Board", "2027-04", "Medium", claude=True)
t("legal", "Policy pack: admissions and fees, safeguarding, conduct, uniform, complaints, data protection, health and safety", "Principal", "2027-11", "High", claude=True)
t("legal", "Staff employment contract and staff handbook", "Bursar", "2027-10", "High", claude=True)
t("legal", "Parent agreement: fees, refunds, photo consent, code of conduct", "Principal", "2027-08", "High", claude=True)

# 3 Site and building
t("site", "Shortlist 3-5 buildings of 6-8 kanal on the Canal Road belt", "Founder", "2027-03", "High", "Two separate entrances, off-road drop-off, room for 36 classrooms.")
t("site", "Building due diligence: title, FDA approval for school use, structure, power", "Consultant", "2027-04", "High")
t("site", "Negotiate the 10-year lease", "Founder", "2027-05", "High", "Capped increases, rent-free fit-out months, stepped rent, landlord fit-out, first right to buy.", claude=True)
t("site", "Sign the lease", "Founder", "2027-06", "High")
t("site", "Architect: two-block layout, prayer halls, labs, washrooms, accessibility", "Consultant", "2027-06", "High")
t("site", "Fit-out tender and contractor selection", "Bursar", "2027-07", "High")
t("site", "Fit-out works (phase 1: Grades 3-9)", "Contractor", "2027-12", "High")
t("site", "Air conditioning and solar installation", "Contractor", "2027-12", "Medium")
t("site", "Science and computer labs (one each per block)", "Contractor", "2028-02", "Medium")
t("site", "Furniture, smart boards and library fit-out", "Bursar", "2028-02", "Medium")
t("site", "Signage production and installation (gate, facade, reception, wayfinding)", "Bursar", "2028-02", "Medium", "Artwork ready in brand/signage.", claude=True)
t("site", "Phase 2 fit-out for Grades 10-11 and second sections", "Bursar", "2029-02", "Low")

# 4 Registration and accreditation
t("reg", "Hire a local registration consultant", "Founder", "2027-03", "High")
t("reg", "Register the school with the Punjab education authorities (District Education Authority Faisalabad)", "Consultant", "2027-10", "High")
t("reg", "Apply to become a Cambridge International school", "Principal", "2027-07", "High", "Approval can take several months; needs the building and leadership in place.")
t("reg", "Confirm the current Punjab rule on annual fee increases", "Consultant", "2027-03", "High")
t("reg", "Fire safety, building safety and health certificates", "Consultant", "2028-02", "High")
t("reg", "Register staff with EOBI and Punjab social security", "Bursar", "2027-12", "Medium")
t("reg", "Cambridge exam centre approval (for Checkpoint and O Level)", "Principal", "2029-01", "Medium")

# 5 Academics and Tarbiyah
t("acad", "Curriculum map Grades 3-11: Cambridge plus Punjab requirements (Urdu, Islamiyat, Pakistan Studies)", "Principal", "2027-10", "High", claude=True)
t("acad", "Tarbiyah framework: Quran, Arabic, Seerah, six values, mentoring", "Head of Tarbiyah", "2027-11", "High", claude=True)
t("acad", "Finalise the six character values and their rubrics", "Head of Tarbiyah", "2027-10", "High", "Adab, Amanah, Ihsan, Sabr, Shukr, Khidmah (proposed).", claude=True)
t("acad", "Optional Hifz track: model, timings, teachers", "Head of Tarbiyah", "2027-12", "Medium", claude=True)
t("acad", "Timetable for both blocks, including Zuhr and Tarbiyah periods", "Principal", "2028-02", "High", claude=True)
t("acad", "Choose textbooks and resources; book list for parents", "Principal", "2027-12", "High")
t("acad", "Assessment policy: entry tests, termly exams, Character Record", "Principal", "2027-11", "High", claude=True)
t("acad", "Entry assessment papers for Grades 3-9", "Principal", "2027-09", "High", claude=True)
t("acad", "Schemes of work for the first term", "Coordinators", "2028-03", "High")
t("acad", "Library: starter collection in English, Urdu and Islamic books", "Principal", "2028-02", "Medium", claude=True)
t("acad", "Co-curricular plan: clubs, debating, sports, service learning, houses", "Principal", "2028-02", "Medium", claude=True)
t("acad", "Student support: counselling and learning support approach", "Principal", "2028-01", "Medium", claude=True)

# 6 People and HR
t("people", "Organisation chart and job descriptions for every role", "Founder", "2027-03", "High", claude=True)
t("people", "Salary bands and benefits", "Founder", "2027-04", "High", claude=True)
t("people", "Recruit the Principal", "Founder", "2027-08", "High", "Cambridge leadership experience; starts November 2027.")
t("people", "Recruit the Head of Girls' Block and Head of Boys' Block", "Principal", "2027-10", "High")
t("people", "Recruit the Head of Tarbiyah", "Founder", "2027-10", "High")
t("people", "Recruit the Bursar and admissions officers", "Principal", "2027-09", "High")
t("people", "Recruit about 29 teachers (more women for the girls' block)", "Principal", "2028-01", "High", "Advertise from November 2027; include Lahore with relocation support.")
t("people", "Recruit support staff: guards, cleaners, nurses, lab assistants", "Bursar", "2028-02", "Medium")
t("people", "Teacher interview tasks and demonstration-lesson rubric", "Principal", "2027-10", "Medium", claude=True)
t("people", "Two-week induction and Cambridge training before opening", "Principal", "2028-03", "High", claude=True)
t("people", "Staff appraisal and professional development plan", "Principal", "2028-04", "Medium", claude=True)
t("people", "Safe recruitment: police checks and references for every staff member", "Bursar", "2028-03", "High")

# 7 Brand rollout
t("brand", "Uniform design (no tie; compulsory hijab for girls)", "Founder", "2026-11", "High", status="Done", claude=True)
t("brand", "Stationery design", "Founder", "2026-11", "Medium", status="Done", claude=True)
t("brand", "Signage design", "Founder", "2026-11", "Medium", status="Done", claude=True)
t("brand", "Social media templates and playbook", "Founder", "2026-11", "Medium", status="Done", claude=True)
t("brand", "Fill real contact details; print-ready stationery PDFs and Word templates", "Admissions", "2027-07", "Medium", claude=True)
t("brand", "Choose the uniform supplier: samples, prices, sizes, school shop", "Bursar", "2027-10", "High")
t("brand", "Real photo shoot to replace the AI visuals", "Admissions", "2028-04", "Medium", "Once uniforms and the building are ready.")
t("brand", "Brand guidelines handbook for staff and printers", "Admissions", "2027-06", "Low", claude=True)

# 8 Admissions and marketing
t("admit", "Website: home, Cambridge and Tarbiyah, fees, admissions form, contact", "Admissions", "2027-08", "High", claude=True)
t("admit", "Prospectus (print and PDF)", "Admissions", "2027-08", "High", claude=True)
t("admit", "Admissions process: enquiry, campus visit, entry test, interview, offer", "Admissions", "2027-07", "High", claude=True)
t("admit", "Founding-family offer and sibling discount rules", "Founder", "2027-07", "High", claude=True)
t("admit", "Launch marketing plan and budget (PKR 1.5 crore)", "Admissions", "2027-07", "High", claude=True)
t("admit", "Admissions open: billboards, digital ads, WhatsApp campaign", "Admissions", "2027-09", "High")
t("admit", "Open days: three rounds, September 2027 to January 2028", "Principal", "2028-01", "High", claude=True)
t("admit", "Enquiry tracker (CRM) and weekly admissions report", "Admissions", "2027-08", "High", claude=True)
t("admit", "Target: 300 students confirmed with deposits", "Admissions", "2028-02", "High", "Base case Year 1. Every 50 extra students improves funding by about PKR 1.5-2 crore.")
t("admit", "Referral programme with community and mosque networks", "Admissions", "2027-10", "Medium", claude=True)
t("admit", "Launch PR: press release, founder interview, launch event", "Founder", "2027-09", "Medium", claude=True)

# 9 Technology and systems
t("tech", "School management system: admissions, attendance, fees, report cards", "Bursar", "2027-09", "High")
t("tech", "Fee collection: bank challans, online payment, receipts", "Bursar", "2028-01", "High")
t("tech", "Parent app or WhatsApp Business broadcast setup", "Admissions", "2028-02", "Medium")
t("tech", "Campus network, Wi-Fi, CCTV and access control", "IT officer", "2028-02", "Medium")
t("tech", "Email and document system for staff (Google Workspace for Education or Microsoft 365)", "IT officer", "2027-11", "Medium")
t("tech", "Student ID cards with QR codes for gate attendance", "IT officer", "2028-03", "Medium", "Design ready in brand/stationery.")

# 10 Operations and safety
t("ops", "Transport contractor: routes, Adabury-branded vans, female attendants, safety checks", "Bursar", "2028-01", "High")
t("ops", "Security plan: guards, visitor policy, separate block entrances", "Bursar", "2028-02", "High", claude=True)
t("ops", "Health room and nurse in each block; first-aid training", "Principal", "2028-03", "Medium")
t("ops", "Canteen or lunch policy (healthy food)", "Bursar", "2028-03", "Low")
t("ops", "Emergency plans: fire drill, heat, earthquake, lockdown", "Principal", "2028-03", "High", claude=True)
t("ops", "Cleaning and maintenance schedule", "Bursar", "2028-03", "Low")
t("ops", "School calendar 2028-29: terms, holidays, exams, events", "Principal", "2028-01", "High", claude=True)

# 11 Parents and community
t("parents", "Parent orientation day and parent handbook", "Principal", "2028-03", "High", claude=True)
t("parents", "Monthly parent newsletter and Value of the month", "Admissions", "2028-04", "Medium", claude=True)
t("parents", "Parent-teacher meetings each term", "Principal", "2028-06", "Medium")
t("parents", "Parent council (from Year 1) and a parent seat on the Board (Year 2)", "Principal", "2028-09", "Low")
t("parents", "Community service partners (hospitals, orphanages, mosques)", "Head of Tarbiyah", "2028-08", "Low")

# 12 First year and growth
t("year1", "Opening day: Grades 3-9 in both blocks", "Principal", "2028-04", "High")
t("year1", "Monthly dashboard: enrolment, fee collection, attendance, cash", "Bursar", "2028-05", "High", claude=True)
t("year1", "Parent and staff satisfaction surveys each term", "Principal", "2028-07", "Medium", claude=True)
t("year1", "Board review against the budget each quarter", "Board", "2028-07", "High")
t("year1", "Admissions for 2029-30: target 450 students", "Admissions", "2028-12", "High")
t("year1", "First Cambridge Checkpoint results (Grade 8) and review", "Principal", "2029-05", "Medium")
t("year1", "Year 1 review and update of the financial model", "Founder", "2029-03", "High", claude=True)

out = {"workstreams": [{"id": a, "name": b} for a, b in WS], "tasks": T}
Path(__file__).with_name("tasks.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
from collections import Counter
print(len(T), "tasks", Counter(x["ws"] for x in T), Counter(x["status"] for x in T), sum(x["claude"] for x in T), "Claude can draft")
