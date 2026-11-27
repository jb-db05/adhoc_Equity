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
SRC='Sources: Syz Research, Bloomberg, company data'; N=7
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
# ---------------- page 1
s=newslide(); header(s,True); label(s,131); headline(s,150,'From Vision Correction to Eye Health Management',21,40)
tb(s,52,190,690,22,[dict(text='27 November 2026 · Syz Research',size=11.2)])
box(s,52,226,690,80); tb(s,70,236,654,66,[dict(text='IMPORTANT NOTICE',size=7.9,color=TIGER,bold=True,after=2),dict(text='Prices are as of the time of writing on 27 November 2026. Company figures come from EssilorLuxottica\'s publications and from those of the other companies mentioned. Industry estimates come from published market studies and differ with their definitions. This note is not a recommendation for any individual investor.',size=8.6,align=J,ls=1.15)])
kpis(s,320,80,[('Share price','EUR 172.15','−36% since the start of 2026'),('Forward P/E','22.1x','Ten-year average: 27.5x'),('Q3 2026 revenue growth','+7.2%','At constant exchange rates'),('Myopia management','+24%','Q3 2026 revenue growth')])
# colour the negative figure
tb(s,52,414,690,24,[dict(text='A defensive market turning into a health-technology ecosystem',size=12.7,bold=True)])
cols(s,442,620,
 [('sub2','A sector in structural transformation'),
  ('p','The eyewear and optical health sector is moving from a traditional vision-correction market towards a high-tech ecosystem built around myopia management, AI wearables and preventive eye health. The category remains defensive: glasses are a medical need, demand follows demographics rather than the economic cycle, and replacement cycles, although they can lengthen when consumers are cautious, remain fundamentally stable.'),
  ('p','The base is large and growing. Industry estimates put worldwide spectacle lens sales at roughly USD 60bn at retail value in 2025, with forecasts of growth of about 4% to 7% a year depending on the source. EssilorLuxottica\'s own revenue rose 7.2% at constant exchange rates in the third quarter and 9.7% in the first half of 2026. Ageing populations need more frequent vision care, and the number of short-sighted people keeps rising.'),
  ('sub2','Myopia management'),
  ('p','Half of the world\'s population, nearly 5 billion people, is projected to be short-sighted by 2050. Lenses that slow the progression of myopia in children turn glasses into a treatment. Published estimates value the myopia-control lens market at about USD 1.6bn to 1.8bn, growing 10% to 12% a year: small next to the number of children concerned, so adoption is still early. Stellest, the group\'s lens, was named one of TIME\'s Best Inventions of 2026; Hoya (MiYOSMART) and CooperVision (MiSight) are scaling their own programmes, and low-dose atropine drops are now approved in the EU and the UK.')],
 [('sub2','AI glasses and diagnostics'),
  ('p','Smart glasses are moving from a niche audio and video tool towards an intelligent assistant that understands its surroundings and could offer navigation, translation and health alerts. Industry trackers report that global shipments grew 139% in the second half of 2025 and 212% in the first half of 2026, with display-less AI glasses making up most of the volume. North America is the largest market (37% of shipments in the second half of 2025), followed by Western Europe (30%), and China is catching up. Meta, the group\'s partner, holds roughly 70% to 85% of shipments depending on the definition.'),
  ('p','In diagnostics, high-resolution retinal imaging (optical coherence tomography) combined with AI could make eye care professionals players in preventive health, because the retina is the one place where blood vessels and nerve tissue can be seen without surgery. Applications beyond eye disease, such as diabetes, heart disease or neurological decline, are still at research stage.'),
  ('sub2','EssilorLuxottica\'s position'),
  ('p','EssilorLuxottica is present in all three: Stellest lenses for myopia, the glasses built with Meta and Nuance Audio hearing glasses, and Heidelberg Engineering, a retinal imaging company in which it holds 80%. Stellest received US FDA authorisation in September 2025 and its myopia management sales grew 24% in the third quarter. The Meta glasses led the smart-glasses category with more than 7 million pairs sold in 2025, and wearables grew 20% in the third quarter. Nuance Audio takes the group into hearing care, and Heidelberg\'s imaging gives it a position on the diagnostic side of eye health, where the eye is increasingly seen as a window on general health.'),
  ('sub2','What this means for investors'),
  ('p','The group could be seen as a defensive eyewear company holding several options on health technology. The new layers move more slowly than smart-glasses headlines but rest on clinical evidence and approvals. The shares trade on 22.1 times expected earnings against 27.5 over ten years, with the earnings forecast unchanged.')],size=8.5,after=4)
