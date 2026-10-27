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
  label("Ad-hoc opinion \u00b7 Energy infrastructure"),
  headline("Enbridge: a reliable dividend, but little growth per share", 52),
  sub1('27 October 2026 · Syz Research'),
  P(r('Prices are as of the close on 26 October 2026 (Toronto listing, CAD).', { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small("This note is intended for professional and qualified investors only. It reviews Enbridge ahead of its third-quarter 2026 results, which the company will publish on 6 November before the market opens. Figures quoted here run to the second quarter of 2026 and to company announcements made since. Please read the important information at the end of this document.")]),
  h2("North American pipelines: steady cash, harder growth"),
  cols([sub2("A sector valued for its income"), body("Large pipeline operators earn most of their profits from regulated tariffs and long-term contracts that pay for reserved capacity whatever the volumes or the oil price. Investors therefore treat them partly as bond substitutes: they own them for a high, growing dividend rather than for rapid earnings growth."), body("Demand is supportive. Gas exports as liquefied natural gas are expanding, data centres need new gas-fired power, and Canadian crude still depends on pipelines to reach US refineries. Assets already in the ground gain value because new routes are hard to permit.")],
       [sub2("Growth now comes through deals and debt"), body("2026 has seen a wave of pipeline acquisitions. Enbridge agreed to buy Tallgrass's crude business for USD 2.55bn and Salt Creek Midstream's crude gathering business for USD 600m, and Williams bought Momentum Midstream for USD 5.5bn. These deals add earnings, but they are paid for with debt and new shares, so growth per share is slower than growth in total profits."),
        box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small("The sector suits investors seeking dependable income. The key checks are what is paid for that income, and whether the dividend can keep growing without stretching the balance sheet. For Enbridge, the dividend is secure, but per-share growth has stalled while the valuation has risen.")], (W-400)/2)]),
  P(r('ENBRIDGE SECOND QUARTER 2026 AT A GLANCE (CAD)', { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([["", "Q2 2026", "Comparison"], ["Adjusted EBITDA", "4.78bn", {"t": "+2.8% y/y (4.64bn)", "color": MINT}], ["Adjusted earnings per share", "0.63", {"t": "-3% y/y (0.65)", "color": TIGER}], ["Distributable cash flow", "2.95bn", "2026 guidance 5.70 to 6.10 per share"], ["Debt to EBITDA", "5.1x", {"t": "Above the 4.5x to 5.0x target range", "color": TIGER}], ["Secured growth backlog", "41bn", {"t": "Record level", "color": MINT}], ["2026 adjusted EBITDA guidance", "20.2 to 20.8bn", "Reaffirmed"]], [4200, 2400, 3606]),
  src('Source: Syz Research, Bloomberg, Company data'),

  label("Ad-hoc opinion \u00b7 Energy infrastructure", true),
  headline("Enbridge (ENB CN)", 46),
  sub2("A 5.7% dividend from contracted assets, with earnings per share that have not grown since 2023"),
  grid4([kpi("Share price", "CAD 67.65", "All-time high CAD 80.21 (24 Jul)"), kpi("Performance 2026 to date", "+3%", "-16% from the July high", MINT), kpi("Forward P/E", "23.6x", "Median since 2021: 18.5x"), kpi("Dividend yield", "5.7%", "CAD 3.88 a year, raised for 31 years")]),
  P(r('', { size: 4 }), { spacing: { after: 60, line: 120 } }),
  cols([h3("1.", "What the company does"), body("Enbridge is North America's largest energy infrastructure company. Its Mainline, the world's longest crude oil pipeline system, carries about 3 million barrels a day from western Canada to US refineries, and liquids pipelines provide about half of group EBITDA. It also runs major US gas pipelines such as Texas Eastern, gas utilities in Ontario and, since the purchase of three Dominion utilities, in Ohio, Utah and North Carolina, plus a smaller renewable power business. About 98% of EBITDA comes from regulated or long-term contracted assets.", { size: 18, after: 40 }), h3("2.", "Why it could do well"), body("The secured growth backlog reached a record CAD 41bn in July, much of it in US gas pipelines and utilities serving LNG exports and data centres. Management reaffirmed 2026 guidance of CAD 20.2 to 20.8bn of adjusted EBITDA and CAD 5.70 to 6.10 of distributable cash flow per share, and targets about 5% annual growth in both after 2026. The Tallgrass and Salt Creek purchases extend its crude network to the Rockies and the Permian, and should add to earnings from 2027.", { size: 18, after: 40 }), h3("3.", "What sets it apart"), body("Scale and contracts. Few companies own hard-to-replicate networks in both crude and gas, and its cash flows have been resilient through oil price cycles. The dividend has risen for 31 consecutive years. At CAD 3.88 a year, it absorbs about two thirds of the midpoint of 2026 distributable cash flow guidance (Syz calculation), a comfortable level for a pipeline company.", { size: 18, after: 40 })],
       [h3("4.", "Is the share cheap?"), body("No. At 23.6x forward earnings, Enbridge trades well above its median of 18.5x since 2021. Consensus forward EPS has slipped from about CAD 3.05 in January 2023 to CAD 2.87 today, while the multiple rose from about 18x to 24x: the share's rise since 2023 came entirely from re-rating. In the second quarter, EBITDA grew 2.8% but adjusted EPS fell to CAD 0.63 from 0.65, as higher interest and depreciation absorbed the growth. The share has fallen 16% since its July high, which removes some of the excess. The 5.7% yield, rather than earnings growth, is what an investor is buying.", { size: 18, after: 40 }), h3("5.", "Main risks"), body("Leverage first: debt stands at 5.1x EBITDA, above the 4.5x to 5.0x target range. That prompted a CAD 3.0bn share issue in September (44.7m shares at CAD 66.85, about 2% dilution) before Tallgrass contributes. Per-share growth could keep lagging total growth if more equity is needed. Line 5 still faces legal challenges in Michigan and Wisconsin. As a high-yield stock, Enbridge is also sensitive to rising bond yields.", { size: 18, after: 40 }), h3("6.", "What to watch next"), body("Third-quarter results on 6 November, with the leverage update after the share issue. The December dividend announcement and 2027 guidance. The closing of the Tallgrass deal. The handover from Greg Ebel to Michele Harradence, head of the gas utilities business, as CEO on 1 January 2027.", { size: 18, after: 40 })]),
  box([boxlabel('CONCLUSION'), body("We see Enbridge as a dependable income holding rather than a growth story. The dividend looks secure, but per-share earnings have not grown in three years and leverage is stretched, so the valuation leaves little room for disappointment. An investor holding it for income could keep it as a core position, noting the overlap if the portfolio also holds Williams, TC Energy or other pipeline names. An investor looking for capital gains could find better growth elsewhere. An investor without exposure who wants the yield could build a position gradually rather than in one go.", { size: 18, after: 0 })]),

  label("Ad-hoc opinion \u00b7 Energy infrastructure", true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r("Chart 1", { bold: true, color: TIGER, size: 24 }), r("· ENB CN: a strong run, cut short in August".replace(/^/, ' '), { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r("Daily closing price in CAD and 200-day moving average since January 2023", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r("Chart 2", { bold: true, color: TIGER, size: 24 }), r("· ENB CN: the multiple rose while earnings did not".replace(/^/, ' '), { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
  P(r("Consensus forward 12-month EPS in CAD (top) and forward P/E (bottom) since January 2023; the dashed line is the median P/E since 2021", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart2_eps_pe.png', 333)]),
  src('Source: Syz Research, Bloomberg'),

  label("Ad-hoc opinion \u00b7 Energy infrastructure", true),
  h2('Sources'),
  P(r('Syz Research, Bloomberg, Company data', { size: 19 }), { spacing: { after: 60 } }),
  h2('Important information'),
  ...disclaimer.map(t => P(r(t.trim(), { size: 16 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 90, line: 252 } })),
];

const doc = new Document({
  creator: 'Syz Research', title: "Enbridge: a reliable dividend, but little growth per share",
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
