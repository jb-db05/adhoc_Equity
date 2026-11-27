import html,sys,re
from content import *
e=lambda s:re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',html.escape(s,quote=False))
DISC=open('/home/user/adhoc_Equity/syz-equity-note/SKILL.md',encoding='utf-8').read().split('## 6. Important information (disclaimer, verbatim)')[1].split('## 7.')[0].strip().split('\n\n')
def fmtneg(t):  # wrap leading −NN% in neg span
    return re.sub(r'^(−\d+%)',r'<span class="neg">\1</span>',e(t))
def head(): return '<header><img class="logo" src="syz-logo.png" alt="Syz"><div class="bar"></div></header>'
def foot(n): return f'<footer><span>{FOOT}</span><span>{n} / {N}</span></footer>'
def blocks(lst):
    o=''
    for k,t in lst:
        o+={'p':f'<p>{e(t)}</p>','sub2':f'<div class="sub2">{e(t)}</div>','h3':f'<h3>{e(t)}</h3>'}[k]+'\n'
    return o
def kpis(l,extra=''):
    o=f'<div class="box grid4" style="margin-top:{extra or 12}px">'
    for k in l:
        note=fmtneg(k[2]) if len(k)>3 and k[3]=='neg' else e(k[2])
        o+=f'<div><div class="kpilabel">{e(k[0])}</div><div class="boxvalue">{e(k[1])}</div><div class="kpinote">{note}</div></div>'
    return o+'</div>'
def page(body,cls=''): return f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>EssilorLuxottica</title><link rel="stylesheet" href="style.css"></head>\n<body>\n<div class="page {cls}">\n{head()}\n{body}\n</div>\n</body></html>'
c=cover
p1=f'''<div class="label">{LABEL}</div><h1 class="headline">{e(c['headline'])}</h1><div class="sub1">{c['sub1']}</div>
<div class="box notice"><div class="boxlabel">IMPORTANT NOTICE</div><p>{e(c['notice'])}</p></div>
{kpis(c['kpis'],14)}<h2>{e(c['h2'])}</h2>
<div class="cols"><div>{blocks(c['left'])}</div><div>{blocks(c['right'])}</div></div>{foot(1)}'''
m=meta
p2=f'''<div class="label">{LABEL}</div><h1 class="headline" style="font-size:25px">{e(m['title'])}</h1><div class="sub2" style="font-size:14px">{e(m['sub'])}</div>
{kpis(m['kpis'],10)}
<div class="cols fiche meta" style="margin-top:4px"><div>{blocks(m['left'])}</div><div>{blocks(m['right'])}</div></div>
<div class="box concl"><div class="boxlabel" style="margin-bottom:2px">WHAT THIS MEANS FOR INVESTORS</div><p>{e(m['concl'])}</p></div>{foot(2)}'''
f=fiche
tech=''.join(f'<div><div class="boxlabel">{e(a)}</div><div class="boxvalue" style="font-size:14px">{e(b)}</div></div>' for a,b in f['tech'])
p3=f'''<div class="label">{LABEL}</div><h1 class="headline">{e(f['title'])}</h1><div class="sub2" style="font-size:14px">{e(f['subtitle'])}</div>
{kpis(f['kpis'],10)}
<div class="box grid4" style="margin-top:10px">{tech}<div class="techline">{e(f['techline'])}</div></div>
<div class="cols fiche" style="margin-top:4px"><div>{blocks(f['left'])}</div><div>{blocks(f['right'])}</div></div>
<div class="box concl"><div class="boxlabel" style="margin-bottom:2px">CONCLUSION</div><p>{e(f['conclusion'])}</p></div>{foot(3)}'''
ch=''
for i,(n,t,s,img) in enumerate(charts):
    ch+=f'<div class="chartblock" style="margin-top:{14 if i==0 else 12}px"><div class="charttitle"><span class="num">{n}</span> · {e(t)}</div><div class="chartsub">{e(s)}</div><div class="box chartframe"><img src="{img}" alt="{e(t)}"></div><div class="src">{SRC}</div></div>'
p4=f'<div class="label">{LABEL}</div><h2 style="margin-top:12px">Charts</h2>{ch}{foot(4)}'
p5=f'<h2 style="margin-top:14px">Sources</h2><ul class="sources"><li>{SRC.replace("Sources: ","")}.</li></ul><h2 style="margin-top:10px">Important information</h2><div class="disc">'+''.join(f'<p>{e(x)}</p>' for x in DISC)+f'</div>{foot(5)}'
for i,(n,b,cl) in enumerate([('page1_cover',p1,'cover'),('page2_meta-glasses',p2,''),('page3_essilorluxottica',p3,''),('page4_charts',p4,''),('page5_sources',p5,'')]):
    open(n+'.html','w',encoding='utf-8').write(page(b,cl))
