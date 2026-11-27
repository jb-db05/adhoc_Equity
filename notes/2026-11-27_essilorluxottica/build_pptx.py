import re
from pptx import Presentation
from pptx.util import Mm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
from content import *
from build_html import DISC
C=lambda h:RGBColor.from_string(h)
SPACE,BLUE,TIGER,GOLD,MINT,GREY=C('202945'),C('4B5F80'),C('FF6C0E'),C('FFC545'),C('3BAF90'),C('D9D9D9')
FONT='Maison Neue'
px=lambda v:Emu(int(v*9525*210/ (794*0.2645833*1.0)/ (210/ (794*0.2645833)) ))  # placeholder replaced below
PX=Mm(210)/794
px=lambda v:int(v*PX)
prs=Presentation(); prs.slide_width,prs.slide_height=Mm(210),Mm(297)
def strip(t): return t.replace('**','')
def addruns(p,txt,size,color=SPACE,bold=False):
    for i,part in enumerate(re.split(r'\*\*(.+?)\*\*',txt)):
        if not part: continue
        r=p.add_run(); r.text=part; f=r.font; f.name=FONT; f.size=Pt(size); f.bold=bold or (i%2==1); f.color.rgb=color
def tb(s,x,y,w,h,paras,anchor=None):
    """paras: list of dict(text,size,color,bold,align,before,after,ls)"""
    t=s.shapes.add_textbox(px(x),px(y),px(w),px(h)); tf=t.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    if anchor: tf.vertical_anchor=anchor
    for i,d in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        addruns(p,d['text'],d.get('size',9.4),d.get('color',SPACE),d.get('bold',False))
        if d.get('align'): p.alignment=d['align']
        p.space_before=Pt(d.get('before',0)); p.space_after=Pt(d.get('after',0)); p.line_spacing=d.get('ls',1.18)
    return t
def box(s,x,y,w,h,r=14):
    b=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,px(x),px(y),px(w),px(h)); b.adjustments[0]=min(.5,r/min(w,h))
    b.fill.solid(); b.fill.fore_color.rgb=C('FFFFFF'); b.line.color.rgb=SPACE; b.line.width=Pt(1.5); b.shadow.inherit=False; return b
def line(s,x1,y1,x2,y2,col=GREY,w=.75):
    l=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,px(x1),px(y1),px(x2),px(y2)); l.line.color.rgb=col; l.line.width=Pt(w)
def header(s,cover=False):
    h=70 if cover else 46; im=Image.open('syz-logo.png'); w=h*im.width/im.height
    s.shapes.add_picture('syz-logo.png',px(742-w),px(28),height=px(h))
    y=28+h+10; bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,px(52),px(y),px(690),px(4)); bar.line.fill.background()
    bar.fill.gradient(); bar.fill.gradient_angle=0; st=bar.fill.gradient_stops; st[0].color.rgb=TIGER; st[1].color.rgb=GOLD; bar.shadow.inherit=False
    return y+4
def footer(s,n):
    tb(s,52,1090,500,16,[dict(text=FOOT,size=7.9)]); tb(s,642,1090,100,16,[dict(text=f'{n} / {N}',size=7.9,align=PP_ALIGN.RIGHT)])
def label(s,y): tb(s,52,y,690,14,[dict(text=LABEL.upper(),size=7.1,color=BLUE)])
def headline(s,y,txt,size=21,h=40): tb(s,52,y,690,h,[dict(text=txt,size=size,color=TIGER,bold=True,ls=1.05)])
def kpis(s,y,h,cells,tw=690/4,labelcol=BLUE,x=52):
    box(s,x,y,690,h)
    for i,k in enumerate(cells):
        cx=x+i*tw
        if i: line(s,cx,y+2,cx,y+h-2)
        ps=[dict(text=k[0],size=8.2,color=labelcol,bold=True),dict(text=k[1],size=12,bold=True,ls=1.1)]
        if len(k)>2: ps.append(dict(text=k[2],size=7.9,color=(TIGER if (len(k)>3 and k[3]=='neg') and False else SPACE)))
        t=tb(s,cx+14,y+9,tw-24,h-12,ps)
        if len(k)>3 and k[3]=='neg':  # coloured leading figure
            p=t.text_frame.paragraphs[2]; txt=k[2]; m=re.match(r'^(−\d+%)(.*)',txt)
            for r in list(p.runs): r._r.getparent().remove(r._r)
            addruns(p,m.group(1),7.9,TIGER); addruns(p,m.group(2),7.9)
def cols(s,y,h,left,right,size=9.4,after=5):
    for x,lst in ((52,left),(412,right)):
        ps=[]
        for k,t in lst:
            if k in('h3','sub2'): ps.append(dict(text=t,size=10.1,color=TIGER,bold=True,before=(6 if ps else 0),after=2))
            else: ps.append(dict(text=t,size=size,align=PP_ALIGN.JUSTIFY,after=after,ls=1.17))
        tb(s,x,y,330,h,ps)
