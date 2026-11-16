import re, sys
src = open(sys.argv[1]).read()
T = {
"16 novembre 2026": "16 November 2026",
"Biotech US : lecture fondamentale de VKTX, IMVT et INCY": "US biotech: a fundamental view on VKTX, IMVT and INCY",
"INCY en cœur de portefeuille, IMVT en satellite, VKTX en spéculatif": "INCY as a core holding, IMVT as a satellite, VKTX as a speculative position",
"Synthèse fondamentale · classement par niveau de risque · ": "Fundamental summary · ranked by risk · ",
"INCY · Cœur de portefeuille": "INCY · Core holding",
"Incyte · rentable, 2028 à franchir": "Incyte · profitable, 2028 to bridge",
"Immunovant · pré-revenus, plateforme validée": "Immunovant · pre-revenue, platform partly validated",
"VKTX · Spéculatif": "VKTX · Speculative",
"Viking · un actif, un résultat binaire en 2027": "Viking · one asset, one binary readout in 2027",
"Profil": "Profile",
"Rentable, ventes 2026 ≈ 5,2–5,3 Md USD": "Profitable, 2026 sales ≈ USD 5.2–5.3 bn",
"Pas de revenu, IMVT-1402 en essais pivots": "No revenue, IMVT-1402 in pivotal trials",
"Pas de revenu, VK2735 en phase 3": "No revenue, VK2735 in Phase 3",
"Ce qui est dans le prix": "What is priced in",
"Le choc Jakafi 2028": "The 2028 Jakafi cliff",
"Le succès dans plusieurs indications": "Success in several indications",
"Beaucoup de doute": "A lot of doubt",
"Prochain test": "Next test",
"Pipeline mutCALR, guidance 2027": "mutCALR pipeline, 2027 guidance",
"Graves et myasthénie, 2027": "Graves' and myasthenia gravis, 2027",
"VANQUISH, 2S 2027": "VANQUISH, 2H 2027",
"Risque principal": "Main risk",
"Trou de revenus après 2028": "Revenue gap after 2028",
"Concurrence FcRn, flottant étroit": "FcRn competition, narrow float",
"Résultat, financement, prix": "Trial outcome, funding, pricing",
"Rôle possible": "Possible role",
"Position cœur": "Core holding",
"Position satellite": "Satellite position",
"Petite position spéculative": "Small speculative position",
"Source : Syz Research, Bloomberg, publications des sociétés (T3 2026).": "Source: Syz Research, Bloomberg, company publications (Q3 2026).",
"Chiffres clés fondamentaux": "Key fundamental figures",
"En USD · cours au 13 novembre 2026, capitalisations au 16 novembre 2026, bilans au 30 septembre 2026":
    "USD · prices as of 13 November 2026, market caps as of 16 November 2026, balance sheets as of 30 September 2026",
"Cours (13.11.2026)": "Share price (13 Nov 2026)",
"120,12": "120.12", "34,09": "34.09", "26,96": "26.96",
"Capitalisation (16.11.2026)": "Market capitalisation (16 Nov 2026)",
"24,7 Md": "24.7 bn", "7,1 Md": "7.1 bn", "3,7 Md": "3.7 bn",
"Trésorerie et placements CT (30.09.2026)": "Cash and short-term investments (30 Sep 2026)",
"3,9 Md *": "3.9 bn *", "722 M": "722 m", "960 M": "960 m",
"Valeur d'entreprise (calcul Syz)": "Enterprise value (Syz calculation)",
"20,8 Md": "20.8 bn", "6,4 Md": "6.4 bn", "2,8 Md": "2.8 bn",
"Chiffre d'affaires 2025": "Revenue 2025", "5,14 Md": "5.14 bn",
"Ventes nettes 2026 (guidance relevée)": "2026 net sales (raised guidance)", "5,21–5,30 Md": "5.21–5.30 bn",
"VE / ventes nettes 2026 (calcul Syz)": "EV / 2026 net sales (Syz calculation)",
"Résultat T3 2026": "Q3 2026 net result", "Perte GAAP (charge Vega 1,23 Md)": "GAAP loss (1.23 bn Vega charge)",
"Perte": "Loss", "−183 M": "−183 m",
"Couverture de trésorerie (calcul Syz)": "Cash runway (Syz calculation)", "Autofinancé": "Self-funded",
"Jusqu'au lancement Graves": "To a Graves' launch", "≈ 5 trimestres": "≈ 5 quarters",
"Principal catalyseur": "Main catalyst", "Pipeline 2027–2028": "Pipeline 2027–2028", "Données 2027": "2027 data",
"VANQUISH 2S 2027": "VANQUISH 2H 2027",
"VE = capitalisation moins trésorerie et placements CT, dette non déduite. Couverture VKTX = trésorerie / perte nette T3. ":
    "EV = market capitalisation less cash and short-term investments, debt not deducted. VKTX runway = cash / Q3 net loss. ",
"* Trésorerie INCY à confirmer après le paiement de Vega. Source : Syz Research, Bloomberg, publications des sociétés.":
    "* INCY cash to be confirmed after the Vega payment. Source: Syz Research, Bloomberg, company publications.",
"Les catalyseurs s'étalent de fin 2026 à 2028": "Catalysts are spread from late 2026 to 2028",
"Calendrier communiqué par les sociétés · les échéances d'options doivent couvrir la bonne fenêtre":
    "Timelines communicated by the companies · option expiries must cover the right window",
"Phase 3 mutCALR en myélofibrose (lancement)": "Phase 3 mutCALR in myelofibrosis (start)",
"Guidance 2027": "2027 guidance",
"Phase 3 KRAS G12D, cancer du pancréas": "Phase 3 KRAS G12D, pancreatic cancer",
"Perte d'exclusivité Jakafi aux États-Unis": "Jakafi US loss of exclusivity",
"Réunion FDA fin de phase 2 (polyarthrite)": "FDA End of Phase 2 meeting (RA)",
"Données pivots Graves et myasthénie": "Registrational data, Graves' and myasthenia gravis",
"Données pivots CIDP": "Registrational data, CIDP",
"VK3019 : étude de doses (T1)": "VK3019 dose study (Q1)",
"Maintenance, partie 2": "Maintenance study, part 2",
"VANQUISH-1 et -2 (2S)": "VANQUISH-1 and -2 (2H)",
"SUNRISE, version orale": "SUNRISE, oral version",
"Dates indicatives communiquées par les sociétés (T3 2026) ; les dates exactes des résultats ne sont pas publiées. Source : Syz Research, publications des sociétés.":
    "Indicative timing communicated by the companies (Q3 2026); exact readout dates are not published. Source: Syz Research, company publications.",
"Source : Syz Research, Bloomberg, publications de la société. Les calculs Syz sont indiqués comme tels.":
    "Source: Syz Research, Bloomberg, company publications. Syz calculations are labelled as such.",
# Incyte
"Incyte : un leader rentable qui doit remplacer Jakafi d'ici 2028": "Incyte: a profitable leader racing to replace Jakafi by 2028",
"Incyte (INCY) · hématologie, oncologie, dermatologie": "Incyte (INCY) · haematology, oncology, dermatology",
"Capitalisation": "Market cap", "24,7 Md USD": "USD 24.7 bn", "16 novembre 2026": "16 November 2026",
"Ventes nettes 2026": "2026 net sales", "Guidance relevée au T3": "Raised with Q3 results",
"Jakafi, T3 2026": "Jakafi, Q3 2026", "827 M USD": "USD 827 m", "+4 % sur un an": "+4% year on year",
"VE / ventes 2026": "EV / 2026 sales", "Calcul Syz": "Syz calculation",
"Pourquoi le titre pourrait progresser": "Why it could do well",
"Le chiffre d'affaires du T3 a progressé de 14 % à 1,56 Md USD et Opzelura de 36 % à 255 M USD. ":
    "Q3 revenue rose 14% to USD 1.56 bn and Opzelura sales rose 36% to USD 255 m. ",
"Hors Jakafi, l'activité représente déjà plus d'un tiers des ventes. Jakafi XR, la version à prise unique, ":
    "The business beyond Jakafi is already more than a third of sales. Jakafi XR, the once-daily version, ",
"commence à contribuer.": "has started to contribute.",
"Le vrai levier : le pipeline": "The real lever: the pipeline",
"L'anticorps anti-mutCALR (INCA033989) est en étude pivot dans la thrombocytémie essentielle, avec une phase 3 ":
    "The mutCALR antibody (INCA033989) is in a pivotal study in essential thrombocythaemia, with a Phase 3 ",
"en myélofibrose fin 2026. L'inhibiteur KRAS G12D vise des données de phase 3 dans le pancréas en 2028. ":
    "in myelofibrosis from late 2026. The KRAS G12D inhibitor targets Phase 3 pancreatic cancer data in 2028. ",
"L'achat de Vega (1,25 Md USD) ajoute un actif dans la maladie de von Willebrand.":
    "The Vega deal (USD 1.25 bn upfront) adds an asset in von Willebrand disease.",
"Le titre est-il bon marché ?": "Is the share cheap?",
"Environ 4 fois les ventes 2026 (calcul Syz), un multiple modeste pour une biotech rentable. La décote reflète ":
    "About 4x 2026 sales (Syz calculation), a modest multiple for a profitable biotech. The discount reflects ",
"le risque 2028 : Jakafi pèse encore près de 60 % des ventes nettes.":
    "the 2028 risk: Jakafi is still close to 60% of net sales.",
"Risques principaux": "Main risks",
"Trou de revenus entre 2028 et l'arrivée des nouveaux produits, échec dans les programmes mutCALR ou KRAS, ":
    "A revenue gap between 2028 and new launches, setbacks in the mutCALR or KRAS programmes, ",
"pression sur les prix (négociation Medicare), acquisitions trop chères. Le T3 est une perte GAAP à cause ":
    "pricing pressure (Medicare negotiation), overpaying for deals. Q3 was a GAAP loss because ",
"de la charge Vega.": "of the Vega charge.",
"À surveiller": "What to watch",
"Lancement de la phase 3 en myélofibrose, données mutCALR, adoption de Jakafi XR, guidance 2027.":
    "Start of the myelofibrosis Phase 3, mutCALR data, Jakafi XR uptake, 2027 guidance.",
"Le plus défensif des trois. Les profits laissent le temps de franchir 2028 et la valorisation intègre déjà une ":
    "The most defensive of the three. Profits buy time to bridge 2028 and the valuation already prices in a ",
"bonne partie du risque. Peut servir de position cœur.": "good part of the risk. Could serve as a core holding.",
# Immunovant
"Immunovant : une plateforme FcRn en partie validée": "Immunovant: an FcRn platform, now partly validated",
"Immunovant (IMVT) · anti-FcRn IMVT-1402 · contrôlée à ~56 % par Roivant": "Immunovant (IMVT) · anti-FcRn IMVT-1402 · ~56% owned by Roivant",
"7,1 Md USD": "USD 7.1 bn", "Trésorerie": "Cash", "722 M USD": "USD 722 m", "30 septembre 2026": "30 September 2026",
"Valeur d'entreprise": "Enterprise value", "6,4 Md USD": "USD 6.4 bn",
"Prochaines données": "Next data", "Graves, myasthénie": "Graves', myasthenia gravis",
"En novembre, la dose de 600 mg a atteint son critère principal dans la polyarthrite rhumatoïde difficile à ":
    "In November the 600 mg dose met its primary endpoint in difficult-to-treat rheumatoid ",
"traiter : 92,5 % des patients ont conservé leur réponse ACR20 à la semaine 28, contre 75,6 % sous placebo. ":
    "arthritis: 92.5% of patients kept their ACR20 response at week 28, against 75.6% on placebo. ",
"C'est le premier signe qu'un anti-FcRn peut fonctionner dans une maladie fréquente.":
    "It is the first sign that an FcRn blocker can work in a common disease.",
"Ce qui le distingue": "What sets it apart",
"IMVT-1402 vise une baisse profonde des IgG sans les effets sur l'albumine et le LDL des produits de première ":
    "IMVT-1402 aims at deep IgG reduction without the albumin and LDL effects of first-generation ",
"génération. Dans la maladie de Graves, aucun anti-FcRn n'est approuvé : une première possible.":
    "agents. No FcRn drug is approved in Graves' disease: a possible first.",
"Non sur les mesures classiques : 6,4 Md USD de VE sans revenu supposent déjà des succès dans plusieurs ":
    "Not on conventional measures: USD 6.4 bn of EV without revenue already assumes success in several ",
"indications. La trésorerie doit couvrir les besoins jusqu'à un lancement dans Graves.":
    "indications. Cash should fund the company to a Graves' launch.",
"Concurrence de produits FcRn déjà commercialisés par de grands groupes. Résultat obtenu sur une seule dose, ":
    "Competition from FcRn drugs already marketed by large groups. The result rests on one dose, ",
"avec un placebo élevé, et une deuxième étude pivot nécessaire. Abandon du lupus cutané, Sjögren peu probable. ":
    "with a high placebo rate, and a second pivotal trial is needed. Cutaneous lupus dropped, Sjögren's unlikely. ",
"Flottant étroit.": "Narrow float.",
"Issue de la réunion FDA fin 2026, design de la prochaine étude, données 2027.":
    "Outcome of the FDA meeting in late 2026, design of the next trial, 2027 data.",
"La société est passée de la promesse à une plateforme en partie validée, mais une bonne partie des bonnes ":
    "The company has moved from promise to a partly validated platform, but much of the good ",
"nouvelles est dans le prix. Convient à une position satellite.": "news is priced in. Suits a satellite position.",
# Viking
"Viking : un candidat sérieux dans l'obésité, un test binaire en 2027": "Viking: a serious obesity contender facing a binary 2027",
"Viking Therapeutics (VKTX) · VK2735, double agoniste GLP-1/GIP": "Viking Therapeutics (VKTX) · VK2735, dual GLP-1/GIP agonist",
"3,7 Md USD": "USD 3.7 bn", "960 M USD": "USD 960 m",
"Perte nette T3 2026": "Net loss, Q3 2026", "−183 M USD": "USD −183 m", "Aucun revenu": "No revenue",
"Données phase 3": "Phase 3 data", "2S 2027": "2H 2027", "VANQUISH-1 et -2": "VANQUISH-1 and -2",
"Deux phases 3 entièrement recrutées (environ 4 500 et 1 000 patients) et une version orale entrée en phase 3 ":
    "Two fully enrolled Phase 3 trials (about 4,500 and 1,000 patients) and an oral version that entered Phase 3 ",
"(SUNRISE) en octobre, données en 2028. Un résultat positif ferait de Viking l'un des rares indépendants ":
    "(SUNRISE) in October, with data in 2028. A positive readout would make Viking one of very few independents ",
"avec un double agoniste avancé, injectable et oral.": "with a late-stage dual agonist, injectable and oral.",
"En phase 2, les patients passés à une injection toutes les deux semaines ou mensuelle ont conservé 82 à 97 % ":
    "In Phase 2, patients switched to every-other-week or monthly injections kept 82% to 97% ",
"de leur perte de poids. Le programme amyline VK3019 ajoute un second mécanisme.":
    "of their weight loss. The VK3019 amylin programme adds a second mechanism.",
"Bon marché, ou piège ?": "Cheap, or a value trap?",
"Une VE d'environ 2,8 Md USD (calcul Syz) paraît faible face au marché de l'obésité, mais le doute est ":
    "An EV of about USD 2.8 bn (Syz calculation) looks small against the obesity market, but the doubt is ",
"rationnel : Viking arriverait des années après les deux leaders, dans un marché où les prix baissent.":
    "rational: Viking would arrive years after the two leaders, in a market where prices are falling.",
"Le résultat lui-même, y compris la tolérance et les abandons. Le financement : environ 5 trimestres de ":
    "The readout itself, including tolerability and drop-outs. Funding: about five quarters of ",
"trésorerie au rythme du T3 (calcul Syz), soit jusqu'aux données ; une levée ou un partenariat serait ":
    "cash at the Q3 burn rate (Syz calculation), i.e. to the data; a raise or a partnership would ",
"très probablement nécessaire. Pas de force de vente.": "very likely be needed. No sales force.",
"Maintenance partie 2, VK3019, partenariat éventuel, puis VANQUISH au 2S 2027.":
    "Maintenance part 2, VK3019, any partnering, then VANQUISH in 2H 2027.",
"Le potentiel le plus élevé des trois, mais le risque le plus concentré : un actif, une fenêtre de résultats, ":
    "The highest potential of the three, but the most concentrated risk: one asset, one readout window, ",
"un besoin de financement. Petite position spéculative uniquement, pas sur le seul espoir d'un rachat.":
    "a funding need. A small speculative position only, not on takeover hopes alone.",
# proposal
"Du fondamental à la proposition : aligner horizon et échéance": "From fundamentals to the proposal: match horizon and expiry",
"Pistes à faire coter par le desk · prix théoriques indicatifs au 13 novembre 2026":
    "Ideas to be priced by the desk · indicative theoretical prices as of 13 November 2026",
"Vue": "View", "Fenêtre clé": "Key window", "Piste (indicative)": "Idea (indicative)", "Point d'attention": "Watch point",
"Cœur": "Core", "Guidance 2027, mutCALR": "2027 guidance, mutCALR",
"Détenteur : collar juin 2027, vente CALL 140 / achat PUT 105, coût ≈ nul. Nouvel investisseur : vente PUT mars 2027 strike 110, prime ≈ 8 USD":
    "Holder: June 2027 collar, sell 140 call / buy 105 put, cost ≈ zero. New money: sell March 2027 110 put, premium ≈ USD 8",
"Volatilité implicite de ~49 % élevée pour Incyte : à vérifier avant de fixer les strikes":
    "Implied volatility of ~49% looks high for Incyte: check before setting strikes",
"Réunion FDA fin 2026, données 2027": "FDA meeting late 2026, 2027 data",
"Vente PUT mars 2027 strike 30, prime ≈ 2,7 USD (entrée effective ≈ 27,3). Ou call spread déc. 2027 35/50, coût ≈ 4 USD pour un gain maximal de 15":
    "Sell March 2027 30 put, premium ≈ USD 2.7 (effective entry ≈ 27.3). Or December 2027 35/50 call spread, cost ≈ USD 4 for a maximum gain of 15",
"Le client doit accepter de détenir le titre. Flottant étroit, short interest élevé : mouvements brutaux":
    "The investor must be willing to own the shares. Narrow float, high short interest: sharp moves",
"Spéculatif": "Speculative",
"Pas de structure à ce stade. Si le client insiste : call spread janv. 2028 30/50, coût ≈ 4 USD pour un gain maximal de 20":
    "No structure at this stage. If the investor insists: January 2028 30/50 call spread, cost ≈ USD 4 for a maximum gain of 20",
"Un glissement des données au-delà de janv. 2028 ferait expirer l'option avant le résultat":
    "If the data slip past January 2028, the option expires before the readout",
"À éviter  ": "Avoid  ",
"un produit structuré « worst-of » sur les trois titres. Le coupon serait élevé, mais avec des volatilités de 50 à 70 % ":
    "a worst-of structured product on the three names. The coupon would be high, but with volatilities of 50% to 70% ",
"et deux résultats binaires, la probabilité de toucher la barrière est forte. Dans tous les cas, limiter la taille ":
    "and two binary readouts, the barrier is likely to be hit. In every case, keep IMVT and VKTX ",
"des positions IMVT et VKTX.": "positions small.",
"Prix théoriques Black-Scholes calculés par Syz à partir des cours et volatilités implicites du 13.11.2026 (taux 3,75 %), ":
    "Theoretical Black-Scholes prices calculated by Syz from 13 Nov 2026 prices and implied volatilities (rate 3.75%), ",
"hors frais et écarts de cotation. Non contractuels : cotation du desk requise.":
    "before fees and bid-ask spreads. Not binding: desk quotes required.",
# checks
"Avant diffusion au client : points à fiabiliser": "Before sending to the client: points to firm up",
"Note interne · à traiter avant de finaliser la proposition": "Internal note · to address before finalising the proposal",
"Données": "Data",
"Mettre tous les 13F au 30.09.2026 (date limite 14.11) : Farallon +275 % date du 30.06, avant les données.":
    "Bring all 13Fs to 30 Sep 2026 (deadline 14 Nov): Farallon +275% is as of 30 Jun, before the data.",
"Fidelity +55 % sur VKTX : probablement une souscription à la levée de 500 M USD du 24.09, pas des achats en bourse.":
    "Fidelity +55% in VKTX: probably an allocation in the USD 500 m raise of 24 Sep, not open-market buying.",
"Ratios hausses / baisses 60 j quasi identiques (0,69 / 0,69 / 0,68) et short interest identique sur VKTX et IMVT (19,9 %) : à recontrôler.":
    "Near-identical 60-day up/down ratios (0.69 / 0.69 / 0.68) and identical short interest for VKTX and IMVT (19.9%): recheck.",
"Remplacer Yahoo Finance par Bloomberg (OMON, HDS, SI).": "Replace Yahoo Finance with Bloomberg (OMON, HDS, SI).",
"Lecture": "Reading",
"Le ratio 2,43 d'IMVT vient surtout de la séance du 09.11 (+15 %, volume ×2,6) : réaction aux données plutôt qu'accumulation.":
    "IMVT's 2.43 ratio comes mostly from the 9 Nov session (+15%, volume ×2.6): a reaction to data rather than accumulation.",
"L'open interest ne dit pas qui achète : les CALL déc. 2027 50 d'IMVT peuvent être des ventes couvertes.":
    "Open interest does not show who is buying: IMVT's Dec 2027 50 calls may be covered-call selling.",
"Les CALL VKTX 50, 60 et 120 sont des reliquats, sans valeur de signal.":
    "VKTX 50, 60 and 120 calls are legacy positions with no signal value.",
"INCY : « 2 phases 3 d'ici fin 2026 » sont des lancements d'études, pas des résultats.":
    "INCY: the \\\"two Phase 3s by end-2026\\\" are trial starts, not readouts.",
"Charte Syz": "Syz guidelines",
"Retirer les objectifs moyens des analystes.": "Remove the average analyst targets.",
"Ne pas conditionner une entrée à un seul niveau technique (« zone 30–31 »).":
    "Do not make an entry depend on a single chart level (the \\\"30–31 zone\\\").",
"Présenter la levée VKTX comme une dilution, pas comme un catalyseur.": "Present the VKTX raise as dilution, not as a catalyst.",
"Parler d'« un investisseur », jamais de prix d'entrée ni de perte latente.":
    "Say \\\"an investor\\\"; never show entry prices or unrealised losses.",
}
used = set()
def sub(m):
    s = m.group(1)
    if s in T:
        used.add(s); return '"' + T[s] + '"'
    return m.group(0)
out = re.sub(r'"((?:[^"\\\n]|\\.)*)"', sub, src)
for k in T:
    if k not in used: print("UNUSED:", k[:70])
for m in re.finditer(r'"((?:[^"\\\n]|\\.)*)"', out):
    if re.search(r'[éèàçêôû]|\b(des|les|une|du|est)\b', m.group(1)): print("LEFT:", m.group(1)[:80])
open(sys.argv[2], "w").write(out)
