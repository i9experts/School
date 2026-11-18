#!/usr/bin/env python3
"""Build the Adabury School Faisalabad financial model (formula-driven Excel workbook).

Output: feasibility/Adabury_Faisalabad_Financial_Model.xlsx
Run scripts/recalc.py (xlsx skill) afterwards to compute cached values.

Structure
  Read Me        legend and how to use
  Assumptions    every input (blue), scenario selector, scenario levers, staff table
  Enrolment      base-case students by year and grade band, O Level grades open
  Capex          start-up investment items
  Calc           full calculation, three identical blocks: Worst, Base, Best
  Profit and Loss, Cash Flow   selected scenario, PKR million
  Summary        key results for all three scenarios side by side
Columns C..M are Y0 (pre-opening, 2027-28) and Y1..Y10 (2028-29 .. 2037-38) on every
time-based sheet.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parents[1] / "Adabury_Faisalabad_Financial_Model.xlsx"

F = "Arial"
BLUE = Font(name=F, color="0000FF")
BLACK = Font(name=F, color="000000")
GREEN = Font(name=F, color="008000")
BOLD = Font(name=F, bold=True)
TITLE = Font(name=F, bold=True, size=14, color="6E1F2F")
HEAD = Font(name=F, bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="6E1F2F")
SECT_FILL = PatternFill("solid", fgColor="F3ECE4")
KEY_FILL = PatternFill("solid", fgColor="FFFF00")
THIN = Side(style="thin", color="C9A962")
TOP = Border(top=THIN)

PKR = '#,##0;(#,##0);"-"'
PKRM = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
NUM = '#,##0;(#,##0);"-"'

YEARS = ["Y0 2027-28\n(pre-opening)"] + [f"Y{i} {2027 + i}-{str(2028 + i)[-2:]}" for i in range(1, 11)]
COLS = [get_column_letter(3 + t) for t in range(11)]  # C..M
SCEN = ["Worst", "Base", "Best"]

wb = Workbook()


def style_ws(ws, widths):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.sheet_view.showGridLines = False


def header_row(ws, row, first_label="", unit_label=""):
    ws.cell(row=row, column=1, value=first_label).font = HEAD
    ws.cell(row=row, column=2, value=unit_label).font = HEAD
    for t, y in enumerate(YEARS):
        c = ws.cell(row=row, column=3 + t, value=y)
        c.font = HEAD
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for col in range(1, 14):
        ws.cell(row=row, column=col).fill = HEAD_FILL
    ws.row_dimensions[row].height = 30


# ----------------------------------------------------------------------------- Read Me
rm = wb.active
rm.title = "Read Me"
style_ws(rm, {"A": 3, "B": 110})
lines = [
    ("Adabury School, Faisalabad: financial feasibility model", TITLE),
    ("Prepared November 2026 for the Board. All money in Pakistani rupees (PKR). Academic year runs April to March.", BLACK),
    ("", BLACK),
    ("How to use", BOLD),
    ("1. Change any blue number on the Assumptions, Enrolment or Capex sheets. Everything else recalculates.", BLACK),
    ("2. Pick the scenario to show on the Profit and Loss and Cash Flow sheets with the selector on Assumptions (cell C5): 1 = Worst, 2 = Base, 3 = Best.", BLACK),
    ("3. The Summary sheet always shows all three scenarios side by side.", BLACK),
    ("", BLACK),
    ("Colour legend", BOLD),
    ("Blue text = input you can change.  Black text = formula.  Green text = link from another sheet.  Yellow fill = key assumption to review first.", BLACK),
    ("", BLACK),
    ("Timeline", BOLD),
    ("Y0 (2027-28) is the pre-opening year: lease, fit-out, hiring and launch marketing. Y1 (2028-29) is the first teaching year, opening April 2028.", BLACK),
    ("", BLACK),
    ("Campus concept", BOLD),
    ("One leased building on the Canal Road belt with two fully separate blocks (girls' block and boys' block), Grades 3 to O Level, Cambridge curriculum with the Adabury Tarbiyah programme.", BLACK),
    ("", BLACK),
    ("Important limits of this model", BOLD),
    ("Market figures (competitor fees, rents, salaries) come from public listings and guides, not quotes. Replace them with real quotes before signing a lease.", BLACK),
    ("Tax is a simple corporate-tax estimate with losses carried forward. Confirm the legal structure (company, AOP or Section 42 non-profit) and tax treatment with a tax adviser.", BLACK),
    ("Transport is outsourced to a contractor paid by parents, so it is excluded from both revenue and cost.", BLACK),
]
for i, (txt, font) in enumerate(lines, start=2):
    c = rm.cell(row=i, column=2, value=txt)
    c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")

# ----------------------------------------------------------------------------- Assumptions
A = {}
asm = wb.create_sheet("Assumptions")
style_ws(asm, {"A": 3, "B": 52, "C": 16, "D": 16, "E": 16, "F": 70})
asm["B2"] = "Assumptions (all inputs)"
asm["B2"].font = TITLE

r = 4
asm.cell(row=r, column=2, value="Scenario selector").font = BOLD
r = 5
asm.cell(row=r, column=2, value="Scenario shown on P&L and Cash Flow (1 Worst, 2 Base, 3 Best)").font = BLACK
c = asm.cell(row=r, column=3, value=2)
c.font = BLUE
c.fill = KEY_FILL
A["sel"] = "Assumptions!$C$5"
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="3", allow_blank=False)
asm.add_data_validation(dv)
dv.add("C5")
asm.cell(row=r, column=4, value='=CHOOSE(C5,"Worst","Base","Best")').font = BLACK

# scenario levers
r = 7
asm.cell(row=r, column=2, value="Scenario levers").font = BOLD
for j, s in enumerate(SCEN):
    cc = asm.cell(row=r, column=3 + j, value=s)
    cc.font = HEAD
    cc.fill = HEAD_FILL
    cc.alignment = Alignment(horizontal="center")
levers = [
    ("enr_mult", "Enrolment versus base plan", [0.80, 1.00, 1.12], PCT, "Worst: slower word of mouth. Best: strong launch."),
    ("fee_mult", "Fee level versus base fees", [0.95, 1.00, 1.05], PCT, "Worst: launch discounts needed to fill seats."),
    ("sal_mult", "Salary level versus base salaries", [1.05, 1.00, 1.00], PCT, "Worst: harder to recruit Cambridge-trained teachers."),
    ("rent_mult", "Rent versus base rent", [1.15, 1.00, 0.95], PCT, "Worst: larger or pricier building than planned."),
]
for k, (key, label, vals, fmt, note) in enumerate(levers):
    rr = r + 1 + k
    asm.cell(row=rr, column=2, value=label).font = BLACK
    for j, v in enumerate(vals):
        cc = asm.cell(row=rr, column=3 + j, value=v)
        cc.font = BLUE
        cc.number_format = fmt
    asm.cell(row=rr, column=6, value=note).font = BLACK
    A[key] = [f"Assumptions!${get_column_letter(3 + j)}${rr}" for j in range(3)]

r = 13
scalars = [
    ("Campus and classes", None, None, None, None),
    ("blocks", "Blocks (girls' block and boys' block)", 2, NUM, "Two fully separate blocks in one building."),
    ("grades_band", "Grades per band (Junior 3-5, Middle 6-8, O Level 9-11)", 3, NUM, ""),
    ("max_sec", "Maximum sections per grade per block", 2, NUM, "Sets the building size: 9 grades x 2 blocks x 2 sections = 36 classrooms."),
    ("class_size", "Maximum class size", 25, NUM, "Premium positioning: no class above 25."),
    ("target_fill", "Planning fill per section (students)", 22, NUM, "A new section is opened when classes average 22."),
    ("Fees (monthly, at April 2028 prices)", None, None, None, None),
    ("fee_j", "Tuition: Junior (Grades 3-5), PKR per month", 19500, PKR, "Owner's band PKR 15-25k. Top-tier Faisalabad schools reported at PKR 30-45k (third-party guides, 2025)."),
    ("fee_m", "Tuition: Middle (Grades 6-8), PKR per month", 23000, PKR, ""),
    ("fee_o", "Tuition: O Level (Grades 9-11), PKR per month", 27500, PKR, ""),
    ("months", "Tuition months billed per year", 12, NUM, "Market practice in Pakistan: 12 monthly fees including summer."),
    ("adm_fee", "Admission fee, one-time per new student", 50000, PKR, ""),
    ("ann_fee", "Annual charges per student (resources, exams admin, activities)", 20000, PKR, ""),
    ("other_inc", "Other income per student per year (uniform and books margin)", 3000, PKR, ""),
    ("discount", "Sibling discounts and scholarships (share of tuition)", 0.08, PCT, ""),
    ("collection", "Fee collection rate", 0.95, PCT, ""),
    ("attrition", "Students leaving each year (share of last year's roll)", 0.07, PCT, "Used to work out new admissions."),
    ("fee_inc", "Annual fee increase", 0.07, PCT, "Punjab rules reported as 5% normally, up to 8% with permission for fees above PKR 4,000/month (Dawn, ARY). Confirm current rules."),
    ("Staff", None, None, None, None),
    ("t_per_sec", "Class and subject teachers per section", 1.3, '0.00', "Covers subject specialists in Middle and O Level."),
    ("stud_per_spec", "Students per specialist teacher (Quran, Arabic, PE, art, counselling)", 80, NUM, ""),
    ("min_spec", "Minimum specialist teachers", 8, NUM, "Separate Quran and PE teachers for each block."),
    ("t_salary", "Average teacher salary, PKR per month (2028)", 75000, PKR, "Lahore O Level posts advertised at PKR 50-70k for juniors and higher for experienced staff (job listings, 2025)."),
    ("pay_months", "Salary payments per year (12 + 1 Eid bonus)", 13, NUM, ""),
    ("benefits", "Employer costs on salaries (EOBI, social security, health)", 0.10, PCT, ""),
    ("sal_inc", "Annual salary increase", 0.08, PCT, ""),
    ("pre_t_months", "Pre-opening teacher months (training before opening)", 1, NUM, ""),
    ("pre_l_months", "Pre-opening months for core leadership team", 5, NUM, "Principal and core team join about November 2027."),
    ("Premises and running costs (2028 prices)", None, None, None, None),
    ("rent", "Building rent, PKR per month", 2000000, PKR, "6-8 kanal two-block building, Canal Road belt. Listings: 1-2 kanal buildings around PKR 3.5-8 lakh (Zameen, 2025)."),
    ("rent_esc", "Annual rent increase", 0.10, PCT, "Typical Pakistani lease clause."),
    ("pre_rent_months", "Rent months paid before opening (fit-out period)", 4, NUM, "Assumes 2 rent-free months negotiated in a 6-month fit-out."),
    ("deposit_months", "Security deposit, months of rent (refundable)", 6, NUM, ""),
    ("util", "Electricity, gas, water and internet, PKR per month", 600000, PKR, "After solar savings. Faisalabad summers need heavy air conditioning."),
    ("infl", "General cost inflation per year", 0.08, PCT, ""),
    ("mkt_launch", "Launch marketing in Y0", 15000000, PKR, "Billboards, digital, open days, Karachi-quality brand launch."),
    ("mkt_pct", "Ongoing marketing, share of revenue", 0.03, PCT, ""),
    ("mkt_min", "Ongoing marketing minimum per year", 5000000, PKR, ""),
    ("materials", "Teaching materials and consumables per student per year", 8000, PKR, ""),
    ("events", "Tarbiyah programmes, events and trips per student per year", 3000, PKR, ""),
    ("it", "IT, software and school system licences per year", 1500000, PKR, ""),
    ("insurance", "Insurance and security systems per year", 800000, PKR, ""),
    ("maint", "Repairs and maintenance per year", 2500000, PKR, ""),
    ("admin_misc", "Administration, printing, legal and audit per year", 2000000, PKR, ""),
    ("cpd", "Teacher training, Cambridge membership and CPD (share of payroll)", 0.02, PCT, ""),
    ("pre_other", "Registration, legal, Cambridge approval and recruitment (Y0)", 4500000, PKR, ""),
    ("Investment, tax and returns", None, None, None, None),
    ("equity", "Owner's investment (cash put in at the start)", 100000000, PKR, "Owner's stated range PKR 8-12 crore."),
    ("life", "Useful life of fit-out and equipment (years)", 10, NUM, "Matched to a 10-year lease."),
    ("repl", "Yearly equipment replacement, share of initial capex (from Y2)", 0.03, PCT, ""),
    ("tax", "Corporate tax rate on profit", 0.29, PCT, "Simplified. Confirm structure and tax with an adviser."),
    ("disc", "Discount rate for NPV (owner's required return)", 0.16, PCT, ""),
]
for key, label, val, fmt, note in scalars:
    r += 1
    if label is None:
        r += 1
        asm.cell(row=r, column=2, value=key).font = BOLD
        continue
    asm.cell(row=r, column=2, value=label).font = BLACK
    cc = asm.cell(row=r, column=3, value=val)
    cc.font = BLUE
    cc.number_format = fmt
    if key in ("fee_j", "fee_m", "fee_o", "rent", "t_salary", "equity"):
        cc.fill = KEY_FILL
    asm.cell(row=r, column=6, value=note).font = BLACK
    A[key] = f"Assumptions!$C${r}"

# staff table
r += 2
asm.cell(row=r, column=2, value="Leadership and support staff (PKR per month, 2028)").font = BOLD
r += 1
for j, h in enumerate(["Role", "Number", "Salary each", "Joins before opening? (1 = yes)"]):
    cc = asm.cell(row=r, column=2 + j, value=h)
    cc.font = HEAD
    cc.fill = HEAD_FILL
    cc.alignment = Alignment(wrap_text=True)
staff = [
    ("Principal", 1, 450000, 1), ("Head of Girls' Block", 1, 250000, 1), ("Head of Boys' Block", 1, 250000, 1),
    ("Head of Tarbiyah", 1, 180000, 1), ("Cambridge academic coordinators", 2, 150000, 1),
    ("Admissions and marketing officers", 2, 80000, 1), ("Accounts and HR", 3, 75000, 1),
    ("IT and exams officers", 2, 70000, 0), ("Front office and administration", 4, 50000, 0),
    ("Nurses (one per block)", 2, 55000, 0), ("Lab assistants", 2, 45000, 0),
    ("Security guards", 8, 42000, 0), ("Cleaning and maintenance staff", 14, 40000, 0),
]
s0 = r + 1
for name, n, sal, pre in staff:
    r += 1
    asm.cell(row=r, column=2, value=name).font = BLACK
    for j, v in enumerate([n, sal, pre]):
        cc = asm.cell(row=r, column=3 + j, value=v)
        cc.font = BLUE
        cc.number_format = PKR if j == 1 else NUM
s1 = r
r += 1
asm.cell(row=r, column=2, value="Total monthly payroll, all leadership and support staff").font = BOLD
asm.cell(row=r, column=4, value=f"=SUMPRODUCT(C{s0}:C{s1},D{s0}:D{s1})").number_format = PKR
A["staff_month"] = f"Assumptions!$D${r}"
r += 1
asm.cell(row=r, column=2, value="Monthly payroll of staff joining before opening").font = BOLD
asm.cell(row=r, column=4, value=f"=SUMPRODUCT(C{s0}:C{s1},D{s0}:D{s1},E{s0}:E{s1})").number_format = PKR
A["staff_pre_month"] = f"Assumptions!$D${r}"
r += 1
asm.cell(row=r, column=2, value="Number of leadership and support staff").font = BOLD
asm.cell(row=r, column=4, value=f"=SUM(C{s0}:C{s1})").number_format = NUM
A["staff_count"] = f"Assumptions!$D${r}"
r += 1
asm.cell(row=r, column=2, value="Support staff are paid at least the Punjab minimum wage (PKR 40,000 from July 2025, ProPakistani).").font = BLACK

# ----------------------------------------------------------------------------- Enrolment plan
en = wb.create_sheet("Enrolment")
style_ws(en, {"A": 46, "B": 14, **{c: 13 for c in COLS}})
en["A1"] = "Enrolment plan (base case, students on roll)"
en["A1"].font = TITLE
header_row(en, 3, "Students", "Unit")
plan = {
    "Junior (Grades 3-5)": [0, 140, 180, 210, 230, 245, 260, 270, 280, 285, 285],
    "Middle (Grades 6-8)": [0, 110, 170, 210, 240, 265, 280, 290, 290, 295, 295],
    "O Level (Grades 9-11)": [0, 50, 100, 160, 220, 270, 290, 300, 300, 300, 300],
}
E = {}
for i, (lab, vals) in enumerate(plan.items()):
    rr = 4 + i
    en.cell(row=rr, column=1, value=lab).font = BLACK
    en.cell(row=rr, column=2, value="students").font = BLACK
    for t, v in enumerate(vals):
        cc = en.cell(row=rr, column=3 + t, value=v)
        cc.font = BLUE
        cc.number_format = NUM
    E[["j", "m", "o"][i]] = rr
en.cell(row=7, column=1, value="Total, base plan").font = BOLD
for t, col in enumerate(COLS):
    en.cell(row=7, column=3 + t, value=f"=SUM({col}4:{col}6)").number_format = NUM
en.cell(row=9, column=1, value="O Level grades open (Grade 9 in Y1, 10 in Y2, 11 from Y3)").font = BLACK
en.cell(row=9, column=2, value="grades").font = BLACK
for t, v in enumerate([0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3]):
    cc = en.cell(row=9, column=3 + t, value=v)
    cc.font = BLUE
E["ol_open"] = 9
en.cell(row=11, column=1, value="Base plan: about 300 students in Y1, growing to about 880 (98% of the 900-seat capacity) by Y9. Edit the blue numbers to test other plans.").font = BLACK

# ----------------------------------------------------------------------------- Capex
cx = wb.create_sheet("Capex")
style_ws(cx, {"A": 3, "B": 60, "C": 18, "D": 60})
cx["B2"] = "Start-up capital investment (spent in Y0, PKR)"
cx["B2"].font = TITLE
cx.cell(row=4, column=2, value="Item").font = HEAD
cx.cell(row=4, column=3, value="PKR").font = HEAD
cx.cell(row=4, column=4, value="Note").font = HEAD
for col in (2, 3, 4):
    cx.cell(row=4, column=col).fill = HEAD_FILL
capex = [
    ("Renovation and fit-out of two blocks (partitions, washrooms, prayer halls)", 30000000, "Separate entrances, prayer hall and washrooms for each block."),
    ("Classroom furniture (36 classrooms, staff rooms, offices)", 12000000, ""),
    ("Science laboratories (one per block)", 8000000, "Physics, chemistry and biology to Cambridge practical standard."),
    ("Computer laboratories and campus network (one per block)", 9000000, ""),
    ("Smart boards and audio-visual equipment", 7000000, ""),
    ("Libraries (one per block)", 3000000, ""),
    ("Air conditioning and power backup", 12000000, ""),
    ("Solar power system (about 100 kW)", 9000000, "Cuts summer electricity bills."),
    ("Sports and play areas", 3000000, ""),
    ("CCTV, access control and safety", 1500000, ""),
    ("Signage and branding (from the approved signage plan)", 1800000, "Gate, facade, reception wall, wayfinding."),
]
for i, (lab, v, note) in enumerate(capex):
    rr = 5 + i
    cx.cell(row=rr, column=2, value=lab).font = BLACK
    cc = cx.cell(row=rr, column=3, value=v)
    cc.font = BLUE
    cc.number_format = PKR
    cx.cell(row=rr, column=4, value=note).font = BLACK
last = 5 + len(capex) - 1
cx.cell(row=last + 1, column=2, value="Subtotal").font = BOLD
cx.cell(row=last + 1, column=3, value=f"=SUM(C5:C{last})").number_format = PKR
cx.cell(row=last + 2, column=2, value="Contingency (share of subtotal)").font = BLACK
cc = cx.cell(row=last + 2, column=4, value=0.10)
cc.font = BLUE
cc.number_format = PCT
cx.cell(row=last + 2, column=3, value=f"=C{last + 1}*D{last + 2}").number_format = PKR
cx.cell(row=last + 3, column=2, value="Total initial capital investment").font = BOLD
tc = cx.cell(row=last + 3, column=3, value=f"=C{last + 1}+C{last + 2}")
tc.number_format = PKR
tc.font = BOLD
A["capex"] = f"Capex!$C${last + 3}"
cx.cell(row=last + 5, column=2, value="Phasing of spend (furnish classrooms and labs as grades open)").font = BOLD
for k, (lab, v) in enumerate([("Spent before opening (Y0)", 0.70), ("Spent in Y1 (for the second intake)", 0.15), ("Spent in Y2 (for O Level Grades 10-11)", 0.15)]):
    rr = last + 6 + k
    cx.cell(row=rr, column=2, value=lab).font = BLACK
    cc = cx.cell(row=rr, column=3, value=v)
    cc.font = BLUE
    cc.number_format = PCT
    A[["ph0", "ph1", "ph2"][k]] = f"Capex!$C${rr}"
cx.cell(row=last + 9, column=2, value="Check: phasing adds up to 100%").font = BLACK
cx.cell(row=last + 9, column=3, value=f"=SUM(C{last + 6}:C{last + 8})").number_format = PCT

# ----------------------------------------------------------------------------- Calc
calc = wb.create_sheet("Calc")
style_ws(calc, {"A": 54, "B": 12, **{c: 15 for c in COLS}})
calc["A1"] = "Calculations: three scenarios with identical formulas (PKR unless stated)"
calc["A1"].font = TITLE
calc.freeze_panes = "C3"


def g(t):  # growth exponent for year t (Y1 = 0)
    return f"({t}-1)"


ROWS = {}  # (scenario, key) -> row number


def build_block(s, start):
    """Write one scenario block starting at row `start`; return next free row."""
    em, fm, sm, rm_ = (A["enr_mult"][s], A["fee_mult"][s], A["sal_mult"][s], A["rent_mult"][s])
    rows = []

    def add(key, label, unit, fn, fmt=PKR, bold=False, section=False):
        rows.append((key, label, unit, fn, fmt, bold, section))

    add("hdr", f"{SCEN[s].upper()} SCENARIO", "", None, section=True)
    add("sec_students", "Students", "", None, section=True)
    for b, lab in (("j", "Junior students"), ("m", "Middle students"), ("o", "O Level students")):
        add(f"st_{b}", lab, "students",
            lambda t, c, b=b: "=0" if t == 0 else
            f"=MIN({A['blocks']}*{A['grades_band']}*{A['max_sec']}*{A['class_size']},ROUND(Enrolment!{c}{E[b]}*{em},0))", NUM)
    add("st_tot", "Total students", "students", lambda t, c: f"=SUM({c}{{st_j}}:{c}{{st_o}})", NUM, bold=True)
    add("capacity", "Seat capacity", "seats", lambda t, c: f"={A['blocks']}*3*{A['grades_band']}*{A['max_sec']}*{A['class_size']}", NUM)
    add("util_pct", "Capacity used", "%", lambda t, c: f"=IF({c}{{capacity}}=0,0,{c}{{st_tot}}/{c}{{capacity}})", PCT)
    add("new_st", "New admissions", "students",
        lambda t, c: "=0" if t == 0 else f"=MAX(0,{c}{{st_tot}}-{COLS[t - 1]}{{st_tot}}*(1-{A['attrition']}))", NUM)

    add("sec_rev", "Revenue", "", None, section=True)
    for b, fee in (("j", "fee_j"), ("m", "fee_m"), ("o", "fee_o")):
        add(f"fee_{b}", f"Monthly tuition, {dict(j='Junior', m='Middle', o='O Level')[b]}", "PKR/month",
            lambda t, c, fee=fee: "=0" if t == 0 else f"={A[fee]}*{fm}*(1+{A['fee_inc']})^{g(t)}", PKR)
    add("rev_tuition", "Tuition fees (after discounts and collection)", "PKR",
        lambda t, c: f"=({c}{{st_j}}*{c}{{fee_j}}+{c}{{st_m}}*{c}{{fee_m}}+{c}{{st_o}}*{c}{{fee_o}})*{A['months']}*(1-{A['discount']})*{A['collection']}")
    add("rev_adm", "Admission fees", "PKR",
        lambda t, c: "=0" if t == 0 else f"={c}{{new_st}}*{A['adm_fee']}*{fm}*(1+{A['fee_inc']})^{g(t)}")
    add("rev_ann", "Annual charges", "PKR",
        lambda t, c: "=0" if t == 0 else f"={c}{{st_tot}}*{A['ann_fee']}*{fm}*(1+{A['fee_inc']})^{g(t)}*{A['collection']}")
    add("rev_other", "Other income (uniform and books margin)", "PKR",
        lambda t, c: "=0" if t == 0 else f"={c}{{st_tot}}*{A['other_inc']}*(1+{A['infl']})^{g(t)}")
    add("rev", "Total revenue", "PKR", lambda t, c: f"=SUM({c}{{rev_tuition}}:{c}{{rev_other}})", bold=True)

    add("sec_staff", "Staffing", "", None, section=True)
    add("sec_j", "Sections, Junior", "sections",
        lambda t, c: "=0" if t == 0 else f"=IF({c}{{st_j}}=0,0,MAX({A['blocks']}*{A['grades_band']},ROUNDUP({c}{{st_j}}/{A['target_fill']},0)))", NUM)
    add("sec_m", "Sections, Middle", "sections",
        lambda t, c: "=0" if t == 0 else f"=IF({c}{{st_m}}=0,0,MAX({A['blocks']}*{A['grades_band']},ROUNDUP({c}{{st_m}}/{A['target_fill']},0)))", NUM)
    add("sec_o", "Sections, O Level", "sections",
        lambda t, c: "=0" if t == 0 else f"=IF({c}{{st_o}}=0,0,MAX({A['blocks']}*Enrolment!{c}{E['ol_open']},ROUNDUP({c}{{st_o}}/{A['target_fill']},0)))", NUM)
    add("sections", "Total sections (classes)", "sections", lambda t, c: f"=SUM({c}{{sec_j}}:{c}{{sec_o}})", NUM, bold=True)
    add("teachers", "Teachers (full-time equivalent)", "people",
        lambda t, c: f"={COLS[1] if t == 0 else c}{{sections}}*{A['t_per_sec']}+MAX({A['min_spec']},ROUNDUP({COLS[1] if t == 0 else c}{{st_tot}}/{A['stud_per_spec']},0))", '#,##0.0')
    add("cost_teach", "Teacher salaries and benefits", "PKR",
        lambda t, c: f"={c}{{teachers}}*{A['t_salary']}*{sm}*{A['pre_t_months']}*(1+{A['benefits']})" if t == 0 else
        f"={c}{{teachers}}*{A['t_salary']}*{sm}*(1+{A['sal_inc']})^{g(t)}*{A['pay_months']}*(1+{A['benefits']})")
    add("cost_staff", "Leadership and support staff", "PKR",
        lambda t, c: f"={A['staff_pre_month']}*{sm}*{A['pre_l_months']}*(1+{A['benefits']})" if t == 0 else
        f"={A['staff_month']}*{sm}*(1+{A['sal_inc']})^{g(t)}*{A['pay_months']}*(1+{A['benefits']})")
    add("payroll", "Total payroll", "PKR", lambda t, c: f"={c}{{cost_teach}}+{c}{{cost_staff}}", bold=True)

    add("sec_opex", "Other operating costs", "", None, section=True)
    add("rent", "Building rent", "PKR",
        lambda t, c: f"={A['rent']}*{rm_}*{A['pre_rent_months']}" if t == 0 else f"={A['rent']}*{rm_}*12*(1+{A['rent_esc']})^{g(t)}")
    add("utilities", "Utilities", "PKR", lambda t, c: "=0" if t == 0 else f"={A['util']}*12*(1+{A['infl']})^{g(t)}")
    add("marketing", "Marketing", "PKR",
        lambda t, c: f"={A['mkt_launch']}" if t == 0 else f"=MAX({A['mkt_min']}*(1+{A['infl']})^{g(t)},{A['mkt_pct']}*{c}{{rev}})")
    add("materials", "Teaching materials and consumables", "PKR",
        lambda t, c: "=0" if t == 0 else f"={c}{{st_tot}}*{A['materials']}*(1+{A['infl']})^{g(t)}")
    add("events", "Tarbiyah programmes, events and trips", "PKR",
        lambda t, c: "=0" if t == 0 else f"={c}{{st_tot}}*{A['events']}*(1+{A['infl']})^{g(t)}")
    add("fixed", "IT, insurance, maintenance and administration", "PKR",
        lambda t, c: "=0" if t == 0 else f"=({A['it']}+{A['insurance']}+{A['maint']}+{A['admin_misc']})*(1+{A['infl']})^{g(t)}")
    add("cpd", "Teacher training and Cambridge membership", "PKR", lambda t, c: f"={c}{{payroll}}*{A['cpd']}")
    add("preopen", "Registration, legal and recruitment (pre-opening)", "PKR", lambda t, c: f"={A['pre_other']}" if t == 0 else "=0")
    add("opex", "Total other operating costs", "PKR", lambda t, c: f"=SUM({c}{{rent}}:{c}{{preopen}})", bold=True)
    add("costs", "Total operating costs (payroll + other)", "PKR", lambda t, c: f"={c}{{payroll}}+{c}{{opex}}", bold=True)

    add("sec_pl", "Profit", "", None, section=True)
    add("ebitda", "EBITDA (operating profit before depreciation)", "PKR", lambda t, c: f"={c}{{rev}}-{c}{{costs}}", bold=True)
    add("ebitda_m", "EBITDA margin", "%", lambda t, c: f"=IF({c}{{rev}}=0,0,{c}{{ebitda}}/{c}{{rev}})", PCT)
    add("capex", "Capital investment", "PKR",
        lambda t, c: f"={A['capex']}*{A['ph0']}" if t == 0 else (f"={A['capex']}*{A['ph1']}" if t == 1 else
            f"={A['capex']}*{A['repl']}*(1+{A['infl']})^{g(t)}" + (f"+{A['capex']}*{A['ph2']}" if t == 2 else "")))
    add("dep", "Depreciation", "PKR",
        lambda t, c: "=0" if t == 0 else f"=SUM($C{{capex}}:{COLS[t - 1]}{{capex}})/{A['life']}")
    add("pbt", "Profit before tax", "PKR", lambda t, c: f"={c}{{ebitda}}-{c}{{dep}}", bold=True)
    add("loss_open", "Tax losses brought forward", "PKR", lambda t, c: "=0" if t == 0 else f"={COLS[t - 1]}{{loss_close}}")
    add("taxable", "Taxable profit after using losses", "PKR", lambda t, c: f"=MAX(0,{c}{{pbt}}-{c}{{loss_open}})")
    add("loss_close", "Tax losses carried forward", "PKR", lambda t, c: f"=MAX(0,{c}{{loss_open}}-{c}{{pbt}})")
    add("taxp", "Tax", "PKR", lambda t, c: f"={c}{{taxable}}*{A['tax']}")
    add("ni", "Net profit after tax", "PKR", lambda t, c: f"={c}{{pbt}}-{c}{{taxp}}", bold=True)

    add("sec_cf", "Cash flow", "", None, section=True)
    add("cfo", "Cash from operations (net profit + depreciation)", "PKR", lambda t, c: f"={c}{{ni}}+{c}{{dep}}")
    add("deposit", "Rent security deposit (refundable)", "PKR",
        lambda t, c: f"={A['rent']}*{rm_}*{A['deposit_months']}" if t == 0 else "=0")
    add("fcf", "Free cash flow (before owner's investment)", "PKR", lambda t, c: f"={c}{{cfo}}-{c}{{capex}}-{c}{{deposit}}", bold=True)
    add("cum_fcf", "Cumulative free cash flow", "PKR", lambda t, c: f"=SUM($C{{fcf}}:{c}{{fcf}})")
    add("equity_in", "Owner's investment", "PKR", lambda t, c: f"={A['equity']}" if t == 0 else "=0")
    add("cash", "Cash balance at year end", "PKR", lambda t, c: f"=SUM($C{{equity_in}}:{c}{{equity_in}})+{c}{{cum_fcf}}", bold=True)
    add("flag_profit", "First profitable year (helper)", "year",
        lambda t, c: '=""' if t == 0 else f'=IF(AND({c}{{ni}}>0,COUNTIF($C{{ni}}:{COLS[t - 1]}{{ni}},">0")=0),{t},"")', NUM)
    add("flag_payback", "Payback year (helper)", "year",
        lambda t, c: '=""' if t == 0 else f'=IF(AND({c}{{cum_fcf}}>=0,{COLS[t - 1]}{{cum_fcf}}<0),{t},"")', NUM)

    # assign rows
    rr = start
    for key, *_ in rows:
        ROWS[(s, key)] = rr
        rr += 1
    # write
    for key, label, unit, fn, fmt, bold, section in rows:
        row = ROWS[(s, key)]
        a = calc.cell(row=row, column=1, value=label)
        a.font = BOLD if (bold or section) else BLACK
        calc.cell(row=row, column=2, value=unit).font = BLACK
        if section:
            for col in range(1, 14):
                calc.cell(row=row, column=col).fill = HEAD_FILL if key == "hdr" else SECT_FILL
            if key == "hdr":
                a.font = HEAD
            continue
        for t, col in enumerate(COLS):
            f = fn(t, col)
            # fill row placeholders such as {st_tot} with this block's row numbers
            for k2 in sorted((k for k, *_ in rows), key=len, reverse=True):
                f = f.replace("{" + k2 + "}", str(ROWS[(s, k2)]))
            assert "{" not in f, (key, f)
            cc = calc.cell(row=row, column=3 + t, value=f)
            cc.number_format = fmt
            cc.font = BOLD if bold else BLACK
            if bold:
                cc.border = TOP
    return rr + 1


header_row(calc, 2, "Line item", "Unit")
nxt = 3
for s in range(3):
    nxt = build_block(s, nxt)


def kref(s, key, col):
    return f"Calc!${col}${ROWS[(s, key)]}"


def pick(key, col):
    return f"CHOOSE({A['sel']},{kref(0, key, col)},{kref(1, key, col)},{kref(2, key, col)})"


# ----------------------------------------------------------------------------- Profit and Loss (selected scenario)
pl = wb.create_sheet("Profit and Loss")
style_ws(pl, {"A": 50, "B": 12, **{c: 13 for c in COLS}})
pl["A1"] = '="Profit and Loss, "&Assumptions!$D$5&" scenario (PKR million)"'
pl["A1"].font = TITLE
header_row(pl, 3, "PKR million", "")
pl_lines = [
    ("Students on roll", "st_tot", NUM, 1, False),
    ("Capacity used", "util_pct", PCT, 1, False),
    (None,),
    ("Tuition fees", "rev_tuition", PKRM, 1e6, False),
    ("Admission fees", "rev_adm", PKRM, 1e6, False),
    ("Annual charges", "rev_ann", PKRM, 1e6, False),
    ("Other income", "rev_other", PKRM, 1e6, False),
    ("Total revenue", "rev", PKRM, 1e6, True),
    (None,),
    ("Teacher salaries", "cost_teach", PKRM, 1e6, False),
    ("Leadership and support staff", "cost_staff", PKRM, 1e6, False),
    ("Rent", "rent", PKRM, 1e6, False),
    ("Utilities", "utilities", PKRM, 1e6, False),
    ("Marketing", "marketing", PKRM, 1e6, False),
    ("Materials, events and training", None, PKRM, 1e6, False),
    ("IT, insurance, maintenance, admin, pre-opening", None, PKRM, 1e6, False),
    ("Total operating costs", "costs", PKRM, 1e6, True),
    (None,),
    ("EBITDA", "ebitda", PKRM, 1e6, True),
    ("EBITDA margin", "ebitda_m", PCT, 1, False),
    ("Depreciation", "dep", PKRM, 1e6, False),
    ("Profit before tax", "pbt", PKRM, 1e6, True),
    ("Tax", "taxp", PKRM, 1e6, False),
    ("Net profit after tax", "ni", PKRM, 1e6, True),
]
PLR = {}
r = 4
for line in pl_lines:
    if line[0] is None:
        r += 1
        continue
    lab, key, fmt, div, bold = line
    pl.cell(row=r, column=1, value=lab).font = BOLD if bold else BLACK
    for t, col in enumerate(COLS):
        if key:
            f = f"={pick(key, col)}" + (f"/{int(div)}" if div != 1 else "")
        elif lab.startswith("Materials"):
            f = f"=({pick('materials', col)}+{pick('events', col)}+{pick('cpd', col)})/1000000"
        else:
            f = f"=({pick('fixed', col)}+{pick('preopen', col)})/1000000"
        cc = pl.cell(row=r, column=3 + t, value=f)
        cc.number_format = fmt
        cc.font = Font(name=F, bold=bold, color="008000")
        if bold:
            cc.border = TOP
    PLR[lab] = r
    r += 1
pl.freeze_panes = "C4"

# chart
ch = BarChart()
ch.type = "col"
ch.title = "Revenue, costs and net profit (PKR million)"
ch.y_axis.title = "PKR million"
data_rows = [PLR["Total revenue"], PLR["Total operating costs"], PLR["Net profit after tax"]]
for dr in data_rows:
    ref = Reference(pl, min_col=2, max_col=13, min_row=dr)
    ch.add_data(ref, titles_from_data=True, from_rows=True)
ch.set_categories(Reference(pl, min_col=3, max_col=13, min_row=3))
ch.height, ch.width = 9, 24
ch.roundedCorners = False
ch.legend.overlay = False
ch.title.overlay = False
ch.y_axis.title.overlay = False
ch.x_axis.delete = False
ch.y_axis.delete = False
# use column B (empty) as series name cell: set names explicitly
for sser, nm in zip(ch.series, ["Total revenue", "Total operating costs", "Net profit after tax"]):
    from openpyxl.chart.series import SeriesLabel
    sser.tx = SeriesLabel(v=nm)
pl.add_chart(ch, f"A{r + 2}")

# ----------------------------------------------------------------------------- Cash Flow (selected scenario)
cf = wb.create_sheet("Cash Flow")
style_ws(cf, {"A": 50, "B": 12, **{c: 13 for c in COLS}})
cf["A1"] = '="Cash flow, "&Assumptions!$D$5&" scenario (PKR million)"'
cf["A1"].font = TITLE
header_row(cf, 3, "PKR million", "")
cf_lines = [
    ("Net profit after tax", "ni", False), ("Add back depreciation", "dep", False),
    ("Cash from operations", "cfo", True), ("Capital investment", "capex", False),
    ("Rent security deposit", "deposit", False), ("Free cash flow", "fcf", True),
    ("Cumulative free cash flow", "cum_fcf", False), ("Owner's investment", "equity_in", False),
    ("Cash balance at year end", "cash", True),
]
r = 4
for lab, key, bold in cf_lines:
    cf.cell(row=r, column=1, value=lab).font = BOLD if bold else BLACK
    sign = "-" if key in ("capex", "deposit") else ""
    for t, col in enumerate(COLS):
        cc = cf.cell(row=r, column=3 + t, value=f"={sign}{pick(key, col)}/1000000")
        cc.number_format = PKRM
        cc.font = Font(name=F, bold=bold, color="008000")
        if bold:
            cc.border = TOP
    r += 1
cf.cell(row=r + 1, column=1, value="Cash balance must stay above zero in every year; if it falls below, more investment or a loan is needed.").font = BLACK
lc = LineChart()
lc.title = "Cash balance and cumulative free cash flow (PKR million)"
for rr_, nm in ((r - 1, "Cash balance at year end"), (10, "Cumulative free cash flow")):
    lc.add_data(Reference(cf, min_col=2, max_col=13, min_row=rr_), titles_from_data=True, from_rows=True)
from openpyxl.chart.series import SeriesLabel
for sser, nm in zip(lc.series, ["Cash balance at year end", "Cumulative free cash flow"]):
    sser.tx = SeriesLabel(v=nm)
lc.set_categories(Reference(cf, min_col=3, max_col=13, min_row=3))
lc.height, lc.width = 9, 24
lc.roundedCorners = False
lc.legend.overlay = False
lc.title.overlay = False
lc.x_axis.delete = False
lc.y_axis.delete = False
cf.add_chart(lc, f"A{r + 3}")

# ----------------------------------------------------------------------------- Summary
sm_ = wb.create_sheet("Summary", 1)
style_ws(sm_, {"A": 3, "B": 58, "C": 18, "D": 18, "E": 18, "F": 60})
sm_["B2"] = "Adabury School, Faisalabad: key results"
sm_["B2"].font = TITLE
sm_["B3"] = "All three scenarios, recalculated from the Assumptions, Enrolment and Capex sheets."
sm_["B3"].font = BLACK
for j, s in enumerate(SCEN):
    cc = sm_.cell(row=5, column=3 + j, value=s)
    cc.font = HEAD
    cc.fill = HEAD_FILL
    cc.alignment = Alignment(horizontal="center")
sm_.cell(row=5, column=2, value="Measure").font = HEAD
sm_.cell(row=5, column=2).fill = HEAD_FILL
sm_.cell(row=5, column=6, value="How to read it").font = HEAD
sm_.cell(row=5, column=6).fill = HEAD_FILL

M = "M"  # Y10 column
D5 = COLS[5]  # Y5
kpis = [
    ("Start-up investment needed (capex + deposit + Y0 costs), PKR million",
     lambda s: f"=({kref(s, 'capex', 'C')}+{kref(s, 'deposit', 'C')}+{kref(s, 'costs', 'C')})/1000000", PKRM,
     "Money spent before the first student arrives."),
    ("Peak funding need (lowest cumulative cash flow), PKR million",
     lambda s: f"=-MIN(0,MIN(Calc!$C${ROWS[(s, 'cum_fcf')]}:$M${ROWS[(s, 'cum_fcf')]}))/1000000", PKRM,
     "The most money the school is ever 'down'. The owner's investment must cover this."),
    ("Owner's investment, PKR million", lambda s: f"={A['equity']}/1000000", PKRM, "From Assumptions."),
    ("Extra funding needed beyond the owner's investment, PKR million",
     lambda s: f"=MAX(0,-MIN(Calc!$C${ROWS[(s, 'cash')]}:$M${ROWS[(s, 'cash')]}))/1000000", PKRM,
     "Zero means the investment is enough. Otherwise this must come from a partner, a bank or a smaller plan."),
    ("Lowest year-end cash balance, PKR million",
     lambda s: f"=MIN(Calc!$C${ROWS[(s, 'cash')]}:$M${ROWS[(s, 'cash')]})/1000000", PKRM,
     "Negative means the investment is not enough in this scenario."),
    ("Students in Y1", lambda s: f"={kref(s, 'st_tot', 'D')}", NUM, ""),
    ("Students in Y5", lambda s: f"={kref(s, 'st_tot', D5)}", NUM, ""),
    ("Revenue in Y1, PKR million", lambda s: f"={kref(s, 'rev', 'D')}/1000000", PKRM, ""),
    ("Revenue in Y5, PKR million", lambda s: f"={kref(s, 'rev', D5)}/1000000", PKRM, ""),
    ("Net profit in Y1, PKR million", lambda s: f"={kref(s, 'ni', 'D')}/1000000", PKRM, ""),
    ("Net profit in Y5, PKR million", lambda s: f"={kref(s, 'ni', D5)}/1000000", PKRM, ""),
    ("EBITDA margin in Y5", lambda s: f"={kref(s, 'ebitda_m', D5)}", PCT, "Mature premium schools typically run 20-30%."),
    ("First year with a net profit",
     lambda s: f'=IF(MIN(Calc!$D${ROWS[(s, "flag_profit")]}:$M${ROWS[(s, "flag_profit")]})=0,"Not within 10 years","Year "&MIN(Calc!$D${ROWS[(s, "flag_profit")]}:$M${ROWS[(s, "flag_profit")]}))',
     None, ""),
    ("Payback year (cumulative cash flow turns positive)",
     lambda s: f'=IF(MIN(Calc!$D${ROWS[(s, "flag_payback")]}:$M${ROWS[(s, "flag_payback")]})=0,"Not within 10 years","Year "&MIN(Calc!$D${ROWS[(s, "flag_payback")]}:$M${ROWS[(s, "flag_payback")]}))',
     None, "Counted from the first teaching year (Y1 = 2028-29)."),
    ("10-year net present value at the discount rate, PKR million",
     lambda s: f"=({kref(s, 'fcf', 'C')}+NPV({A['disc']},Calc!$D${ROWS[(s, 'fcf')]}:$M${ROWS[(s, 'fcf')]}))/1000000", PKRM,
     "Positive means the school beats the owner's required return within 10 years, with no value counted after Y10."),
    ("10-year internal rate of return",
     lambda s: f'=IFERROR(IRR(Calc!$C${ROWS[(s, "fcf")]}:$M${ROWS[(s, "fcf")]}),"Below zero")', PCT,
     "Excludes the value of the school after Y10, so it understates the true return."),
    ("Net profit in Y10, PKR million", lambda s: f"={kref(s, 'ni', M)}/1000000", PKRM, ""),
]
SR = {}
for i, (lab, fn, fmt, note) in enumerate(kpis):
    rr = 6 + i
    sm_.cell(row=rr, column=2, value=lab).font = BLACK
    for s in range(3):
        cc = sm_.cell(row=rr, column=3 + s, value=fn(s))
        cc.font = GREEN
        cc.alignment = Alignment(horizontal="right")
        if fmt:
            cc.number_format = fmt
    sm_.cell(row=rr, column=6, value=note).font = BLACK
    SR[lab] = rr
for rr in range(6, 6 + len(kpis)):
    sm_.row_dimensions[rr].height = 18

# Base case 10-year strip
r0 = 6 + len(kpis) + 2
sm_.cell(row=r0, column=2, value="Base case by year").font = BOLD
for t, y in enumerate(YEARS):
    cc = sm_.cell(row=r0 + 1, column=3 + t, value=y.replace("\n", " "))
    cc.font = HEAD
    cc.fill = HEAD_FILL
    cc.alignment = Alignment(wrap_text=True, horizontal="center")
sm_.cell(row=r0 + 1, column=2, value="Base case").font = HEAD
sm_.cell(row=r0 + 1, column=2).fill = HEAD_FILL
sm_.row_dimensions[r0 + 1].height = 30
for i, (lab, key, fmt, div) in enumerate([("Students", "st_tot", NUM, 1), ("Revenue (PKR million)", "rev", PKRM, 1e6),
                                         ("EBITDA (PKR million)", "ebitda", PKRM, 1e6),
                                         ("Net profit (PKR million)", "ni", PKRM, 1e6),
                                         ("Cash balance (PKR million)", "cash", PKRM, 1e6)]):
    rr = r0 + 2 + i
    sm_.cell(row=rr, column=2, value=lab).font = BLACK
    for t, col in enumerate(COLS):
        cc = sm_.cell(row=rr, column=3 + t, value=f"={kref(1, key, col)}" + (f"/{int(div)}" if div != 1 else ""))
        cc.number_format = fmt
        cc.font = GREEN
for col in COLS[3:]:
    sm_.column_dimensions[col].width = 13
sm_.freeze_panes = "C6"

# sheet order: Read Me, Summary, Assumptions, Enrolment, Capex, Profit and Loss, Cash Flow, Calc
order = ["Read Me", "Summary", "Assumptions", "Enrolment", "Capex", "Profit and Loss", "Cash Flow", "Calc"]
wb._sheets = [wb[n] for n in order]
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = "6E1F2F" if ws.title in ("Summary", "Assumptions") else "C9A962"
    for row in ws.iter_rows():
        for cell in row:
            if cell.font and cell.font.name != F:
                cell.font = Font(name=F, bold=cell.font.bold, color=cell.font.color, size=cell.font.size)

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print("saved", OUT)
print("rows", {k: v for k, v in ROWS.items() if k[0] == 1 and k[1] in ("st_tot", "rev", "ni", "cash", "fcf")})
