"""Build the merged luxury note: HTML pages -> PDF, and a PowerPoint laid out from the rendered HTML.

Run from any directory:  python3 build.py
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C  # noqa: E402

STEM = "Syz_LVMH-Hermes_ad-hoc_2026-11-26"
N = 6


def head(title):
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="style.css"></head>\n<body>\n')


def header(cover=False):
    return ('  <header><img class="logo" src="syz-logo.png" alt="Syz"><div class="bar"></div></header>\n')


def footer(n):
    return f'  <footer><span>{C.FOOTER}</span><span>{n} / {N}</span></footer>\n</div>\n</body></html>\n'


def kpis(rows, style=""):
    cells = "".join(f'<div><div class="kpilabel">{a}</div><div class="boxvalue">{b}</div>'
                    f'<div class="kpinote">{c}</div></div>' for a, b, c in rows)
    return f'  <div class="box grid4"{style}>{cells}</div>\n'


def blocks(items):
    out = []
    for kind, txt in items:
        if kind == "p":
            out.append(f"<p>{txt}</p>")
        elif kind == "sub2":
            out.append(f'<div class="sub2">{txt}</div>')
        elif kind == "h3":
            out.append(f"<h3>{txt}</h3>")
    return "\n      ".join(out)


def cols(left, right, style=""):
    return (f'  <div class="cols"{style}>\n    <div>\n      {blocks(left)}\n    </div>\n'
            f'    <div>\n      {blocks(right)}\n    </div>\n  </div>\n')


def page_sector():
    s = C.SECTOR
    return (head("Luxury sector") + '<div class="page cover">\n' + header(True)
            + f'  <div class="label">{C.LABEL}</div>\n  <h1 class="headline">{s["headline"]}</h1>\n'
            + f'  <div class="sub1">{s["sub1"]}</div>\n'
            + f'  <div class="box notice"><div class="boxlabel">IMPORTANT NOTICE</div><p>{s["notice"]}</p></div>\n'
            + kpis(s["kpis"], ' style="margin-top:14px"')
            + f'  <h2>{s["h2"]}</h2>\n' + cols(s["left"], s["right"]) + footer(1))


def page_fiche(d, n):
    tech = "".join(f'<div><div class="boxlabel">{a}</div><div class="boxvalue" style="font-size:14px">{b}</div></div>'
                   for a, b in d["tech"])
    return (head(d["headline"]) + '<div class="page fiche">\n' + header()
            + f'  <div class="label">{C.LABEL}</div>\n  <h1 class="headline">{d["headline"]}</h1>\n'
            + f'  <div class="sub2" style="font-size:14px">{d["sub2"]}</div>\n'
            + kpis(d["kpis"], ' style="margin-top:10px"')
            + f'  <div class="box grid4" style="margin-top:10px">{tech}<div class="techline">{d["techline"]}</div></div>\n'
            + cols(d["left"], d["right"], ' style="margin-top:4px"')
            + f'  <div class="box concl"><div class="boxlabel" style="margin-bottom:2px">CONCLUSION</div>'
              f'<p>{d["conclusion"]}</p></div>\n'
            + footer(n))


def page_charts(title, charts, n, img_h):
    out = [head(title) + '<div class="page">\n' + header(),
           f'  <div class="label">{C.LABEL}</div>\n  <h2 style="margin-top:12px">{title}</h2>\n']
    for i, (num, t, sub, img) in enumerate(charts):
        mt = "" if i == 0 else ' style="margin-top:12px"'
        out.append(f'  <div class="chartblock"{mt}>\n'
                   f'    <div class="charttitle"><span class="num">{num}</span> · {t}</div>\n'
                   f'    <div class="chartsub">{sub}</div>\n'
                   f'    <div class="box chartframe"><img src="{img}" alt="{t}" style="height:{img_h}px"></div>\n'
                   f'    <div class="src">{C.SRC}</div>\n  </div>\n')
    return "".join(out) + footer(n)


def page_sources():
    disc = "\n    ".join(f"<p>{p}</p>" for p in C.DISCLAIMER)
    return (head("Sources") + '<div class="page">\n' + header()
            + '  <h2 style="margin-top:14px">Sources</h2>\n  <ul class="sources">\n'
              '    <li>Syz Research, Bloomberg, Company data.</li>\n  </ul>\n'
            + f'  <h2 style="margin-top:10px">Important information</h2>\n  <div class="disc">\n    {disc}\n  </div>\n'
            + footer(6))


PAGES = [
    ("page1_sector.html", page_sector()),
    ("page2_lvmh.html", page_fiche(C.LVMH, 2)),
    ("page3_lvmh_charts.html", page_charts("LVMH: charts", C.LVMH_CHARTS, 3, 0)),
    ("page4_hermes.html", page_fiche(C.RMS, 4)),
    ("page5_hermes_charts.html", page_charts("Hermès: charts", C.RMS_CHARTS, 5, 0)),
    ("page6_sources.html", page_sources()),
]

# Walk the rendered page and describe every box, line, image and text block in px.
MEASURE_JS = r"""
() => {
  const page = document.querySelector('.page'); const P = page.getBoundingClientRect();
  const R = el => { const r = el.getBoundingClientRect(); return [r.left-P.left, r.top-P.top, r.width, r.height]; };
  const out = {shapes: [], texts: [], images: [], overflow: []};
  const foot = page.querySelector('footer').getBoundingClientRect();
  page.querySelectorAll('.box').forEach(b => {
    out.shapes.push({kind:'box', r:R(b)});
    if (b.classList.contains('grid4')) {
      [...b.children].forEach((c, i) => {
        if (c.classList.contains('techline')) out.shapes.push({kind:'hline', r:R(c)});
        else if (i % 4) out.shapes.push({kind:'vline', r:R(c)});
      });
    }
  });
  page.querySelectorAll('.bar').forEach(b => out.shapes.push({kind:'bar', r:R(b)}));
  page.querySelectorAll('img').forEach(i => out.images.push({src: i.getAttribute('src'), r:R(i)}));
  const sel = 'p,h1,h2,h3,li,.label,.sub1,.sub2,.boxlabel,.boxvalue,.kpilabel,.kpinote,.techline,.charttitle,.chartsub,.src,footer span';
  page.querySelectorAll(sel).forEach(el => {
    const cs = getComputedStyle(el); const runs = [];
    const walk = (n) => n.childNodes.forEach(ch => {
      if (ch.nodeType === 3) { const s = getComputedStyle(n);
        runs.push({t: ch.textContent.replace(/\s+/g,' '), c: s.color, w: +s.fontWeight}); }
      else if (ch.nodeType === 1) walk(ch);
    });
    walk(el);
    let col = cs.color; if (el.classList.contains('headline')) col = 'rgb(255, 108, 14)';
    runs.forEach(r => { if (el.classList.contains('headline')) r.c = col; });
    const rr = R(el); const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
    out.texts.push({r:[rr[0]+pl, rr[1]+pt, rr[2]-pl-pr, rr[3]-pt-pb], size: parseFloat(cs.fontSize), w:+cs.fontWeight, c: col, lh: parseFloat(cs.lineHeight),
      align: cs.textAlign, ls: parseFloat(cs.letterSpacing)||0, upper: cs.textTransform==='uppercase', runs,
      li: el.tagName === 'LI', grp: (() => { const g = el.closest('.disc, .cols > div'); return g ? [...page.querySelectorAll('.disc, .cols > div')].indexOf(g) : -1; })()});
    const r = el.getBoundingClientRect();
    if (!el.closest('footer') && r.bottom > foot.top - 2) out.overflow.push(el.textContent.slice(0, 60));
  });
  // text clipped inside its own box?
  page.querySelectorAll('.box').forEach(b => { if (b.scrollHeight > b.clientHeight + 1) out.overflow.push('box: ' + b.textContent.slice(0,60)); });
  return out;
}
"""

FIT_JS = r"""
(s) => { document.querySelectorAll('.chartframe img').forEach(i => { i.style.width = (i.getAttribute('src').includes('divisions') ? 100 : s) + '%'; i.style.height = 'auto';
  i.style.margin = '0 auto'; }); }
