// Build the Adabury School Faisalabad investor and Board deck (PowerPoint).
// Usage: node build_deck.js <model_results.json> <out.pptx>
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const [jsonPath, outPath] = process.argv.slice(2);
const D = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
const B = D.rows.base, K = D.kpi;
const ROOT = path.resolve(__dirname, "..", "..");
const img = (p) => "image/" + (p.endsWith(".png") ? "png" : "jpeg") + ";base64," + fs.readFileSync(path.join(ROOT, p)).toString("base64");

const THEME = {
  name: "Adabury",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "2A1418", lt1: "FFFFFF", dk2: "6E1F2F", lt2: "F5EEE6",
    accent1: "6E1F2F", accent2: "C2A15A", accent3: "3E4249", accent4: "A8843E", accent5: "B3261E", accent6: "2E6B3F",
    hlink: "6E1F2F", folHlink: "A8843E",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.title = "Adabury School, Faisalabad: feasibility";
pres.author = "Adabury School";
pres.company = "Adabury School";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const M = (v) => Number(v) / 1e6;
const cr = (v) => (Number(v) / 1e7).toFixed(1);
const f1 = (v) => (v < 0 ? `(${Math.abs(v).toFixed(1)})` : v.toFixed(1));
const YRS = ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"];
const crestRev = img("brand/logo/png/adabury-crest-reverse.png");
const crest = img("brand/logo/png/adabury-crest.png");
const hRev = img("brand/logo/png/adabury-logo-horizontal-reverse.png");

// ------------------------------------------------------------------ layouts
pres.defineSlideMaster({
  title: "Title dark",
  background: { color: C.background2 },
  objects: [
    { rect: { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.text2 } } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 2.2, w: 6.2, h: 1.5, fontSize: 36, bold: true, color: C.background1, align: "left", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.8, w: 6.2, h: 1.1, fontSize: 16, color: C.background2, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Closing dark",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.5, w: 6.2, h: 0.8, fontSize: 36, bold: true, color: C.background1, align: "left", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.5, w: 6.4, h: 3.5, fontSize: 18, color: C.background2, valign: "top", margin: 0, paraSpaceAfter: 10 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Content",
  background: { color: C.background1 },
  margin: [0.5, 0.5, 0.6, 0.5],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.25, w: 8.5, h: 0.8, fontSize: 22, bold: true, color: C.text2, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: "Adabury School · Faisalabad feasibility · November 2026", options: { x: 0.5, y: 5.22, w: 6, h: 0.25, fontSize: 10, color: C.accent3, margin: 0 } } },
    { image: { x: 9.18, y: 0.3, w: 0.38, h: 0.395, data: crest } },
  ],
  slideNumber: { x: 9.1, y: 5.2, w: 0.4, h: 0.25, fontSize: 10, color: C.accent3, align: "right" },
});

const sec = (t) => pres.addSection({ title: t });
let section = "";
const slide = (master) => pres.addSlide({ masterName: master, sectionTitle: section });
const title = (s, t) => s.addText(t, { placeholder: "title" });
const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, fontSize: 14, color: C.text1, margin: 0, valign: "top" }, o));

// stat card
function stat(s, x, y, w, big, label, opts = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.25, rectRadius: 0.06, fill: { color: opts.dark ? C.text2 : C.background2 }, line: { color: opts.dark ? C.text2 : C.background2 }, objectName: "stat " + label });
  txt(s, big, { x: x + 0.2, y: y + 0.17, w: w - 0.4, h: 0.55, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: opts.warn ? C.accent5 : opts.dark ? C.background1 : C.text2 });
  txt(s, label, { x: x + 0.2, y: y + 0.75, w: w - 0.4, h: 0.4, fontSize: 12, color: opts.dark ? C.background2 : C.accent3 });
}
// card with heading
function card(s, x, y, w, h, head, body, opts = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: opts.fill || C.background2 }, line: { color: opts.fill || C.background2 }, objectName: "card " + head });
  txt(s, head, { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.35, fontSize: 15, bold: true, color: opts.headColor || C.text2 });
  if (body) txt(s, body, { x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.65, fontSize: 13, color: opts.bodyColor || C.text1 });
}
const chartBase = (o) => Object.assign({
  catAxisLabelColor: HEX.accent3, valAxisLabelColor: HEX.accent3, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt", titleFontFace: "+mn-lt",
  valGridLine: { color: "E6DEDA", size: 0.75 }, catGridLine: { style: "none" }, dataLabelFontSize: 10, dataLabelColor: HEX.dk1,
  legendFontSize: 11, legendColor: HEX.dk1,
}, o);

