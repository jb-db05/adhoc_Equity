# -*- coding: utf-8 -*-
import re, copy
from pptx import Presentation
from pptx.util import Mm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image
C=lambda h:RGBColor.from_string(h)
SPACE,BLUE,TIGER,GOLD,GREY=C('202945'),C('4B5F80'),C('FF6C0E'),C('FFC545'),C('D9D9D9')
FONT='Nunito Sans'; LABEL='Ad-hoc opinion · Eyewear and medtech'; FOOT='Syz Research · Ad-hoc opinion · 27 November 2026'
SRC='Sources: Syz Research, Bloomberg, company data'; N=4
DISC=open('/home/user/adhoc_Equity/syz-equity-note/SKILL.md',encoding='utf-8').read().split('## 6. Important information (disclaimer, verbatim)')[1].split('## 7.')[0].strip().split('\n\n')
PX=Mm(210)/794; px=lambda v:int(v*PX)
prs=Presentation(); prs.slide_width,prs.slide_height=Mm(210),Mm(297)
def addruns(p,txt,size,color=SPACE,bold=False):
    for i,part in enumerate(re.split(r'\*\*(.+?)\*\*',txt)):
        if not part: continue
        r=p.add_run(); r.text=part; f=r.font; f.name=FONT; f.size=Pt(size); f.bold=bold or (i%2==1); f.color.rgb=color
def tb(s,x,y,w,h,paras):
    t=s.shapes.add_textbox(px(x),px(y),px(w),px(h)); tf=t.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    for i,d in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        addruns(p,d['text'],d.get('size',9),d.get('color',SPACE),d.get('bold',False))
        if d.get('align'): p.alignment=d['align']
        p.space_before=Pt(d.get('before',0)); p.space_after=Pt(d.get('after',0)); p.line_spacing=d.get('ls',1.17)
    return t
def box(s,x,y,w,h,r=14):
    b=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,px(x),px(y),px(w),px(h)); b.adjustments[0]=min(.5,r/min(w,h))
    b.fill.solid(); b.fill.fore_color.rgb=C('FFFFFF'); b.line.color.rgb=SPACE; b.line.width=Pt(1.5); b.shadow.inherit=False; return b
def line(s,x1,y1,x2,y2,col=GREY,w=.75):
    l=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,px(x1),px(y1),px(x2),px(y2)); l.line.color.rgb=col; l.line.width=Pt(w)
def header(s,cover=False):
    h=70 if cover else 46; im=Image.open('syz-logo.png'); w=h*im.width/im.height
    s.shapes.add_picture('syz-logo.png',px(742-w),px(28),height=px(h))
    bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(52),px(28+h+10),px(690),px(4)); bar.line.fill.background()
    bar.fill.gradient(); bar.fill.gradient_angle=0; st=bar.fill.gradient_stops; st[0].color.rgb=TIGER; st[1].color.rgb=GOLD; bar.shadow.inherit=False
def footer(s,n):
    tb(s,52,1090,500,16,[dict(text=FOOT,size=7.9)]); tb(s,642,1090,100,16,[dict(text=f'{n} / {N}',size=7.9,align=PP_ALIGN.RIGHT)])
def label(s,y): tb(s,52,y,690,14,[dict(text=LABEL.upper(),size=7.1,color=BLUE)])
def headline(s,y,txt,size,h): tb(s,52,y,690,h,[dict(text=txt,size=size,color=TIGER,bold=True,ls=1.05)])
def sub2(s,y,txt): tb(s,52,y,690,20,[dict(text=txt,size=10.5,color=TIGER,bold=True)])
def kpis(s,y,h,cells):
    box(s,52,y,690,h); tw=690/4
    for i,k in enumerate(cells):
        cx=52+i*tw
        if i: line(s,cx,y+2,cx,y+h-2)
        tb(s,cx+14,y+9,tw-24,h-12,[dict(text=k[0],size=8.2,color=BLUE,bold=True),dict(text=k[1],size=12,bold=True,ls=1.1),dict(text=k[2],size=7.9)])
def cols(s,y,h,left,right,size=8.8,after=4.5):
    for x,lst in ((52,left),(412,right)):
        ps=[]
        for k,t in lst:
            if k in('h3','sub2'): ps.append(dict(text=t,size=10.1,color=TIGER,bold=True,before=(6 if ps else 0),after=2))
            else: ps.append(dict(text=t,size=size,align=PP_ALIGN.JUSTIFY,after=after,ls=1.17))
        tb(s,x,y,330,h,ps)
def concl(s,y,h,lab,txt):
    box(s,52,y,690,h); tb(s,70,y+11,654,h-14,[dict(text=lab,size=7.9,color=TIGER,bold=True,after=2),dict(text=txt,size=8.7,align=PP_ALIGN.JUSTIFY,ls=1.17)])
def border(cell,side,color='202945',w=9525):
    tcPr=cell._tc.get_or_add_tcPr()
    for e in tcPr.findall(qn('a:'+side)): tcPr.remove(e)
    ln=etree.SubElement(tcPr,qn('a:'+side),w=str(w),cap='flat',cmpd='sng',algn='ctr')
    sf=etree.SubElement(ln,qn('a:solidFill')); etree.SubElement(sf,qn('a:srgbClr'),val=color)
    etree.SubElement(ln,qn('a:prstDash'),val='solid')
def nolines(cell):
    tcPr=cell._tc.get_or_add_tcPr()
    for side in ('lnL','lnR','lnT','lnB'):
        for e in tcPr.findall(qn('a:'+side)): tcPr.remove(e)
        ln=etree.SubElement(tcPr,qn('a:'+side),w='0'); etree.SubElement(ln,qn('a:noFill'))
def table(s,x,y,widths,header_row,rows,size=8.2,rowh=36,title=None):
    if title: tb(s,x,y,690,16,[dict(text=title.upper(),size=8.6,color=TIGER,bold=True)]); y+=20
    n=len(rows)+1; gs=s.shapes.add_table(n,len(widths),px(x),px(y),px(sum(widths)),px(24+rowh*len(rows)))
    t=gs.table; tblPr=t._tbl.tblPr
    for a in ('firstRow','bandRow'): tblPr.set(a,'0')
    sid=tblPr.find(qn('a:tableStyleId'))
    if sid is not None: sid.text='{2D5ABB26-0587-4C30-8999-92F81FD0307C}'  # no style, no grid
    for j,w in enumerate(widths): t.columns[j].width=px(w)
    t.rows[0].height=px(24)
    for i in range(1,n): t.rows[i].height=px(rowh)
    for i in range(n):
        for j in range(len(widths)):
            c=t.cell(i,j); c.fill.background(); nolines(c)
            c.margin_left=px(4); c.margin_right=px(6); c.margin_top=px(3); c.margin_bottom=px(3)
            tf=c.text_frame; tf.word_wrap=True
            txt=header_row[j] if i==0 else rows[i-1][j]; p=tf.paragraphs[0]
            if i==0: addruns(p,txt.upper(),7.6,BLUE,True)
            else: addruns(p,txt,size,SPACE,bold=(j==0)); p.line_spacing=1.1
            if i==0: border(c,'lnT'); border(c,'lnB')
            elif i==n-1: border(c,'lnB')
            else: border(c,'lnB','D9D9D9',6350)
    return gs
def newslide(): return prs.slides.add_slide(prs.slide_layouts[6])
J=PP_ALIGN.JUSTIFY

import sys, importlib.util
spec=importlib.util.spec_from_file_location('v1content','../2026-11-27_essilorluxottica/content.py'); v1=importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
meta=v1.meta; charts=v1.charts
def L(*items): return list(items)
