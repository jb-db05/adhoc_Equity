// Render each A4 page to PNG (overflow check) and PDF, then report overflow.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
  for (let i = 1; i <= 5; i++) {
    await p.goto('file://' + path.resolve(__dirname, `page${i}.html`)); await p.evaluate(() => document.fonts.ready);
    const o = await p.evaluate(() => { const pg = document.querySelector('.page'); const f = document.querySelector('footer');
      const kids = [...pg.children].filter(e => e.tagName !== 'FOOTER'); const last = kids[kids.length - 1].getBoundingClientRect().bottom;
      return { overflow: pg.scrollHeight > pg.clientHeight, gap: Math.round(f.getBoundingClientRect().top - last), fonts: document.fonts.check('12px Nunito') }; });
    console.log('page', i, JSON.stringify(o));
    await p.screenshot({ path: path.resolve(__dirname, `preview/page${i}.png`) });
    await p.pdf({ path: path.resolve(__dirname, `preview/page${i}.pdf`), width: '794px', height: '1123px', printBackground: true });
  }
  await b.close();
})();
