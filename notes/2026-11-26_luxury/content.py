"""Content of the merged luxury ad-hoc opinion (LVMH and Hermès), 26 November 2026.

build.py turns this into one HTML file per page, the PDF and the PowerPoint.
"""

DATE = "26 November 2026"
LABEL = "Ad-hoc opinion · Luxury goods"
FOOTER = f"Syz Research · Ad-hoc opinion · {DATE}"
SRC = "Sources: Syz Research, Bloomberg, company data"

# ---------------------------------------------------------------- page 1
SECTOR = {
    "headline": "Luxury: a third slow year, a sector split in two",
    "sub1": f"{DATE} · Syz Research",
    "notice": (
        "Prices are as of 26 November 2026. Company figures come from the 2025 annual results, the 2026 "
        "half-year results and the third-quarter 2026 revenue releases of LVMH (12 October 2026) and Hermès "
        "(22 October 2026). Multiples, averages, relative performance and the dividend yield are Syz "
        "calculations from Bloomberg data. This note is not an investment recommendation."
    ),
    "kpis": [
        ("Chinese luxury market", "<span class='neg'>−3% to −5%</span>", "In 2025, after <span class='neg'>−17% to −19%</span> in 2024"),
        ("LVMH core division", "<span class='neg'>−5%</span>", "Fashion &amp; Leather Goods, Q3 organic"),
        ("Hermès Leather Goods", "<span class='pos'>+11%</span>", "Q3, at constant exchange rates"),
        ("Share prices in 2026", "<span class='neg'>−38% / −40%</span>", "LVMH / Hermès, year to date"),
    ],
    "h2": "Exclusivity holds, volume suffers",
    "left": [
        ("sub2", "A third year of slowdown"),
        ("p", "The luxury sector is in its third consecutive year of slowdown, and the gap between brands keeps "
              "widening. Jewellery and the most exclusive houses are holding up, while fashion and leather goods "
              "are suffering. The third quarter showed the split clearly: Hermès grew its Leather Goods by 11% on "
              "the back of waiting lists for the Birkin and the Kelly, while LVMH's Fashion &amp; Leather Goods, home "
              "to Louis Vuitton and Dior, fell 5%. At LVMH, jewellery, Sephora and spirits grew 6% to 8%, "
              "while at Hermès the categories sold in volume, such as ready-to-wear and watches, declined."),
        ("p", "Years of strong price increases explain part of the split. Aspirational buyers have moved to "
              "cheaper brands or to second-hand, and the customers who remain favour the rarest products."),
        ("sub2", "China no longer drives growth"),
        ("p", "The Chinese luxury market fell 3% to 5% in 2025, after a decline of 17% to 19% in 2024. In the third "
              "quarter, Asia excluding Japan declined at LVMH and was flat at Hermès. The American customer is now "
              "the last engine of the sector: LVMH grew 5% in the United States and Hermès 9% in the Americas, "
              "although the pace is slowing."),
    ],
    "right": [
        ("sub2", "No catalyst in the short term"),
        ("p", "Nothing points to a quick improvement. The fourth quarter could be difficult, with France suffering "
              "(Hermès grew 4% there in the third quarter, against 10% in the rest of Europe), the Middle East not "
              "recovering and no visible improvement in China. A strong euro also reduces the reported revenue "
              "of European groups."),
        ("sub2", "Valuations have reset"),
        ("p", "Share prices have adjusted faster than earnings. LVMH has lost 38% since the start of the year and "
              "trades on about 17 times expected earnings, against 20 to 25 times historically. Hermès has lost "
              "about 40% and trades on about 27 times, its lowest level since 2016. Both multiples are near "
              "ten-year lows, but analysts are still cutting their 2027 forecasts, so a low multiple alone does "
              "not mark the bottom."),
        ("sub2", "What this means for investors"),
        ("p", "In a split market, the strength of the franchise matters more than the cycle. Hermès remains on the "
              "right side of the split through its leather goods, while the core of LVMH is on the wrong side for "
              "now. Valuations already discount a lot, but with no short-term catalyst and estimates still "
              "falling, the full-year results of LVMH in late January 2027 and of Hermès in February 2027 are the "
              "next data points."),
    ],
}

