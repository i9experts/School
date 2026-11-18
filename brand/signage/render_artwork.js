// Render each signage artwork page to PNG at its exact pixel size.
// Usage: node render_artwork.js <html-dir> <png-out-dir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [src, out] = process.argv.slice(2);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(src, f), 'utf8');
    const [, w, h] = html.match(/width:(\d+)px;height:(\d+)px/);
    const p = await b.newPage({ viewport: { width: +w, height: +h } });
    await p.setContent(html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
    await p.close();
    console.log('rendered', f);
  }
  await b.close();
})();
