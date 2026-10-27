const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, Header, Footer, TabStopType, PageNumber, ShadingType, LevelFormat, VerticalAlign } = require('docx');
const DIR = process.argv[2], OUT = process.argv[3];
const SPACE='202945', BLUEBERRY='4B5F80', TIGER='FF6C0E', MINT='3BAF90', LINE='D9D9D9', F='Nunito';
const W = 10206; // content width in DXA (A4 minus 850 margins)

const r = (text, o={}) => new TextRun({ text, font: F, color: SPACE, size: 22, ...o });
const P = (children, o={}) => new Paragraph({ children: Array.isArray(children)?children:[children], ...o });
const body = (t, o={}) => P(r(t, {size: o.size||21}), { alignment: AlignmentType.JUSTIFIED, spacing: { after: o.after??100, line: 276 } });
const label = (t, brk=false) => P(r(t.toUpperCase(), { size: 17, color: BLUEBERRY, characterSpacing: 60 }), { pageBreakBefore: brk, spacing: { before: 60, after: 40 } });
const headline = (t, size=50) => P(r(t, { size, bold: true, color: TIGER }), { spacing: { after: 60 } });
const sub1 = t => P(r(t, { size: 28 }), { spacing: { after: 40 } });
const sub2 = t => P(r(t, { size: 22, bold: true, color: TIGER }), { spacing: { before: 60, after: 60 } });
const h2 = t => P(r(t, { size: 30, bold: true }), { spacing: { before: 180, after: 80 } });
const h3 = (n, t) => P([r(n + ' ', { size: 22, bold: true, color: TIGER }), r(t, { size: 22, bold: true })], { spacing: { before: 80, after: 30 } });
const boxlabel = (t, color=TIGER) => P(r(t, { size: 17, bold: true, color, characterSpacing: 20 }), { spacing: { after: 40 } });
const small = t => P(r(t, { size: 18 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 40 } });
const src = t => P(r(t, { size: 16 }), { spacing: { before: 60, after: 120 } });

const B = (style, size, color) => ({ style, size, color });
const none = B(BorderStyle.NONE, 0, 'FFFFFF');
const frame = B(BorderStyle.SINGLE, 14, SPACE);
const grey = B(BorderStyle.SINGLE, 4, LINE);
const margins = { top: 140, bottom: 140, left: 220, right: 220 };

// framed box: single cell, white, Space Blue frame
const box = (children, width=W) => new Table({ width: { size: width, type: WidthType.DXA }, columnWidths: [width],
  rows: [new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: width, type: WidthType.DXA }, margins, children,
    borders: { top: frame, bottom: frame, left: frame, right: frame } })] })] });

// four-cell KPI row
const grid4 = cells => { const cw = W/4; return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [cw,cw,cw,cw],
  rows: [new TableRow({ children: cells.map((c, i) => new TableCell({ width: { size: cw, type: WidthType.DXA }, margins: { top: 100, bottom: 100, left: 160, right: 120 },
    borders: { top: frame, bottom: frame, left: i===0?frame:grey, right: i===3?frame:grey }, children: c })) })] }); };
const kpi = (lab, val, note, valColor=SPACE) => [boxlabel(lab, BLUEBERRY), P(r(val, { size: 30, bold: true, color: valColor }), { spacing: { after: 20 } }), ...(note?[P(r(note, { size: 16 }))]:[])];
const tech = (lab, val) => [boxlabel(lab), P(r(val, { size: 26, bold: true }))];

// two text columns as a borderless table
const cols = (left, right) => { const g = 400, cw = (W-g)/2; const nb = { top: none, bottom: none, left: none, right: none };
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [cw, g, cw], borders: { insideHorizontal: none, insideVertical: none, top: none, bottom: none, left: none, right: none },
    rows: [new TableRow({ children: [
      new TableCell({ width: { size: cw, type: WidthType.DXA }, borders: nb, margins: { left: 0, right: 0 }, children: left }),
      new TableCell({ width: { size: g, type: WidthType.DXA }, borders: nb, children: [P(r(''))] }),
      new TableCell({ width: { size: cw, type: WidthType.DXA }, borders: nb, margins: { left: 0, right: 0 }, children: right })] })] }); };