# ---------------------------------------------------------------- page 2
LVMH = {
    "headline": "LVMH (MC FP)",
    "sub2": "The strongest portfolio in luxury at its lowest multiple in a decade, with its core still shrinking",
    "kpis": [
        ("Share price", "EUR 402.20", "<span class='neg'>−38%</span> year to date"),
        ("Forward P/E", "16.8x", "Historically 20x to 25x"),
        ("Dividend for 2025", "EUR 13.00", "3.2% trailing yield"),
        ("Net debt", "EUR 8.2bn", "30 June 2026"),
    ],
    "tech": [("Technical trend", "Negative, stabilising"), ("Support", "EUR 380"),
             ("Resistance", "EUR 416 / 456"), ("200-day average", "EUR 455.6")],
    "techline": ("The shares are back above their 40-day average (EUR 392.6) but far below a still-falling 200-day "
                 "average (EUR 455.6). A close above EUR 416, the early-November high, could signal a stabilisation; "
                 "EUR 380, near the October low, is the level to watch on the downside."),
    "left": [
        ("h3", "1. What the company does"),
        ("p", "LVMH is the world's largest luxury group, with about 75 houses in five divisions: Fashion &amp; Leather "
              "Goods (Louis Vuitton, Dior, Loro Piana, Celine), Perfumes &amp; Cosmetics, Watches &amp; Jewelry (Tiffany, "
              "Bulgari), Selective Retailing (Sephora) and Wines &amp; Spirits (Moët &amp; Chandon, Hennessy). Revenue "
              "was EUR 80.8bn in 2025."),
        ("h3", "2. Why it could do well"),
        ("p", "The other divisions are growing: in the third quarter Selective Retailing rose 8% and Wines &amp; Spirits "
              "6%, and Watches &amp; Jewelry grew 8% over nine months. The group also has levers of its own: creative renewal at Dior, newness at "
              "Louis Vuitton, cost discipline and a leaner portfolio, with Marc Jacobs sold in September and the "
              "stake in SirDavis whisky in July. Operating free cash flow reached EUR 11.3bn in 2025."),
        ("h3", "3. What sets it apart"),
        ("p", "Few groups own as many brands with pricing power, control their own stores and production, and can "
              "keep investing through a downturn. Net debt of EUR 8.2bn at the end of June was less than half of "
              "2025 operating profit, and control by the Arnault family gives the group a long-term horizon."),
    ],
    "right": [
        ("h3", "4. Cheap, or a value trap?"),
        ("p", "Valuation is the only reason for patience. At about 17 times expected earnings, against 20 to 25 times "
              "historically, the multiple is at its lowest in about ten years. Earnings are now the risk. Fashion "
              "&amp; Leather Goods, about 70% of group operating profit, fell 5% in the third quarter against about −2% "
              "expected, and management rules out price cuts and sees no shortcut back to growth. As long as organic "
              "growth does not recover, the margin will be hard to defend, and analysts keep lowering their 2027 "
              "forecasts."),
        ("h3", "5. Main risks"),
        ("p", "On the upside, a quick rebound if Louis Vuitton stabilises sooner than expected, as the shares are "
              "heavily oversold. On the downside, if the margin gives way, estimates would fall and the shares would no "
              "longer look so cheap. Also a longer slump in China, where the Molly Tea dispute hurt the brand; "
              "aspirational customers trading down; a strong euro and tariffs; succession (Bernard Arnault is 77)."),
        ("h3", "6. What to watch next"),
        ("p", "Full-year results in late January 2027, especially the Fashion &amp; Leather Goods margin; Chinese "
              "demand; the new Dior collections and newness at Louis Vuitton; revisions to 2027 estimates."),
    ],
    "conclusion": (
        "The core of LVMH is shrinking: Fashion &amp; Leather Goods fell 5% in the third quarter and group growth slowed "
        "to 1%, and Sephora, jewellery and spirits cannot make up for it. Valuation is the only reason to wait, with "
        "the multiple near a ten-year low and the shares down nearly 40% this year. The selling looks like "
        "capitulation, which is never a comfortable moment to sell, but a choice will have to be made at some point: "
        "without a return to organic growth, the margin and 2027 forecasts remain under pressure."
    ),
}