footer(s,1)
# ---------------- page 2
s=newslide(); header(s); label(s,108); headline(s,126,'Myopia, diagnostics and hearing',21,34)
sub2(s,163,'Growth areas that rest on clinical evidence and regulatory approvals rather than fashion')
kpis(s,198,74,[('Myopia management','+24%','Q3 2026 revenue growth'),('Stellest in the US','Authorised','FDA, September 2025'),('Heidelberg Engineering','80%','Stake, closed October 2024'),('Nuance Audio','FDA-cleared','US launch April 2025')])
cols(s,290,640,
 [('h3','1. Myopia: from correction to treatment'),
  ('p','Myopia is rising worldwide. A widely cited projection puts about half of the world\'s population, nearly 5 billion people, among the short-sighted by 2050. In children the concern is progression: the faster the eye grows, the higher the long-term risk of eye disease. Defocus lenses slow that progression, which turns a routine pair of glasses into a treatment followed over several years, with regular check-ups.'),
  ('h3','2. Where the group stands'),
  ('p','Stellest is the group\'s lens for this. In September 2025 the US FDA granted it market authorisation, described by the company as the first for a spectacle lens to control myopia, and in October 2026 TIME named it one of its Best Inventions of 2026. Myopia management sales grew 24% in the third quarter, and Stellest is scaling in most major markets, including the US.'),
  ('h3','3. Who else is competing'),
  ('p','Hoya has its own defocus lens, MiYOSMART, and is rolling out a new generation, MiYOSMART iQ. CooperVision sells MiSight, a contact lens for the same purpose. Drugs are also arriving: low-dose atropine drops (Ryjunea, developed by Sydnexis and licensed to Santen for Europe) were approved in the EU in June 2025 and in the UK later that year, and slowed myopia progression by about 30% over two years against placebo in the main trial. The US FDA has not approved them. Lenses, contact lenses and drops will be judged on clinical evidence, and could be combined or compete.')],
 [('h3','4. The eye as a window on health'),
  ('p','The retina is the one place where blood vessels and nerve tissue can be seen directly without surgery. High-resolution imaging (optical coherence tomography, OCT) combined with artificial intelligence can reveal eye diseases such as glaucoma and macular degeneration early, and research is exploring links to diabetes, heart disease and neurological decline. This field, called oculomics, could turn the eye care visit into a screening point for preventive health.'),
  ('h3','5. The group\'s exposure to diagnostics'),
  ('p','In October 2024 the group completed the purchase of 80% of Heidelberg Engineering, a German maker of OCT and retinal imaging systems used for early detection of glaucoma and age-related macular degeneration. The group also has the lens, store and optician network that could carry such tools to a wider audience.'),
  ('h3','6. Hearing: Nuance Audio'),
  ('p','Nuance Audio are over-the-counter hearing glasses, FDA-cleared for adults with mild to moderate hearing loss and launched in the US in April 2025. A second generation, Nuance Audio Plus, was launched this autumn with a longer battery life (up to 10 hours against 8), and the range has reached 14 countries. More than a billion people live with some hearing loss, and glasses are a discreet way to address it. The product extends the group from sight to hearing care.')],size=9.3,after=5.5)
