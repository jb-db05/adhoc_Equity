# -*- coding: utf-8 -*-
import importlib.util
spec=importlib.util.spec_from_file_location('v1content','../2026-11-27_essilorluxottica-nunito/content.py'); v1=importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
charts=v1.charts; fiche=v1.fiche
# ---------------- page 1 : the market
s=newslide(); header(s,True); label(s,131); headline(s,150,'The Eyewear & Vision Care Market',21,40)
tb(s,52,190,690,22,[dict(text='27 November 2026 · Syz Research',size=11.2)])
box(s,52,224,690,78); tb(s,70,234,654,64,[dict(text='IMPORTANT NOTICE',size=7.9,color=TIGER,bold=True,after=2),dict(text='Prices are as of the time of writing on 27 November 2026. Company figures come from the 2025 annual results, the first-half 2026 results and the third-quarter revenue release of 20 October 2026. Multiples use Bloomberg consensus earnings. This is not an investment recommendation.',size=8.6,align=J,ls=1.15)])
kpis(s,314,72,[('Global eyewear market','USD 160-190 bn','2025 estimates, wide range'),('Vision impairment','2.2 bn+','People worldwide, at least'),('Ageing populations','x 2','People aged 60+, by 2050'),('Short-sighted by 2050','Nearly 5 bn','About half of humanity')])
tb(s,52,398,690,24,[dict(text='A defensive market with new areas of growth',size=12.7,bold=True)])
table(s,52,424,[104,246,340],['Segment','What is happening','Indicators'],[
 ['Core eyewear','Defensive and non-discretionary; replacement cycles can lengthen but remain stable','Spectacle lenses: roughly USD 60bn at retail in 2025; growth of about 4% to 7% a year'],
 ['Myopia management','From correction to treatment; lenses, contact lenses and drops compete','Nearly 5bn people projected to be short-sighted by 2050; control-lens market about USD 1.6bn to 1.8bn, growing 10% to 12% a year'],
 ['AI glasses','From audio and video capture towards assistants with navigation, translation and health alerts','Shipments +139% in H2 2025 and +212% in H1 2026; North America 37% and Western Europe 30% of H2 2025 shipments']],size=7.7,rowh=34,title='The market at a glance')
cols(s,588,440,
 [('sub2','A defensive sector with new trends'),
  ('p','The category remains defensive because demand is non-discretionary and follows demographics: the number of short-sighted people is rising and ageing populations need more frequent vision care. But new trends are emerging alongside this traditional vision-correction business: myopia management, which turns lenses for children into a treatment; AI glasses, which add a camera, microphones and an assistant to the frame; hearing glasses, which bring eyewear into audiology; and retinal imaging with AI (oculomics), which could make the eye care visit a screening point for wider health.'),
  ('sub2','Myopia management'),
  ('p','Stellest, the lens at the centre of this trend, belongs to Essilor, part of EssilorLuxottica, the world\'s largest eyewear group and its leading lens maker, which is why its position is essential to understand. The more the eye lengthens in childhood, the higher the later risk of serious eye disease such as retinal detachment, glaucoma or myopic maculopathy, so slowing progression early could protect sight for life. In the US trial behind its authorisation, children aged 6 to 12 wearing Stellest saw their myopia progress 71% more slowly over two years than with standard lenses, according to the company.'),
  ('p','Stellest is FDA-authorised, through the De Novo pathway, as the first and only spectacle lens to correct myopia and slow its progression in children aged 6 to 12. That makes it a medical device backed by clinical data and fitted by eye care professionals, not a fashion accessory: it places the group in a different market, closer to paediatric ophthalmology and medtech, with follow-up visits and a higher value per patient. Rivals include Hoya (MiYOSMART), CooperVision (MiSight) and low-dose atropine drops, approved in the EU and the UK.')],
 [('sub2','AI glasses'),
  ('p','Smart eyewear is moving from a niche multimedia tool towards an intelligent platform that understands its surroundings. Display-less AI glasses make up most of the volume, and Meta with EssilorLuxottica leads the category (roughly 70% to 85% of shipments depending on the definition). Google and Samsung are entering; the optics (waveguides, adaptive lenses) are becoming an electronics-grade field, but prescription lenses and optical laboratories remain a barrier for pure technology players.'),
  ('p','Stepping back, privacy could be the largest risk for the whole category, not only for one maker. A camera worn on the face can record people who do not know it, and AI features can process what it sees. The regions that protect personal data most strictly are also among the biggest markets: North America is about 37% of smart-glasses shipments and Western Europe about 30%, and European law already treats images of identifiable people as personal data. Retailers have pulled the product in the Netherlands and Belgium, and the Dutch data protection authority has advised consumers not to buy AI camera glasses for now. Tighter rules, bans in sensitive places or a loss of public trust in these regions could slow adoption for every maker, and would weigh most on the groups most exposed to them.'),
  ('sub2','Oculomics'),
  ('p','The retina is the one place where blood vessels and nerve tissue can be seen without surgery. High-resolution imaging (OCT) with AI could turn eye care professionals into players in preventive health, but uses beyond eye disease, such as diabetes, heart disease or neurological decline, are still being researched.')],size=8.0,after=3.5)
