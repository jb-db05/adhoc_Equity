const fs = require('fs');
const d = require('docx');
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, Header, Footer, PageNumber, PositionalTab, PositionalTabAlignment, PositionalTabRelativeTo,
  PositionalTabLeader, LevelFormat, LineRuleType, TabStopType, Tab, VerticalAlign, PageBreak, TableLayoutType } = d;
const C = JSON.parse(fs.readFileSync('content.json', 'utf8'));
const DIR = process.argv[2], OUT = process.argv[3];
const SPACE = '202945', BLUEBERRY = '4B5F80', TIGER = 'FF6C0E', MINT = '3BAF90', LINE = 'D9D9D9';
const F = 'Nunito', FL = 'Nunito Light';
const W = 10346; // content width in DXA
const txt = (p, i) => C[p][i][1];

const run = (t, o = {}) => new TextRun({ text: t, font: o.light ? FL : F, size: o.size || 18, bold: !!o.bold,
  color: o.color || SPACE, characterSpacing: o.spacing, allCaps: !!o.caps });
const para = (t, o = {}) => new Paragraph({ alignment: o.align || AlignmentType.JUSTIFIED,
  spacing: { before: o.before || 0, after: o.after ?? 110, line: o.line || 250, lineRule: LineRuleType.AUTO }, keepNext: !!o.keepNext,
  children: Array.isArray(t) ? t : [run(t, o)] });
const label = t => para(t, { light: true, size: 14, color: BLUEBERRY, spacing: 56, caps: true, after: 60, before: 120, align: AlignmentType.LEFT });
const headline = (t, size = 42) => para(t, { bold: true, size, color: TIGER, after: 40, line: 240, align: AlignmentType.LEFT });
const h2 = t => para(t, { bold: true, size: 26, before: 200, after: 80, keepNext: true, align: AlignmentType.LEFT });
const h3 = t => para(t, { bold: true, size: 20, color: TIGER, before: 140, after: 40, keepNext: true, align: AlignmentType.LEFT });
const body = (t, size = 18) => para(t, { size });

const NB = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };
const frame = { style: BorderStyle.SINGLE, size: 12, color: SPACE };
const boxBorders = { top: frame, bottom: frame, left: frame, right: frame, insideHorizontal: NB, insideVertical: { style: BorderStyle.SINGLE, size: 4, color: LINE } };

function box(children, opts = {}) {
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], layout: TableLayoutType.FIXED, borders: boxBorders,
    rows: [new TableRow({ children: [new TableCell({ width: { size: W, type: WidthType.DXA }, children,
      margins: { top: opts.pad ?? 140, bottom: opts.pad ?? 120, left: 220, right: 220 } })] })] });
}
function twoCols(left, right) {
  const cw = 5000, gap = W - 2 * cw;
  const cell = (children, w) => new TableCell({ width: { size: w, type: WidthType.DXA }, children, margins: { top: 0, bottom: 0, left: 0, right: 0 } });
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [cw, gap, cw], layout: TableLayoutType.FIXED, borders: noBorders,
    rows: [new TableRow({ children: [cell(left, cw), cell([new Paragraph({ children: [] })], gap), cell(right, cw)] })] });
}
function kpis(items) {
  const cw = W / 4;
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [cw, cw, cw, cw], layout: TableLayoutType.FIXED, borders: boxBorders,
    rows: [new TableRow({ children: items.map(([l, v, n, col]) => new TableCell({ width: { size: cw, type: WidthType.DXA },
      margins: { top: 140, bottom: 140, left: 200, right: 160 }, children: [
        para(l, { bold: true, size: 15, color: BLUEBERRY, after: 20, align: AlignmentType.LEFT }),
        para(v, { bold: true, size: 24, after: 20, line: 240, align: AlignmentType.LEFT }),
        para(n, { size: 15, color: col || SPACE, after: 0, align: AlignmentType.LEFT })] })) })] });
}
const img = (file, w, h) => new ImageRun({ type: 'png', data: fs.readFileSync(file), transformation: { width: w, height: h } });
const chartBox = file => box([new Paragraph({ alignment: AlignmentType.CENTER, children: [img(`${DIR}/${file}`, 600, 276)] })], { pad: 100 });
const spacer = (after = 120) => new Paragraph({ spacing: { after, before: 0 }, children: [] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const header = logoH => new Header({ children: [
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 140 }, children: [img(`${DIR}/syz-logo.png`, Math.round(logoH * 206 / 186), logoH)] }),
  new Paragraph({ spacing: { after: 0 }, children: [img('gradbar.png', 690, 4)] })] });
