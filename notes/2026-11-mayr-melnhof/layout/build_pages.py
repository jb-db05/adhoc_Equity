"""Generate the A4 HTML pages of the Mayr-Melnhof ad-hoc opinion."""
import re, pathlib
HERE = pathlib.Path(__file__).parent
DATE = '11 November 2026'
N = 7
skill = (HERE / '../../../syz-equity-note/SKILL.md').read_text()
disc = skill.split('## 5. Important information (disclaimer, verbatim)')[1].split('## 6.')[0].strip()
disc_html = ''.join(f'<p class="small">{p.strip()}</p>' for p in disc.split('\n\n'))

def page(n, body, cover=False):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=794">
<title>Mayr-Melnhof ad-hoc opinion {n}/{N}</title><link rel="stylesheet" href="style.css"></head><body>
<div class="page{' cover' if cover else ''}">
<header><img class="logo" src="syz-logo.png" alt="Syz"><div class="bar"></div></header>
{body}
<footer><span>Syz Research · Ad-hoc opinion · {DATE}</span><span>{n} / {N}</span></footer>
</div></body></html>'''

P1 = f'''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h1 class="headline">Mayr-Melnhof: the cash is priced, the rest is almost free</h1>
<div class="sub1">{DATE} · Syz Research</div>
<div class="box notice"><span class="boxlabel">Important notice</span><br>
Prices are as of the close on {DATE}. The special distribution is planned, not approved: its amount, timing and form depend on the closing of the transaction, expected in H1 2027.</div>

<h2>A deal that splits the group in two</h2>
<p>On 9 November, Mayr-Melnhof (MM) agreed to sell 70% of its Packaging business to the US private equity firm KPS Capital Partners and announced a special distribution to shareholders. The share rose 11% over the week to EUR 74.10, still close to its 23 October low (EUR 64.10), the lowest since at least 2014. Does the market price the distribution? It prices the cash. What it barely prices is the business that remains.</p>

<div class="box grid4 two-rows">
  <div><div class="kpilabel">Enterprise value</div><div class="boxvalue">EUR 2.4bn</div><div class="boxnote">100% of Packaging, about 9x 2026 EBITDA</div></div>
  <div><div class="kpilabel">MM keeps</div><div class="boxvalue">30%</div><div class="boxnote">of the new holding, for about EUR 0.4bn</div></div>
  <div><div class="kpilabel">Cash to MM</div><div class="boxvalue">EUR 1.8 to 1.9bn</div><div class="boxnote">after costs, taxes and reinvestment</div></div>
  <div><div class="kpilabel">Special distribution</div><div class="boxvalue">EUR 0.5 to 0.6bn</div><div class="boxnote">EUR 25 to 30 a share, 34 to 40% of the price</div></div>
  <div><div class="kpilabel">Net cash after closing</div><div class="boxvalue">EUR 0.8 to 0.9bn</div><div class="boxnote">before the distribution; EUR 0.3bn kept after</div></div>
  <div><div class="kpilabel">Closing</div><div class="boxvalue">H1 2027</div><div class="boxnote">subject to approvals</div></div>
  <div><div class="kpilabel">Adjustment</div><div class="boxvalue">30% to 20%</div><div class="boxnote">if 2027 EBITDA targets are missed</div></div>
  <div><div class="kpilabel">Accounting</div><div class="boxvalue">Equity method</div><div class="boxnote">for the 30% stake</div></div>
</div>

