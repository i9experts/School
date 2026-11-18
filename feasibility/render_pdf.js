// Render the feasibility report HTML to an A4 PDF.
// Usage: node render_pdf.js <report.html> <out.pdf>
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  const html = fs.readFileSync(src, 'utf8');
  await p.setContent(`<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">${html}</body></html>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: 'print', colorScheme: 'light' });
  await p.pdf({
    path: out, format: 'A4', printBackground: true,
    margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' },
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font:8px Arial;color:#888;text-align:center">Adabury School, Faisalabad · Feasibility study · Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
  });
  await b.close();
  console.log('pdf', out);
})();
