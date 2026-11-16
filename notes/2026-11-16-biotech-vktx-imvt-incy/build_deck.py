import copy, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
SPACE, BLUE, TIGER, MANGO, GOLD, MINT, GREY, LINE = (RGBColor.from_string(c) for c in
    ("202945", "4B5F80", "FF6C0E", "FFA400", "FFC545", "3BAF90", "7A8494", "D9D9D9"))
FONT = "Open Sans"
DATE = "16 novembre 2026"

prs = Presentation(SRC)
layout = next(l for l in prs.slide_layouts if l.name == "One Content")
old_ids = list(prs.slides._sldIdLst)
cover_id, disc_id, final_id = old_ids[0], old_ids[14], old_ids[15]

# ---------- helpers ----------
def run(p, text, size=11, bold=False, color=SPACE, italic=False):
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = FONT; f.color.rgb = color
    return r

def textbox(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, name=None, margin=0):
    """paras: list of (runs, opts); runs = list of (text, size, bold, color)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name: tb.name = name
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
    first = True
    for runs, opts in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.alignment = opts.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(opts.get("after", 4))
        p.line_spacing = opts.get("ls", 1.05)
        for t in runs:
            run(p, *t)
    return tb

def P(text, size=10.5, bold=False, color=SPACE, after=4, align=PP_ALIGN.LEFT):
    return ([(text, size, bold, color)], {"after": after, "align": align})

def new_slide(title, subtitle):
    s = prs.slides.add_slide(layout)
    for ph in list(s.placeholders):
        idx = ph.placeholder_format.idx
        if idx == 0: ph.text_frame.text = title
        elif idx == 14: ph.text_frame.text = subtitle
        else: ph._element.getparent().remove(ph._element)
    for ph in s.placeholders:
        for p in ph.text_frame.paragraphs:
            for r in p.runs: r.font.name = FONT
    return s

def box(slide, x, y, w, h, name=None, line=SPACE, width=1.25):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.08
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(255, 255, 255)
    sh.line.color.rgb = line; sh.line.width = Pt(width)
    sh.shadow.inherit = False
    if name: sh.name = name
    sh.text_frame.text = ""
    return sh

def rect(slide, x, y, w, h, color, name=None, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background(); sh.shadow.inherit = False
    if name: sh.name = name
    return sh

def set_border(cell, side, color, w):
    tcPr = cell._tc.get_or_add_tcPr()
    tag = {"L": "a:lnL", "R": "a:lnR", "T": "a:lnT", "B": "a:lnB"}[side]
    for e in tcPr.findall(qn(tag)): tcPr.remove(e)
    ln = etree.SubElement(tcPr, qn(tag), w=str(int(w)))
    if color is None:
        etree.SubElement(ln, qn("a:noFill"))
    else:
        sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr"), val=str(color))
    # schema order: lnL lnR lnT lnB ... fill
    order = [qn(t) for t in ("a:lnL", "a:lnR", "a:lnT", "a:lnB")]
    lns = sorted([e for e in tcPr if e.tag in order], key=lambda e: order.index(e.tag))
    others = [e for e in tcPr if e.tag not in order]
    for e in list(tcPr): tcPr.remove(e)
    for e in lns + others: tcPr.append(e)

def table(slide, x, y, w, col_w, rows, size=10, header_size=10, row_h=0.3, first_col_bold=True,
          align_right_from=1, name=None, colors=None):
    nr, nc = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    if name: gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for a in ("bandRow", "firstRow"): tblPr.set(a, "0")
    st = tblPr.find(qn("a:tableStyleId"))
    if st is not None: tblPr.remove(st)
    for i, cw in enumerate(col_w): tbl.columns[i].width = Inches(cw)
    for r in range(nr):
        tbl.rows[r].height = Inches(row_h)
        for c in range(nc):
            cell = tbl.cell(r, c)
            cell.fill.background()
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if (c >= align_right_from) else PP_ALIGN.LEFT
            val = rows[r][c]
            if r == 0:
                run(p, val, header_size, True, GREY)
            else:
                col = SPACE
                if colors and (r, c) in colors: col = colors[(r, c)]
                run(p, val, size, bold=(c == 0 and first_col_bold) or bool(colors and (r, c) in colors), color=col)
            for side in "LRT": set_border(cell, side, None, 0)
            if r == 0 or r == nr - 1: set_border(cell, "B", "202945", 9525)
            else: set_border(cell, "B", "D9D9D9", 6350)
    return gf

def source(slide, text, y=7.38):
    textbox(slide, 0.73, y, 10.28, 0.3, [P(text, 8, color=BLUE)], name="Source")

def section_col(slide, x, y, w, h, blocks, size=10, name=None):
    paras = []
    for head, body in blocks:
        paras.append(P(head, size + 0.5, True, TIGER, after=2))
        paras.append(P(body, size, after=9))
    return textbox(slide, x, y, w, h, paras, name=name)

def kpis(slide, items, y=2.5, h=0.85):
    x0, W, gap = 0.73, 10.28, 0.18
    w = (W - gap * (len(items) - 1)) / len(items)
    for i, (label, value, note, vcol) in enumerate(items):
        x = x0 + i * (w + gap)
        box(slide, x, y, w, h, name=f"KPI {i+1}")
        textbox(slide, x + 0.15, y + 0.08, w - 0.3, h - 0.16, [
            P(label, 9, True, BLUE, after=1),
            ([(value, 17, True, vcol)], {"after": 0}),
            P(note, 8, color=BLUE, after=0)], anchor=MSO_ANCHOR.MIDDLE)

def conclusion(slide, text, y=6.62, h=0.7):
    box(slide, 0.73, y, 10.28, h, name="Conclusion box")
    textbox(slide, 0.93, y + 0.06, 9.9, h - 0.12, [
        ([("Conclusion  ", 10.5, True, TIGER), (text, 10.5, False, SPACE)], {"after": 0})],
        anchor=MSO_ANCHOR.MIDDLE, name="Conclusion")

# ---------- cover ----------
cover = prs.slides[0]
for ph in cover.placeholders:
    idx = ph.placeholder_format.idx
    if idx == 0:
        r = ph.text_frame.paragraphs[0].runs
        r[0].text = "Biotech US : lecture fondamentale de VKTX, IMVT et INCY"
        for x in r[1:]: x.text = ""
    elif idx == 13:
        r = ph.text_frame.paragraphs[0].runs
        r[0].text = DATE + " · Syz Research"
        for x in r[1:]: x.text = ""

# ---------- 2. synthèse ----------
s = new_slide("INCY en cœur de portefeuille, IMVT en satellite, VKTX en spéculatif",
              "Synthèse fondamentale · classement par niveau de risque · " + DATE)
cards = [("INCY · Cœur de portefeuille", "Incyte · rentable, 2028 à franchir", BLUE),
         ("IMVT · Satellite", "Immunovant · pré-revenus, plateforme validée", TIGER),
         ("VKTX · Spéculatif", "Viking · un actif, un résultat binaire en 2027", GOLD)]
for i, (t, sub, col) in enumerate(cards):
    x = 0.73 + i * 3.49
    rect(s, x, 2.5, 0.06, 0.95, col, name=f"Accent {i+1}")
    textbox(s, x + 0.2, 2.5, 3.1, 0.95, [P(t, 15, True, after=4), P(sub, 9, color=BLUE, after=0)],
            anchor=MSO_ANCHOR.MIDDLE, name=f"Card {i+1}")
table(s, 0.73, 3.7, 10.28, [2.0, 2.76, 2.76, 2.76], [
    ["", "INCY", "IMVT", "VKTX"],
    ["Profil", "Rentable, ventes 2026 ≈ 5,2–5,3 Md USD", "Pas de revenu, IMVT-1402 en essais pivots", "Pas de revenu, VK2735 en phase 3"],
    ["Ce qui est dans le prix", "Le choc Jakafi 2028", "Le succès dans plusieurs indications", "Beaucoup de doute"],
    ["Prochain test", "Pipeline mutCALR, guidance 2027", "Graves et myasthénie, 2027", "VANQUISH, 2S 2027"],
    ["Risque principal", "Trou de revenus après 2028", "Concurrence FcRn, flottant étroit", "Résultat, financement, prix"],
    ["Rôle possible", "Position cœur", "Position satellite", "Petite position spéculative"],
], size=10, row_h=0.5, align_right_from=99, name="Synthesis table")
source(s, "Source : Syz Research, Bloomberg, publications des sociétés (T3 2026).")

# ---------- 3. chiffres clés ----------
s = new_slide("Chiffres clés fondamentaux",
              "En USD · cours au 13 novembre 2026, capitalisations au 16 novembre 2026, bilans au 30 septembre 2026")
table(s, 0.73, 2.5, 10.28, [4.0, 2.09, 2.09, 2.1], [
    ["", "INCY", "IMVT", "VKTX"],
    ["Cours (13.11.2026)", "120,12", "34,09", "26,96"],
    ["Capitalisation (16.11.2026)", "24,7 Md", "7,1 Md", "3,7 Md"],
    ["Trésorerie et placements CT (30.09.2026)", "3,9 Md *", "722 M", "960 M"],
    ["Valeur d'entreprise (calcul Syz)", "20,8 Md", "6,4 Md", "2,8 Md"],
    ["Chiffre d'affaires 2025", "5,14 Md", "–", "–"],
    ["Ventes nettes 2026 (guidance relevée)", "5,21–5,30 Md", "–", "–"],
    ["VE / ventes nettes 2026 (calcul Syz)", "≈ 4x", "–", "–"],
    ["Résultat T3 2026", "Perte GAAP (charge Vega 1,23 Md)", "Perte", "−183 M"],
    ["Couverture de trésorerie (calcul Syz)", "Autofinancé", "Jusqu'au lancement Graves", "≈ 5 trimestres"],
    ["Principal catalyseur", "Pipeline 2027–2028", "Données 2027", "VANQUISH 2S 2027"],
], size=10.5, row_h=0.4, align_right_from=1, name="Key figures table",
   colors={(8, 3): TIGER, (9, 3): TIGER})
source(s, "VE = capitalisation moins trésorerie et placements CT, dette non déduite. Couverture VKTX = trésorerie / perte nette T3. "
          "* Trésorerie INCY à confirmer après le paiement de Vega. Source : Syz Research, Bloomberg, publications des sociétés.", y=7.15)

# ---------- 4. calendrier ----------
s = new_slide("Les catalyseurs s'étalent de fin 2026 à 2028",
              "Calendrier communiqué par les sociétés · les échéances d'options doivent couvrir la bonne fenêtre")
X0, X1, M = 2.45, 10.95, 26.0           # Nov 2026 -> Dec 2028
xm = lambda m: X0 + (X1 - X0) * m / M
top, lane_h = 2.75, 1.42
for m, lab in ((2, "2027"), (14, "2028")):
    ln = s.shapes.add_connector(1, Inches(xm(m)), Inches(top - 0.05), Inches(xm(m)), Inches(top + 3 * lane_h - 0.1))
    ln.line.color.rgb = LINE; ln.line.width = Pt(0.75)
    textbox(s, xm(m) + 0.05, top - 0.3, 0.75 if m == 0 else 1.2, 0.25, [P(lab, 9, True, GREY, after=0)])
lanes = [("INCY", BLUE, [(0.5, 2, 0, "Phase 3 mutCALR en myélofibrose (lancement)"),
                         (2.5, 4, 1, "Guidance 2027"),
                         (14, 26, 0, "Phase 3 KRAS G12D, cancer du pancréas"),
                         (14, 26, 1, "Perte d'exclusivité Jakafi aux États-Unis")]),
         ("IMVT", TIGER, [(0.5, 2, 0, "Réunion FDA fin de phase 2 (polyarthrite)"),
                          (2, 14, 1, "Données pivots Graves et myasthénie"),
                          (14, 26, 0, "Données pivots CIDP")]),
         ("VKTX", GOLD, [(2, 5, 0, "VK3019 : étude de doses (T1)"),
                         (2, 14, 1, "Maintenance, partie 2"),
                         (8, 14, 0, "VANQUISH-1 et -2 (2S)"),
                         (14, 26, 1, "SUNRISE, version orale")])]
for li, (tick, col, evs) in enumerate(lanes):
    y = top + li * lane_h
    textbox(s, 0.73, y + 0.25, 1.5, 0.5, [P(tick, 15, True, after=0)], anchor=MSO_ANCHOR.MIDDLE)
    if li:
        ln = s.shapes.add_connector(1, Inches(0.73), Inches(y - 0.08), Inches(X1), Inches(y - 0.08))
        ln.line.color.rgb = LINE; ln.line.width = Pt(0.75)
    for (a, b, row, lab) in evs:
        yy = y + 0.12 + row * 0.62
        textbox(s, xm(a), yy, max(xm(b) - xm(a), 3.6), 0.26, [P(lab, 9.5, color=SPACE, after=0)])
        rect(s, xm(a), yy + 0.29, xm(b) - xm(a), 0.13, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
source(s, "Dates indicatives communiquées par les sociétés (T3 2026) ; les dates exactes des résultats ne sont pas publiées. Source : Syz Research, publications des sociétés.", y=7.15)

# ---------- 5-7. fiches ----------
def fiche(title, sub, kp, left, right, concl):
    s = new_slide(title, sub)
    kpis(s, kp)
    section_col(s, 0.73, 3.55, 4.98, 3.0, left, size=11)
    section_col(s, 6.03, 3.55, 4.98, 3.0, right, size=11)
    conclusion(s, concl)
    source(s, "Source : Syz Research, Bloomberg, publications de la société. Les calculs Syz sont indiqués comme tels.", y=7.38)
    return s

fiche("Incyte : un leader rentable qui doit remplacer Jakafi d'ici 2028",
      "Incyte (INCY) · hématologie, oncologie, dermatologie",
      [("Capitalisation", "24,7 Md USD", "16 novembre 2026", SPACE),
       ("Ventes nettes 2026", "5,21–5,30 Md", "Guidance relevée au T3", SPACE),
       ("Jakafi, T3 2026", "827 M USD", "+4 % sur un an", SPACE),
       ("VE / ventes 2026", "≈ 4x", "Calcul Syz", SPACE)],
      [("Pourquoi le titre pourrait progresser",
        "Le chiffre d'affaires du T3 a progressé de 14 % à 1,56 Md USD et Opzelura de 36 % à 255 M USD. "
        "Hors Jakafi, l'activité représente déjà plus d'un tiers des ventes. Jakafi XR, la version à prise unique, "
        "commence à contribuer."),
       ("Le vrai levier : le pipeline",
        "L'anticorps anti-mutCALR (INCA033989) est en étude pivot dans la thrombocytémie essentielle, avec une phase 3 "
        "en myélofibrose fin 2026. L'inhibiteur KRAS G12D vise des données de phase 3 dans le pancréas en 2028. "
        "L'achat de Vega (1,25 Md USD) ajoute un actif dans la maladie de von Willebrand.")],
      [("Le titre est-il bon marché ?",
        "Environ 4 fois les ventes 2026 (calcul Syz), un multiple modeste pour une biotech rentable. La décote reflète "
        "le risque 2028 : Jakafi pèse encore près de 60 % des ventes nettes."),
       ("Risques principaux",
        "Trou de revenus entre 2028 et l'arrivée des nouveaux produits, échec dans les programmes mutCALR ou KRAS, "
        "pression sur les prix (négociation Medicare), acquisitions trop chères. Le T3 est une perte GAAP à cause "
        "de la charge Vega."),
       ("À surveiller", "Lancement de la phase 3 en myélofibrose, données mutCALR, adoption de Jakafi XR, guidance 2027.")],
      "Le plus défensif des trois. Les profits laissent le temps de franchir 2028 et la valorisation intègre déjà une "
      "bonne partie du risque. Peut servir de position cœur.")

fiche("Immunovant : une plateforme FcRn en partie validée",
      "Immunovant (IMVT) · anti-FcRn IMVT-1402 · contrôlée à ~56 % par Roivant",
      [("Capitalisation", "7,1 Md USD", "16 novembre 2026", SPACE),
       ("Trésorerie", "722 M USD", "30 septembre 2026", SPACE),
       ("Valeur d'entreprise", "6,4 Md USD", "Calcul Syz", SPACE),
       ("Prochaines données", "2027", "Graves, myasthénie", SPACE)],
      [("Pourquoi le titre pourrait progresser",
        "En novembre, la dose de 600 mg a atteint son critère principal dans la polyarthrite rhumatoïde difficile à "
        "traiter : 92,5 % des patients ont conservé leur réponse ACR20 à la semaine 28, contre 75,6 % sous placebo. "
        "C'est le premier signe qu'un anti-FcRn peut fonctionner dans une maladie fréquente."),
       ("Ce qui le distingue",
        "IMVT-1402 vise une baisse profonde des IgG sans les effets sur l'albumine et le LDL des produits de première "
        "génération. Dans la maladie de Graves, aucun anti-FcRn n'est approuvé : une première possible.")],
      [("Le titre est-il bon marché ?",
        "Non sur les mesures classiques : 6,4 Md USD de VE sans revenu supposent déjà des succès dans plusieurs "
        "indications. La trésorerie doit couvrir les besoins jusqu'à un lancement dans Graves."),
       ("Risques principaux",
        "Concurrence de produits FcRn déjà commercialisés par de grands groupes. Résultat obtenu sur une seule dose, "
        "avec un placebo élevé, et une deuxième étude pivot nécessaire. Abandon du lupus cutané, Sjögren peu probable. "
        "Flottant étroit."),
       ("À surveiller", "Issue de la réunion FDA fin 2026, design de la prochaine étude, données 2027.")],
      "La société est passée de la promesse à une plateforme en partie validée, mais une bonne partie des bonnes "
      "nouvelles est dans le prix. Convient à une position satellite.")

fiche("Viking : un candidat sérieux dans l'obésité, un test binaire en 2027",
      "Viking Therapeutics (VKTX) · VK2735, double agoniste GLP-1/GIP",
      [("Capitalisation", "3,7 Md USD", "16 novembre 2026", SPACE),
       ("Trésorerie", "960 M USD", "30 septembre 2026", SPACE),
       ("Perte nette T3 2026", "−183 M USD", "Aucun revenu", TIGER),
       ("Données phase 3", "2S 2027", "VANQUISH-1 et -2", SPACE)],
      [("Pourquoi le titre pourrait progresser",
        "Deux phases 3 entièrement recrutées (environ 4 500 et 1 000 patients) et une version orale entrée en phase 3 "
        "(SUNRISE) en octobre, données en 2028. Un résultat positif ferait de Viking l'un des rares indépendants "
        "avec un double agoniste avancé, injectable et oral."),
       ("Ce qui le distingue",
        "En phase 2, les patients passés à une injection toutes les deux semaines ou mensuelle ont conservé 82 à 97 % "
        "de leur perte de poids. Le programme amyline VK3019 ajoute un second mécanisme.")],
      [("Bon marché, ou piège ?",
        "Une VE d'environ 2,8 Md USD (calcul Syz) paraît faible face au marché de l'obésité, mais le doute est "
        "rationnel : Viking arriverait des années après les deux leaders, dans un marché où les prix baissent."),
       ("Risques principaux",
        "Le résultat lui-même, y compris la tolérance et les abandons. Le financement : environ 5 trimestres de "
        "trésorerie au rythme du T3 (calcul Syz), soit jusqu'aux données ; une levée ou un partenariat serait "
        "très probablement nécessaire. Pas de force de vente."),
       ("À surveiller", "Maintenance partie 2, VK3019, partenariat éventuel, puis VANQUISH au 2S 2027.")],
      "Le potentiel le plus élevé des trois, mais le risque le plus concentré : un actif, une fenêtre de résultats, "
      "un besoin de financement. Petite position spéculative uniquement, pas sur le seul espoir d'un rachat.")

# ---------- 8. lien vers la proposition ----------
s = new_slide("Du fondamental à la proposition : aligner horizon et échéance",
              "Pistes à faire coter par le desk · prix théoriques indicatifs au 13 novembre 2026")
table(s, 0.73, 2.5, 10.28, [0.85, 1.45, 1.6, 3.2, 3.18], [
    ["", "Vue", "Fenêtre clé", "Piste (indicative)", "Point d'attention"],
    ["INCY", "Cœur", "Guidance 2027, mutCALR",
     "Détenteur : collar juin 2027, vente CALL 140 / achat PUT 105, coût ≈ nul. Nouvel investisseur : vente PUT mars 2027 strike 110, prime ≈ 8 USD",
     "Volatilité implicite de ~49 % élevée pour Incyte : à vérifier avant de fixer les strikes"],
    ["IMVT", "Satellite", "Réunion FDA fin 2026, données 2027",
     "Vente PUT mars 2027 strike 30, prime ≈ 2,7 USD (entrée effective ≈ 27,3). Ou call spread déc. 2027 35/50, coût ≈ 4 USD pour un gain maximal de 15",
     "Le client doit accepter de détenir le titre. Flottant étroit, short interest élevé : mouvements brutaux"],
    ["VKTX", "Spéculatif", "VANQUISH, 2S 2027",
     "Pas de structure à ce stade. Si le client insiste : call spread janv. 2028 30/50, coût ≈ 4 USD pour un gain maximal de 20",
     "Un glissement des données au-delà de janv. 2028 ferait expirer l'option avant le résultat"],
], size=9.5, header_size=10, row_h=1.0, align_right_from=99, name="Proposal table")
box(s, 0.73, 6.35, 10.28, 0.85, name="Avoid box")
textbox(s, 0.93, 6.4, 9.9, 0.75, [
    ([("À éviter  ", 10.5, True, TIGER),
      ("un produit structuré « worst-of » sur les trois titres. Le coupon serait élevé, mais avec des volatilités de 50 à 70 % "
       "et deux résultats binaires, la probabilité de toucher la barrière est forte. Dans tous les cas, limiter la taille "
       "des positions IMVT et VKTX.", 10, False, SPACE)], {"after": 0})], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Prix théoriques Black-Scholes calculés par Syz à partir des cours et volatilités implicites du 13.11.2026 (taux 3,75 %), "
          "hors frais et écarts de cotation. Non contractuels : cotation du desk requise.", y=7.3)

# ---------- 9. points à vérifier ----------
s = new_slide("Avant diffusion au client : points à fiabiliser",
              "Note interne · à traiter avant de finaliser la proposition")
cols = [("Données", [
            "Mettre tous les 13F au 30.09.2026 (date limite 14.11) : Farallon +275 % date du 30.06, avant les données.",
            "Fidelity +55 % sur VKTX : probablement une souscription à la levée de 500 M USD du 24.09, pas des achats en bourse.",
            "Ratios hausses / baisses 60 j quasi identiques (0,69 / 0,69 / 0,68) et short interest identique sur VKTX et IMVT (19,9 %) : à recontrôler.",
            "Remplacer Yahoo Finance par Bloomberg (OMON, HDS, SI)."]),
        ("Lecture", [
            "Le ratio 2,43 d'IMVT vient surtout de la séance du 09.11 (+15 %, volume ×2,6) : réaction aux données plutôt qu'accumulation.",
            "L'open interest ne dit pas qui achète : les CALL déc. 2027 50 d'IMVT peuvent être des ventes couvertes.",
            "Les CALL VKTX 50, 60 et 120 sont des reliquats, sans valeur de signal.",
            "INCY : « 2 phases 3 d'ici fin 2026 » sont des lancements d'études, pas des résultats."]),
        ("Charte Syz", [
            "Retirer les objectifs moyens des analystes.",
            "Ne pas conditionner une entrée à un seul niveau technique (« zone 30–31 »).",
            "Présenter la levée VKTX comme une dilution, pas comme un catalyseur.",
            "Parler d'« un investisseur », jamais de prix d'entrée ni de perte latente."])]
for i, (head, items) in enumerate(cols):
    x = 0.73 + i * 3.49
    box(s, x, 2.5, 3.3, 4.7, name=f"Check {head}")
    paras = [P(head, 14, True, TIGER, after=10)] + [P(t, 11, after=10) for t in items]
    textbox(s, x + 0.18, 2.62, 2.94, 4.5, paras)

# ---------- reorder ----------
lst = prs.slides._sldIdLst
new_ids = list(lst)[16:]
for e in list(lst): lst.remove(e)
for e in [cover_id] + new_ids + [disc_id, final_id]: lst.append(e)
prs.save(OUT)
print("slides:", len(lst))