const ni5 = M(B["Net profit after tax"][5]), rev5 = M(B["Total revenue"][5]);
const peak = Number(K["Peak funding need (lowest cumulative cash flow), PKR million"][1]);
const gap = Number(K["Extra funding needed beyond the owner's investment, PKR million"][1]);
const firstYr = K["First year with a net profit"][1], payback = K["Payback year (cumulative cash flow turns positive)"][1];
const startup = Number(K["Start-up investment needed (capex + deposit + Y0 costs), PKR million"][1]);

// ================================================================== 1 Title
section = "Overview"; sec(section);
let s = slide("Title dark");
s.addImage({ data: hRev, x: 0.6, y: 0.6, w: 3.2, h: 0.98, objectName: "Adabury logo" });
s.addText("Adabury School, Faisalabad", { placeholder: "title" });
s.addText("Feasibility study for the founder and Board of Governors · November 2026", { placeholder: "body" });
s.addImage({ data: crestRev, x: 7.2, y: 1.2, w: 2.2, h: 2.29, objectName: "Crest" });
s.addNotes("Introduce Adabury: a new, fully separate brand for families who want a world-class Cambridge school with character first. This deck summarises the feasibility study for the Faisalabad campus opening April 2028.");

// ================================================================== 2 Verdict
s = slide("Content");
title(s, "Viable once established, but needs about twice the planned start-up money");
stat(s, 0.5, 1.2, 2.1, `${B["Total students"][1]} → ${B["Total students"][5]}`, "Students, Year 1 to Year 5");
stat(s, 2.75, 1.2, 2.1, `PKR ${(rev5 / 10).toFixed(1)} cr`, "Revenue in Year 5");
stat(s, 5.0, 1.2, 2.1, firstYr, "First year with a net profit");
stat(s, 7.25, 1.2, 2.25, `PKR ${(peak / 10).toFixed(1)} cr`, "Peak funding need (budget PKR 8–12 cr)", { warn: true });
txt(s, [
  { text: `Base case: about PKR ${ni5.toFixed(0)} million net profit a year by Year 5; the investment is paid back in ${payback.toLowerCase()}.`, options: { bullet: true, breakLine: true } },
  { text: `Early losses plus fit-out leave the school up to PKR ${(peak / 10).toFixed(1)} crore down in Year 2: about PKR ${(gap / 10).toFixed(1)} crore more than the PKR 10 crore budgeted.`, options: { bullet: true, breakLine: true } },
  { text: "Recommendation: proceed to site search and registration; sign a lease only once the funding plan is agreed.", options: { bullet: true, bold: true } },
], { x: 0.5, y: 2.75, w: 9, h: 2.2, fontSize: 15, paraSpaceAfter: 8 });
s.addNotes("The headline: the business works at maturity, but the funding need is about double the budget. Slide 11 shows how to close most of the gap.");