"""


def render():
    layouts = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROME", "/opt/pw-browsers/chromium") if os.path.exists("/opt/pw-browsers") else None)
        pg = b.new_page(viewport={"width": 794, "height": 1123})
        writer = PdfWriter()
        for name, html in PAGES:
            path = os.path.join(HERE, name)
            if "charts" in name:
                html = html.replace('style="height:0px"', "")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            pg.goto("file://" + path)
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            if "charts" in name:
                # largest chart height that keeps the page above the footer
                for h in range(100, 50, -1):
                    pg.evaluate(FIT_JS, h)
                    if not pg.evaluate(MEASURE_JS)["overflow"]:
                        break
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html.replace('<img src=', f'<img style="width:{h}%;height:auto;margin:0 auto" src=').replace(
                    f'style="width:{h}%;height:auto;margin:0 auto" src="rms_chart3', 'style="width:100%;height:auto" src="rms_chart3'))
                pg.goto("file://" + path); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            m = pg.evaluate(MEASURE_JS)
            if m["overflow"]:
                print("OVERFLOW", name, m["overflow"])
            layouts.append(m)
            pdf = pg.pdf(width="794px", height="1123px", print_background=True)
            tmp = os.path.join(HERE, "_tmp.pdf")
            open(tmp, "wb").write(pdf)
            for p in PdfReader(tmp).pages:
                writer.add_page(p)
            os.remove(tmp)
        writer.write(os.path.join(HERE, STEM + ".pdf"))
        b.close()
    return layouts


# ---------------------------------------------------------------- PowerPoint
PX = 210 / 794  # mm per CSS px
EMU_PX = int(36000 * PX)
SPACE = RGBColor.from_string("202945")
WHITE = RGBColor(255, 255, 255)
LINE = RGBColor.from_string("D9D9D9")


def E(v):
    return Emu(int(v * EMU_PX))


def rgb(css):
    v = [int(x) for x in css[css.index("(") + 1:css.index(")")].split(",")[:3]]
    return RGBColor(*v)


def build_pptx(layouts):
    prs = Presentation()
    prs.slide_width, prs.slide_height = E(794), E(1123)
    for m in layouts:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        for sh in m["shapes"]:
            x, y, w, h = sh["r"]
            if sh["kind"] == "box":
                r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x + 1), E(y + 1), E(w - 2), E(h - 2))
                r.adjustments[0] = min(0.5, 14 / max(1, min(w, h)))
                r.fill.solid(); r.fill.fore_color.rgb = WHITE
                r.line.color.rgb = SPACE; r.line.width = Pt(1.5); r.shadow.inherit = False
            elif sh["kind"] == "bar":
                r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
                r.line.fill.background(); r.fill.gradient(); r.fill.gradient_angle = 0
                st = r.fill.gradient_stops
                st[0].color.rgb = RGBColor.from_string("FF6C0E"); st[1].color.rgb = RGBColor.from_string("FFC545")
            elif sh["kind"] in ("vline", "hline"):
                if sh["kind"] == "vline":
                    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x), E(y), E(x), E(y + h))
                else:
                    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x), E(y), E(x + w), E(y))
                c.line.color.rgb = LINE; c.line.width = Pt(0.75)
        for im in m["images"]:
            x, y, w, h = im["r"]
            s.shapes.add_picture(os.path.join(HERE, im["src"]), E(x), E(y), E(w), E(h))
        # texts in the same column or disclaimer block share one text box, so lines flow instead of overlapping
        groups = []
        for t in m["texts"]:
            if not "".join(r["t"] for r in t["runs"]).strip():
                continue
            if t["grp"] >= 0 and groups and groups[-1][0]["grp"] == t["grp"]:
                groups[-1].append(t)
            else:
                groups.append([t])
        for g in groups:
            x = min(t["r"][0] for t in g); y = g[0]["r"][1]
            w = max(t["r"][0] + t["r"][2] for t in g) - x
            h = max(t["r"][1] + t["r"][3] for t in g) - y
            # a little extra width absorbs small differences between Nunito and Maison Neue
            tb = s.shapes.add_textbox(E(x), E(y), E(w * 1.02 + 2), E(h + 2))
            tf = tb.text_frame; tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            tf.vertical_anchor = MSO_ANCHOR.TOP
            prev_bottom = None
            for k, t in enumerate(g):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                if prev_bottom is not None:
                    p.space_before = Pt(max(0, t["r"][1] - prev_bottom) * 0.75)
                prev_bottom = t["r"][1] + t["r"][3]
                p.alignment = {"justify": PP_ALIGN.JUSTIFY, "right": PP_ALIGN.RIGHT, "center": PP_ALIGN.CENTER}.get(
                    t["align"], PP_ALIGN.LEFT)
                p.line_spacing = Pt(t["lh"] * 0.75) if t["lh"] else 1.0
                runs = t["runs"]
                if t["li"]:
                    runs = [{"t": "•  ", "c": t["c"], "w": 400}] + runs
                first = True
                for rr in runs:
                    txt = rr["t"]
                    if first:
                        txt = txt.lstrip(); first = not txt
                    if not txt:
                        continue
                    if t["upper"]:
                        txt = txt.upper()
                    run = p.add_run(); run.text = txt
                    f = run.font
                    f.name = "Maison Neue"; f.size = Pt(round(t["size"] * 0.75 * 2) / 2)
                    f.bold = rr["w"] >= 700
                    f.color.rgb = rgb(rr["c"])
                    if t["ls"]:
                        rPr = run._r.get_or_add_rPr(); rPr.set("spc", str(int(t["ls"] * 0.75 * 100)))
                if p.runs:
                    p.runs[-1].text = p.runs[-1].text.rstrip()
    prs.save(os.path.join(HERE, STEM + ".pptx"))


if __name__ == "__main__":
    L = render()
    json.dump(L, open(os.path.join(HERE, "_layout.json"), "w"))
    build_pptx(L)
    print("done")