const footer = new Footer({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }], children: [
  run('Syz Research · Ad-hoc opinion · 17 November 2026', { size: 16 }),
  new TextRun({ font: F, size: 16, color: SPACE, children: [new Tab(), PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES] })] })] });

// Page 1: cover
const p1 = [
  label(txt('p1', 0)), headline(txt('p1', 1)), , para(txt('p1', 2), { light: true, size: 23, after: 220, align: AlignmentType.LEFT }),
  box([para('IMPORTANT NOTICE', { bold: true, size: 15, color: TIGER, spacing: 16, after: 40, align: AlignmentType.LEFT }), para(txt('p1', 4), { size: 18, after: 0 })]),
  h2(txt('p1', 5)),
  twoCols([h3(txt('p1', 6)), body(txt('p1', 7), 19), body(txt('p1', 8), 19), h3(txt('p1', 9)), body(txt('p1', 10), 19)],
          [h3(txt('p1', 11)), body(txt('p1', 12), 19), body(txt('p1', 13), 19), h3(txt('p1', 14)), body(txt('p1', 15), 19)]),
  pageBreak()];

// Page 2: company fiche
const s = i => txt('p2', i);
const p2 = [
  label(s(0)), headline(s(1), 37), para(s(2), { bold: true, size: 20, color: TIGER, after: 160, align: AlignmentType.LEFT }),
  kpis([[s(3), s(4), s(5)], [s(6), s(7), s(8)], [s(9), s(10), s(11), MINT], [s(12), s(13), s(14), TIGER]]),
  spacer(40),
  twoCols([h3(s(15)), body(s(16)), h3(s(17)), body(s(18)), h3(s(19)), body(s(20))],
          [h3(s(21)), body(s(22)), h3(s(23)), body(s(24)), h3(s(25)), body(s(26))]),
  spacer(120),
  box([para('CONCLUSION', { bold: true, size: 15, color: TIGER, spacing: 16, after: 40, align: AlignmentType.LEFT }), para(s(28), { size: 18, after: 0 })]),
  pageBreak()];

// Page 3: charts
const ct = t => { const [, a, b] = t.split('§'); return para([run(a, { bold: true, size: 22, color: TIGER }), run(b, { bold: true, size: 22 })], { before: 200, after: 20, align: AlignmentType.LEFT, keepNext: true }); };
const p3 = [
  label(txt('p3', 0)), h2(txt('p3', 1)), body(txt('p3', 2), 19),
  ct(txt('p3', 3)), para(txt('p3', 4), { size: 17, color: BLUEBERRY, after: 80, align: AlignmentType.LEFT, keepNext: true }), chartBox('chart1.png'),
  para(txt('p3', 5), { size: 15, before: 60, after: 0, align: AlignmentType.LEFT }),
  ct(txt('p3', 6)), para(txt('p3', 7), { size: 17, color: BLUEBERRY, after: 80, align: AlignmentType.LEFT, keepNext: true }), chartBox('chart2.png'),
  para(txt('p3', 8), { size: 15, before: 60, after: 0, align: AlignmentType.LEFT }),
  pageBreak()];

// Page 4: sources and disclaimer
const p4 = [label(txt('p4', 0)), h2(txt('p4', 1)),
  ...C.p4.filter(x => x[0] === 'li').map(x => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 30, line: 250, lineRule: LineRuleType.AUTO },
    children: [run(x[1], { size: 17 })] })),
  h2(C.p4.find(x => x[1] === 'Important information')[1]),
  ...C.p4.slice(C.p4.findIndex(x => x[1] === 'Important information') + 1).map(x => para(x[1], { size: 15, after: 90, line: 250 }))];

const doc = new Document({
  creator: 'Syz Research', title: 'SpaceX ad-hoc opinion, 17 November 2026',
  styles: { default: { document: { run: { font: F, size: 18, color: SPACE } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 280, hanging: 200 } }, run: { color: SPACE } } }] }] },
  sections: [{
    properties: { titlePage: true, page: { size: { width: 11906, height: 16838 }, margin: { top: 1900, bottom: 900, left: 780, right: 780, header: 420, footer: 450 } } },
    headers: { default: header(46), first: header(70) },
    footers: { default: footer, first: footer },
    children: [...p1, ...p2, ...p3, ...p4] }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync(OUT, b));