def newslide(): return prs.slides.add_slide(prs.slide_layouts[6])
# page 1
s=newslide(); y=header(s,True); label(s,131); headline(s,150,cover['headline'],21,70)
tb(s,52,225,690,22,[dict(text=cover['sub1'],size=11.2)])
box(s,52,262,690,95); tb(s,70,273,654,78,[dict(text='IMPORTANT NOTICE',size=7.9,color=TIGER,bold=True,after=2),dict(text=cover['notice'],size=8.6,align=PP_ALIGN.JUSTIFY,ls=1.15)])
kpis(s,373,88,cover['kpis'])
tb(s,52,484,690,24,[dict(text=cover['h2'],size=12.7,bold=True)])
cols(s,516,540,cover['left'],cover['right']); footer(s,1)
# page 2
s=newslide(); y=header(s); label(s,108); headline(s,126,meta['title'],18.8,30)
tb(s,52,163,690,20,[dict(text=meta['sub'],size=10.5,color=TIGER,bold=True)])
kpis(s,198,74,meta['kpis'])
cols(s,290,640,meta['left'],meta['right'],size=8.5,after=4)
box(s,52,941,690,114); tb(s,70,952,654,96,[dict(text='WHAT THIS MEANS FOR INVESTORS',size=7.9,color=TIGER,bold=True,after=2),dict(text=meta['concl'],size=8.7,align=PP_ALIGN.JUSTIFY,ls=1.17)])
footer(s,2)
# page 3
s=newslide(); y=header(s); label(s,108); headline(s,126,fiche['title'],21,34)
tb(s,52,163,690,20,[dict(text=fiche['subtitle'],size=10.5,color=TIGER,bold=True)])
kpis(s,198,74,fiche['kpis'])
box(s,52,287,690,126)
tw=690/4
for i,(a,b) in enumerate(fiche['tech']):
    cx=52+i*tw
    if i: line(s,cx,289,cx,339)
    tb(s,cx+14,297,tw-24,40,[dict(text=a,size=7.9,color=TIGER,bold=True),dict(text=b,size=10.5,bold=True)])
line(s,54,340,740,340)
tb(s,70,347,654,60,[dict(text=fiche['techline'],size=8.6,align=PP_ALIGN.JUSTIFY,ls=1.15)])
cols(s,427,510,fiche['left'],fiche['right'],size=8.9,after=4.5)
box(s,52,943,690,112); tb(s,70,954,654,96,[dict(text='CONCLUSION',size=7.9,color=TIGER,bold=True,after=2),dict(text=fiche['conclusion'],size=8.7,align=PP_ALIGN.JUSTIFY,ls=1.17)])
footer(s,3)
# page 4
s=newslide(); y=header(s); label(s,108); tb(s,52,128,300,24,[dict(text='Charts',size=12.7,bold=True)])
cy=178
for i,(n,t,sub,img) in enumerate(charts):
    tb(s,52,cy,690,18,[dict(text='',size=10.1)])
    tt=s.shapes[-1].text_frame.paragraphs[0]; r=tt.add_run(); r.text=n; r.font.name=FONT; r.font.size=Pt(10.1); r.font.bold=True; r.font.color.rgb=TIGER
    r=tt.add_run(); r.text=' · '+t; r.font.name=FONT; r.font.size=Pt(10.1); r.font.bold=True; r.font.color.rgb=SPACE
    nl=2 if len(sub)>110 else 1
    tb(s,52,cy+22,690,16*nl,[dict(text=sub,size=8.6,color=BLUE)])
    im=Image.open(img); w=674-16; hh=w*im.height/im.width; fy=cy+22+17*nl+6
    box(s,52,fy,690,hh+16); s.shapes.add_picture(img,px(60),px(fy+8),width=px(w))
    tb(s,52,fy+hh+16+5,690,14,[dict(text=SRC,size=7.9)])
    cy=fy+hh+16+5+14+10
footer(s,4)
# page 5
s=newslide(); y=header(s)
tb(s,52,112,300,24,[dict(text='Sources',size=12.7,bold=True)]); tb(s,52,142,690,18,[dict(text='•  '+SRC.replace('Sources: ','')+'.',size=8.6)])
tb(s,52,176,300,24,[dict(text='Important information',size=12.7,bold=True)])
tb(s,52,206,690,800,[dict(text=x,size=7.9,align=PP_ALIGN.JUSTIFY,after=5,ls=1.15) for x in DISC])
footer(s,5)
prs.save('Syz_EssilorLuxottica_ad-hoc_2026-11-27.pptx')