<div class="cols" style="margin-top:6px">
<div>
<h3>Packaging: the part a buyer wanted</h3>
<p>Folding cartons for food, consumer brands and pharma sell on service, design and proximity to the customer, and demand follows consumption rather than the paper cycle. The business averaged an adjusted EBITDA margin of about 12% over 2021 to 2025, and in the first nine months of 2026 both packaging divisions improved their earnings on a like-for-like basis. At EUR 2.4bn, Packaging alone is now worth more than the whole group was before the deal (EUR 2.3bn enterprise value on 6 November). The group traded at about 6x EBITDA; Packaging is being sold at about 9x.</p>
</div>
<div>
<h3>Board &amp; Paper: the part the market ignores</h3>
<p>Cartonboard and kraft paper are a commodity business with heavy fixed costs, in a Europe with too much capacity and high energy and fibre costs. Over nine months its adjusted EBITDA more than halved to EUR 39m and it lost EUR 44m at operating level, despite slightly higher volumes. After closing, it becomes MM's core business, with a long-term contract to keep supplying the Packaging business it just sold. A mill with high fixed costs gains a lot of profit from a small rise in prices, so the upside is real when the cycle turns, but nobody can date that turn today.</p>
</div>
</div>

<div class="box" style="margin-top:4px">
<div class="boxlabel">What this means for investors</div>
<ul style="margin-top:5px">
<li>The special distribution is real, but it is not free money: it is cash that will already sit on the balance sheet, and the share price would fall by the same amount on the ex-date.</li>
<li>What the market does not price is what remains after the cash and the stake: at EUR 74.10, Board &amp; Paper is valued at about EUR 0.23bn, less than 2x its 2025 EBITDA (Syz calculation, page 5).</li>
<li>The case suits investors with an appetite for family-controlled small caps who can wait until 2027: liquidity is limited, and the amount, timing and form of the payout are not locked.</li>
</ul></div>
'''

P2 = '''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin-top:8px">The deal in numbers</h2>
<div class="chart-title"><span>Chart 1</span> · MM: from EUR 2.4bn to the special distribution</div>
<div class="chart-sub">Expected cash proceeds from the transaction, EUR bn, rounded as published by the company</div>
<div class="box chartbox"><img src="../charts/chart_bridge.png" alt="Cash bridge"></div>
<div class="source">Source: Mayr-Melnhof, investor presentation of 9 November 2026; Syz Research</div>
<p style="margin-top:8px">The EUR 0.4bn is not a payment to MM: it is what MM invests to keep 30% of the new holding. It is also well below 30% of EUR 2.4bn (EUR 0.72bn), because the enterprise value includes debt. EUR 0.4bn for 30% implies about EUR 1.3bn of equity for 100%, so the new holding would carry about EUR 1.0 to 1.1bn of acquisition debt (Syz calculation). MM's stake is therefore leveraged equity: more upside if KPS grows the business, more downside if it does not, which is also why the stake can be cut to 20%.</p>

<div class="chart-title"><span>Chart 2</span> · Same sales, very different price tags</div>
<div class="chart-sub">Packaging vs. Board &amp; Paper: 2025 sales and adjusted EBITDA, value and value/EBITDA</div>
<div class="box chartbox"><img src="../charts/chart_two_businesses.png" alt="Packaging vs Board and Paper"></div>
<div class="source">Packaging value: KPS deal value. Board &amp; Paper value: implied by the share price at EUR 74.10 (Syz calculation). Board &amp; Paper figures include the remaining packaging operations in Iran and Tunisia. Source: Mayr-Melnhof, investor presentation of 9 November 2026; Syz Research, Bloomberg</div>

'''

P3 = '''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin:8px 0 2px;font-size:20px">Mayr-Melnhof Karton AG (MMK AV)</h2>
<div class="sub2">A cash box with a cyclical mill attached, priced as if the mill were worth almost nothing</div>
<div class="box grid4" style="margin-top:6px">
  <div><div class="kpilabel">Share price</div><div class="boxvalue">EUR 74.10</div><div class="boxnote pos">+10.9% over the week</div></div>
  <div><div class="kpilabel">Market cap</div><div class="boxvalue">EUR 1.5bn</div><div class="boxnote">about 20m shares, 42% free float</div></div>
  <div><div class="kpilabel">Planned distribution</div><div class="boxvalue">EUR 25 to 30</div><div class="boxnote">per share, after closing in H1 2027</div></div>
  <div><div class="kpilabel">Forward P/E</div><div class="boxvalue">9.8x</div><div class="boxnote">10-year average 12.4x</div></div>
