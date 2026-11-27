import re
from pptx import Presentation
from pptx.util import Mm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from content import *
C=lambda h:RGBColor.from_string(h)
SPACE,BLUE,TIGER,GOLD,LINE=C('202945'),C('4B5F80'),C('FF6C0E'),C('FFC545'),C('D9D9D9')
PX=210/794
px=lambda v:Mm(v*PX)
prs=Presentation(); prs.slide_width,prs.slide_height=Mm(210),Mm(297)
FONT='Maison Neue'
def tb(s,x,y,w,h,paras,align=None):
    """paras: list of (text,size_px,color,bold,space_after_px)"""
    sh=s.shapes.add_textbox(px(x),px(y),px(w),px(h)); tf=sh.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    for i,(t,sz,col,b,sa) in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        r=p.add_run(); r.text=t; f=r.font; f.name=FONT; f.size=Pt(sz*.75); f.bold=b; f.color.rgb=col
        p.space_after=Pt(sa*.75); p.line_spacing=1.12
        if align: p.alignment=align
        elif sz<=14 and not b or True: pass
    return sh
def box(s,x,y,w,h):
    r=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,px(x),px(y),px(w),px(h)); r.adjustments[0]=14/min(w,h)
    r.fill.solid(); r.fill.fore_color.rgb=C('FFFFFF'); r.line.color.rgb=SPACE; r.line.width=Pt(1.5); r.shadow.inherit=False; return r
def vline(s,x,y,h):
    l=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(x),px(y),Emu(9525),px(h)); l.fill.solid(); l.fill.fore_color.rgb=LINE; l.line.fill.background(); l.shadow.inherit=False
def hline(s,x,y,w):
    l=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(x),px(y),px(w),Emu(9525)); l.fill.solid(); l.fill.fore_color.rgb=LINE; l.line.fill.background(); l.shadow.inherit=False
def frame(s,n,logo_h=46,label=True):
    s.shapes.add_picture('syz-logo.png',px(794-52-logo_h*206/186),px(28),height=px(logo_h))
    y=28+logo_h+10
    bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(52),px(y),px(690),px(4)); bar.line.fill.background(); bar.shadow.inherit=False
    bar.fill.gradient(); bar.fill.gradient_angle=0; st=bar.fill.gradient_stops; st[0].color.rgb=TIGER; st[1].color.rgb=GOLD
    if label: tb(s,52,y+18,690,14,[(LABEL.upper(),9.5,BLUE,False,0)])
    tb(s,52,1083,500,16,[(FOOT,10.5,SPACE,False,0)]); tb(s,642,1083,100,16,[(f'{n} / 4',10.5,SPACE,False,0)],PP_ALIGN.RIGHT)
    return y
def kpis(s,x,y,w,h,items,small=False):
    box(s,x,y,w,h); n=len(items); cw=w/n
    for i,it in enumerate(items):
        cx=x+i*cw
        if i: vline(s,cx,y+1,h-2)
        if len(it)==3:
            tb(s,cx+14,y+9,cw-24,h-10,[(it[0],11,BLUE,True,1),(it[1],16,SPACE,True,1),(it[2],10.5,SPACE,False,0)])
        else:
            tb(s,cx+14,y+9,cw-24,h-10,[(it[0],10.5,TIGER,True,1),(it[1],14,SPACE,True,0)])
def column(s,x,y,w,h,items,body=13):
    paras=[]
    for k,t in items:
        if k=='p': paras.append((t,body,SPACE,False,8))
        else: paras.append((t,13.5,TIGER,True,3))
    tb(s,x,y,w,h,paras)
# page 1
s=prs.slides.add_slide(prs.slide_layouts[6]); y=frame(s,1,70)
tb(s,52,y+18,690,14,[(LABEL.upper(),9.5,BLUE,False,0)]) if False else None
tb(s,52,y+40,690,76,[(cover['headline'],28,TIGER,True,0)]); tb(s,52,y+112,690,24,[(cover['sub1'],15,SPACE,False,0)])
ny=y+150; box(s,52,ny,690,84); tb(s,68,ny+10,658,70,[('IMPORTANT NOTICE',10.5,TIGER,True,3),(cover['notice'],11.5,SPACE,False,0)])
ky=ny+98; kpis(s,52,ky,690,78,cover['kpis'])
hy=ky+98; tb(s,52,hy,690,24,[(cover['h2'],17,SPACE,True,0)])
cw=(690-30)/2; column(s,52,hy+34,cw,560,cover['left'],12.5); column(s,52+cw+30,hy+34,cw,560,cover['right'],12.5)
# page 2
f=fiche; s=prs.slides.add_slide(prs.slide_layouts[6]); y=frame(s,2,46)
tb(s,52,y+40,690,40,[(f['title'],28,TIGER,True,0)]); tb(s,52,y+78,690,20,[(f['subtitle'],14,TIGER,True,0)])
ky=y+106; kpis(s,52,ky,690,70,f['kpis'])
ty=ky+80; box(s,52,ty,690,118)
cw4=690/4
for i,(a,b) in enumerate(f['tech']):
    if i: vline(s,52+i*cw4,ty+1,52)
    tb(s,52+i*cw4+14,ty+9,cw4-24,44,[(a,10.5,TIGER,True,1),(b,14,SPACE,True,0)])
hline(s,54,ty+58,686); tb(s,66,ty+64,662,52,[(f['techline'],11.5,SPACE,False,0)])
cy=ty+130; cw=(690-30)/2
column(s,52,cy,cw,520,f['left'],12.5); column(s,52+cw+30,cy,cw,520,f['right'],12.5)
by=905; box(s,52,by,690,142); tb(s,68,by+10,658,126,[('CONCLUSION',10.5,TIGER,True,2),(f['concl'],12.5,SPACE,False,0)])
# page 3
s=prs.slides.add_slide(prs.slide_layouts[6]); y=frame(s,3,46)
tb(s,52,y+36,690,24,[('Charts',17,SPACE,True,0)])
cy=y+70
for i,(n,t,sub,img) in enumerate(charts):
    tb(s,52,cy,690,20,[(f'{n} · {t}',14,SPACE,True,0)]); tb(s,52,cy+19,690,16,[(sub,11,BLUE,False,0)])
    box(s,52,cy+40,690,0+215); s.shapes.add_picture(img,px(60),px(cy+48),width=px(674))
    tb(s,52,cy+40+215+6,690,14,[(SRC,10.5,SPACE,False,0)]); cy+=40+215+6+14+12
# page 4
s=prs.slides.add_slide(prs.slide_layouts[6]); y=frame(s,4,46,label=False)
import html as H
src=open('page4_sources.html').read()
paras=[(H.unescape(p),10.5,SPACE,False,7) for p in re.findall(r'<p>(.*?)</p>',src,re.S)]
tb(s,52,y+22,690,24,[('Sources',17,SPACE,True,0)]); tb(s,52,y+54,690,16,[(SRC,11.5,SPACE,False,0)])
tb(s,52,y+90,690,24,[('Important information',17,SPACE,True,0)]); tb(s,52,y+122,690,800,paras)
prs.save('Syz_EssilorLuxottica_ad-hoc_2026-11-27.pptx')
