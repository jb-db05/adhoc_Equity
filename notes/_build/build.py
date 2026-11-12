"""Build Syz ad-hoc opinion notes (one HTML file per A4 page) for IMB, PRU, KHC."""
import os

OUT = '/home/user/adhoc_Equity/notes'
DATE = '12 November 2026'
NOTE_TYPE = 'Ad-hoc opinion'

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700;800&display=swap');
@page{size:794px 1123px;margin:0}
:root{--space:#202945;--blueberry:#4B5F80;--tiger:#FF6C0E;--mango:#FFA400;--gold:#FFC545;--mint:#3BAF90;--line:#D9D9D9;
  --grad-orange:linear-gradient(90deg,#FF6C0E 0%,#FFA400 50%,#FFC545 100%)}
html,body{margin:0;padding:0;background:#fff}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:794px;height:1123px;box-sizing:border-box;padding:28px 52px 30px;display:flex;flex-direction:column;
  background:#fff;color:var(--space);font-family:'Maison Neue',Nunito,Arial,sans-serif;font-weight:400;font-size:12.8px;line-height:1.5;overflow:hidden}
header{display:flex;flex-direction:column;align-items:flex-end;gap:10px}
.logo{height:46px;min-width:40px}
.cover .logo{height:70px}
.bar{align-self:stretch;height:4px;background:var(--grad-orange)}
main{flex:1;overflow:hidden;display:flex;flex-direction:column}
.label{margin-top:18px;color:var(--blueberry);font-weight:300;font-size:9.5px;letter-spacing:.4em;text-transform:uppercase}
.headline{margin:8px 0 4px;font-size:28px;line-height:1.25;font-weight:800;color:var(--tiger)}
.sub1{font-weight:300;font-size:15px;margin-bottom:4px}
.sub2{font-weight:700;color:var(--tiger);font-size:14.5px;margin:0 0 8px}
.lead{font-weight:300;font-size:17px;line-height:1.55;margin:30px 0 30px;text-align:left}
h2{margin:22px 0 14px;font-size:18px;font-weight:800;color:var(--space)}
p{margin:0 0 11px;text-align:justify}
.box{background:#fff;border:2px solid var(--space);border-radius:14px;color:var(--space);padding:12px 16px}
.notice{margin-top:22px;font-size:11.5px;line-height:1.45}
.notice .boxlabel{margin-bottom:3px}
.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));padding:0;overflow:hidden;margin:20px 0 26px}
.grid4>div{padding:14px 16px;border-left:1px solid var(--line)}.grid4>div:first-child{border-left:0}
.boxlabel{color:var(--tiger);font-weight:700;font-size:10.5px;letter-spacing:.08em}
.kpilabel{color:var(--blueberry);font-weight:700;font-size:10.5px;line-height:1.3;min-height:28px}
.boxvalue{font-size:18px;font-weight:800;margin-top:4px}
.pos{color:var(--mint)}.neg{color:var(--tiger)}
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:30px}
.sec{margin-bottom:18px}
.sec h3{margin:0 0 6px;font-size:14.5px;font-weight:700;color:var(--tiger)}
.sec h3 span{color:var(--space)}
.sec p{margin:0;font-size:13.4px;line-height:1.58}
.company{margin-top:24px;font-size:26px;font-weight:800;line-height:1.2}
.company .ticker{font-weight:300;color:var(--blueberry);font-size:18px;margin-left:8px}
.subtitle{color:var(--tiger);font-weight:700;font-size:14px;margin-top:4px}
.conclusion{margin-top:auto;padding:16px 20px}
.conclusion p{margin:0;font-size:13.4px;line-height:1.55}
.investors{margin-top:22px;padding:18px 22px}
.investors p{margin:0;font-size:13.6px;line-height:1.6}
.sources li{margin-bottom:3px}
.sources ul{margin:0 0 10px;padding-left:18px;font-size:12.5px;line-height:1.5}
.disclaimer p{font-size:10.8px;line-height:1.5;margin:0 0 8px}
p.cp{font-size:13.6px;line-height:1.62}
footer{margin-top:14px;display:flex;justify-content:space-between;font-size:10.5px;color:var(--space)}
"""


def page(body, n, total, cover=False):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=794"><title>Syz Research</title><style>{CSS}</style></head>
<body><div class="page{' cover' if cover else ''}">
<header><img class="logo" src="../syz-logo.png" alt="Syz"><div class="bar"></div></header>
<main>{body}</main>
<footer><span>Syz Research · {NOTE_TYPE} · {DATE}</span><span>{n} / {total}</span></footer>
</div></body></html>"""


def cover(c):
    return f"""
<div class="label">{NOTE_TYPE} · {c['sector']}</div>
<h1 class="headline">{c['headline']}</h1>
<div class="sub1">{DATE} · Syz Research</div>
<div class="sub1" style="font-size:12.5px">Market data as of {DATE}.</div>
<div class="box notice"><div class="boxlabel">IMPORTANT NOTICE</div>
{c['short']} is not part of the Syz Focus List and is neither actively recommended nor followed by Syz Research.
This document is intended only for professional and institutional clients and qualified investors. It is not a personalised
recommendation. Please read the important information at the end of this document.</div>
<p class="lead">{c['lead']}</p>
<h2>{c['sector_title']}</h2>
<div class="cols">
  <div><div class="sub2">{c['col1'][0]}</div><p class="cp">{c['col1'][1]}</p></div>
  <div><div class="sub2">{c['col2'][0]}</div><p class="cp">{c['col2'][1]}</p></div>
</div>
<div class="box investors"><div class="sub2" style="margin-bottom:4px">What this means for investors</div><p>{c['investors']}</p></div>
"""


def fiche(c):
    tiles = ''.join(
        f'<div><div class="kpilabel">{l}</div><div class="boxvalue{(" " + cls) if cls else ""}">{v}</div></div>'
        for l, v, cls in c['kpis'])
    secs = c['sections']
    def render(items):
        return ''.join(f'<div class="sec"><h3><span>{i}.</span> {t}</h3><p>{p}</p></div>' for i, (t, p) in items)
    numbered = list(enumerate(secs, 1))
    left, right = numbered[:3], numbered[3:]
    return f"""
<div class="company">{c['name']}<span class="ticker">{c['ticker']}</span></div>
<div class="subtitle">{c['subtitle']}</div>
<div class="box grid4">{tiles}</div>
<div class="cols"><div>{render(left)}</div><div>{render(right)}</div></div>
<div class="box conclusion"><div class="sub2" style="margin-bottom:4px">Conclusion</div><p>{c['conclusion']}</p></div>
"""


DISCLAIMER = open(os.path.join(os.path.dirname(__file__), 'disclaimer.txt')).read().strip().split('\n\n')


def sources(c):
    items = ''.join(f'<li>{s}</li>' for s in c['sources'])
    disc = ''.join(f'<p>{p}</p>' for p in DISCLAIMER)
    return f"""
<h2 style="margin-top:22px">Sources</h2>
<div class="sources"><ul>{items}</ul></div>
<h2>Important information</h2>
<div class="disclaimer">{disc}</div>
"""


from content import NOTES  # noqa: E402

for slug, c in NOTES.items():
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    pages = [cover(c), fiche(c), sources(c)]
    for i, body in enumerate(pages, 1):
        with open(os.path.join(d, f'page-{i}.html'), 'w') as f:
            f.write(page(body, i, len(pages), cover=(i == 1)))
print('built', list(NOTES))
