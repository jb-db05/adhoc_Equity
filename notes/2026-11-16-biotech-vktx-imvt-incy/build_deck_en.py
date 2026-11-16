import copy, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
SPACE, BLUE, TIGER, MANGO, GOLD, MINT, GREY, LINE = (RGBColor.from_string(c) for c in
    ("202945", "4B5F80", "FF6C0E", "FFA400", "FFC545", "3BAF90", "7A8494", "D9D9D9"))
FONT = "Open Sans"
DATE = "16 November 2026"

prs = Presentation(SRC)
layout = next(l for l in prs.slide_layouts if l.name == "One Content")
old_ids = list(prs.slides._sldIdLst)
cover_id, disc_id, final_id = old_ids[0], old_ids[14], old_ids[15]

# ---------- helpers ----------
def run(p, text, size=11, bold=False, color=SPACE, italic=False):
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = FONT; f.color.rgb = color
    return r

def textbox(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, name=None, margin=0):
    """paras: list of (runs, opts); runs = list of (text, size, bold, color)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name: tb.name = name
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
    first = True
    for runs, opts in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.alignment = opts.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(opts.get("after", 4))
        p.line_spacing = opts.get("ls", 1.05)
        for t in runs:
            run(p, *t)
    return tb

def P(text, size=10.5, bold=False, color=SPACE, after=4, align=PP_ALIGN.LEFT):
    return ([(text, size, bold, color)], {"after": after, "align": align})

def new_slide(title, subtitle):
    s = prs.slides.add_slide(layout)
    for ph in list(s.placeholders):
        idx = ph.placeholder_format.idx
        if idx == 0: ph.text_frame.text = title
        elif idx == 14: ph.text_frame.text = subtitle
        else: ph._element.getparent().remove(ph._element)
    for ph in s.placeholders:
        for p in ph.text_frame.paragraphs:
            for r in p.runs: r.font.name = FONT
    return s

def box(slide, x, y, w, h, name=None, line=SPACE, width=1.25):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.08
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(255, 255, 255)
    sh.line.color.rgb = line; sh.line.width = Pt(width)
    sh.shadow.inherit = False
    if name: sh.name = name
    sh.text_frame.text = ""
    return sh

def rect(slide, x, y, w, h, color, name=None, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background(); sh.shadow.inherit = False
    if name: sh.name = name
    return sh

def set_border(cell, side, color, w):
    tcPr = cell._tc.get_or_add_tcPr()
    tag = {"L": "a:lnL", "R": "a:lnR", "T": "a:lnT", "B": "a:lnB"}[side]
    for e in tcPr.findall(qn(tag)): tcPr.remove(e)
    ln = etree.SubElement(tcPr, qn(tag), w=str(int(w)))
    if color is None:
        etree.SubElement(ln, qn("a:noFill"))
    else:
        sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr"), val=str(color))
    # schema order: lnL lnR lnT lnB ... fill
    order = [qn(t) for t in ("a:lnL", "a:lnR", "a:lnT", "a:lnB")]
    lns = sorted([e for e in tcPr if e.tag in order], key=lambda e: order.index(e.tag))
    others = [e for e in tcPr if e.tag not in order]
    for e in list(tcPr): tcPr.remove(e)
    for e in lns + others: tcPr.append(e)

def table(slide, x, y, w, col_w, rows, size=10, header_size=10, row_h=0.3, first_col_bold=True,
          align_right_from=1, name=None, colors=None):
    nr, nc = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    if name: gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for a in ("bandRow", "firstRow"): tblPr.set(a, "0")
    st = tblPr.find(qn("a:tableStyleId"))
    if st is not None: tblPr.remove(st)
    for i, cw in enumerate(col_w): tbl.columns[i].width = Inches(cw)
    for r in range(nr):
        tbl.rows[r].height = Inches(row_h)
        for c in range(nc):
            cell = tbl.cell(r, c)
            cell.fill.background()
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if (c >= align_right_from) else PP_ALIGN.LEFT
            val = rows[r][c]
            if r == 0:
                run(p, val, header_size, True, GREY)
            else:
                col = SPACE
                if colors and (r, c) in colors: col = colors[(r, c)]
                run(p, val, size, bold=(c == 0 and first_col_bold) or bool(colors and (r, c) in colors), color=col)
            for side in "LRT": set_border(cell, side, None, 0)
            if r == 0 or r == nr - 1: set_border(cell, "B", "202945", 9525)
            else: set_border(cell, "B", "D9D9D9", 6350)
    return gf

def source(slide, text, y=7.38):
    textbox(slide, 0.73, y, 10.28, 0.3, [P(text, 8, color=BLUE)], name="Source")

def section_col(slide, x, y, w, h, blocks, size=10, name=None):
    paras = []
    for head, body in blocks:
        paras.append(P(head, size + 0.5, True, TIGER, after=2))
        paras.append(P(body, size, after=9))
    return textbox(slide, x, y, w, h, paras, name=name)

def kpis(slide, items, y=2.5, h=0.85):
    x0, W, gap = 0.73, 10.28, 0.18
    w = (W - gap * (len(items) - 1)) / len(items)
    for i, (label, value, note, vcol) in enumerate(items):
        x = x0 + i * (w + gap)
        box(slide, x, y, w, h, name=f"KPI {i+1}")
        textbox(slide, x + 0.15, y + 0.08, w - 0.3, h - 0.16, [
            P(label, 9, True, BLUE, after=1),
            ([(value, 17, True, vcol)], {"after": 0}),
            P(note, 8, color=BLUE, after=0)], anchor=MSO_ANCHOR.MIDDLE)

def conclusion(slide, text, y=6.62, h=0.7):
    box(slide, 0.73, y, 10.28, h, name="Conclusion box")
    textbox(slide, 0.93, y + 0.06, 9.9, h - 0.12, [
        ([("Conclusion  ", 10.5, True, TIGER), (text, 10.5, False, SPACE)], {"after": 0})],
        anchor=MSO_ANCHOR.MIDDLE, name="Conclusion")

# ---------- cover ----------
cover = prs.slides[0]
for ph in cover.placeholders:
    idx = ph.placeholder_format.idx
    if idx == 0:
        r = ph.text_frame.paragraphs[0].runs
        r[0].text = "US biotech: a fundamental view on VKTX, IMVT and INCY"
        for x in r[1:]: x.text = ""
    elif idx == 13:
        r = ph.text_frame.paragraphs[0].runs
        r[0].text = DATE + " · Syz Research"
        for x in r[1:]: x.text = ""

# ---------- 2. synthèse ----------
s = new_slide("INCY the most robust, IMVT partly validated, VKTX the most binary",
              "Fundamental summary · ranked by risk · " + DATE)
cards = [("INCY · Defensive profile", "Incyte · profitable, 2028 to bridge", BLUE),
         ("IMVT · Intermediate risk", "Immunovant · pre-revenue, platform partly validated", TIGER),
         ("VKTX · Binary risk", "Viking · one asset, one binary readout in 2027", GOLD)]
for i, (t, sub, col) in enumerate(cards):
    x = 0.73 + i * 3.49
    rect(s, x, 2.5, 0.06, 0.95, col, name=f"Accent {i+1}")
    textbox(s, x + 0.2, 2.5, 3.1, 0.95, [P(t, 15, True, after=4), P(sub, 9, color=BLUE, after=0)],
            anchor=MSO_ANCHOR.MIDDLE, name=f"Card {i+1}")
table(s, 0.73, 3.7, 10.28, [2.0, 2.76, 2.76, 2.76], [
    ["", "INCY", "IMVT", "VKTX"],
    ["Profile", "Profitable, 2026 sales ≈ USD 5.2–5.3 bn", "No revenue, IMVT-1402 in pivotal trials", "No revenue, VK2735 in Phase 3"],
    ["What is priced in", "The 2028 Jakafi cliff", "Success in several indications", "A lot of doubt"],
    ["Next test", "mutCALR pipeline, 2027 guidance", "Graves' and myasthenia gravis, 2027", "VANQUISH, 2H 2027"],
    ["Main risk", "Revenue gap after 2028", "FcRn competition, narrow float", "Trial outcome, funding, pricing"],
    ["Risk profile", "Moderate: profitable, pipeline risk", "High: pre-revenue", "Very high: one asset, one readout"],
], size=10, row_h=0.5, align_right_from=99, name="Synthesis table")
source(s, "Source: Syz Research, Bloomberg, company publications (Q3 2026).")

# ---------- 3. chiffres clés ----------
s = new_slide("Key fundamental figures",
              "USD · prices as of 13 November 2026, market caps as of 16 November 2026, balance sheets as of 30 September 2026")
table(s, 0.73, 2.5, 10.28, [4.0, 2.09, 2.09, 2.1], [
    ["", "INCY", "IMVT", "VKTX"],
    ["Share price (13 Nov 2026)", "120.12", "34.09", "26.96"],
    ["Market capitalisation (16 Nov 2026)", "24.7 bn", "7.1 bn", "3.7 bn"],
    ["Cash and short-term investments (30 Sep 2026)", "3.9 bn *", "722 m", "960 m"],
    ["Enterprise value (Bloomberg)", "20.8 bn", "6.2 bn", "2.8 bn"],
    ["Revenue 2025", "5.14 bn", "–", "–"],
    ["2026 net sales (raised guidance)", "5.21–5.30 bn", "–", "–"],
    ["EV / 2026 net sales (Syz calculation)", "≈ 4x", "–", "–"],
    ["Q3 2026 net result", "GAAP loss (1.23 bn Vega charge)", "Loss", "−183 m"],
    ["Cash runway (Syz calculation)", "Self-funded", "To a Graves' launch", "≈ 5 quarters"],
    ["Main catalyst", "Pipeline 2027–2028", "2027 data", "VANQUISH 2H 2027"],
], size=10.5, row_h=0.4, align_right_from=1, name="Key figures table",
   colors={(8, 3): TIGER, (9, 3): TIGER})
source(s, "EV: Bloomberg. EV / sales = Bloomberg EV / midpoint of 2026 guidance. VKTX runway = cash / Q3 net loss. "
          "* INCY cash to be confirmed after the Vega payment. Source: Syz Research, Bloomberg, company publications.", y=7.15)

# ---------- 4. calendrier ----------
s = new_slide("Catalysts are spread from late 2026 to 2028",
              "Timelines communicated by the companies · option expiries must cover the right window")
X0, X1, M = 2.45, 10.95, 26.0           # Nov 2026 -> Dec 2028
xm = lambda m: X0 + (X1 - X0) * m / M
top, lane_h = 2.75, 1.42
for m, lab in ((2, "2027"), (14, "2028")):
    ln = s.shapes.add_connector(1, Inches(xm(m)), Inches(top - 0.05), Inches(xm(m)), Inches(top + 3 * lane_h - 0.1))
    ln.line.color.rgb = LINE; ln.line.width = Pt(0.75)
    textbox(s, xm(m) + 0.05, top - 0.3, 0.75 if m == 0 else 1.2, 0.25, [P(lab, 9, True, GREY, after=0)])
lanes = [("INCY", BLUE, [(0.5, 2, 0, "Phase 3 mutCALR in myelofibrosis (start)"),
                         (2.5, 4, 1, "2027 guidance"),
                         (14, 26, 0, "Phase 3 KRAS G12D, pancreatic cancer"),
                         (14, 26, 1, "Jakafi US loss of exclusivity")]),
         ("IMVT", TIGER, [(0.5, 2, 0, "FDA End of Phase 2 meeting (RA)"),
                          (2, 14, 1, "Registrational data, Graves' and myasthenia gravis"),
                          (14, 26, 0, "Registrational data, CIDP")]),
         ("VKTX", GOLD, [(2, 5, 0, "VK3019 dose study (Q1)"),
                         (2, 14, 1, "Maintenance study, part 2"),
                         (8, 14, 0, "VANQUISH-1 and -2 (2H)"),
                         (14, 26, 1, "SUNRISE, oral version")])]
for li, (tick, col, evs) in enumerate(lanes):
    y = top + li * lane_h
    textbox(s, 0.73, y + 0.25, 1.5, 0.5, [P(tick, 15, True, after=0)], anchor=MSO_ANCHOR.MIDDLE)
    if li:
        ln = s.shapes.add_connector(1, Inches(0.73), Inches(y - 0.08), Inches(X1), Inches(y - 0.08))
        ln.line.color.rgb = LINE; ln.line.width = Pt(0.75)
    for (a, b, row, lab) in evs:
        yy = y + 0.12 + row * 0.62
        textbox(s, xm(a), yy, max(xm(b) - xm(a), 3.6), 0.26, [P(lab, 9.5, color=SPACE, after=0)])
        rect(s, xm(a), yy + 0.29, xm(b) - xm(a), 0.13, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
source(s, "Indicative timing communicated by the companies (Q3 2026); exact readout dates are not published. Source: Syz Research, company publications.", y=7.15)

# ---------- 5-7. fiches ----------
def fiche(title, sub, kp, left, right, concl):
    s = new_slide(title, sub)
    kpis(s, kp)
    section_col(s, 0.73, 3.55, 4.98, 3.0, left, size=11)
    section_col(s, 6.03, 3.55, 4.98, 3.0, right, size=11)
    conclusion(s, concl)
    source(s, "Source: Syz Research, Bloomberg, company publications. Syz calculations are labelled as such.", y=7.38)
    return s

fiche("Incyte: a profitable leader racing to replace Jakafi by 2028",
      "Incyte (INCY) · haematology, oncology, dermatology",
      [("Market cap", "USD 24.7 bn", "16 November 2026", SPACE),
       ("2026 net sales", "5.21–5.30 bn", "Raised with Q3 results", SPACE),
       ("Jakafi, Q3 2026", "USD 827 m", "+4% year on year", SPACE),
       ("EV / 2026 sales", "≈ 4x", "Syz calculation", SPACE)],
      [("Why it could do well",
        "Q3 revenue rose 14% to USD 1.56 bn and Opzelura sales rose 36% to USD 255 m. "
        "The business beyond Jakafi is already more than a third of sales. Jakafi XR, the once-daily version, "
        "has started to contribute."),
       ("The real lever: the pipeline",
        "The mutCALR antibody (INCA033989) is in a pivotal study in essential thrombocythaemia, with a Phase 3 "
        "in myelofibrosis from late 2026. The KRAS G12D inhibitor targets Phase 3 pancreatic cancer data in 2028. "
        "The Vega deal (USD 1.25 bn upfront) adds an asset in von Willebrand disease.")],
      [("Is the share cheap?",
        "About 4x 2026 sales (Syz calculation), a modest multiple for a profitable biotech. The discount reflects "
        "the 2028 risk: Jakafi is still close to 60% of net sales."),
       ("Main risks",
        "A revenue gap between 2028 and new launches, setbacks in the mutCALR or KRAS programmes, "
        "pricing pressure (Medicare negotiation), overpaying for deals. Q3 was a GAAP loss because "
        "of the Vega charge."),
       ("What to watch", "Start of the myelofibrosis Phase 3, mutCALR data, Jakafi XR uptake, 2027 guidance.")],
      "The most defensive of the three. Profits buy time to bridge 2028 and the valuation already prices in a "
      "good part of the risk. The 2027–2028 pipeline is the real test.")

fiche("Immunovant: an FcRn platform, now partly validated",
      "Immunovant (IMVT) · anti-FcRn IMVT-1402 · ~56% owned by Roivant",
      [("Market cap", "USD 7.1 bn", "16 November 2026", SPACE),
       ("Cash", "USD 722 m", "30 September 2026", SPACE),
       ("Enterprise value", "USD 6.2 bn", "Bloomberg", SPACE),
       ("Next data", "2027", "Graves', myasthenia gravis", SPACE)],
      [("Why it could do well",
        "In November the 600 mg dose met its primary endpoint in difficult-to-treat rheumatoid "
        "arthritis: 92.5% of patients kept their ACR20 response at week 28, against 75.6% on placebo. "
        "It is the first sign that an FcRn blocker can work in a common disease."),
       ("What sets it apart",
        "IMVT-1402 aims at deep IgG reduction without the albumin and LDL effects of first-generation "
        "agents. No FcRn drug is approved in Graves' disease: a possible first.")],
      [("Is the share cheap?",
        "Not on conventional measures: USD 6.2 bn of EV without revenue already assumes success in several "
        "indications. Cash should fund the company to a Graves' launch."),
       ("Main risks",
        "Competition from FcRn drugs already marketed by large groups. The result rests on one dose, "
        "with a high placebo rate, and a second pivotal trial is needed. Cutaneous lupus dropped, Sjögren's unlikely. "
        "Narrow float."),
       ("What to watch", "Outcome of the FDA meeting in late 2026, design of the next trial, 2027 data.")],
      "The company has moved from promise to a partly validated platform, but much of the good "
      "news is priced in. The 2027 data are the next test.")

fiche("Viking: a serious obesity contender facing a binary 2027",
      "Viking Therapeutics (VKTX) · VK2735, dual GLP-1/GIP agonist",
      [("Market cap", "USD 3.7 bn", "16 November 2026", SPACE),
       ("Cash", "USD 960 m", "30 September 2026", SPACE),
       ("Net loss, Q3 2026", "USD −183 m", "No revenue", TIGER),
       ("Phase 3 data", "2H 2027", "VANQUISH-1 and -2", SPACE)],
      [("Why it could do well",
        "Two fully enrolled Phase 3 trials (about 4,500 and 1,000 patients) and an oral version that entered Phase 3 "
        "(SUNRISE) in October, with data in 2028. A positive readout would make Viking one of very few independents "
        "with a late-stage dual agonist, injectable and oral."),
       ("What sets it apart",
        "In Phase 2, patients switched to every-other-week or monthly injections kept 82% to 97% "
        "of their weight loss. The VK3019 amylin programme adds a second mechanism.")],
      [("Cheap, or a value trap?",
        "An EV of about USD 2.8 bn (Bloomberg) looks small against the obesity market, but the doubt is "
        "rational: Viking would arrive years after the two leaders, in a market where prices are falling."),
       ("Main risks",
        "The readout itself, including tolerability and drop-outs. Funding: about five quarters of "
        "cash at the Q3 burn rate (Syz calculation), i.e. to the data; a raise or a partnership would "
        "very likely be needed. No sales force."),
       ("What to watch", "Maintenance part 2, VK3019, any partnering, then VANQUISH in 2H 2027.")],
      "The highest potential of the three, but the most concentrated risk: one asset, one readout window, "
      "a funding need. The profile stays binary until VANQUISH; takeover hopes alone do not justify the share.")

# ---------- 8. lien vers la proposition ----------
s = new_slide("From fundamentals to the proposal: match horizon and expiry",
              "Ideas to be priced by the desk · indicative theoretical prices as of 13 November 2026")
table(s, 0.73, 2.5, 10.28, [0.85, 1.45, 1.6, 3.2, 3.18], [
    ["", "Profile", "Key window", "Idea (indicative)", "Watch point"],
    ["INCY", "Defensive", "2027 guidance, mutCALR",
     "Holder: June 2027 collar, sell 140 call / buy 105 put, cost ≈ zero. New money: sell March 2027 110 put, premium ≈ USD 8",
     "Implied volatility of ~49% looks high for Incyte: check before setting strikes"],
    ["IMVT", "Intermediate", "FDA meeting late 2026, 2027 data",
     "Sell March 2027 30 put, premium ≈ USD 2.7 (effective entry ≈ 27.3). Or December 2027 35/50 call spread, cost ≈ USD 4 for a maximum gain of 15",
     "The investor must be willing to own the shares. Narrow float, high short interest: sharp moves"],
    ["VKTX", "Binary", "VANQUISH, 2H 2027",
     "No structure at this stage. If the investor insists: January 2028 30/50 call spread, cost ≈ USD 4 for a maximum gain of 20",
     "If the data slip past January 2028, the option expires before the readout"],
], size=9.5, header_size=10, row_h=1.0, align_right_from=99, name="Proposal table")
box(s, 0.73, 6.35, 10.28, 0.85, name="Avoid box")
textbox(s, 0.93, 6.4, 9.9, 0.75, [
    ([("Avoid  ", 10.5, True, TIGER),
      ("a worst-of structured product on the three names. The coupon would be high, but with volatilities of 50% to 70% "
       "and two binary readouts, the barrier is likely to be hit.", 10, False, SPACE)], {"after": 0})], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Theoretical Black-Scholes prices calculated by Syz from 13 Nov 2026 prices and implied volatilities (rate 3.75%), "
          "before fees and bid-ask spreads. Not binding: desk quotes required.", y=7.3)

# ---------- 9. points à vérifier ----------
s = new_slide("Before sending to the client: points to firm up",
              "Internal note · to address before finalising the proposal")
cols = [("Data", [
            "Bring all 13Fs to 30 Sep 2026 (deadline 14 Nov): Farallon +275% is as of 30 Jun, before the data.",
            "Fidelity +55% in VKTX: probably an allocation in the USD 500 m raise of 24 Sep, not open-market buying.",
            "Near-identical 60-day up/down ratios (0.69 / 0.69 / 0.68) and identical short interest for VKTX and IMVT (19.9%): recheck.",
            "Replace Yahoo Finance with Bloomberg (OMON, HDS, SI)."]),
        ("Reading", [
            "IMVT's 2.43 ratio comes mostly from the 9 Nov session (+15%, volume ×2.6): a reaction to data rather than accumulation.",
            "Open interest does not show who is buying: IMVT's Dec 2027 50 calls may be covered-call selling.",
            "VKTX 50, 60 and 120 calls are legacy positions with no signal value.",
            "INCY: the \"two Phase 3s by end-2026\" are trial starts, not readouts."]),
        ("Syz guidelines", [
            "Remove the average analyst targets.",
            "Do not make an entry depend on a single chart level (the \"30–31 zone\").",
            "Present the VKTX raise as dilution, not as a catalyst.",
            "Say \"an investor\"; never show entry prices or unrealised losses."])]
for i, (head, items) in enumerate(cols):
    x = 0.73 + i * 3.49
    box(s, x, 2.5, 3.3, 4.7, name=f"Check {head}")
    paras = [P(head, 14, True, TIGER, after=10)] + [P(t, 11, after=10) for t in items]
    textbox(s, x + 0.18, 2.62, 2.94, 4.5, paras)

# ---------- reorder ----------
lst = prs.slides._sldIdLst
new_ids = list(lst)[16:]
for e in list(lst): lst.remove(e)
for e in [cover_id] + new_ids + [disc_id, final_id]: lst.append(e)
prs.save(OUT)
print("slides:", len(lst))
