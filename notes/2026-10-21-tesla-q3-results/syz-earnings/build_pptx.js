// build_pptx.js: Syz Earnings update, portrait A4 PowerPoint with the same visual as the PDF.
// Usage: node build_pptx.js fill.json out.pptx
// fill.json carries the same keys as the HTML template (plain text, no HTML entities).
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const [fillPath, outPath] = process.argv.slice(2);
const F = JSON.parse(fs.readFileSync(fillPath, "utf8"));

const NAVY = "202945", BLUEB = "4B5F80", ORANGE = "FF6C0E", AMBER = "FFA400", MINT = "3BAF90";
const GREY = "6B7280", LIGHT = "9AA0A8", HAIR = "D6D9DE", WHITE = "FFFFFF";
const FONT = "Nunito";
const W = 8.27, H = 11.69, ML = 0.59, MR = 0.59, MT = 0.71, MB = 0.49;   // A4 portrait, PDF margins
const CW = W - ML - MR;

const pres = new pptxgen();
pres.defineLayout({ name: "A4P", width: W, height: H });
pres.layout = "A4P";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.author = "Syz Research"; pres.title = F.TITLE;

// ---- text metrics (Nunito Bold, calibrated against the WeasyPrint render)
// CSS line-height values from the PDF template; PowerPoint's multiple is relative to ~1.2 x font size
const LH = 1.42, NAT = 1.2;
const mult = lh => lh / NAT;
function lines(text, pt, width) {
  const cpl = Math.max(10, Math.floor((width * 72) / (pt * 0.475)));
  return text.split("\n").reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);
}
function hOf(text, pt, width, lh = LH) { return (lines(text, pt, width) * pt * lh) / 72; }

// ---- page chrome
function chrome(slide, pageNo) {
  slide.background = { color: WHITE };
  slide.addImage({ path: F.LOGO, x: W - MR - 0.55, y: 0.18, w: 0.55, h: 0.55 * 186 / 206 });
  slide.addImage({ path: F.GRADBAR, x: ML, y: MT, w: CW, h: 0.045 });
  slide.addText(`Syz Research · ${F.DOC_TYPE} · ${F.DATE}`, {
    x: ML, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: 7, color: LIGHT, bold: true, margin: 0, isTextBox: true, valign: "bottom" });
  slide.addText(`${pageNo} / 3`, {
    x: W - MR - CW / 2, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: 7, color: LIGHT, bold: true, margin: 0, align: "right", isTextBox: true, valign: "bottom" });
  return MT + 0.045 + 0.16;   // y after the gradient rule
}