LVMH_CHARTS = [
    ("Chart 1", "MC FP: share price over two years",
     "Daily close with 40-day and 200-day simple moving averages, EUR; the dashed line marks the Q3 revenue release", "lvmh_chart1_price.png"),
    ("Chart 2", "MC FP against the Stoxx Europe 600 over five years",
     "Price performance over the last five years, rebased to 100, excluding dividends", "lvmh_chart2_stoxx.png"),
    ("Chart 3", "MC FP: forward P/E over ten years",
     "Price over consensus earnings for the next twelve months, ten-year average and one standard deviation "
     "either side", "lvmh_chart3_pe.png"),
]

# ---------------------------------------------------------------- page 4
RMS = {
    "headline": "Hermès International (RMS FP)",
    "sub2": "Still the best house in leather goods, at its lowest multiple since 2016 but dear against the sector",
    "kpis": [
        ("Share price", "EUR 1,277", "<span class='neg'>−40%</span> year to date"),
        ("Forward P/E", "26.8x", "Lowest since 2016"),
        ("Q3 revenue growth", "+4.3%", "Constant rates, vs. 5% expected"),
        ("Leather Goods, Q3", "<span class='pos'>+11%</span>", "Nearly half of revenue"),
    ],
    "tech": [("Technical trend", "Bearish"), ("Support", "EUR 1,225.5"),
             ("Resistance", "EUR 1,357 / 1,578"), ("200-day average", "EUR 1,578")],
    "techline": ("The share price is below both its 40-day (EUR 1,303) and 200-day (EUR 1,578) averages, after a 45% "
                 "fall from the January high to the low of 20 November. A close above EUR 1,357, the 21 October high, "
                 "could be a first sign of stabilisation; EUR 1,225.5, the low of the year, is the level to watch on "
                 "the downside."),
    "left": [
        ("h3", "1. What the company does"),
        ("p", "Hermès designs and makes luxury goods in its own workshops, mostly in France: Leather Goods and "
              "Saddlery (Birkin, Kelly), nearly half of revenue, then Ready-to-wear and Accessories, Silk and "
              "Textiles, Perfumes, Watches, Jewellery and Home. It sells through its own stores, which keeps "
              "control of prices and of the customer relationship."),
        ("h3", "2. Why it could do well"),
        ("p", "Leather Goods grew 11% in the third quarter in a weak market, thanks to a scarcity model: waiting lists "
              "for the Birkin and the Kelly keep demand above supply, and new workshops add capacity each year. "
              "The rest of the group is flat, as elsewhere in luxury, with ready-to-wear down 2% and watches down "
              "6%. As the finance director put it, it is the “volume” divisions that are suffering."),
        ("h3", "3. What sets it apart"),
        ("p", "A vertically integrated model: the company makes its own products, limits supply and sells to a loyal, "
              "wealthy clientele. Its profitability is the highest in the sector, and it has historically held up "
              "better than peers in downturns."),
    ],
    "right": [
        ("h3", "4. Is the share cheap?"),
        ("p", "Cheaper than at any time since 2016, but still expensive against the sector. The shares have lost about "
              "40% this year and trade on about 27 times expected earnings, against a ten-year average of 44.6 "
              "times. Growth is slowing: +4.3% in the third quarter against 5% expected, flat in Asia excluding "
              "Japan and down to +9% in the Americas. Price increases will be smaller in 2027 than the 5% to 6% of "
              "2026, and analysts have cut their earnings forecasts by 1% to 10%."),
        ("h3", "5. Main risks"),
        ("p", "China first: Chinese customers account for more than 40% of sales, the highest exposure in the sector. "
              "Some iconic bags are also losing a little of their appeal, with copies and influencers. At about "
              "EUR 17bn of sales the group may be too large to avoid the cycle, and a weaker yen reduces reported "
              "revenue."),
        ("h3", "6. What to watch next"),
        ("p", "Full-year 2026 results in February 2027; the pace of Leather Goods and any recovery among Chinese "
              "customers; the pricing decision for 2027; the first men's collection by Grace Wales Bonner and the "
              "first Couture collection by Nadège Vanhée in January 2027."),
    ],
    "conclusion": (
        "Hermès remains the best house in leather goods, where its scarcity model delivered 11% growth in the third "
        "quarter, while the rest of the group is flat like the rest of luxury. After a 40% fall the shares trade at "
        "their lowest multiple since 2016, yet remain expensive against the sector. The long-term value of the "
        "franchise can justify keeping a position, but there is no obvious catalyst in the short term, and China, at "
        "more than 40% of sales, is the main risk."
    ),
}