// ================================================================== 3 Opportunity
s = slide("Content");
title(s, "Parents want character and Cambridge quality in one school");
card(s, 0.5, 1.2, 2.85, 2.6, "Premium chains", "Beaconhouse, LGS, Roots and others. Strong academics and facilities, but values and Islamic learning are not the core promise. Reported at PKR 30,000–45,000 a month.");
card(s, 3.575, 1.2, 2.85, 2.6, "Adabury", "Cambridge academics with character first: daily Quran, Arabic, six rated values, separate girls' and boys' blocks. PKR 19,500–27,500 a month in 2028.", { fill: C.text2, headColor: C.accent2, bodyColor: C.background1 });
card(s, 6.65, 1.2, 2.85, 2.6, "Islamic schools", "Strong on Quran and values, but rarely seen as offering Cambridge-level academics or a modern, premium experience.");
txt(s, "Target families: business, textile and professional households on the Canal Road belt, moving their child after Grade 2 for stronger values and stronger academics.", { x: 0.5, y: 4.1, w: 9, h: 0.8, fontSize: 15, italic: true, color: C.text2 });
s.addNotes("Over 13 years at Deenway the founder saw many parents who want character but not a strictly traditional look. Adabury fills the gap between premium chains and Islamic schools. Competitor fees come from third-party guides and need checking.");

// ================================================================== 4 Brand
section = "The school"; sec(section);
s = slide("Content");
title(s, "A brand rooted in Faisalabad, built for a premium market");
s.addImage({ data: img("brand/uniform/photos/web/10-group-campus.jpg"), x: 4.6, y: 1.15, w: 4.9, h: 2.76, objectName: "Uniform group photo" });
txt(s, [
  { text: "Ghanta Ghar crest", options: { bold: true, color: C.text2, breakLine: true } },
  { text: "The Clock Tower between olive branches, under the eight-point star.", options: { breakLine: true } },
  { text: " ", options: { fontSize: 8, breakLine: true } },
  { text: "Claret and gold", options: { bold: true, color: C.text2, breakLine: true } },
  { text: "Blazers, vans and gates in one colour the city learns to recognise.", options: { breakLine: true } },
  { text: " ", options: { fontSize: 8, breakLine: true } },
  { text: "Bilingual", options: { bold: true, color: C.text2, breakLine: true } },
  { text: "ادبری اسکول · \"Adab is the first grace\"", options: {} },
], { x: 0.5, y: 1.2, w: 3.8, h: 3.5, fontSize: 14 });
txt(s, "Photo: AI visualisation of the approved uniform; to be replaced by a real shoot.", { x: 4.6, y: 4.0, w: 4.9, h: 0.3, fontSize: 10, color: C.accent3 });
s.addNotes("The full brand is complete: logo, uniform (no tie, compulsory hijab for girls), stationery, signage and social templates. See the brand pages.");

// ================================================================== 5 Academic model
s = slide("Content");
title(s, "Cambridge pathway with a daily Tarbiyah programme");
const stages = [["Junior · Grades 3–5", "Cambridge Primary: English, Maths, Science, Global Perspectives, Computing, Urdu, Islamiyat"],
  ["Middle · Grades 6–8", "Cambridge Lower Secondary with Checkpoint tests in Grade 8"],
  ["O Level · Grades 9–11", "About 8 Cambridge O Levels including Islamiyat, Pakistan Studies and Urdu"]];
stages.forEach(([h, b], i) => card(s, 0.5, 1.15 + i * 1.18, 4.3, 1.05, h, b));
card(s, 5.1, 1.15, 4.4, 3.4, "The Adabury Tarbiyah programme", "", { fill: C.text2, headColor: C.accent2 });
txt(s, [
  { text: "Daily Quran: Nazra, Tajweed, optional Hifz track", options: { bullet: true, breakLine: true } },
  { text: "Arabic from Grade 3", options: { bullet: true, breakLine: true } },
  { text: "Six values rated each term: Adab, Amanah, Ihsan, Sabr, Shukr, Khidmah", options: { bullet: true, breakLine: true } },
  { text: "Zuhr in congregation in each block", options: { bullet: true, breakLine: true } },
  { text: "Weekly mentor groups, service and leadership", options: { bullet: true } },
], { x: 5.3, y: 1.7, w: 4.0, h: 2.75, fontSize: 14, color: C.background1, paraSpaceAfter: 6 });
s.addNotes("The report card puts academic grades beside the Adabury Character Record, which makes the brand promise visible to parents every term.");

