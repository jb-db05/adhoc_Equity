import html,re
from content import *
e=html.escape
def blocks(items):
    o=''
    for k,t in items:
        o+={'p':f'<p>{e(t)}</p>','sub2':f'<div class="sub2">{e(t)}</div>','h3':f'<h3>{e(t)}</h3>'}[k]
    return o
def foot(n):return f'<footer><span>{FOOT}</span><span>{n} / 4</span></footer>'
def head(title):return f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{title}</title><link rel="stylesheet" href="style.css"></head>\n<body>\n'
hd='<header><img class="logo" src="syz-logo.png" alt="Syz"><div class="bar"></div></header>'
def grid(k,note=True):return ''.join(f'<div><div class="kpilabel">{e(a)}</div><div class="boxvalue">{e(b)}</div><div class="kpinote">{e(c)}</div></div>' for a,b,c in k)
c=cover
open('page1_cover.html','w').write(head('EssilorLuxottica ad-hoc opinion')+f'''<div class="page cover">
  {hd}
  <div class="label">{LABEL}</div>
  <h1 class="headline">{e(c['headline'])}</h1>
  <div class="sub1">{c['sub1']}</div>
  <div class="box notice"><div class="boxlabel">IMPORTANT NOTICE</div><p>{e(c['notice'])}</p></div>
  <div class="box grid4" style="margin-top:14px">{grid(c['kpis'])}</div>
  <h2>{e(c['h2'])}</h2>
  <div class="cols"><div>{blocks(c['left'])}</div><div>{blocks(c['right'])}</div></div>
  {foot(1)}
</div>
</body></html>''')
f=fiche
tech=''.join(f'<div><div class="boxlabel">{e(a)}</div><div class="boxvalue" style="font-size:14px">{e(b)}</div></div>' for a,b in f['tech'])
open('page2_essilorluxottica.html','w').write(head('EssilorLuxottica company page')+f'''<div class="page fiche">
  {hd}
  <div class="label">{LABEL}</div>
  <h1 class="headline">{e(f['title'])}</h1>
  <div class="sub2" style="font-size:14px">{e(f['subtitle'])}</div>
  <div class="box grid4" style="margin-top:10px">{grid(f['kpis'])}</div>
  <div class="box grid4" style="margin-top:10px">{tech}<div class="techline">{e(f['techline'])}</div></div>
  <div class="cols" style="margin-top:4px"><div>{blocks(f['left'])}</div><div>{blocks(f['right'])}</div></div>
  <div class="box concl"><div class="boxlabel" style="margin-bottom:2px">CONCLUSION</div><p>{e(f['concl'])}</p></div>
  {foot(2)}
</div>
</body></html>''')
cb=''.join(f'''  <div class="chartblock"{' style="margin-top:12px"' if i else ''}>
    <div class="charttitle"><span class="num">{n}</span> · {e(t)}</div>
    <div class="chartsub">{e(s)}</div>
    <div class="box chartframe"><img src="{img}" alt="{e(t)}"></div>
    <div class="src">{SRC}</div>
  </div>
''' for i,(n,t,s,img) in enumerate(charts))
open('page3_charts.html','w').write(head('EssilorLuxottica charts')+f'''<div class="page">
  {hd}
  <div class="label">{LABEL}</div>
  <h2 style="margin-top:12px">Charts</h2>
{cb}  {foot(3)}
</div>
</body></html>''')
old=open('../2026-11-24_take-two/page4_sources.html').read()
old=old.replace('Take-Two sources','EssilorLuxottica sources').replace('Syz Research, Bloomberg, Company data.','Syz Research, Bloomberg, company data').replace('Syz Research · Ad-hoc opinion · 24 November 2026',FOOT)
old=old.replace('<li>Syz Research, Bloomberg, company data</li>','<li>Sources: Syz Research, Bloomberg, company data</li>')
open('page4_sources.html','w').write(old)
