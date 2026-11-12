const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = '/home/user/adhoc_Equity/notes';
const SHOTS = path.join(__dirname, 'shots');
fs.mkdirSync(SHOTS, { recursive: true });
(async () => {
  const opts = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {};
  const browser = await chromium.launch(opts);
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  for (const slug of ['imperial-brands', 'prudential', 'kraft-heinz']) {
    for (let i = 1; i <= 3; i++) {
      const f = path.join(OUT, slug, `page-${i}.html`);
      await page.goto('file://' + f, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      const r = await page.evaluate(() => {
        const m = document.querySelector('main');
        return { overflow: m.scrollHeight - m.clientHeight, nunito: document.fonts.check('16px Nunito') };
      });
      console.log(slug, i, JSON.stringify(r));
      await page.screenshot({ path: path.join(SHOTS, `${slug}-${i}.png`) });
      await page.pdf({ path: path.join(SHOTS, `${slug}-${i}.pdf`), width: '794px', height: '1123px', printBackground: true });
    }
  }
  await browser.close();
})();