</div>
<div class="cols" style="margin-top:4px">
<div>
<h3>1. What the company does</h3>
<p>MM is the world's largest producer of recycled cartonboard outside China and, until this deal, one of Europe's largest folding carton makers. After the deal it becomes a board and paper producer with seven sites, about EUR 2.0bn of sales, net cash and a 30% stake in its former Packaging business.</p>
<h3>2. Why it could do well</h3>
<p>The deal turns a complex group into something simple to value: cash, a stake priced by a private equity buyer, and a mill business. The special distribution would return 34 to 40% of today's share price, and the consensus earnings estimate for the next twelve months was raised from EUR 6.61 to EUR 7.55 per share in the week of the deal.</p>
<h3>3. What sets it apart</h3>
<p>The value of Packaging comes from a real transaction, not from a model, and MM keeps a share of the upside. Few European small caps go from net debt of about EUR 1.0bn to net cash in one step, and the supply contract with Packaging gives Board &amp; Paper a stable outlet.</p>
<h3>4. Cheap, or a value trap?</h3>
<p>Net cash and the stake explain about 84% of the share price (page 5). The remaining EUR 12 per share values Board &amp; Paper at less than 2x its 2025 EBITDA of EUR 138m, a business that averaged a 9% EBITDA margin over 2021 to 2025. Even on the depressed last twelve months (divisional EBITDA of about EUR 67m), the multiple stays below 4x. The trap would be a downturn long enough to keep the division loss-making, and cash spent on acquisitions instead of being returned.</p>
</div>
<div>
<h3>5. Main risks</h3>
<ul>
<li><b>The payout is not locked.</b> Approvals, closing, the tax bill on the disposal and acquisition plans could reduce or delay it.</li>
<li><b>The stake can shrink.</b> If Packaging misses its 2027 EBITDA targets, MM's 30% falls to as low as 20%, about EUR 7 per share less.</li>
<li><b>Board &amp; Paper</b> made an operating loss over nine months, and management still expects sustained margin pressure.</li>
<li><b>Acquisitions:</b> MM plans to buy the Arnsberg cartonboard mill; more deals could absorb cash that would otherwise be returned.</li>
<li><b>Iran:</b> MM keeps its operations there (sales of about EUR 60m), a small but real geopolitical exposure.</li>
<li><b>Liquidity:</b> family control, a 42% free float and a small market cap mean wider spreads and harder exits in stressed markets.</li>
</ul>
<h3>6. What to watch next</h3>
<ul>
<li>The form of the payout (dividend or repayment of capital) and its timing.</li>
<li>Whether the price increases implemented since October hold, and whether the order backlog stays above last year's level.</li>
<li>MM's capital allocation policy for the cash it keeps.</li>
<li>Regulatory approvals ahead of closing in H1 2027.</li>
</ul>
</div>
</div>
<div class="box conclusion">
<div class="boxlabel">Conclusion</div>
<p style="margin:5px 0 0">The special distribution is not what makes the case; it only returns cash the market already counts. The case is that, after the cash and the stake, an investor buys a European board and paper business for about EUR 0.2bn at a low point of its cycle. It suits investors who are comfortable with a family-controlled small cap, limited liquidity and a 2027 horizon, and who see a recovery in board prices as an option rather than a certainty.</p>
</div>
'''

P4 = '''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin-top:8px">Is the share cheap?</h2>
<div class="chart-title"><span>Chart 4</span> · MMK AV: what EUR 74.10 buys</div>
<div class="chart-sub">Sum of the parts, EUR per share, mid-point of the company's net cash range (Syz calculation)</div>
<div class="box chartbox"><img src="../charts/chart_sotp.png" alt="Sum of the parts"></div>
<div class="source">Source: Mayr-Melnhof, investor presentation of 9 November 2026; Syz Research, Bloomberg</div>
<div class="cols" style="margin-top:10px">
<div>
<table class="compact">
<caption>Sum of the parts (Syz calculation)</caption>
<tr><th>EUR per share</th><th>Low</th><th>Mid</th><th>High</th></tr>
<tr><td>Net cash after closing</td><td>40.0</td><td>42.5</td><td>45.0</td></tr>
<tr><td>30% stake in Packaging</td><td>20.0</td><td>20.0</td><td>20.0</td></tr>
<tr class="total"><td>Cash and stake</td><td>60.0</td><td>62.5</td><td>65.0</td></tr>
<tr><td>Share price</td><td>74.10</td><td>74.10</td><td>74.10</td></tr>
<tr class="total"><td>Implied Board &amp; Paper</td><td>14.1</td><td>11.6</td><td>9.1</td></tr>
<tr><td>In EUR bn</td><td>0.28</td><td>0.23</td><td>0.18</td></tr>
<tr><td>Times 2025 EBITDA</td><td>2.0x</td><td>1.7x</td><td>1.3x</td></tr>
</table>
<p class="small">Method: net cash guided by MM after closing (EUR 0.8 to 0.9bn, before the special distribution), plus the 30% stake at the EUR 0.4bn MM is investing, divided by about 20m shares. The remainder is what the share price implies for Board &amp; Paper. If the stake is cut to 20%, its value falls by about EUR 7 per share.</p>
</div>
<div>
<h3 style="margin-top:0">Why the distribution itself is not the opportunity</h3>
<p>The EUR 25 to 30 per share will be paid out of cash that is already counted in the share price. On the ex-date the price should fall by roughly the same amount, so an investor who buys only for the distribution gains nothing on paper. The return comes from what is left: about EUR 15 per share of cash kept by MM, the 30% stake, and Board &amp; Paper.</p>
<div class="box" style="margin-top:8px">
<div class="boxlabel">Swiss investors: the form of the payout matters</div>
<p class="small" style="margin:5px 0 0">A dividend bears 27.5% Austrian withholding tax, of which 12.5 points can be reclaimed under the Austria and Switzerland tax treaty, leaving 15%. A repayment of capital out of capital reserves would in principle not bear Austrian withholding tax. Management says the form is still open. Investors should check their own situation with a tax adviser.</p>
</div>
</div>
</div>
'''

P5 = '''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin-top:8px">The share and its owners</h2>
<div class="chart-title"><span>Chart 5</span> · MMK AV: share price, 40-week moving average and forward P/E</div>
<div class="chart-sub">Weekly data since September 2014; forward P/E on consensus earnings for the next twelve months, with its 10-year average and a band of plus or minus one standard deviation</div>
<div class="box chartbox"><img src="../charts/chart_price_pe.png" alt="Share price and P/E"></div>
<div class="source">Source: Syz Research, Bloomberg</div>
<div class="cols" style="margin-top:12px">
<div>
<h3 style="margin-top:0">A long decline, a first rebound</h3>
<p>The share fell about 60% from its January 2022 peak of EUR 186, as the end of post-Covid destocking, higher energy costs and weak demand hit board prices and earnings. The deal triggered the first sharp rebound in months, from EUR 66.80 to EUR 74.10 in a week.</p>
</div>
<div>
<h3 style="margin-top:0">Levels to watch</h3>
<p>The share is still below its 40-week moving average (EUR 80.2). A move back above that level could confirm that the deal has changed the trend; the October low of EUR 64.10 is the level to watch on the downside. At 9.8x, the forward P/E sits just below the lower end of its usual range, more than one standard deviation under its 10-year average of 12.4x.</p>
</div>
</div>

