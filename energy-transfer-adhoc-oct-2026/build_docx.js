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
  headline("Energy Transfer: a 6.6% yield, with strings attached", 52),
  sub1('27 October 2026 · Syz Research'),
  P(r("Prices are as of the close on 26 October 2026 (New York listing, USD).", { size: 18 }), { spacing: { after: 120 } }),
  box([boxlabel('IMPORTANT NOTICE'), small("This note is intended for professional and qualified investors only. It reviews Energy Transfer ahead of its third-quarter 2026 results, which the partnership will publish on 3 November before the US market opens. Figures quoted here run to the second quarter of 2026 and to announcements made since. Please read the important information at the end of this document.")]),
  h2("US midstream: record volumes, steady income"),
  cols([sub2("Volumes at record levels"), body("US pipeline operators are moving record volumes of gas, NGLs and crude oil. Permian output keeps growing with oil above USD 100 a barrel, Gulf Coast LNG terminals are taking more gas, and data centres are signing direct gas supply deals. For the largest networks, this means more fees at little extra cost."), body("Most of these companies are paid for capacity rather than for the commodity, so their cash flows are steadier than those of producers, and many return the bulk of that cash to investors.")],
       [sub2("Partnerships: high yields, different rules"), body("Several large operators, including Energy Transfer, are organised as master limited partnerships (MLPs). They issue units rather than shares and pay distributions rather than dividends. MLPs usually offer higher yields than corporations, but they come with specific US tax reporting (a K-1 form) and withholding rules for non-US holders."),
        box([boxlabel('WHAT THIS MEANS FOR INVESTORS'), small("MLPs suit income-focused investors who can handle the tax administration. Before investing, a non-US investor should check how the custodian handles MLP units, since US withholding can apply to both distributions and sale proceeds.")], (W-400)/2)]),
  P(r("ENERGY TRANSFER SECOND QUARTER 2026 AT A GLANCE (USD)", { size: 18, bold: true, color: TIGER, characterSpacing: 20 }), { spacing: { before: 160, after: 60 } }),
  compact([["", "Q2 2026", "Comparison"], ["Adjusted EBITDA", "5.07bn", {"t": "+31% y/y (3.87bn)", "color": MINT}], ["Net income attributable to partners", "2.09bn", {"t": "+80% y/y (1.16bn)", "color": MINT}], ["Distributable cash flow", "2.59bn", {"t": "+32% y/y (1.96bn)", "color": MINT}], ["Quarterly distribution per unit", "0.34", {"t": "Over 3% above a year earlier", "color": MINT}], ["2026 adjusted EBITDA guidance", "18.8 to 19.1bn", {"t": "Raised from 18.2 to 18.6bn", "color": MINT}], ["2026 organic growth capital", "5.6 to 5.9bn", "Excluding Sunoco and USA Compression"]], [4200, 2400, 3606]),
  src('Source: Syz Research, Bloomberg, Company data'),

  label("Ad-hoc opinion · Energy infrastructure", true),
  headline("Energy Transfer (ET US)", 46),
  sub2("One of the largest US pipeline networks, paying a 6.6% distribution well covered by cash flow"),
  grid4([kpi("Unit price", "USD 20.60", "52-week high USD 21.73 (10 Sep)"), kpi("Performance 2026 to date", "+25%", "+23% over 12 months", MINT), kpi("Forward P/E", "11.9x", "Median since 2021: 10.1x"), kpi("Distribution yield", "6.6%", "USD 1.36 a year, raised quarterly")]),
  P(r('', { size: 4 }), { spacing: { after: 60, line: 120 } }),
  cols([h3("1.", "What the company does"), body("Energy Transfer owns one of the largest and most diversified energy networks in the United States, with more than 140,000 miles of pipelines in 44 states. It gathers and processes gas; transports gas, crude oil and NGLs; runs fractionation plants and export terminals such as Nederland in Texas; and holds stakes in Sunoco and USA Compression. Around 90% of earnings come from fees, and no single segment provides more than about a third of EBITDA.", { size: 18, after: 40 }), h3("2.", "Why it could do well"), body("Results are strong. Second-quarter adjusted EBITDA rose 31% to USD 5.07bn on record volumes, and the 2026 guidance was raised to USD 18.8 to 19.1bn. The Hugh Brinson pipeline, carrying Permian gas to north Texas, is in service, and Energy Transfer has agreed to build facilities supplying a 900 MW expansion of Crusoe's AI data centre campus in Abilene. The USD 2.6bn purchase of Vaquero Midstream, due to close in the fourth quarter, adds 675 MMcf/d of Delaware Basin processing and is expected to add to cash flow per unit from the start.", { size: 18, after: 40 }), h3("3.", "What sets it apart"), body("Scale and the payout. Few networks match its reach across gas, crude and NGLs, which lets it sell integrated services and capture extra margin along the chain. Distributable cash flow of USD 2.59bn in the second quarter covered the distribution about twice (Syz calculation), leaving room to fund growth and keep raising the payout within the targeted 3% to 5% a year.", { size: 18, after: 40 })],
       [h3("4.", "Is the share cheap?"), body("Reasonably priced. At 11.9x forward earnings, the units trade above their median of 10.1x since 2021, but far below the 27x to 29x of Targa and Williams. Since January 2023, consensus forward EPS has risen only about 9%, from USD 1.59 to USD 1.73, while the multiple went from about 7x to 12x: the re-rating has largely played out, and further gains would need earnings growth. The 6.6% distribution yield is the main attraction, and it is well covered.", { size: 18, after: 40 }), h3("5.", "Main risks"), body("Capital discipline is the main question. Energy Transfer has a history of large acquisitions and heavy spending, with organic growth capital of USD 5.6 to 5.9bn this year and the large Desert Southwest gas pipeline ahead. The Vaquero deal is paid partly in 33.3m new units. Legal challenges around the Dakota Access pipeline remain an overhang. Part of the 2026 strength reflects high oil prices and wide regional price gaps, which may not last. For non-US investors, MLP tax reporting and withholding add cost and complexity.", { size: 18, after: 40 }), h3("6.", "What to watch next"), body("Third-quarter results on 3 November, including the ramp-up of Hugh Brinson. The closing of the Vaquero acquisition. The second phase of Hugh Brinson in early 2027. The 2027 guidance and capital budget early next year.", { size: 18, after: 40 })]),
  box([boxlabel('CONCLUSION'), body("We see Energy Transfer as the most attractive income vehicle among the US pipeline groups we have reviewed: the payout is high, well covered and growing, and the valuation is undemanding. The trade-offs are an appetite for large projects and deals, and the tax complexity of the MLP structure. An investor seeking income who can hold MLP units could build or keep a position, sized with any overlap with Targa, Williams or Enbridge in mind. An investor for whom K-1 reporting or US withholding is a problem could prefer corporate peers, accepting a lower yield.", { size: 18, after: 0 })]),

  label("Ad-hoc opinion · Energy infrastructure", true),
  h2('Charts'),
  P(r('Charts as of the close on 26 October 2026.', { size: 18 })),
  P([r("Chart 1", { bold: true, color: TIGER, size: 24 }), r(' ' + "· ET US: steady gains since 2023", { bold: true, size: 24 })], { spacing: { before: 200, after: 40 } }),
  P(r("Daily closing price in USD and 200-day moving average since January 2023", { size: 19, color: BLUEBERRY }), { spacing: { after: 80 } }),
  box([chart('chart1_price.png', 294)]),
  src('Source: Syz Research, Bloomberg'),
  P([r("Chart 2", { bold: true, color: TIGER, size: 24 }), r(' ' + "· ET US: the re-rating has outpaced earnings", { bold: true, size: 24 })], { spacing: { before: 160, after: 40 } }),
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
  creator: 'Syz Research', title: "Energy Transfer: a 6.6% yield, with strings attached",
  styles: { default: { document: { run: { font: F, color: SPACE, size: 21 } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1050, bottom: 650, left: 850, right: 850, header: 380, footer: 360 } } },
    headers: { default: header }, footers: { default: footer }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('written', OUT); });
