import sys
from pptx import Presentation
from pptx.oxml.ns import qn
from lxml import etree
f=sys.argv[1]; p=Presentation(f)
def ln(tag,color=None,w=9525):
    e=etree.Element(qn('a:'+tag),w=str(w if color else 0),cap='flat',cmpd='sng',algn='ctr')
    if color:
        sf=etree.SubElement(e,qn('a:solidFill')); etree.SubElement(sf,qn('a:srgbClr'),val=color); etree.SubElement(e,qn('a:prstDash'),val='solid')
    else: etree.SubElement(e,qn('a:noFill'))
    return e
for s in p.slides:
    for sh in s.shapes:
        if not getattr(sh,'has_table',False): continue
        t=sh.table; n=len(t.rows)
        for i in range(n):
            for j in range(len(t.columns)):
                tcPr=t.cell(i,j)._tc.get_or_add_tcPr()
                for ch in list(tcPr):
                    if ch.tag in [qn('a:'+x) for x in ('lnL','lnR','lnT','lnB')]: tcPr.remove(ch)
                top=ln('lnT','202945') if i==0 else ln('lnT')
                bot=ln('lnB','202945') if i in (0,n-1) else ln('lnB','D9D9D9',6350)
                for k,e in enumerate([ln('lnL'),ln('lnR'),top,bot]): tcPr.insert(k,e)
                if tcPr.find(qn('a:noFill')) is None: etree.SubElement(tcPr,qn('a:noFill'))
p.save(f)