// ================================================================== 6 Campus
s = slide("Content");
title(s, "One building on the Canal Road belt, two separate blocks");
s.addImage({ data: img("brand/signage/mockups/web/01-main-gate.jpg"), x: 0.5, y: 1.15, w: 4.6, h: 2.6, objectName: "Gate visualisation" });
txt(s, "Gate visualisation (AI); final design depends on the building leased.", { x: 0.5, y: 3.85, w: 4.6, h: 0.3, fontSize: 10, color: C.accent3 });
txt(s, [
  { text: "6–8 kanal; 36 classrooms at full size", options: { bullet: true, breakLine: true } },
  { text: "Girls' and boys' blocks with separate entrances, prayer halls, labs and libraries", options: { bullet: true, breakLine: true } },
  { text: "Safe off-road drop-off for vans and cars", options: { bullet: true, breakLine: true } },
  { text: "Rent assumed PKR 20 lakh a month from April 2028, +10% a year", options: { bullet: true, breakLine: true } },
  { text: "Targets: 10-year lease, capped increases, rent-free fit-out months, first right to buy", options: { bullet: true } },
], { x: 5.4, y: 1.15, w: 4.1, h: 3.6, fontSize: 14, paraSpaceAfter: 8 });
s.addNotes("Rent is the single biggest cost to negotiate. Listings show 1-2 kanal Canal Road buildings at roughly PKR 3.5-8 lakh, scaled up here.");

// ================================================================== 7 Enrolment
section = "Financials"; sec(section);
s = slide("Content");
title(s, "Enrolment grows from 300 to about 880 as grades open and fill");
s.addChart(pres.charts.BAR, [{ name: "Students", labels: YRS, values: B["Total students"].slice(1).map(Number) }], chartBase({
  x: 0.5, y: 1.1, w: 6.2, h: 3.9, barDir: "col", chartColors: [HEX.dk2], showValue: true, dataLabelPosition: "outEnd",
  valAxisMaxVal: 1000, valAxisMinVal: 0, valAxisMajorUnit: 200, showLegend: false, barGapWidthPct: 60,
  showTitle: true, title: "Students on roll, base case (capacity 900)", titleFontSize: 12, titleColor: HEX.accent3,
}));
txt(s, [
  { text: "Year 1 opens Grades 3–9 in both blocks", options: { bullet: true, breakLine: true } },
  { text: "Grades 10–11 open as the first O Level class moves up", options: { bullet: true, breakLine: true } },
  { text: "No class above 25; a new section opens at an average of 22", options: { bullet: true, breakLine: true } },
  { text: "Worst case: 20% fewer students", options: { bullet: true } },
], { x: 7.0, y: 1.3, w: 2.5, h: 3.5, fontSize: 14, paraSpaceAfter: 8 });

// ================================================================== 8 Revenue vs costs
s = slide("Content");
title(s, "Revenue overtakes costs in Year 3; 20% margin by Year 5");
s.addChart(pres.charts.BAR, [
  { name: "Revenue", labels: YRS, values: B["Total revenue"].slice(1).map((v) => +M(v).toFixed(1)) },
  { name: "Operating costs", labels: YRS, values: B["Total operating costs (payroll + other)"].slice(1).map((v) => +M(v).toFixed(1)) },
], chartBase({
  x: 0.5, y: 1.1, w: 6.4, h: 3.95, barDir: "col", barGrouping: "clustered", chartColors: [HEX.dk2, HEX.accent2],
  showLegend: true, legendPos: "t", valAxisMinVal: 0, valAxisMaxVal: 500, valAxisMajorUnit: 100,
  showTitle: true, title: "PKR million, base case", titleFontSize: 12, titleColor: HEX.accent3, barGapWidthPct: 50,
}));
stat(s, 7.2, 1.2, 2.3, `PKR ${ni5.toFixed(0)} m`, "Net profit in Year 5");
stat(s, 7.2, 2.6, 2.3, `PKR ${M(B["Net profit after tax"][10]).toFixed(0)} m`, "Net profit in Year 10");
txt(s, "Payroll about 53% of revenue at maturity; rent falls from 26% to 12% of revenue by Year 5.", { x: 7.2, y: 4.0, w: 2.3, h: 1.0, fontSize: 12, color: C.accent3 });

