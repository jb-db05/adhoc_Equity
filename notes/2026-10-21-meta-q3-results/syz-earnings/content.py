"""content.py: all text of the Meta Q3 2026 Earnings update (HTML entities)."""

DOC_TYPE = "Earnings update"
THEME = ""   # no sector in the kicker (author's request)
DATE = "22 October 2026"
TITLE = "Meta Q3 2026: the ads deliver, the 2027 bill waits"

QUOTE = ("The benefits our AI investments are delivering to the core business, combined with emerging "
         "opportunities from model advances and product launches, position us to sustain strong overall "
         "revenue growth throughout 2027.")
QUOTE_WHO = "Susan Li, Chief Financial Officer, Q3 2026 earnings call, 21 October 2026"

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 64.6bn, 2% above consensus and the top of guidance, on a 14% higher price per ad."),
    ("pos", "Muse", "Over 10 million Muse users in six weeks; a quarter of them are active on any given day."),
    ("neg", "Watch", "Free cash flow of USD &minus;2.1bn as capex reached USD 34.9bn; no 2027 capex figure until January."),
    ("neu", "Valuation", "21.3x forward earnings, close to the 22.4x average since 2016: the rally since July is all multiple."),
]

KPIS = [
    ("Revenue", "USD 64.6bn", "+2.0% vs. consensus", "pos"),
    ("EPS excl. legal charge", "USD 7.40", "+13.1% vs. consensus", "pos"),
    ("Q4 revenue guide", "USD 73&ndash;76bn", "Mid-point +1.2% vs. consensus", "pos"),
    ("Free cash flow", "USD &minus;2.1bn", "Capex USD 34.9bn", "neg"),
]

H_P1 = "The core business is funding the AI build-out"
P1 = ("The quarter answered two of the three questions we set before the print. Advertising delivered, with "
      "operating income 13% above consensus once the USD 9.9bn legal charge is excluded, and Muse, Meta&rsquo;s "
      "new personal AI agent, came with usage data rather than downloads alone. The third question, the size of "
      "the 2027 investment bill, is deferred to the Q4 results in January, while free cash flow turned negative "
      "this quarter.")

C1_TITLE = "META: Q3 2026 results vs. consensus"
C1_SUB = ("Surprise vs. FactSet pre-results consensus, % &middot; operating income and EPS exclude the USD 9.9bn "
          "legal charge &middot; Q4 guide at the mid-point")
C1_COMMENT = ("The beat came from profitability more than from sales. Revenue was 2% above consensus, but operating "
              "income and earnings per share, both excluding the legal charge, beat by 13%, helped by a 14% rise in "
              "the price per ad while headcount fell 12% from Q2. The Q4 revenue guide brackets consensus, with the "
              "mid-point 1.2% above.")

BASE_CASE = ("We stay constructive on Meta over the long term. The share is on the Syz master list but not on the "
             "focus list, and this update is not a recommendation to buy it. We underwrite an advertising-led earnings path: "
             "management expects strong revenue growth throughout 2027 and Reality Labs losses to "
             "narrow to about USD 15bn. The debate is now the cost of the AI build-out, as the "
             "reaction showed: after a 19% rise since July, the share spiked by "
             "about 7% after hours, then gave back most of the gain once management said Muse&rsquo;s "
             "serving costs would rise. The next test is the 2027 guidance in late January.")
UPSIDE = ("Consensus 12-month forward earnings rising again after a 10% cut since July. A 2027 capex guide in January "
          "that operating cash flow can fund. First Muse revenue, retention and cost-per-user figures, and traction "
          "for the paid tier, the API and Muse Code.")
DOWNSIDE = ("Capex guided well above the USD 135&ndash;145bn of 2026 without matching revenue. Ad impression growth "
            "slowing below 10%. Use of the new non-voting share to raise equity. Adverse rulings in the US "
            "youth-related trials scheduled for the coming months.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: pricing carried a clean beat"
A1 = [
    ("Family of Apps revenue reached USD 64.2bn, up 26%, with advertising at USD 63.1bn, also up 26% at constant "
     "currency. Ad impressions grew 10%, and the average price per ad rose "
     "14% on better ad performance and an easier macro backdrop. Daily active people reached 3.64bn. "
     "Other Family of Apps revenue grew 59% to USD 1.1bn on WhatsApp paid messaging and subscriptions, and Meta One, "
     "the new subscription bundle, passed 15 million subscriptions and trials. Reality Labs revenue fell 6% to "
     "USD 443m as lower Quest sales offset growth in AI glasses."),
    ("Total expenses rose 68% to USD 51.6bn, including the USD 9.9bn charge for the August settlement with US state "
     "attorneys general; the rest came from infrastructure and third-party AI token costs. Headcount fell 12% from Q2 to about 66,000. Reported operating income dropped 37% to USD 13.0bn, a 20% "
     "margin; excluding the charge it rose 11% to USD 22.9bn, a margin of about 35% against 40% a year ago. Capex of "
     "USD 34.9bn left free cash flow negative at USD 2.1bn, and debt of USD 83.7bn now slightly exceeds cash and "
     "marketable securities of USD 82.4bn."),
]
H_A2 = "Outlook: 2027 waits for January, Muse for scale"
A2 = [
    ("The Q4 revenue guide of USD 73&ndash;76bn compares with FactSet consensus "
     "of USD 73.65bn. Full-year 2026 expenses of USD 175&ndash;179bn are the previous range plus the legal charge, "
     "and the 2026 capex range was narrowed to USD 135&ndash;145bn. For 2027, management "
     "expects to keep investing aggressively but gives no figure before the Q4 call. A new non-voting share, "
     "distributed one for one from late January, widens funding options; no financing is planned."),
    ("Muse is where the 2027 bill and the upside meet. Over a quarter of weekly users shop through it, with an "
     "average purchase above USD 200, and Muse Wonder, in the paid tier, lifts "
     "retention. Most users would stay free, with businesses paying a fee on "
     "transactions, while subscriptions cover advanced models and business use. Its US users already "
     "bring several hundred dollars a year each in app revenue, and Meta expects Muse to reach a higher "
     "level through commerce. Serving costs will rise as capacity is built for over 1 billion users; "
     "Meta targets a more than tenfold efficiency gain next year but gives no cost per user."),
]
H_C2 = "Valuation: the rally since July is all multiple"
C2_TITLE = "META: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, May 2012 to 21 October 2026 &middot; last price is the 21 October close, before the release "
          "&middot; Bloomberg 12m-forward consensus EPS &middot; 40-week moving average &middot; log scale &middot; "
          "P/E vs. its average since 2016")
C2_COMMENT = ("At USD 697.5, 10% above its 40-week average, the share is 2.7% lower than a year ago while forward consensus earnings fell "
              "5.3%. Since July the gap is wider: the price is up 19.1% and forward earnings are down "
              "10.4%, taking the multiple from 16.1x to 21.3x. That is 4.8% below the 22.4x average since 2016, but "
              "above the one-year average of 19.2x and the 14.9x low of June 2026. A 10% earnings upgrade at an unchanged price would bring the multiple back "
              "to 19.4x, its one-year average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, FactSet, Meta Platforms Q3 2026 earnings release and call "
               "transcript of 21 October 2026")