<div class="box" style="margin-top:6px">
<div class="boxlabel">A family company, with the trade-offs that come with it</div>
<p style="margin:5px 0 4px">The founding families hold about 58% of the shares through a syndicate; the rest is free float. For an outside shareholder, family control cuts both ways. It brings a long horizon, a conservative balance sheet and a habit of returning cash, and here incentives are aligned: the families receive 58% of any special distribution, which makes it more likely to happen. The deal also shows the families are open to bold portfolio moves and to outside capital, something the market had not assumed.</p>
<p style="margin:0">On the other side, a takeover premium is unlikely, minority shareholders have little say on the use of the cash that remains (MM mentions strategic opportunities as well as debt repayment), and a 42% free float on a EUR 1.5bn company limits liquidity.</p>
</div>
'''

PBP = '''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin-top:8px">Packaging vs. Board &amp; Paper: two markets moving apart</h2>
<p>The third quarter, published four days before the deal, shows why a buyer wanted Packaging and why the market gives little value to Board &amp; Paper.</p>
<div class="chart-title"><span>Chart 3</span> · MM: quarterly adjusted EBITDA by business</div>
<div class="chart-sub">EUR m. Packaging: Food &amp; Premium (excluding the TANN business sold in 2025) plus Pharma &amp; Healthcare. Hatched: Q3 2026 maintenance costs</div>
<div class="box chartbox"><img src="../charts/chart_quarterly.png" alt="Quarterly EBITDA"></div>
<div class="source">Source: Mayr-Melnhof, Trading Statement for the first three quarters of 2026 (5 November 2026); Syz Research</div>
<div class="cols" style="margin-top:10px">
<div>
<h3 style="margin-top:0">Packaging keeps delivering</h3>
<p>Packaging's quarterly EBITDA has held between EUR 66m and 77m through the downturn, and the third quarter of 2026 was its best in the period. Over nine months, Food &amp; Premium lifted its EBITDA margin to 14.5% (+0.9 points excluding TANN) despite lower volumes, thanks to cost savings. Pharma &amp; Healthcare grew EBITDA by 13% to EUR 68m, helped by customers making GLP-1 weight-loss drugs. Management says demand in Packaging is picking up.</p>
</div>
<div>
<h3 style="margin-top:0">Board &amp; Paper: a third quarter hit from three sides</h3>
<p>Strong price competition in an oversupplied market; energy, transport and chemicals costs pushed up by the conflict in the Middle East; and planned maintenance at two virgin-fibre mills, Kwidzyn and Kotkamills, which cost about EUR 36m. The division's EBITDA turned negative (EUR -18m). Without the maintenance it would have been around EUR +18m (Syz calculation), about the level of the same quarter of 2025 (EUR 17m).</p>
</div>
</div>
<div class="box" style="margin-top:4px">
<div class="boxlabel">Early signs of a turn, not yet a recovery</div>
<ul style="margin-top:5px">
<li><b>Prices:</b> MM has implemented price increases since October to pass on higher costs.</li>
<li><b>Orders:</b> the average order backlog reached 183,000 tonnes over nine months, against 157,000 a year earlier, and mills ran at good capacity utilisation.</li>
<li><b>Supply:</b> overcapacity in Europe has been reduced by the exit of a competitor, and MM plans to buy the Arnsberg cartonboard mill, which it expects to bring synergies.</li>
<li><b>Costs:</b> the Fit-For-Future savings programme is partly offsetting cost pressure.</li>
</ul>
<p class="small" style="margin:0">Management still expects sustained margin pressure in Board &amp; Paper, so these signals support patience rather than a call on the timing of the recovery.</p>
</div>
'''

P6 = f'''
<div class="label">Ad-hoc opinion · Paper &amp; Packaging</div>
<h2 style="margin-top:8px">Sources</h2>
<p class="small" style="margin-bottom:2px">Mayr-Melnhof Karton AG: investor presentation and press release of 9 November 2026 (sale of a majority stake in the Packaging business to KPS Capital Partners and planned special distribution); Trading Statement for the first three quarters of 2026, 5 November 2026; shareholder structure, company website.</p>
<p class="small">Syz Research, Bloomberg (prices, moving average, consensus earnings and forward P/E as of the close on {DATE}). Syz calculation: sum of the parts, implied equity value and debt of the new Packaging holding, implied value of Board &amp; Paper.</p>
<h2>Important information</h2>
{disc_html}
'''

for n, (body, cover) in enumerate([(P1, True), (P2, False), (PBP, False), (P3, False), (P4, False), (P5, False), (P6, False)], 1):
    (HERE / f'page{n}.html').write_text(page(n, body, cover))
print('ok')
