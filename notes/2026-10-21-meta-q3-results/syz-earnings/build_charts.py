"""build_charts.py: Chart 1 (surprise vs. consensus) and Chart 2 (price vs. EPS and P/E) for the Meta update.
Usage: python3 build_charts.py <bloomberg_daily.xlsx> <out_dir>"""
import sys

import pandas as pd

import syz_charts as sc

PARAMS = {
    "ticker": "META",
    "asof": "21 Oct 2026",
    "pe_avg_from": "2016-01-01",
    # reported vs. FactSet pre-results consensus (USD bn, USD per share)
    "lines": [
        ("Revenue", 64.60, 63.34),
        ("Operating income", 22.88, 20.17),
        ("EPS", 7.40, 6.54),
        ("Q4 revenue guide", 74.5, 73.65),
    ],
}


def load_daily_as_weekly(path):
    """The Meta export is daily (Last Price, BEst EPS, BEst P/E, 40- and 200-day SMA): resample to weekly
    Friday closes and compute the 40-week simple MA from the weekly closes, as the kit expects."""
    raw = pd.read_excel(path, sheet_name=0).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).sort_values("date")
    d = d[d["price"].notna() & d["eps"].notna()]
    last = d["date"].iloc[-1]
    w = d.set_index("date").resample("W-FRI").last().dropna(subset=["price"]).reset_index()
    w.loc[w.index[-1], "date"] = last          # last point carries its real date (pre-results close)
    w["ma40"] = w["price"].rolling(40).mean()
    return w[w["eps"].notna()].reset_index(drop=True)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    sc.setup_fonts()
    p = PARAMS
    labels = [l for l, _, _ in p["lines"]]
    surprises = [(r / c - 1) * 100 for _, r, c in p["lines"]]
    sc.bar_chart(f"{out}/Chart1_META_Q32026_vs_consensus.png", labels, surprises, f"{p['ticker']}: Q3 2026 results vs. consensus",
                 "Surprise vs. pre-results consensus, %; operating income and EPS exclude the legal charge",
                 sc.source_line("FactSet", p["asof"], "Consensus: FactSet pre-results",
                                "Operating income and EPS exclude the USD 9.9bn legal charge",
                                "Q4 guide at the mid-point of USD 73 to 76bn"))
    df = load_daily_as_weekly(src)
    stats = sc.price_eps_pe_chart(
        f"{out}/Chart2_META_price_eps_pe.png", df, "Meta", f"{p['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "META US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale", "P/E shaded vs. its 2016-26 average"),
        ccy="USD", pe_avg_from=pd.Timestamp(p["pe_avg_from"]))
    sc.crop_for_pdf(f"{out}/Chart1_META_Q32026_vs_consensus.png", f"{out}/c1_crop.png", "bar")
    sc.crop_for_pdf(f"{out}/Chart2_META_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print("surprises", [round(s, 1) for s in surprises])
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()})