// compact table: Space Blue rules top and bottom, thin grey rules between rows, no fills
const compact = (rows, widths = [3800, 1900, 2300, 2206]) => {
  const cell = (t, i, head, last, o={}) => new TableCell({ width: { size: widths[i], type: WidthType.DXA }, columnSpan: o.span, margins: { top: 70, bottom: 70, left: 120, right: 120 },
    borders: { top: head?frame:none, bottom: last?frame:grey, left: none, right: none },
    children: [P(r(head?t.toUpperCase():t, head ? { size: 16, bold: true, color: BLUEBERRY, characterSpacing: 20 } : { size: 20, color: o.color||SPACE }), { alignment: i===0?AlignmentType.LEFT:AlignmentType.RIGHT })] });
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: rows.map((row, ri) => new TableRow({ children:
    row.map((c, i) => typeof c === 'object' ? cell(c.t, i, ri===0, ri===rows.length-1, c) : cell(c, i, ri===0, ri===rows.length-1)) })) }); };

const chart = (file, h) => P(new ImageRun({ type: 'png', data: fs.readFileSync(`${DIR}/${file}`), transformation: { width: 640, height: h } }), { alignment: AlignmentType.CENTER });


const logo = fs.readFileSync(`${DIR}/syz-logo.png`);
const header = new Header({ children: [
  P(new ImageRun({ type: 'png', data: logo, transformation: { width: 51, height: 46 } }), { alignment: AlignmentType.RIGHT,
    border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: TIGER, space: 6 } }, spacing: { after: 0 } })] });
const footerX = null;
const footer = new Footer({ children: [P([r('Syz Research · Ad-hoc opinion · 27 October 2026', { size: 18 }), r('\t', { size: 18 }),
  new TextRun({ children: [PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], font: F, size: 18, color: SPACE })],
  { tabStops: [{ type: TabStopType.RIGHT, position: W }] })] });

const disclaimer = fs.readFileSync(process.argv[4], 'utf8').split('## 5. Important information (disclaimer, verbatim)')[1].split('## 6.')[0].trim().split('\n\n');

