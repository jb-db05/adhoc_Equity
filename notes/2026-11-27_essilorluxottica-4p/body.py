# -*- coding: utf-8 -*-
import importlib.util
spec=importlib.util.spec_from_file_location('v1content','../2026-11-27_essilorluxottica-nunito/content.py'); v1=importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
charts=v1.charts; fiche=v1.fiche
# ---------------- page 1 : the market
s=newslide(); header(s,True); label(s,131); headline(s,150,'From Vision Correction to Eye Health Management',21,40)
tb(s,52,190,690,22,[dict(text='27 November 2026 · Syz Research',size=11.2)])
box(s,52,224,690,78); tb(s,70,234,654,64,[dict(text='IMPORTANT NOTICE',size=7.9,color=TIGER,bold=True,after=2),dict(text='Prices are as of the time of writing on 27 November 2026. Company figures come from the 2025 annual results, the first-half 2026 results and the third-quarter revenue release of 20 October 2026. Multiples use Bloomberg consensus earnings. This is not an investment recommendation.',size=8.6,align=J,ls=1.15)])
kpis(s,316,76,[('Share price','EUR 172.15','−36% since the start of 2026'),('Forward P/E','22.1x','Ten-year average: 27.5x'),('Q3 2026 revenue growth','+7.2%','At constant exchange rates'),('Myopia management','+24%','Q3 2026 revenue growth')])
tb(s,52,404,690,24,[dict(text='A defensive market turning into a health-technology ecosystem',size=12.7,bold=True)])
table(s,52,436,[104,246,340],['Segment','What is happening','Indicators'],[
 ['Core eyewear','Defensive and non-discretionary; replacement cycles can lengthen but remain stable','Spectacle lenses: roughly USD 60bn at retail in 2025; growth of about 4% to 7% a year depending on the source'],
 ['Myopia management','From correction to treatment; lenses, contact lenses and drops compete','Nearly 5bn people projected to be short-sighted by 2050; control-lens market about USD 1.6bn to 1.8bn, growing 10% to 12% a year'],
 ['AI glasses','From audio and video capture towards assistants with navigation, translation and health alerts','Shipments +139% in H2 2025 and +212% in H1 2026; North America 37% and Western Europe 30% of H2 2025 shipments'],
 ['Hearing','Over-the-counter hearing glasses enter audiology','More than 1bn people live with some hearing loss'],
 ['Diagnostics','Retinal imaging and AI could make the eye care visit a screening point','Early detection of glaucoma and macular degeneration today; wider disease detection at research stage'],
 ['Retail','Chains scale up and add their own technology','Lenskart revenue +32% in the year to March 2026 with 603 stores added; Fielmann expanding in the US']],size=7.7,rowh=40,title='The market at a glance')
cols(s,738,314,
 [('sub2','A sector in structural transformation'),
  ('p','The eyewear and optical health sector is moving from a traditional vision-correction market towards a high-tech ecosystem built around myopia management, AI wearables and preventive eye health. The category remains defensive because demand is non-discretionary and follows demographics: the number of short-sighted people is rising and ageing populations need more frequent vision care.'),
  ('sub2','Myopia management'),
  ('p','Myopia is now seen as a global epidemic. Lenses that slow its progression in children move the field from simple correction to evidence-based prevention. Stellest, the group\'s lens, was named one of TIME\'s Best Inventions of 2026; Hoya (MiYOSMART) and CooperVision (MiSight) are scaling their own programmes, and low-dose atropine drops are approved in the EU and the UK. The market is small next to the number of children concerned, so adoption is still early.')],
 [('sub2','AI glasses'),
  ('p','Smart eyewear is moving from a niche multimedia tool towards an intelligent platform that understands its surroundings. Display-less AI glasses make up most of the volume, and Meta with EssilorLuxottica leads the category (roughly 70% to 85% of shipments depending on the definition). Google and Samsung are entering; the complexity of prescription lenses and optical laboratories is a barrier for pure technology players, and the optics themselves (waveguides, adaptive lenses) are becoming an electronics-grade field.'),
  ('sub2','Oculomics'),
  ('p','The retina is the one place where blood vessels and nerve tissue can be seen without surgery. High-resolution imaging (OCT) with AI could turn eye care professionals into players in preventive health, but uses beyond eye disease, such as diabetes, heart disease or neurological decline, are still being researched.')],size=8.4,after=4)
footer(s,1)
# ---------------- page 2 : the company
s=newslide(); header(s); label(s,108); headline(s,126,fiche['title'],21,34)
tb(s,52,163,690,20,[dict(text='Stable earnings, a lower multiple and a smart-glasses debate that is still open',size=10.5,color=TIGER,bold=True)])
kpis(s,192,70,[k[:3] for k in fiche['kpis']])
box(s,52,272,690,104); tw=690/4
for i,(a,b) in enumerate(fiche['tech']):
    cx=52+i*tw
    if i: line(s,cx,274,cx,318)
    tb(s,cx+14,281,tw-24,40,[dict(text=a,size=7.9,color=TIGER,bold=True),dict(text=b,size=10.5,bold=True)])