footer(s,1)
# ---------------- page 2 : the company
s=newslide(); header(s); label(s,108); headline(s,126,fiche['title'],21,34)
tb(s,52,163,690,20,[dict(text='Stable earnings, a lower multiple and a smart-glasses debate that is still open',size=10.5,color=TIGER,bold=True)])
kpis(s,190,66,[k[:3] for k in fiche['kpis']])
cols(s,266,685,
 [('h3','1. What the company does'),
  ('p','EssilorLuxottica is by far the largest company in eyewear. Its 2025 revenue of EUR 28.5bn compares with EUR 2.4bn for Fielmann, a leading European optical retailer, and EUR 1.0bn for the frame maker Safilo, and estimates of its global share range from about 13% to 25%. It was formed by the 2018 merger of Essilor and Luxottica and added GrandVision in 2021.'),
  ('p','It reports two divisions. Professional Solutions (about 45% of third-quarter revenue) makes lenses, frames and instruments and sells them to opticians and other retailers it does not own. Direct to Consumer (about 55%) is its own retail: LensCrafters, Sunglass Hut, Pearle Vision, GrandVision stores and e-commerce. By region, North America is about 43% of revenue, EMEA 39%, Asia-Pacific 13% and Latin America 6%.'),
  ('p','Two distinctions matter. On brands, the group owns Ray-Ban and Oakley, but many big names (Prada, Chanel, Armani and others) are licences: the fashion house lends its name and earns a royalty, while the group designs, makes and distributes the frames. On channels, its stores are a retail outlet rather than a brand and can carry other makers\' products, while its own products also reach consumers through independent opticians and other retailers.'),
  ('h3','2. Investment case: a leader at a low valuation'),
  ('p','**Scale and resilience.** Demand is non-discretionary and the group sells across the chain: third-quarter revenue rose 7.2% at constant exchange rates (+8.9% over nine months), Asia-Pacific grew 15.7%, and first-half adjusted operating profit rose 15%, helped by US tariff refunds.'),
  ('p','**A valuation that looks low.** The shares are 46% below their November 2025 record and trade on 22.1 times expected earnings against 27.5 over ten years, while the earnings forecast is almost unchanged (EUR 7.80 against EUR 7.87). The multiple touched 17.7x in September, its lowest in ten years, so much of the bad news may already be in the price. A close above EUR 194 could confirm a trend change; EUR 150 and EUR 139 are levels to watch.'),
  ('p','**Problems that could be resolved.** Margin dilution could ease as wearables gain scale and move to higher-priced models; privacy risk can be addressed through design, such as camera-free models, and clearer rules; governance could be settled at the 2027 shareholder meeting.'),
  ('p','**Positive prospects.** Several lines outgrow the core: myopia management +24% and wearables +20%, helped by ageing and rising myopia. Hearing glasses (Nuance Audio) and retinal imaging (Heidelberg Engineering) are small examples of the medtech push.')],
 [('h3','3. The Meta glasses'),
  ('p','The partnership with Meta created the smart-glasses category: more than 7 million pairs were sold in 2025, AI glasses revenue nearly doubled in the second quarter and wearables grew 20% in the third, at close to 6.5% of revenue according to press reports. Looking ahead, the September launches (camera-free Ray-Ban Meta Audio, a third generation, Meta\'s Muse AI agent, new countries) are not yet in these numbers, and capacity is heading towards 10 million units a year.'),
  ('p','The catch is margin. The cameras, chips, batteries and speakers inside the frame are expensive, so these glasses earn less than traditional eyewear, and the adjusted operating margin fell 70 basis points to 16.0% in 2025. Price mix could be part of the answer: connected Oakley glasses sell above Ray-Ban Meta (USD 399 against USD 299 at launch), and about a third of wearables sales already include a prescription lens, which adds lens revenue; management points to price mix, scale and productivity for a better margin in the second half.'),
  ('p','Privacy remains the main outside threat: the glasses can film without an obvious signal, retailers in the Netherlands and Belgium stopped selling them, and on 19 November the Dutch data protection authority advised consumers not to buy AI camera glasses for now. The data is Meta\'s, but the Ray-Ban brand is the group\'s, creating a potential reputational risk.'),
  ('h3','4. Main risks'),
  ('p','The risks are linked and weigh on the shares together. Wearables earn less today, and first-half profit was helped by US tariff refunds that may not repeat, so the market wants proof that margins recover as volumes grow. On top of that sits a governance question that is not yet resolved. The largest shareholder, Delfin (32.4%), the founder\'s family holding, is split among eight heirs and its bylaws make change difficult. In July an heir left his roles at the group after a reported dispute with the CEO, linked to a plan to buy out his siblings\' stakes in Delfin, and questioned how succession had been prepared. The board said on 9 September that it has full confidence in the CEO and the strategy, but his mandate comes up for renewal at the shareholder meeting expected in spring 2027, and the family deadlock has not been settled. Until it is, governance weighs on the shares alongside margin dilution. Privacy rules, dependence on Meta, new rivals and US consumer spending add to the list.'),
  ('h3','5. What to watch next'),
  ('p','Full-year 2026 results, due early in 2027; holiday sales of the new Ray-Ban Meta models and the Muse rollout; the spring 2027 shareholder meeting; European rules on camera glasses; products from Google, Samsung and Apple.')],size=7.8,after=3)
concl(s,956,96,'CONCLUSION','EssilorLuxottica combines a stable lens, frame and retail business with a fast-growing but contested smart-glasses line and a widening medtech offer. Earnings forecasts have hardly moved in a year while the multiple has fallen from about 40 to 22 times, which shows how much of the share price rested on sentiment around Meta glasses. The outcome could depend on adoption, competition, governance and the social and regulatory acceptance of camera glasses.')
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
