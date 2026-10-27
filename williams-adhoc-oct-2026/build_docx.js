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
  label('Ad-hoc opinion · Energy infrastructure'),
  headline('Williams: a quality pipeline, with the power story already in the price', 52),
  sub1('27 October 2026 · Syz Research'),
  P(r('Prices are as of the close on 26 October 2026 (New York listing, USD).', { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small('This note is intended for professional and qualified investors only. It reviews Williams ahead of its third-quarter 2026 results, which the company will publish on 2 November after the US market close. Figures quoted here run to the second quarter of 2026 and to company announcements made since. Please read the important information at the end of this document.')]),
  h2('US gas infrastructure: weak gas prices, strong demand for pipes'),
  cols([
    sub2('A cheap commodity, a valuable network'),
    body('US natural gas remains inexpensive. The Henry Hub benchmark traded around USD 3.1 to 3.2 per MMBtu in mid-October, with storage above its five-year average. For producers this is a headwind; for pipeline owners it matters much less, because most of their revenue comes from fees for reserved capacity rather than from the gas price.'),
    body('What drives pipeline value is demand for new capacity. Two sources stand out: liquefied natural gas exports from the Gulf Coast, and gas-fired power for data centres, whose electricity needs are growing faster than grids can connect them.'),
  ], [
    sub2('Pipeline companies move into power'),
    body('Some operators now build gas power plants directly at data centre sites, "behind the meter", so customers do not have to wait for a grid connection. Owning the gas supply and the pipeline gives them a cost and timing edge. Williams is among the most advanced of the large US operators in this field, with its first project for Meta in Ohio already partly in service.'),
    box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small('The sector offers fee-based cash flows with a growth kicker from power demand. The question for an investor is price: the market already pays a premium for the data centre theme, so the next leg of returns depends on new contracts being signed, not on the theme itself.')], (W-400)/2),
  ]),
  P(r('WILLIAMS SECOND QUARTER 2026 AT A GLANCE (USD)', { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([
    ['', 'Q2 2026', 'Comparison'],
    ['Adjusted EBITDA', '1.92bn', { t: '+6% y/y', color: MINT }],
    ['Available funds from operations', '1.45bn', { t: '+10% y/y', color: MINT }],
    ['Adjusted earnings per share', '0.50', { t: '+9% y/y (0.46)', color: MINT }],
    ['Dividend coverage (AFFO)', '2.26x', '2.16x a year earlier'],
    ['Debt to adjusted EBITDA', '3.67x', 'About 3.9x expected at year-end'],
    ['2026 adjusted EBITDA guidance', '8.3 to 8.5bn', { t: 'Midpoint raised by 200m', color: MINT }],
  ], [4200, 2400, 3606]),
  src('Source: Syz Research, Bloomberg, Company data'),

  label('Ad-hoc opinion · Energy infrastructure', true),
  headline('Williams Companies (WMB US)', 46),
  sub2('An irreplaceable gas network turning into a power supplier, valued as if the transition were already done'),
  grid4([
    kpi('Share price', 'USD 71.75', 'All-time high USD 79.40 (19 May)'),
    kpi('Performance 2026 to date', '+19%', 'Flat over six months', MINT),
    kpi('Forward P/E', '29.4x', 'Median since 2021: 22.7x'),
    kpi('Dividend yield', '2.9%', 'USD 2.10 a year, +5% in 2026'),
  ]),
  P(r('', { size: 4 }), { spacing: { after: 60, line: 120 } }),
  cols([
    h3('1.', 'What the company does'),
    body('Williams moves about one third of US natural gas. Its core is Transco, the country\'s largest gas pipeline system by volume, running from the Gulf Coast to New York. Most earnings come from regulated, fee-based transport and storage contracts, so they depend little on the gas price. Williams also gathers and processes gas in the Marcellus, Haynesville and Rockies basins, runs a gas marketing arm and, since 2025, builds gas power plants for data centres ("Power Innovation").', { size: 18, after: 40 }),
    h3('2.', 'Why it could do well'),
    body('Growth is visible and contracted. In August, management raised 2026 adjusted EBITDA guidance to USD 8.3 to 8.5bn and lifted its long-term target to 11%+ annual EBITDA growth through 2030. The first phase of Socrates, a 400 MW project for Meta in Ohio, is in service, with phase two due in the fourth quarter. Williams has announced more than 2.6 GW of power projects and cites a pipeline of over 6 GW. The USD 5.5bn purchase of Momentum Midstream, closed on 3 September, adds Haynesville gathering capacity of 6 Bcf/d feeding Gulf Coast LNG and industrial demand.', { size: 18, after: 40 }),
    h3('3.', 'What sets it apart'),
    body('Transco cannot be replicated: new interstate pipelines take years to permit, so existing routes gain value as demand grows. Williams also funds growth smartly. In July, a Blackstone-led group committed USD 5.34bn for 49% of five power projects, covering its share of their capital spending and paying Williams about USD 0.9bn upfront, while Williams keeps control and a buyback right. This protects the balance sheet, at the cost of sharing future profits.', { size: 18, after: 40 }),
  ], [
    h3('4.', 'Is the share cheap?'),
    body('No. At 29.4x forward earnings, Williams trades well above its median of 22.7x since 2021. Since January 2023, consensus forward EPS has risen by about a third, from USD 1.80 to USD 2.44, while the multiple went from about 18x to 29x: most of the share\'s doubling came from re-rating, not earnings. Even if earnings per share grew at the 11% EBITDA target, it would take about two and a half years at today\'s price to bring the multiple back to its median (Syz calculation). The share has stalled since February, a sign that the power story is largely priced. The 2.9% dividend yield, covered more than twice, offers some support.', { size: 18, after: 40 }),
    h3('5.', 'Main risks'),
    body('Valuation is the first: at this multiple, a delay in new power contracts could weigh on the share even if results are solid. The guidance increase came from the Momentum deal rather than the base business. The 2026 growth capital budget of USD 7.3 to 7.9bn brings execution and permitting risk on large projects such as the Northeast Supply Enhancement pipeline. Leverage rises to about 3.9x at year-end, and about USD 2bn of new shares issued to Momentum\'s sellers could weigh on the stock as they are sold. The marketing arm adds quarterly noise.', { size: 18, after: 40 }),
    h3('6.', 'What to watch next'),
    body('Third-quarter results on 2 November, the first with Momentum. Any new behind-the-meter contract with a data centre customer. Completion of Socrates phase two in the fourth quarter. The 2027 guidance, expected early in 2027, for the pace of growth and leverage.', { size: 18, after: 40 }),
  ]),
  box([boxlabel('CONCLUSION'), body('We like Williams as a business: a unique network, contracted growth and a well-covered, rising dividend. We are more cautious on the share, which already prices much of the power opportunity at 29x earnings. An investor who holds it could keep a core position for its quality and income, without adding at this level, especially if the portfolio already carries other data centre or US power names. An investor without exposure could wait for the third-quarter results and evidence of new power contracts, or build a position gradually rather than in one go.', { size: 18, after: 0 })]),

  label('Ad-hoc opinion · Energy infrastructure', true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r('Chart 1', { bold: true, color: TIGER, size: 24 }), r(' · WMB US: a doubling since 2023, then a pause', { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r('Daily closing price in USD and 200-day moving average since January 2023', { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r('Chart 2', { bold: true, color: TIGER, size: 24 }), r(' · WMB US: the multiple has risen faster than earnings', { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
  P(r('Consensus forward 12-month EPS in USD (top) and forward P/E (bottom) since January 2023; the dashed line is the median P/E since 2021', { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart2_eps_pe.png', 333)]),
  src('Source: Syz Research, Bloomberg'),

  label('Ad-hoc opinion · Energy infrastructure', true),
  h2('Sources'),
  P(r('Syz Research, Bloomberg, Company data', { size: 19 }), { spacing: { after: 60 } }),
  h2('Important information'),
  ...disclaimer.map(t => P(r(t.trim(), { size: 16 }), { alignment: AlignmentType.JUSTIFIED, spacing: { after: 90, line: 252 } })),
];

const doc = new Document({
  creator: 'Syz Research', title: 'Williams: a quality pipeline, with the power story already in the price',
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