line(s,54,320,740,320)
tb(s,70,326,654,46,[dict(text=fiche['techline'],size=8.2,align=J,ls=1.12)])
cols(s,388,545,
 [('h3','1. What the company does'),
  ('p','EssilorLuxottica was formed by the 2018 merger of Essilor (lenses) and Luxottica (frames and retail), and added GrandVision\'s stores in 2021. Revenue in 2025 was EUR 28.5bn, up 7.5% (11.2% at constant exchange rates). It is vertically integrated: it makes lenses and frames, owns brands such as Ray-Ban and Oakley, and sells through opticians and its own stores and online (LensCrafters, Sunglass Hut).'),
  ('h3','2. Why it could do well'),
  ('p','Third-quarter revenue rose 7.2% at constant exchange rates (+8.9% over nine months), with Asia-Pacific up 15.7%, EMEA up 7.5% and North America up 4.7%. First-half adjusted operating profit rose 15%, at an 18.6% margin, helped by US tariff refunds. Myopia management grew 24% in the quarter and in the nine months, and Stellest opened about 12,000 doors in the US in its first year. Transitions lenses reached about 60% penetration in the group\'s own retail, from 40% to 50% a year earlier.'),
  ('h3','3. What sets it apart'),
  ('p','No competitor combines lenses, frames, brands and retail at this scale. The medtech side is widening: Stellest for myopia (FDA-authorised in the US), Nuance Audio for hearing, Heidelberg Engineering for retinal imaging, and ophthalmology clinics (Optegra, Signifeye). The group is also building its own optics, with an Applied Materials development agreement (June 2026) on waveguides and adaptive lenses.'),
  ('h3','4. Is the share cheap?'),
  ('p','Cheaper than it has been for most of the past decade: 22.1 times expected earnings, against 27.5 over ten years and about 40 a year ago, with the forecast almost unchanged (EUR 7.80 against EUR 7.87). Part of the earlier premium paid for smart-glasses growth.')],
 [('h3','5. The Meta glasses'),
  ('p','The partnership with Meta created the smart-glasses category: more than 7 million pairs were sold in 2025, AI glasses revenue nearly doubled in the second quarter and wearables grew 20% in the third, at close to 6.5% of revenue according to press reports. About a third of wearables sales include a prescription lens, which brings lens revenue with the frame. In September the companies added a camera-free model, a third generation and Meta\'s Muse AI agent. The line still dilutes margins, and it carries a privacy problem: the glasses can film without an obvious signal, Hans Anders and Wehkamp stopped selling them in the Netherlands and Belgium, and on 19 November the Dutch data protection authority advised consumers not to buy AI camera glasses for now. The data is Meta\'s, but the Ray-Ban brand is the group\'s.'),
  ('h3','6. Main risks'),
  ('p','Margin dilution while wearables scale, and first-half profit that benefited from US tariff refunds, which may not repeat. Privacy rules and retailer reactions in Europe. Dependence on Meta, and rivals from Google, Samsung, Apple and Chinese makers. Governance: an heir of the founder left his roles at the group in July after a reported dispute with the CEO, the largest shareholder, Delfin (32.4%), is split among eight heirs, the board backed the CEO in September, and his mandate comes up for renewal in spring 2027. Weaker US consumer spending could also hit traffic.'),
  ('h3','7. What to watch next'),
  ('p','Full-year 2026 results, due early in 2027, with the wearables margin and the tariff effect; holiday sales of the new Ray-Ban Meta models and the Muse rollout; the shareholder meeting in spring 2027; European rules on camera glasses; products from Google, Samsung and Apple; the Nuance Audio roll-out.')],size=8.1,after=3.5)
concl(s,940,116,'CONCLUSION','EssilorLuxottica combines a stable lens, frame and retail business with a fast-growing but contested smart-glasses line and a widening medtech offer. Over the past year its earnings forecasts have hardly moved while its multiple has fallen from about 40 to 22 times, which shows how much of the share price rested on sentiment around Meta glasses. The outcome could depend on adoption, on competition, on governance and, more and more, on the social and regulatory acceptance of camera glasses.')
footer(s,2)
# ---------------- page 3 : charts
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
footer(s,3)
# ---------------- page 4 : sources
s=newslide(); header(s)
tb(s,52,112,300,24,[dict(text='Sources',size=12.7,bold=True)]); tb(s,52,142,690,18,[dict(text='•  Syz Research, Bloomberg, company data.',size=8.6)])
tb(s,52,176,300,24,[dict(text='Important information',size=12.7,bold=True)])
tb(s,52,206,690,800,[dict(text=x,size=7.9,align=J,after=5,ls=1.15) for x in DISC])
footer(s,4)
prs.save('Syz_EssilorLuxottica_4p_ad-hoc_2026-11-27.pptx')