concl(s,941,114,'WHY THE THREE LAYERS FIT TOGETHER','Myopia management, diagnostics and hearing glasses address the same customer: someone who already visits an optician or one of the group\'s stores. They share distribution, brands and professional relationships, and each one is sold on clinical evidence rather than fashion. That is what could make them harder for new entrants to copy, and could make the group\'s existing network a source of recurring visits. The next page sets out the opportunities and the risks in more detail.')
footer(s,2)
# ---------------- page 3
s=newslide(); header(s); label(s,108); headline(s,126,'Opportunities and risks',21,34)
sub2(s,163,'What the medtech layer could bring, and what could stand in the way')
table(s,52,196,[96,200,200,194],['Area','Opportunity','Risk','What to watch'],[
 ['Myopia management','Growing epidemic; a treatment instead of a correction; Stellest +24% in Q3 and FDA-authorised in the US','Rival lenses (Hoya, CooperVision) and atropine drops; clinical data or approvals could favour others','Stellest adoption in the US; rivals\' data and launches'],
 ['Diagnostics','Retinal imaging could make the optician a screening point; Heidelberg supplies the technology','Applications beyond eye disease are at research stage; integration takes time','How Heidelberg\'s tools are used in practice; what the group discloses'],
 ['Hearing','More than a billion people with hearing loss; FDA-cleared glasses, second generation launched','Hearing-aid makers; adoption and reimbursement differ by country','Country roll-out; sales disclosure'],
 ['Smart glasses','An assistant with navigation, translation and health alerts; lens expertise is a barrier for tech groups','Dependence on Meta; privacy rules; entry of Google, Samsung and Apple','Holiday sales; regulation in Europe; rival launches'],
 ['Group','A defensive base with recurring demand and stable replacement cycles','A multiple already lowered: 22.1x against 27.5x over ten years','Full-year 2026 results']],size=7.9,rowh=64,title='Opportunities and risks at a glance')
cols(s,606,330,
 [('h3','The main opportunities'),
  ('p','**Higher value per customer.** Myopia lenses and hearing glasses are sold as treatments or health devices rather than fashion items, and they come with follow-up visits. That could lift the average spend per customer and keep families coming back to the group\'s opticians and stores for years.'),
  ('p','**A large, early market.** Nearly 5 billion people are projected to be short-sighted by 2050, yet the myopia-control lens market is estimated at only USD 1.6bn to 1.8bn today. Over a billion people live with some hearing loss. Penetration of both is low, so growth could last for years.'),
  ('p','**A moat that is hard to copy.** Approvals (the US FDA for Stellest and Nuance Audio), clinical data and an optician network take years to build. In smart glasses, prescription lenses and laboratories are a barrier for technology groups, and the same lens expertise could matter as AI glasses move towards health alerts.')],
 [('h3','The main risks'),
  ('p','**Competition on evidence.** Hoya, CooperVision and drug makers are all publishing clinical data, and atropine drops are already approved in the EU and the UK. A rival result or approval could shift the choice of prescribers.'),
  ('p','**Affordability and adoption.** These products cost more than standard lenses and are paid for by families or patients in many markets. Reimbursement differs by country, so adoption could be slower than the medical need suggests.'),
  ('p','**Execution and visibility.** Diagnostics beyond eye disease are mostly at research stage, and integrating medtech businesses takes time. The group gives growth rates but not amounts, so investors cannot easily size what is working. Health data from glasses and imaging would also add privacy and regulatory questions, as the Meta glasses already show.')],size=8.4,after=4)
concl(s,943,112,'WHAT THIS MEANS FOR INVESTORS','The opportunities are real but slow: clinical evidence, approvals and adoption take years, and the group does not yet disclose how large these businesses are. The risks are mostly about speed and competition rather than about demand, which remains structural. In the near term the share price could continue to depend mostly on the core business and on smart glasses, while progress in myopia, diagnostics and hearing could build the case for a higher multiple over time.')
footer(s,3)
# ---------------- page 4 : Meta glasses, as in the first version
s=newslide(); header(s); label(s,108); headline(s,126,meta['title'],18.8,30)
tb(s,52,163,690,20,[dict(text=meta['sub'],size=10.5,color=TIGER,bold=True)])
kpis(s,198,74,[k[:3] for k in meta['kpis']])
cols(s,290,640,meta['left'],meta['right'],size=8.5,after=4)
concl(s,941,114,'WHAT THIS MEANS FOR INVESTORS',meta['concl'])
footer(s,4)
# ---------------- page 5 : competition
s=newslide(); header(s); label(s,108); headline(s,126,'Who competes where',21,34)

