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
  label("Ad-hoc opinion · Energy infrastructure"),
  headline("Targa Resources: the best Permian growth story, priced for it", 52),
  sub1('27 October 2026 · Syz Research'),
  P(r("Prices are as of the close on 26 October 2026 (New York listing, USD).", { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small("This note is intended for professional and qualified investors only. It reviews Targa Resources ahead of its third-quarter 2026 results, which the company will publish on 5 November before the US market opens. Figures quoted here run to the second quarter of 2026 and to company announcements made since. Please read the important information at the end of this document.")]),
  h2("Permian midstream: more gas, more liquids, more pipes"),
  cols([sub2("High oil prices keep Permian drilling busy"), body("The Permian Basin in west Texas and New Mexico is the largest US oil field. Each barrel of oil there comes with natural gas and natural gas liquids (NGLs) such as ethane and propane, which must be gathered, processed and moved to the Gulf Coast. With Brent above USD 100 a barrel for most of 2026, producers have kept drilling and these volumes keep rising."), body("Pipeline capacity has struggled to keep up. Bottlenecks around the Waha hub in west Texas have at times pushed local gas prices below zero in recent years, and new pipelines are being built to carry the gas toward Texas and Louisiana markets.")],
       [sub2("Exports pull the chain"), body("US exports of liquefied petroleum gas (LPG) keep growing. Companies that own the full chain, from the gas plant to the export dock, can collect a fee at every step and profit when regional prices diverge. Targa is one of a handful of operators that own the whole chain."),
        box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small("The Permian offers the fastest volume growth in US midstream, but it remains tied to oil drilling. The question for an investor is how much of that growth is already priced: the best-positioned names now trade at premium multiples.")], (W-400)/2)]),
  P(r("TARGA SECOND QUARTER 2026 AT A GLANCE (USD)", { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([["", "Q2 2026", "Comparison"], ["Adjusted EBITDA", "1.60bn", {"t": "+38% y/y (1.16bn)", "color": MINT}], ["Net income attributable to Targa", "765m", {"t": "+22% y/y (629m)", "color": MINT}], ["Quarterly dividend per share", "1.25", {"t": "+25% y/y", "color": MINT}], ["Consolidated leverage", "3.4x", "Within the 3x to 4x target"], ["2026 adjusted EBITDA outlook", "5.7 to 5.9bn", {"t": "Top end of the range expected", "color": MINT}], ["2026 growth capital", "About 5.0bn", {"t": "Raised from 4.5bn in August", "color": TIGER}]], [4200, 2400, 3606]),
  src('Source: Syz Research, Bloomberg, Company data'),

  label("Ad-hoc opinion · Energy infrastructure", true),
  headline("Targa Resources (TRGP US)", 46),
  sub2("A fully integrated Permian NGL chain delivering record results, at a record share price"),
  grid4([kpi("Share price", "USD 304.68", "All-time high, set on 26 Oct"), kpi("Performance 2026 to date", "+65%", "+98% over 12 months", MINT), kpi("Forward P/E", "26.8x", "Median since 2021: 21.6x"), kpi("Dividend yield", "1.6%", "USD 5.00 a year, +25% in 2026")]),
  P(r('', { size: 4 }), { spacing: { after: 60, line: 120 } }),
  cols([h3("1.", "What the company does"), body("Targa is the largest gatherer and processor of natural gas in the Permian Basin. Its gathering and processing business collects gas at the wellhead and separates out the liquids. Its logistics business then moves the NGLs by pipeline to its fractionation hub at Mont Belvieu, Texas, where they are split into products, and exports LPG from its Galena Park terminal near Houston. Most earnings come from fees, but part of the processing business is still paid as a share of the products sold, which keeps some exposure to commodity prices.", { size: 18, after: 40 }), h3("2.", "Why it could do well"), body("Volumes and contracts. Second-quarter adjusted EBITDA reached a record USD 1.60bn, up 38% on a year earlier, and management expects 2026 to land at the top end of its USD 5.7 to 5.9bn range. In August, Targa signed 20-year agreements with ExxonMobil covering Delaware and Midland acreage, with three new processing plants (about 825 MMcf/d) and a new gas pipeline due in the first half of 2028, and up to five more plants under study. The 25% dividend increase signals confidence in future cash flow.", { size: 18, after: 40 }), h3("3.", "What sets it apart"), body("Integration. Keeping molecules on its own system from the well to the dock lets Targa earn a fee at each step and capture marketing gains when prices differ between regions. Acreage dedications from leading Permian producers, now including a 20-year anchor with ExxonMobil, give volume visibility into the 2040s. Leverage of 3.4x is comfortable for the sector.", { size: 18, after: 40 })],
       [h3("4.", "Is the share cheap?"), body("No. At 26.8x forward earnings, Targa trades above its median of 21.6x since 2021. Unlike some peers, the rise rests on real earnings growth: consensus forward EPS has nearly doubled since January 2023, from about USD 5.97 to USD 11.35. A re-rating from about 12x to 27x did the rest, and the share has quadrupled. Part of the recent strength is less repeatable: press reports put second-quarter marketing gains, linked to regional price gaps, at around USD 250m, and these could fade as new pipelines ease bottlenecks. The 1.6% dividend yield offers little support if sentiment turns.", { size: 18, after: 40 }), h3("5.", "Main risks"), body("Valuation first: after a 65% rise this year, a slowdown in Permian drilling or a fall in oil prices could hit both earnings estimates and the multiple. Targa still has more commodity exposure than most large US midstream groups. Growth capital of about USD 5bn in 2026 keeps free cash flow thin until large projects start up. Long lead times for turbines and compressors could delay new plants.", { size: 18, after: 40 }), h3("6.", "What to watch next"), body("Third-quarter results on 5 November, and whether 2026 EBITDA comes in above the range. The 2027 outlook, expected early in 2027, for capital spending and the timing of higher free cash flow. Progress on the ExxonMobil plants and any decision on the additional plants under study.", { size: 18, after: 40 })]),
  box([boxlabel('CONCLUSION'), body("We like Targa as the best-positioned operator in the Permian, with earnings growth that justifies part of its re-rating. The share, however, sits at an all-time high and a premium multiple, which leaves little room for disappointment. An investor who holds it could take partial profits to bring the weight back to target, keeping a core position for its growth. An investor without exposure could build a position gradually, after the third-quarter results, rather than chase the recent rise. Holders of Energy Transfer or Williams already have overlapping US midstream exposure.", { size: 18, after: 0 })]),

  label("Ad-hoc opinion · Energy infrastructure", true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r("Chart 1", { bold: true, color: TIGER, size: 24 }), r(' ' + "· TRGP US: a fourfold rise since 2023", { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r("Daily closing price in USD and 200-day moving average since January 2023", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r("Chart 2", { bold: true, color: TIGER, size: 24 }), r(' ' + "· TRGP US: earnings and the multiple have both doubled", { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
  P(r("Consensus forward 12-month EPS in USD (top) and forward P/E (bottom) since January 2023; the dashed line is the median P/E since 2021", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart2_eps_pe.png', 333)]),
  src('Source: Syz Research, Bloomberg'),

  label("Ad-hoc opinion · Energy infrastructure", true),
  h2('Sources'),
  P(r('Syz Research, Bloomberg, Company data', { size: 19 }), { spacing: { after: 60 } }),
  h2('Important information'),
  ...disclaimer.map(t => P(r(t.trim(), { size: 16 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 90, line: 252 } })),
];

const doc = new Document({
  creator: 'Syz Research', title: "Targa Resources: the best Permian growth story, priced for it",
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