// ================================================================== 9 Investment
s = slide("Content");
title(s, `About PKR ${(startup / 10).toFixed(1)} crore is spent before the first student arrives`);
const capex = D.capex.slice(0, -3).map(([n, v]) => [n.replace(/ \(.*\)/, "").replace("Renovation and fit-out of two blocks", "Fit-out of two blocks"), +M(v).toFixed(1)]).sort((a, b) => a[1] - b[1]);
s.addChart(pres.charts.BAR, [{ name: "PKR million", labels: capex.map((c) => c[0]), values: capex.map((c) => c[1]) }], chartBase({
  x: 0.5, y: 1.05, w: 5.9, h: 4.05, barDir: "bar", chartColors: [HEX.accent2], showValue: true, dataLabelPosition: "outEnd",
  showLegend: false, valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 10, barGapWidthPct: 40,
  showTitle: true, title: "Fit-out and equipment, PKR million (plus 10% contingency)", titleFontSize: 12, titleColor: HEX.accent3,
}));
stat(s, 6.7, 1.2, 2.8, `PKR ${cr(D.capex[D.capex.length - 1][1])} cr`, "Fit-out and equipment incl. contingency");
txt(s, [
  { text: "70% before opening, 30% in Years 1–2", options: { bullet: true, breakLine: true } },
  { text: "Plus deposit, fit-out rent, pre-opening salaries, PKR 1.5 cr launch campaign", options: { bullet: true, breakLine: true } },
  { text: "Transport outsourced: saves about PKR 5 cr of vans", options: { bullet: true } },
], { x: 6.7, y: 2.65, w: 2.8, h: 2.4, fontSize: 13, paraSpaceAfter: 6 });

// ================================================================== 10 Funding gap
s = slide("Content");
title(s, `With PKR 10 crore invested, cash runs about PKR ${(gap / 10).toFixed(1)} crore short in Year 2`);
s.addChart(pres.charts.LINE, [{ name: "Cash balance (PKR million)", labels: ["Y0", ...YRS], values: B["Cash balance at year end"].map((v) => +M(v).toFixed(1)) }], chartBase({
  x: 0.5, y: 1.05, w: 5.6, h: 4.0, chartColors: [HEX.dk2], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 7,
  showLegend: false, valAxisMinVal: -150, valAxisMaxVal: 300, valAxisMajorUnit: 50,
  showTitle: true, title: "Cash balance at year end, PKR million, base case", titleFontSize: 12, titleColor: HEX.accent3,
}));
card(s, 6.4, 1.1, 3.1, 3.95, "Closing the gap", "");
txt(s, [
  { text: "Ijarah lease for AC, solar, IT: about PKR 3–4 cr", options: { bullet: true, breakLine: true } },
  { text: "Landlord-funded fit-out: about PKR 2–3 cr", options: { bullet: true, breakLine: true } },
  { text: "Stepped rent in Years 1–2: about PKR 1–1.5 cr", options: { bullet: true, breakLine: true } },
  { text: "Remaining PKR 3–5 cr from a partner or Islamic bank facility", options: { bullet: true } },
], { x: 6.6, y: 1.65, w: 2.7, h: 3.3, fontSize: 13, paraSpaceAfter: 6 });
s.addNotes("Savings are approximate and must be tested in the Excel model with real quotes before a lease is signed.");

