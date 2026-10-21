// Render each A4 page, check that nothing overflows into the footer, and export PDF + PNG previews.
const { chromium } = require('playwright');
const path = require('path');

const pages = [1, 2, 3, 4, 5].map(n => `page${n}.html`);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  let ok = true;
  for (const file of pages) {
    await page.goto('file://' + path.resolve(__dirname, file));
    await page.evaluate(() => document.fonts.ready);
    const check = await page.evaluate(() => {
      const p = document.querySelector('.page');
      const footer = p.querySelector('footer');
      const fTop = footer.getBoundingClientRect().top;
      let maxBottom = 0;
      p.querySelectorAll('*').forEach(el => {
        if (footer.contains(el)) return;
        maxBottom = Math.max(maxBottom, el.getBoundingClientRect().bottom);
      });
      return { gap: Math.round(fTop - maxBottom), overflow: p.scrollHeight > p.clientHeight,
               font: getComputedStyle(p).fontFamily, nunito: document.fonts.check('12px Nunito') };
    });
    if (check.gap < 0 || check.overflow) ok = false;
    console.log(file, JSON.stringify(check));
    await page.screenshot({ path: path.resolve(__dirname, 'preview', file.replace('.html', '.png')) });
    await page.pdf({ path: path.resolve(__dirname, 'preview', file.replace('.html', '.pdf')),
                     width: '794px', height: '1123px', printBackground: true, pageRanges: '1' });
  }
  await browser.close();
  if (!ok) { console.error('OVERFLOW'); process.exit(1); }
})();
