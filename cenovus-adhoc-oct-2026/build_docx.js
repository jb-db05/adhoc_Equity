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
const compact = rows => { const widths = [3800, 1900, 2300, 2206];
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
const footer = new Footer({ children: [P([r('Syz Research · Ad-hoc opinion · 27 October 2026', { size: 18 }), r('\t', { size: 18 }),
  new TextRun({ children: [PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], font: F, size: 18, color: SPACE })],
  { tabStops: [{ type: TabStopType.RIGHT, position: W }] })] });

const disclaimer = fs.readFileSync(process.argv[4], 'utf8').split('## 5. Important information (disclaimer, verbatim)')[1].split('## 6.')[0].trim().split('\n\n');

const children = [
  // Page 1: cover
  label('Ad-hoc opinion · Energy'),
  headline('Cenovus Energy: a stronger company, a less obvious bargain', 52),
  sub1('27 October 2026 · Syz Research'),
  P(r('Prices are as of the close on 26 October 2026 (Toronto listing, CAD).', { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small("This note is intended for professional and qualified investors only. It reviews Cenovus Energy ahead of its third-quarter 2026 results, which the company usually publishes at the end of October. Third-quarter figures quoted here are the company's own estimates from its 5 October announcement and may be revised. Please read the important information at the end of this document.")]),
  h2('Canadian oil sands: record cash, borrowed in part from geopolitics'),
  cols([
    sub2('An oil price set by events, not by demand'),
    body('Brent has moved from close to USD 60 a barrel in mid-December 2025 to around USD 110 to 115 at the end of October 2026, after peaking near USD 138 in early April. The driver is supply risk in the Middle East, including disruption to shipping through the Strait of Hormuz, rather than a surge in global demand. Prices set by a conflict can fall quickly when tensions ease.'),
    body('Oil sands producers are among the most exposed to this move. Their costs are largely fixed, so most of each extra dollar per barrel flows straight to cash flow. Cenovus generated CAD 5.0bn of adjusted funds flow in the second quarter of 2026, against CAD 3.4bn in the first quarter.'),
  ], [
    sub2('Consolidation and better market access'),
    body('The sector has moved from growth at any cost to scale and returns. Cenovus closed its purchase of MEG Energy in November 2025 for more than CAD 8.6bn including assumed debt, and on 5 October 2026 agreed to buy Athabasca Oil for an implied enterprise value of CAD 5.7bn. Buying leases next to existing plants lets the buyer share facilities and cut unit costs.'),
    body('The Trans Mountain expansion, in service since May 2024, gives Canadian heavy crude a route to Pacific markets and has reduced the discount at which it trades to US benchmarks.'),
    box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small("Today's cash flows are exceptional and largely returned to shareholders. The question for an investor is how much of the share price now depends on oil staying above USD 100. For Cenovus, the operating progress is real, but the low earnings multiple mostly reflects earnings the market expects to fade.")], (W-400)/2),
  ]),
  P(r('CENOVUS SECOND QUARTER 2026 AT A GLANCE (CAD)', { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([
    ['', 'Q1 2026', 'Q2 2026', 'Change'],
    ['Revenue', '12.4bn', '17.4bn', { t: '+40%', color: MINT }],
    ['Operating margin', '4.4bn', '5.9bn', { t: '+34%', color: MINT }],
    ['Adjusted funds flow', '3.4bn', '5.0bn', { t: '+48%', color: MINT }],
    ['Excess free funds flow', '1.7bn', '3.3bn', { t: '+89%', color: MINT }],
    ['Net debt, end of quarter', '8.1bn', '5.4bn', { t: '-2.7bn', color: MINT }],
    ['Upstream production (boe/d)', 'broadly flat', '970,400', { t: '+200,000 y/y', color: MINT }],
  ]),
  src('Source: Cenovus Energy second-quarter 2026 results (29 July 2026), Syz Research'),

  // Page 2: company fiche
  label('Ad-hoc opinion · Energy', true),
  headline('Cenovus Energy (CVE CN)', 46),
  sub2('Record volumes and a fast-falling debt, priced at a multiple that assumes the oil windfall will fade'),
  grid4([
    kpi('Share price', 'CAD 46.54', 'All-time high CAD 48.40 (17 Sep)'),
    kpi('Performance 2026 to date', '+100%', '+95% over 12 months', MINT),
    kpi('Forward P/E', '8.2x', 'Median since 2021: 9.6x'),
    kpi('Net debt, end Q3 2026', '~CAD 3.0bn', 'Company estimate; CAD 5.0 to 5.5bn after Athabasca'),
  ]),
  P(r('', { size: 4 }), { spacing: { after: 0, line: 120 } }),
  grid4([tech('TECHNICAL TREND', 'Upward'), tech('SUPPORT', 'CAD 43.67'), tech('RESISTANCE', 'CAD 48.40'), tech('200-DAY AVERAGE', 'CAD 37.66')]),
  P(r('The share trades 24% above its 200-day average. A close above CAD 48.40 could open a new leg higher, while CAD 43.67, the early October low, is the level to watch on the downside.', { size: 18 }), { spacing: { before: 60, after: 20 } }),
  cols([
    h3('1.', 'What the company does'),
    body("Cenovus is Canada's second-largest oil producer. It extracts bitumen with steam (SAGD) at Christina Lake, Foster Creek and Sunrise, and has conventional and offshore assets. Downstream, it operates the Lloydminster upgrader and refinery and three US refineries (Lima, Toledo, Superior), with 472,800 bbl/d of capacity after the sale of its 50% WRB stake to Phillips 66. Second-quarter 2026 output was 970,400 boe/d, including a record 786,400 boe/d from the oil sands.", { size: 17, after: 30 }),
    h3('2.', 'Why it could do well'),
    body('Volumes are growing for company-specific reasons. Output is up by more than 200,000 boe/d in a year, driven by MEG and a record 372,100 bbl/d at Christina Lake. In July, the CEO said monthly production passed one million boe/d. 2026 guidance was raised to 970,000 to 1,010,000 boe/d, oil sands unit costs were cut by about 6% at the midpoint and capital spending held at CAD 5.0 to 5.3bn. MEG synergies are targeted at CAD 150m a year in 2026 and 2027, rising above CAD 400m from 2028. West White Rose, with a gross peak of about 80,000 bbl/d, was guided to first oil late in the third quarter.', { size: 17, after: 30 }),
    h3('3.', 'What sets it apart'),
    body('Scale and adjacency: the MEG and Athabasca leases sit next to Christina Lake, so new barrels can share plants and pipes. Athabasca adds about 45,000 boe/d and a plan to reach 115,000 bbl/d of thermal output by 2032. Cash returns are large: in the second quarter Cenovus returned CAD 1.4bn, including CAD 1.0bn of buybacks, and with net debt below CAD 6bn it targets returning about 75% of excess free funds flow. The refineries take far fewer heavy barrels than the oil sands produce, so most volumes still sell at Canadian heavy crude prices.', { size: 17, after: 30 }),
  ], [
    h3('4.', 'Cheap, or a value trap?'),
    body("Neither, quite. At 8.2x forward earnings, the share sits below its median of 9.6x since 2021. But consensus forward EPS has risen from about CAD 1.45 in early March to CAD 5.66 today, almost entirely because of the oil price. On the CAD 2.01 expected at the end of 2025, when Brent was near USD 60, today's price would be about 23x earnings (Syz calculation). The multiple has fallen while the share doubled: the market is valuing these earnings as a windfall. The balance sheet and volume growth rule out a value trap, but the share is cheap only if oil stays high. The CAD 0.88 annual dividend yields 1.9%; buybacks do most of the work.", { size: 17, after: 30 }),
    h3('5.', 'Main risks'),
    body('The oil price first: a de-escalation in the Middle East could cut earnings as fast as they rose. Athabasca lifts year-end net debt back to CAD 5.0 to 5.5bn and could issue up to 44.4m shares, which delays the move toward the CAD 4bn long-term target and a higher payout. Execution remains a watch point: West White Rose slipped from the second to the third quarter, and the downstream business has a history of unplanned outages. Carbon costs, including the Pathways carbon capture project, are a longer-term risk.', { size: 17, after: 30 }),
    h3('6.', 'What to watch next'),
    body('Third-quarter results, expected shortly, including confirmation of West White Rose first oil and the actual net debt. The Athabasca shareholder vote and closing, expected in December. The 2027 budget, usually published in December, for the pace of buybacks and the oil price assumption behind it.', { size: 17, after: 30 }),
  ]),
  box([boxlabel('CONCLUSION'), body('We are positive on Cenovus as a business, with volumes rising and debt falling. We are more cautious on the share after a 100% rise, because the low multiple rests on oil prices driven by conflict. An investor without exposure could build a position gradually and size it as an oil position. An investor who already holds it, possibly alongside other Canadian producers or energy funds, could take partial profits to bring the weight back to target while keeping a core position for buybacks and volume growth.', { size: 17, after: 0 })]),

  // Page 3: charts
  label('Ad-hoc opinion · Energy', true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r('Chart 1', { bold: true, color: TIGER, size: 24 }), r(' · CVE CN: the share has doubled in 2026', { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r('Daily closing price in CAD and 200-day moving average since January 2023, with the recent high and low as reference levels', { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r('Chart 2', { bold: true, color: TIGER, size: 24 }), r(' · CVE CN: earnings estimates have soared, the multiple has not', { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
  P(r('Consensus forward 12-month EPS in CAD (top) and forward P/E (bottom) since January 2024; the dashed line is the median P/E since 2021', { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart2_eps_pe.png', 333)]),
  src('Source: Syz Research, Bloomberg'),

  // Page 4: sources and disclaimer
  label('Ad-hoc opinion · Energy', true),
  h2('Sources'),
  ...['Syz Research, Bloomberg (share price, consensus forward EPS and P/E, moving averages; close of 26 October 2026)',
    "Cenovus Energy, second-quarter 2026 results and management's discussion and analysis, 29 July 2026",
    'Cenovus Energy, agreement to acquire Athabasca Oil Corporation, 5 October 2026',
    'Cenovus Energy, first-quarter 2026 results, 6 May 2026; 2026 capital budget and corporate guidance, 11 December 2025',
    'Cenovus Energy, fourth-quarter and full-year 2025 results (MEG synergy targets); closing of MEG Energy acquisition, 13 November 2025',
    'Cenovus Energy, sale of interest in WRB Refining to Phillips 66, 9 September 2025',
    'Press reports (July 2026 production above one million boe/d; MEG transaction value; Brent price levels and Middle East supply disruption)',
    'Syz calculation: share price of CAD 46.54 divided by the consensus forward EPS of CAD 2.01 recorded on 31 December 2025',
  ].map(t => P(r(t, { size: 19 }), { numbering: { reference: 'bullets', level: 0 }, spacing: { after: 30 } })),
  h2('Important information'),
  ...disclaimer.map(t => P(r(t.trim(), { size: 16 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 90, line: 252 } })),
];

const doc = new Document({
  creator: 'Syz Research', title: 'Cenovus Energy: a stronger company, a less obvious bargain',
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