// ================================================================== 11 Scenarios
s = slide("Content");
title(s, "A strong first intake decides the outcome");
const kv = (lab, i) => K[lab][i];
const fm = (v) => { const n = Number(v); return n < 0 ? `(${Math.abs(n).toFixed(1)})` : n.toFixed(1); };
const pc = (v) => (isNaN(Number(v)) ? String(v) : (Number(v) * 100).toFixed(1) + "%");
const rows = [
  ["Students in Year 5", (i) => String(kv("Students in Y5", i))],
  ["Net profit in Year 5 (PKR m)", (i) => fm(kv("Net profit in Y5, PKR million", i))],
  ["First net profit", (i) => kv("First year with a net profit", i)],
  ["Payback", (i) => kv("Payback year (cumulative cash flow turns positive)", i)],
  ["Peak funding need (PKR m)", (i) => fm(kv("Peak funding need (lowest cumulative cash flow), PKR million", i))],
  ["10-year return (IRR)", (i) => pc(kv("10-year internal rate of return", i))],
];
const hdr = ["", "Worst", "Base", "Best"].map((t, j) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 }, align: j ? "center" : "left" } }));
const body = rows.map(([lab, fn], r) => [{ text: lab, options: { bold: true } }, ...[0, 1, 2].map((i) => ({ text: fn(i), options: { align: "center", fill: { color: i === 1 ? C.background2 : C.background1 } } }))]);
s.addTable([hdr, ...body], { x: 0.5, y: 1.15, w: 9, colW: [3.6, 1.8, 1.8, 1.8], fontSize: 13, color: C.text1, border: { type: "solid", pt: 0.75, color: "E6DEDA" }, rowH: 0.42, valign: "middle" });
txt(s, "Worst: 20% fewer students, fees 5% lower, salaries 5% and rent 15% higher. Best: 12% more students, fees 5% higher, rent 5% lower.", { x: 0.5, y: 4.3, w: 9, h: 0.6, fontSize: 12, color: C.accent3 });

// ================================================================== 12 Governance
section = "Delivery"; sec(section);
s = slide("Content");
title(s, "A separate company with an independent Board");
const box = (x, y, w, t, sub, dark) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.62, rectRadius: 0.05, fill: { color: dark ? C.text2 : C.background2 }, line: { color: dark ? C.text2 : C.background2 }, objectName: "org " + t });
  s.addText([{ text: t, options: { bold: true, breakLine: !!sub } }, ...(sub ? [{ text: sub, options: { fontSize: 10 } }] : [])], { isTextBox: true, x, y, w, h: 0.62, fontSize: 12, align: "center", valign: "middle", color: dark ? C.background1 : C.text1, margin: 2 });
};
box(3.0, 1.1, 4.0, "Board of Governors", "founder (chair), 2 educators, finance, Shariah scholar, parent", true);
box(3.75, 2.05, 2.5, "Principal", "", true);
const heads = [["Head, Girls' Block", ""], ["Head, Boys' Block", ""], ["Head of Tarbiyah", ""], ["Bursar", "finance, HR, admin"], ["Admissions", "and marketing"]];
heads.forEach(([t, sub], i) => box(0.5 + i * 1.83, 3.0, 1.7, t, sub));
[[5, 1.72, 5, 2.05], [5, 2.67, 5, 2.85], [1.35, 2.85, 8.67, 2.85]].forEach(([x1, y1, x2, y2]) => s.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: HEX.accent2, width: 1.25 } }));
heads.forEach((_, i) => s.addShape(pres.shapes.LINE, { x: 1.35 + i * 1.83, y: 2.85, w: 0, h: 0.15, line: { color: HEX.accent2, width: 1.25 } }));
txt(s, "Private limited company (SECP), fully separate from The Deenway School. Board committees: Academic and Tarbiyah · Finance and Audit · People and Safeguarding. An advisory Shariah and Tarbiyah Council approves the Tarbiyah curriculum each year.", { x: 0.5, y: 3.9, w: 9, h: 1.0, fontSize: 13 });

