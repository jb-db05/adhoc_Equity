"""content.py: all text of the Tesla Q3 2026 Earnings update (HTML entities)."""

DOC_TYPE = "Earnings update"
THEME = ""   # no sector in the kicker
DATE = "22 October 2026"
TICKER = "TSLA"
TITLE = "Tesla Q3 2026: margins recover, the valuation still rides on AI"

STATUS = ("Tesla is on neither the Syz master list nor the focus list, and this update is not a "
          "recommendation to buy the share.")

QUOTE = ("We are in a huge investment cycle to set us up for the future. Therefore, as previously guided, operating "
         "expenses continue to increase sequentially.")
QUOTE_WHO = "Vaibhav Taneja, Chief Financial Officer, Q3 2026 earnings call, 21 October 2026"

TAKEAWAYS = [
    ("pos", "Beat", "Adjusted EPS of USD 0.48, 9% above consensus, on flat revenue; reported EPS was USD 0.22."),
    ("pos", "Margin", "Automotive gross margin excluding credits rose to 18.1% from 16.3%, 1.4 points above consensus."),
    ("neg", "Watch", "Operating expenses keep rising with AI and robotics spending; capex to expand beyond the 2026 level."),
    ("neu", "Valuation", "223.7x forward earnings, 64% above the 2020 to 2026 average: the price discounts autonomy and robots."),
]

KPIS = [
    ("Revenue", "USD 28.05bn", "In line with consensus", "neu"),
    ("Adjusted EPS", "USD 0.48", "+9.1% vs. consensus", "pos"),
    ("Auto gross margin excl. credits", "18.1%", "+140bp vs. consensus", "pos"),
    ("Free cash flow", "USD 1.53bn", "Capex guide about USD 20bn", "neu"),
]

H_P1 = "Margins buy time for the AI investment cycle"
P1 = ("The quarter was better than feared on profitability. The automotive gross margin recovered, energy and services "
      "margins rose, and free cash flow stayed positive despite heavy spending. Revenue, however, was flat and reported "
      "net income fell 43%, as research and development for autonomy, Optimus and chips keeps lifting operating "
      "expenses. The core business is stabilising, but it does not yet carry a valuation built on robotaxis and "
      "humanoid robots.")

C1_TITLE = "TSLA: automotive gross margin excluding regulatory credits"
C1_SUB = ("% of automotive revenue &middot; Q2 2026 reported, Q3 2026 pre-results consensus and Q3 2026 reported")
C1_COMMENT = ("The margin recovery is the main positive surprise. At 18.1%, the automotive gross margin excluding "
              "regulatory credits is 1.8 points above Q2 and 1.4 points above consensus, helped by a higher share of "
              "deliveries in Asia-Pacific. Management flags rising commodity costs and interest rates as continuing "
              "headwinds, so we read the gain as mix, not as a new run-rate.")

BASE_CASE = ("Our stance on Tesla is neutral and cautious: USD 1.53bn of free cash flow and over USD 45bn of "
             "cash fund the build-out, but do not justify the multiple. The car business is stabilising, with the "
             "highest order backlog in four years, but the earnings base remains thin: 12-month forward consensus EPS "
             "is only USD 1.73. The valuation rests on autonomy, Optimus and the Terafab chip project, none yet "
             "generating revenue at scale, while capex will keep rising. Results move the share sharply: it fell 14.5% "
             "after the July print. The next tests are EU approval of Full Self-Driving and Cybercab launches beyond "
             "Austin.")
UPSIDE = ("EU-wide approval of supervised Full Self-Driving by the first quarter of 2027. Cybercab launches in other "
          "cities before year-end, with the cost per paid mile approaching the USD 0.30 target. External Optimus "
          "deliveries around the end of 2027, as planned.")
DOWNSIDE = ("The automotive margin falling back below 17% as the Asia mix normalises. Capex and Terafab spending "
            "drawing on the new USD 30bn credit lines. Robotaxi miles failing to turn into revenue in 2027. A SpaceX "
            "combination on terms unfavourable to Tesla shareholders.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: margins up, revenue and profit down"
A1 = [
    ("Revenue was USD 28.05bn, essentially flat on a year earlier, as automotive revenue fell 3% to USD 20.6bn. "
     "Deliveries of 486,532 vehicles were 2% lower, but this was the second consecutive quarter above 480,000 and "
     "Tesla ended the quarter with its highest backlog in four years, with deliveries limited by production. Full "
     "Self-Driving is the main demand driver: over 75% of North American buyers took a paid subscription at delivery, "
     "and the paid base passed 1.7 million customers. Energy storage deployments reached 13.7 GWh, the second-best "
     "quarter, with Megapacks for 2027 almost sold out, and services and other margins hit a record 15.9%."),
    ("Energy gross margin jumped to 33.1% from 20.4%, but mostly on tariff refunds and warranty adjustments, which we "
     "treat as one-offs. Operating expenses rose again on AI compute, chip development and pre-production costs for "
     "Optimus, Megapack 3 and the Semi, and management expects them to keep rising until these products are "
     "commercialised. Reported net income fell 43% to USD 787m, or USD 0.22 per share, including a USD 142m loss on "
     "the SpaceX stake and a USD 290m Bitcoin gain. Free cash flow was USD 1.53bn and cash and investments exceed "
     "USD 45bn."),
]
H_A2 = "Outlook: capex rises, robotaxis scale in 2027"
A2 = [
    ("Capex guidance for 2026 was revised to about USD 20bn, funded mainly from operating cash flow, but management "
     "expects capex to keep expanding for several years with the robotaxi fleet, Optimus, solar, compute and a chip "
     "fab. Tesla secured USD 30bn of credit lines, undrawn this year. The Terafab "
     "will need tens of billions of dollars by early 2028 and over USD 100bn in the long run, shared with SpaceX "
     "in proportions still open. The CFO expects robotaxis to become a significant part of revenue and profit "
     "in 2027, and external Optimus deliveries are targeted around the end of 2027. A potential SpaceX merger was not "
     "discussed."),
]
H_C2 = "Valuation: the price runs ahead of earnings"
C2_TITLE = "TSLA: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, January 2020 to 21 October 2026 (window starts when 12m-forward consensus EPS turns positive) "
          "&middot; last price is the 21 October close, before the release &middot; 40-week moving average &middot; "
          "log scale &middot; P/E vs. its average since 2020")
C2_COMMENT = ("At USD 386.5, before the release, Tesla trades on 223.7x 12-month forward consensus earnings, 64% above "
              "its 136.6x average since 2020 and close to its one-year average of 218.5x. Over 12 months the share "
              "fell 13.9% while forward earnings rose 3.0%, but since the July results the price has rebounded 20.9% "
              "as forward earnings slipped 4.8%. The share sits just above its 40-week average of USD 383.6. At an "
              "unchanged price, consensus earnings would have to rise 64% to bring the multiple back to its 2020 to "
              "2026 average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, Tesla Q3 2026 update and earnings call transcript of 21 October 2026, "
               "press reports")