const children = [
  label("Ad-hoc opinion · Mining royalties"),
  headline("Altius Minerals: a record quarter, a sharp correction", 52),
  sub1('27 October 2026 · Syz Research'),
  P(r("Prices are as of the close on 26 October 2026 (Toronto listing, CAD).", { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small("This note is intended for professional and qualified investors only. It reviews Altius Minerals after its preliminary third-quarter revenue release of 20 October and ahead of full results on 10 November. Please read the important information at the end of this document.")]),
  h2("Royalty companies: revenue without running the mine"),
  cols([sub2("How royalties work"), body("A royalty company provides upfront money to a mine or energy project and in return receives a share of its revenue for many years, without paying operating or expansion costs. Margins are high and the model scales easily, but the royalty holder has no say in how or when the asset is developed."), body("Most listed royalty companies focus on gold and silver. A smaller group, including Altius, focuses on base metals, fertilisers, battery metals and, increasingly, renewable power.")],
       [sub2("Renewables and lithium: two different cycles"), body("Renewable power royalties pay out as wind and solar farms produce electricity, which makes them steady once projects are built. Lithium royalties behave very differently: lithium prices collapsed in 2023 and 2024 and remain volatile, so revenue swings with the market."),
        box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small("Royalty companies are usually valued on the worth of their royalties rather than on current earnings, and tend to trade at a premium for their low costs and diversification. The question for an investor is whether the growth now coming from renewables and lithium justifies that premium.")], (W-400)/2)]),
  P(r("ALTIUS THIRD QUARTER 2026 PRELIMINARY REVENUE (CAD)", { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([["", "Q3 2026", "Comparison"], ["Attributable royalty revenue", "33.2m", {"t": "+55% y/y (21.4m)", "color": MINT}], ["Electricity (renewables)", "13.2m", "Largest contributor"], ["Base metals", "8.5m", ""], ["Potash", "4.6m", ""], ["Lithium", "4.2m", {"t": "Down from 6.4m in Q2", "color": TIGER}], ["Iron ore", "1.6m", ""], ["Interest and investment income", "About 9m", {"t": "Included in the total above", "color": TIGER}]], [4200, 2400, 3606]),
  src('Source: Syz Research, Bloomberg, Company data'),

  label("Ad-hoc opinion · Mining royalties", true),
  headline("Altius Minerals (ALS CN)", 46),
  sub2("A diversified royalty portfolio pivoting to power and lithium, now 26% below its September high"),
  grid4([kpi("Share price", "CAD 50.59", "All-time high CAD 68.70 (22 Sep)"), kpi("Performance 2026 to date", "+24%", "-26% from the September high", MINT), kpi("Forward P/E", "66.7x", "Median since 2021: 57.3x"), kpi("Q3 attributable revenue", "CAD 33.2m", "+55% y/y, preliminary", MINT)]),
  P(r('', { size: 4 }), { spacing: { after: 60, line: 120 } }),
  cols([h3("1.", "What the company does"), body("Altius owns royalties on mines and power projects run by others. Its portfolio includes base metal royalties, notably on the Chapada copper mine in Brazil; potash royalties in Saskatchewan; iron ore interests in Labrador; lithium royalties acquired with Lithium Royalty Corp in March 2026; and a 50% stake in Great Bay Renewables, which funds US wind, solar and storage projects in exchange for revenue royalties. A project generation unit stakes mineral ground, sells it to developers and keeps royalties.", { size: 18, after: 40 }), h3("2.", "Why it could do well"), body("Growth is coming from new assets. Preliminary third-quarter attributable revenue reached a record CAD 33.2m, up 55% on a year earlier, with electricity now the largest contributor. In 2026, Altius bought Lithium Royalty Corp for about CAD 520m, raised its Great Bay Renewables stake to 50% and enlarged its credit facility, while a CAD 181.5m share issue in July strengthened the balance sheet. The Kami iron ore project, the Curipamba mine in Ecuador and the Arthur gold project in Nevada could add value over the next few years.", { size: 18, after: 40 }), h3("3.", "What sets it apart"), body("Origination. Altius creates many of its royalties itself at low cost through project generation. The clearest example is Arthur, where it sold a 1% royalty to Franco-Nevada in 2025 for up to USD 275m while keeping 0.5%. Its focus on base metals, fertilisers and renewables, rather than gold, also sets it apart from most royalty peers.", { size: 18, after: 40 })],
       [h3("4.", "Cheap, or a value trap?"), body("Neither clearly. At 66.7x forward earnings, the share is still above its median of 57.3x since 2021, even after falling 26% since 22 September. Forward EPS has roughly doubled since the end of 2025, from CAD 0.39 to CAD 0.76, on the back of acquisitions. The record quarter needs context: about CAD 9m of the CAD 33.2m came from interest and investment income, mainly on financing for renewable projects, rather than from royalties, and lithium revenue fell from the second quarter. Royalty companies are usually valued on their assets rather than on earnings, but the correction has removed only part of the premium. The dividend yield is below 1%.", { size: 18, after: 40 }), h3("5.", "Main risks"), body("Altius has no control over the projects it depends on: timelines for Kami, Curipamba or Arthur rest with their operators. Revenue remains sensitive to copper, potash and especially lithium prices. The renewables business depends on US power markets and policy toward wind and solar. Acquisitions were paid partly in shares, and the July share issue at CAD 60.50 is now above the market price, which can weigh on sentiment. No clear cause has been given for the recent fall, which makes the short term hard to read.", { size: 18, after: 40 }), h3("6.", "What to watch next"), body("Full third-quarter results on 10 November, including the contribution of the consolidated renewables business. Feasibility work on Kami and Arthur. First production at Curipamba, expected in 2027. Any new acquisition, and how it is financed.", { size: 18, after: 40 })]),
  box([boxlabel('CONCLUSION'), body("We see Altius as a well-run royalty company whose pivot to renewables and lithium adds growth, but also new sources of volatility. The recent fall offers a better entry point than in September, yet the valuation still assumes the new assets deliver, and the record quarter was flattered by interest income. An investor without exposure could build a position gradually, using weakness rather than buying in one go. An investor who holds it could keep the position and wait for the full third-quarter results before adding.", { size: 18, after: 0 })]),

  label("Ad-hoc opinion · Mining royalties", true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r("Chart 1", { bold: true, color: TIGER, size: 24 }), r(' ' + "· ALS CN: a strong run, then a 26% fall", { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r("Daily closing price in CAD and 200-day moving average since January 2023", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r("Chart 2", { bold: true, color: TIGER, size: 24 }), r(' ' + "· ALS CN: earnings estimates rebounded in 2026", { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
  P(r("Consensus forward 12-month EPS in CAD (top) and forward P/E (bottom) since January 2023; the dashed line is the median P/E since 2021", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart2_eps_pe.png', 333)]),
  src('Source: Syz Research, Bloomberg'),

  label("Ad-hoc opinion · Mining royalties", true),
  h2('Sources'),
  P(r('Syz Research, Bloomberg, Company data', { size: 19 }), { spacing: { after: 60 } }),
  h2('Important information'),
  ...disclaimer.map(t => P(r(t.trim(), { size: 16 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 90, line: 252 } })),
];

const doc = new Document({
  creator: 'Syz Research', title: "Altius Minerals: a record quarter, a sharp correction",
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