RMS_CHARTS = [
    ("Chart 4", "RMS FP: share price over two years",
     "Daily close with 40-day and 200-day simple moving averages, EUR, to 26 November 2026", "rms_chart1_price.png"),
    ("Chart 5", "RMS FP: forward P/E over ten years",
     "Price over consensus earnings for the next twelve months, with the ten-year average", "rms_chart2_pe.png"),
    ("Chart 6", "RMS FP: third-quarter 2026 revenue growth by division",
     "Growth at constant exchange rates; declines in orange", "rms_chart3_divisions.png"),
]

DISCLAIMER = [
    "This communication has been issued and made available to recipients for the purpose of advertising investment services and/or financial instruments. It has been sent for information purposes and cannot be considered as an offer or a personalised recommendation to buy or sell a financial instrument or any other investment or currency. This communication does not constitute investment research within the meaning of regulatory rules applicable in the European Economic Area, or research under the rules of the U.S. Self-Regulatory Organizations.",
    "This information is made solely for professional and institutional clients as defined by the Swiss Financial Services Act, as well as qualified investors according to the Swiss Collective Investment Schemes Act. It is not intended for retail clients or non-qualified investors and consequently cannot be transmitted to any third party.",
    "This communication is not directed to any person in any jurisdiction where, by reason of that person's nationality, residence or otherwise, its dissemination or use is prohibited. It cannot be quoted, reproduced, disclosed, distributed or otherwise referred to, in whole or in part, to any third party without the Bank's prior written consent.",
    "This communication may contain information on past performances of a financial product, all kinds of economic and financial valuations and analyses, as well as opinions of the Bank or of third parties. Any market valuations, terms and calculation methods, yields and opinions expressed are subject to change without notice. The information and opinions contained herein have been compiled and provided in good faith, based on information obtained from sources believed to be trustworthy. However, such information has not been independently verified. No guarantee, representation, or warranty of any kind, whether express or implied, is provided by the Bank or by relevant data vendors and other sources with respect to the accuracy, reliability, currentness or exhaustiveness of the information communicated, the methodology employed or the prices contained herein.",
    "Past performance is not a reliable indicator of current or future results. Any reference to the past performance of an investment does not guarantee its future performance. Fluctuations in exchange rates may adversely affect the value, price or income of any investment.",
    "Nothing in the present communication constitutes investment, legal, accounting or tax advice. This information is purely objective since it does not take into consideration the personal situation (including financial knowledge and experience), the investment objectives and risk profile of any recipient. Moreover, certain financial instruments mentioned (in particular, but not exclusively, derivatives, options and futures) involve a high risk of loss and may not be suitable. Accordingly, recipients should consult their own advisors on such matters, including but not limited to the possible tax consequences of investing in any financial product mentioned herein, and make their own assessment of the suitability of such investment product.",
    "Should a recipient make an investment on the basis of the present communication, the recipient alone shall bear the consequences thereof. In no event shall the Bank, its directors, employees, affiliates or agents be held responsible for damages of any kind arising out of the use of all or part of the information provided herein.",
]
