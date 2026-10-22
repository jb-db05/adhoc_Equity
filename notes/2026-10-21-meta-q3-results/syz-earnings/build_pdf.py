"""build_pdf.py: fill the template from content.py, render the PDF, rasterise the pages and write fill.json.
Usage: python3 build_pdf.py <out_dir> [W1 W2]"""
import html as H
import json
import re
import sys

from PIL import Image
from weasyprint import HTML
from pdf2image import convert_from_path

import content as C

OUT = sys.argv[1]
W1 = int(sys.argv[2]) if len(sys.argv) > 2 else 80
W2 = int(sys.argv[3]) if len(sys.argv) > 3 else 88
PDF = f"{OUT}/Earnings_Update_META_Q32026.pdf"


def words(s):
    return len(re.sub(r"&\w+;", " ", s).split())


def budget():
    rows = [("quote", C.QUOTE, 20, 35), ("P1", C.P1, 65, 85), ("C1 comment", C.C1_COMMENT, 55, 65),
            ("base case", C.BASE_CASE, 95, 110), ("upside", C.UPSIDE, 36, 45), ("downside", C.DOWNSIDE, 36, 45),
            ("A1 #1", C.A1[0], 100, 115), ("A1 #2", C.A1[1], 90, 105), ("A2 #1", C.A2[0], 70, 90), ("A2 #2 Muse", C.A2[1], 95, 115),
            ("C2 comment", C.C2_COMMENT, 85, 100)]
    rows += [(f"takeaway {i + 1}", t, 0, 18) for i, (_, _, t) in enumerate(C.TAKEAWAYS)]
    for name, text, lo, hi in rows:
        n = words(text)
        print(f"{name:12s} {n:4d}  [{lo}-{hi}]{'  <-- OUT' if not lo <= n <= hi else ''}")


def fill_html():
    quote = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
             if C.QUOTE else "")
    takeaways = "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>'
                          for c, l, t in C.TAKEAWAYS)
    kpis = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{d}</div></td>'
                     for l, v, d, s in C.KPIS)
    fill = {
        "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote,
        "TAKEAWAYS": takeaways, "KPI_TILES": kpis, "H_P1": C.H_P1, "P1_PARAGRAPH": f"<p>{C.P1}</p>",
        "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": f"{OUT}/c1_crop.png",
        "C1_COMMENT": f"<p>{C.C1_COMMENT}</p>", "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE,
        "DOWNSIDE": C.DOWNSIDE, "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1,
        "A1_PARAGRAPHS": "".join(f"<p>{p}</p>" for p in C.A1), "H_A2": C.H_A2, "A2_PARAGRAPHS": "".join(f"<p>{p}</p>" for p in C.A2),
        "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": f"{OUT}/c2_crop.png",
        "C2_COMMENT": f"<p>{C.C2_COMMENT}</p>", "SOURCE_LINE": C.SOURCE_LINE, "W1": W1, "W2": W2,
    }
    doc = open("template.html").read()
    for k, v in fill.items():
        doc = doc.replace("{{" + k + "}}", str(v))
    if not C.THEME:   # kicker without a sector
        doc = doc.replace(f"{C.DOC_TYPE} &middot; </div>", f"{C.DOC_TYPE}</div>")
    assert "{{" not in doc, "unfilled placeholder"
    assert "—" not in doc, "em dash"
    return doc


def plain(s):
    return H.unescape(s).replace("−", "-")


def fill_json(doc):
    legal = re.findall(r"<p>(This communication has.*?|This information is made.*?|This communication is not.*?|"
                       r"This communication may.*?|Past performance.*?|Nothing in the present.*?|"
                       r"Should a recipient.*?)</p>", doc, re.S)
    aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
    data = {
        "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
        "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": plain(C.TITLE),
        "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO),
        "TAKEAWAYS": [{"tag": c, "label": l, "text": plain(t)} for c, l, t in C.TAKEAWAYS],
        "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(d), "sign": s} for l, v, d, s in C.KPIS],
        "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1), "C1_TITLE": plain(C.C1_TITLE), "C1_SUB": plain(C.C1_SUB),
        "C1_IMG": f"{OUT}/c1_crop.png", "C1_ASPECT": aspect(f"{OUT}/c1_crop.png"), "W1": 66,
        "C1_COMMENT": plain(C.C1_COMMENT), "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE),
        "DOWNSIDE": plain(C.DOWNSIDE), "P2_TITLE": C.P2_TITLE, "H_A1": plain(C.H_A1),
        "A1_PARAGRAPHS": [plain(p) for p in C.A1], "H_A2": plain(C.H_A2), "A2_PARAGRAPH": [plain(p) for p in C.A2],
        "H_C2": plain(C.H_C2), "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB),
        "C2_IMG": f"{OUT}/c2_crop.png", "C2_ASPECT": aspect(f"{OUT}/c2_crop.png"), "W2": 80,
        "C2_COMMENT": plain(C.C2_COMMENT), "SOURCE_LINE": plain(C.SOURCE_LINE),
        "DISCLAIMER": [plain(p) for p in legal],
    }
    assert len(data["DISCLAIMER"]) == 7
    json.dump(data, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    budget()
    doc = fill_html()
    open(f"{OUT}/doc.html", "w").write(doc)
    HTML(f"{OUT}/doc.html").write_pdf(PDF)
    pages = convert_from_path(PDF, dpi=100)
    for i, p in enumerate(pages):
        p.save(f"{OUT}/page{i + 1}.png")
    print("pages:", len(pages))
    fill_json(doc)