// ================================================================== 13 Risks
s = slide("Content");
title(s, "Five risks to manage from day one");
const risks = [["High", "Slow first intake", "Admissions from September 2027, open days, founding-family offer"],
  ["High", "Funding gap in Years 0–2", "Agree the funding plan before signing the lease"],
  ["Medium", "Hiring Cambridge-trained teachers, especially women", "Recruit from November 2027; pay above market for key posts"],
  ["Medium", "Fee increases capped below cost inflation", "Confirm the Punjab rule; set launch fees right; payroll at or below 55% of revenue"],
  ["Medium", "Approval delays (FDA, registration, Cambridge)", "Start as soon as the building is chosen; use a consultant"]];
risks.forEach(([lvl, r, m], i) => {
  const y = 1.12 + i * 0.78;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y, w: 1.0, h: 0.6, rectRadius: 0.05, fill: { color: lvl === "High" ? C.accent5 : C.accent4 }, line: { color: lvl === "High" ? C.accent5 : C.accent4 }, objectName: "risk level " + (i + 1) });
  s.addText(lvl, { isTextBox: true, x: 0.5, y, w: 1.0, h: 0.6, fontSize: 12, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
  txt(s, r, { x: 1.7, y: y + 0.05, w: 3.4, h: 0.55, fontSize: 14, bold: true, color: C.text2 });
  txt(s, m, { x: 5.2, y: y + 0.05, w: 4.3, h: 0.55, fontSize: 13 });
});

// ================================================================== 14 Timeline
s = slide("Content");
title(s, "Seventeen months to opening day: April 2028");
const tl = [["Dec 26 – Feb 27", "Approve study and funding; register company and trademarks"],
  ["Mar – Jun 27", "Find building, sign lease; apply to Cambridge"],
  ["Jul – Oct 27", "Fit-out; hire Principal and block heads; admissions open"],
  ["Nov 27 – Jan 28", "Core team in post; hire teachers; first admissions round"],
  ["Feb – Mar 28", "Training, uniforms, parent orientation, inspections"],
  ["Apr 2028", "Adabury opens: Grades 3–9, both blocks"]];
s.addShape(pres.shapes.LINE, { x: 0.8, y: 2.65, w: 8.4, h: 0, line: { color: HEX.accent2, width: 2 } });
tl.forEach(([d, t], i) => {
  const x = 0.5 + i * 1.5;
  s.addShape(pres.shapes.OVAL, { x: x + 0.15, y: 2.45, w: 0.4, h: 0.4, fill: { color: i === 5 ? C.accent2 : C.text2 }, line: { color: C.background1, width: 1.5 }, objectName: "milestone " + (i + 1) });
  txt(s, d, { x, y: 1.6, w: 1.4, h: 0.6, fontSize: 14, bold: true, color: C.text2 });
  txt(s, t, { x, y: 3.1, w: 1.4, h: 1.9, fontSize: 13 });
});

// ================================================================== 15 Decisions
s = slide("Closing dark");
s.addText("Decisions needed", { placeholder: "title" });
s.addText([
  { text: "Approve the site search and registration stage", options: { bullet: { type: "number" }, breakLine: true } },
  { text: "Choose the funding approach for the gap", options: { bullet: { type: "number" }, breakLine: true } },
  { text: "Confirm 2028 fees: PKR 19,500 / 23,000 / 27,500", options: { bullet: { type: "number" }, breakLine: true } },
  { text: "Send real salary and rent figures to update the model", options: { bullet: { type: "number" }, breakLine: true } },
  { text: "Nominate the first Board and Shariah Council", options: { bullet: { type: "number" } } },
], { placeholder: "body" });
s.addImage({ data: crestRev, x: 7.4, y: 1.4, w: 1.8, h: 1.87, objectName: "Crest" });

(async () => {
  await pres.writeFile({ fileName: outPath });
  await applyTheme(outPath, THEME);
  console.log("wrote", outPath);
})();