// ---- flow helpers (all return the new y)
function para(slide, y, text, opts = {}) {
  const pt = opts.pt || 8.7, w = opts.w || CW, x = opts.x || ML;
  const h = hOf(text, pt, w) + 0.02;
  slide.addText(text, { x, y, w, h, fontFace: FONT, fontSize: pt, color: opts.color || NAVY, bold: true,
    align: opts.align || "justify", valign: "top", margin: 0, isTextBox: true, lineSpacingMultiple: mult(LH), paraSpaceAfter: 0 });
  return y + h + (opts.gap === undefined ? 0.087 : opts.gap);
}
function h2(slide, y, text) {
  slide.addText(text, { x: ML, y, w: CW, h: 0.24, fontFace: FONT, fontSize: 11, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  return y + 0.24 + 0.03;
}
function chartTitle(slide, y, num, title, sub) {
  slide.addText([{ text: `Chart ${num}`, options: { color: ORANGE } }, { text: ` · ${title}`, options: { color: NAVY } }],
    { x: ML, y, w: CW, h: 0.2, fontFace: FONT, fontSize: 9.5, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += 0.2;
  const hs = hOf(sub, 7.2, CW, 1.3);
  slide.addText(sub, { x: ML, y, w: CW, h: hs, fontFace: FONT, fontSize: 7.2, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.3) });
  return y + hs + 0.05;
}
function chart(slide, y, path, widthPct, aspect) {
  const w = CW * widthPct / 100, h = w * aspect;
  slide.addImage({ path, x: ML + (CW - w) / 2, y, w, h });
  return y + h + 0.06;
}

// ================= PAGE 1
let s = pres.addSlide();
let y = chrome(s, 1);
s.addText(F.THEME ? `${F.DOC_TYPE} · ${F.THEME}` : F.DOC_TYPE, { x: ML, y, w: CW, h: 0.18, fontFace: FONT, fontSize: 8, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
y += 0.21;
const th = hOf(F.TITLE, 17, CW, 1.22);
s.addText(F.TITLE, { x: ML, y, w: CW, h: th, fontFace: FONT, fontSize: 17, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.22) });
y += th + 0.04;
s.addText(`${F.DATE} · Syz Research`, { x: ML, y, w: CW, h: 0.18, fontFace: FONT, fontSize: 8.5, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
y += 0.18 + 0.05;
if (F.STATUS) {
  const sh = hOf(F.STATUS, 8.5, CW, 1.3);
  s.addText(F.STATUS, { x: ML, y, w: CW, h: sh, fontFace: FONT, fontSize: 8.5, color: ORANGE, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.3) });
  y += sh;
}
y += 0.13;

if (F.QUOTE) {
  const qw = CW - 0.2, qh = hOf(F.QUOTE, 9.8, qw, 1.35);
  s.addShape(pres.ShapeType.rect, { x: ML, y, w: 0.047, h: qh + 0.26, fill: { color: ORANGE }, line: { color: ORANGE, width: 0 } });
  s.addText(`“${F.QUOTE}”`, { x: ML + 0.2, y: y + 0.02, w: qw, h: qh, fontFace: FONT, fontSize: 9.8, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.35) });
  s.addText(F.QUOTE_WHO, { x: ML + 0.2, y: y + qh + 0.06, w: qw, h: 0.17, fontFace: FONT, fontSize: 7.6, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += qh + 0.26 + 0.13;
}

y = h2(s, y, "Key takeaways");
for (const t of F.TAKEAWAYS) {
  const col = t.tag === "pos" ? MINT : t.tag === "neg" ? ORANGE : BLUEB;
  const tw = CW - 0.65, hh = hOf(t.text, 8.7, tw);
  s.addText(t.label, { x: ML, y: y + 0.015, w: 0.63, h: hh, fontFace: FONT, fontSize: 7, color: col, bold: true, charSpacing: 0.8, margin: 0, isTextBox: true, valign: "top" });
  s.addText(t.text, { x: ML + 0.65, y: y - 0.01, w: tw, h: hh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
  y += hh + 0.05;
}
y += 0.08;

// key numbers strip: the only box on the page
const kh = 0.74;
s.addShape(pres.ShapeType.rect, { x: ML, y, w: CW, h: kh, fill: { color: WHITE }, line: { color: NAVY, width: 1.3 } });
F.KPIS.forEach((k, i) => {
  const cx = ML + (CW / 4) * i, cw = CW / 4;
  if (i > 0) s.addShape(pres.ShapeType.line, { x: cx, y: y, w: 0, h: kh, line: { color: HAIR, width: 0.6 } });
  s.addText(k.label, { x: cx + 0.12, y: y + 0.09, w: cw - 0.2, h: 0.16, fontFace: FONT, fontSize: 7.2, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.value, { x: cx + 0.12, y: y + 0.25, w: cw - 0.2, h: 0.26, fontFace: FONT, fontSize: 13, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.sub, { x: cx + 0.12, y: y + 0.51, w: cw - 0.2, h: 0.16, fontFace: FONT, fontSize: 7.2, color: k.sign === "pos" ? MINT : k.sign === "neg" ? ORANGE : BLUEB, bold: true, margin: 0, isTextBox: true, valign: "top" });
});
y += kh + 0.13;

y = h2(s, y, F.H_P1);
y = para(s, y, F.P1_PARAGRAPH);
y = chartTitle(s, y, 1, F.C1_TITLE, F.C1_SUB);
y = chart(s, y, F.C1_IMG, F.W1, F.C1_ASPECT);
y = para(s, y, F.C1_COMMENT);
y += 0.04;
y = h2(s, y, "Base case and implications");
y = para(s, y, F.BASE_CASE);
y += 0.04;
const colW = CW / 2 - 0.2;
const uh = hOf(F.UPSIDE, 8.7, colW), dh = hOf(F.DOWNSIDE, 8.7, colW), ch = Math.max(uh, dh) + 0.22;
s.addShape(pres.ShapeType.line, { x: ML + CW / 2, y, w: 0, h: ch, line: { color: HAIR, width: 0.6 } });
s.addText("What would strengthen our view", { x: ML, y, w: colW, h: 0.17, fontFace: FONT, fontSize: 7.8, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.UPSIDE, { x: ML, y: y + 0.21, w: colW, h: uh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
s.addText("What would change our view", { x: ML + CW / 2 + 0.2, y, w: colW, h: 0.17, fontFace: FONT, fontSize: 7.8, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.DOWNSIDE, { x: ML + CW / 2 + 0.2, y: y + 0.21, w: colW, h: dh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
y += ch;
console.log("page 1 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 2
s = pres.addSlide();
y = chrome(s, 2);
if (F.P2_TITLE) {
  s.addText(F.P2_TITLE, { x: ML, y, w: CW, h: 0.3, fontFace: FONT, fontSize: 14, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += 0.3 + 0.08;
}
y = h2(s, y, F.H_A1);
for (const p of F.A1_PARAGRAPHS) y = para(s, y, p);
y += 0.04;
y = h2(s, y, F.H_A2);
for (const p of [].concat(F.A2_PARAGRAPH)) y = para(s, y, p);
y += 0.04;
y = h2(s, y, F.H_C2);
y = chartTitle(s, y, 2, F.C2_TITLE, F.C2_SUB);
y = chart(s, y, F.C2_IMG, F.W2, F.C2_ASPECT);
y = para(s, y, F.C2_COMMENT);
console.log("page 2 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 3: source + disclaimer pinned to the bottom
s = pres.addSlide();
chrome(s, 3);
const legal = F.DISCLAIMER;
let lh = 0;
const parts = legal.map(p => { const h = hOf(p, 6.8, CW, 1.4) + 0.06; lh += h; return h; });
const srcH = 0.2, headH = 0.2;
let ly = H - MB - 0.35 - lh - srcH - headH - 0.16;
s.addText([{ text: "SYZ", options: { color: ORANGE } }, { text: ` ${F.SOURCE_LINE}`, options: { color: LIGHT } }],
  { x: ML, y: ly, w: CW, h: srcH, fontFace: FONT, fontSize: 6.8, bold: true, margin: 0, isTextBox: true, valign: "top" });
ly += srcH + 0.16;
s.addText("Disclaimer", { x: ML, y: ly, w: CW, h: headH, fontFace: FONT, fontSize: 6.8, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
ly += headH;
legal.forEach((p, i) => {
  s.addText(p, { x: ML, y: ly, w: CW, h: parts[i], fontFace: FONT, fontSize: 6.8, color: LIGHT, bold: true, align: "justify", margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.4) });
  ly += parts[i];
});

pres.writeFile({ fileName: outPath }).then(() => console.log("written", outPath));