sub2(s,163,'The group faces a different set of rivals in each layer, and a vertically integrated model in all of them')
table(s,52,198,[112,290,288],['Area','Main competitors','Where the group stands'],[
 ['Prescription lenses','Hoya, Zeiss and other lens makers','The world\'s largest lens maker (Essilor, Varilux, Transitions)'],
 ['Myopia management','Hoya (MiYOSMART), CooperVision (MiSight), atropine drops (Santen, Sydnexis)','Stellest, FDA-authorised in the US; myopia management +24% in Q3'],
 ['Smart glasses','Google and Samsung (Android XR), Apple (reported), Chinese makers such as Xiaomi and Alibaba, retailers\' own projects','Meta partnership: above 7 million pairs in 2025, between about 70% and 85% of shipments'],
 ['Hearing','Traditional hearing-aid makers','Nuance Audio: FDA-cleared hearing glasses, second generation this autumn'],
 ['Diagnostics','Imaging specialists such as Zeiss and Topcon','Heidelberg Engineering, 80% owned since October 2024'],
 ['Retail','Fielmann, Lenskart, National Vision, Warby Parker','Own stores and online: Sunglass Hut, LensCrafters, GrandVision']],size=8.2,rowh=46,title='Competitive map')
cols(s,566,370,
 [('h3','Technology groups'),
  ('p','Google and Samsung are developing glasses on Android XR, and Apple is reported to be preparing a product. Google has said it is working with eyewear brands such as Warby Parker and Gentle Monster. Their arrival could raise awareness of the category, which could help the group, but it also gives its partner Meta its first serious rivals. Prescription lenses, fitting and laboratories are a barrier that technology groups have to solve or buy, and one of the group\'s strengths.'),
  ('h3','Retailers')  ,
  ('p','Chains are scaling and adding their own technology. Lenskart in India reported revenue up 32% to INR 9,002 crore in the year to March 2026, with 603 stores added, and has launched its own smart glasses with Google\'s Gemini. Fielmann has entered the US through SVS Vision (2023) and Shopko Optical (2024).')],
 [('h3','Lens and medtech peers'),
  ('p','Hoya is the closest competitor in lenses and, with MiYOSMART, in myopia management; it reported record quarterly revenue and operating profit in August 2026. In diagnostics, Heidelberg Engineering competes with specialists such as Zeiss and Topcon.'),
  ('h3','What to watch next'),
  ('p','More clinical data and US adoption for Stellest; competitors\' approvals and launches in myopia; products from Google, Samsung and Apple; how Heidelberg Engineering\'s tools are used in practice; and whether the group discloses more on the size of its medtech and wearables businesses.')],size=8.6,after=4)
concl(s,931,124,'CONCLUSION','The group is one of few large players present in all three new layers of the sector, and it sells through the largest lens, frame and retail network. Each layer has strong rivals: Hoya in lenses, technology groups in smart glasses, imaging specialists in diagnostics. The market has reduced what it pays for these options, with the multiple at 22 times against 27.5 over ten years and forecast earnings unchanged. The pace of clinical evidence, approvals and adoption could decide how much of that is regained.')
footer(s,5)

# ---------------- page 6 : charts (same three charts as the first version)
s=newslide(); header(s); label(s,108); tb(s,52,128,300,24,[dict(text='Charts',size=12.7,bold=True)])
cy=178
for i,(n,t,sub,img) in enumerate(charts):
    t_=tb(s,52,cy,690,18,[dict(text='',size=10.1)]); p=t_.text_frame.paragraphs[0]
    addruns(p,n,10.1,TIGER,True); addruns(p,' · '+t,10.1,SPACE,True)
    nl=2 if len(sub)>110 else 1
    tb(s,52,cy+22,690,16*nl,[dict(text=sub,size=8.6,color=BLUE)])
    im=Image.open(img); w=674-16; hh=w*im.height/im.width; fy=cy+22+17*nl+6
    box(s,52,fy,690,hh+16); s.shapes.add_picture(img,px(60),px(fy+8),width=px(w))
    tb(s,52,fy+hh+16+5,690,14,[dict(text=SRC,size=7.9)])
    cy=fy+hh+16+5+14+10
footer(s,6)
# ---------------- page 7
s=newslide(); header(s)
tb(s,52,112,300,24,[dict(text='Sources',size=12.7,bold=True)]); tb(s,52,142,690,18,[dict(text='•  Syz Research, Bloomberg, company data.',size=8.6)])
tb(s,52,176,300,24,[dict(text='Important information',size=12.7,bold=True)])
tb(s,52,206,690,800,[dict(text=x,size=7.9,align=J,after=5,ls=1.15) for x in DISC])
footer(s,7)
prs.save('Syz_EssilorLuxottica_eye-health_ad-hoc_2026-11-27.pptx')
