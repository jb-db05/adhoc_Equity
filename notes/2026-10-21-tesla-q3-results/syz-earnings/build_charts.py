"""build_charts.py: Chart 1 (surprise vs. consensus) and Chart 2 (price vs. EPS and P/E) for the Tesla update.
Usage: python3 build_charts.py <bloomberg_daily.xlsx> <out_dir>"""
import sys

import pandas as pd

import syz_charts as sc

PARAMS = {
    "ticker": "TSLA",
    "asof": "21 Oct 2026",
    "last_date": "2026-10-21",      # pre-results close; later rows are dropped
    # reported vs. pre-results consensus; filled once the consensus table is confirmed
    "lines": [],
}


def load_daily_as_weekly(path, last_date):
    """Daily Bloomberg export (Last Price, BEst EPS, BEst P/E, 40- and 200-day SMA): weekly Friday closes,
    40-week simple MA computed from the weekly closes. The window starts after the last non-positive
    consensus EPS (log scale)."""
    raw = pd.read_excel(path, sheet_name=0).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).sort_values("date")
    d = d[d["price"].notna() & d["eps"].notna() & (d["date"] <= last_date)]
    w = d.set_index("date").resample("W-FRI").last().dropna(subset=["price"]).reset_index()
    w.loc[w.index[-1], "date"] = d["date"].iloc[-1]
    w["ma40"] = w["price"].rolling(40).mean()
    start = w.loc[w["eps"] <= 0, "date"].max()
    return w[(w["date"] > start) & w["eps"].notna()].reset_index(drop=True)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    sc.setup_fonts()
    p = PARAMS
    if p["lines"]:
        labels = [l for l, _, _ in p["lines"]]
        surprises = [(r / c - 1) * 100 for _, r, c in p["lines"]]
        sc.bar_chart(f"{out}/Chart1_TSLA_Q32026_vs_consensus.png", labels, surprises,
                     f"{p['ticker']}: Q3 2026 results vs. consensus", "Surprise vs. pre-results consensus, %",
                     sc.source_line("FactSet", p["asof"], "Consensus: FactSet pre-results"))
        sc.crop_for_pdf(f"{out}/Chart1_TSLA_Q32026_vs_consensus.png", f"{out}/c1_crop.png", "bar")
        print("surprises", [round(s, 1) for s in surprises])
    df = load_daily_as_weekly(src, p["last_date"])
    stats = sc.price_eps_pe_chart(
        f"{out}/Chart2_TSLA_price_eps_pe.png", df, "Tesla", f"{p['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "TSLA US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale", "P/E shaded vs. its 2020-26 average"),
        ccy="USD")
    sc.crop_for_pdf(f"{out}/Chart2_TSLA_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print("window", df["date"].iloc[0].date(), "to", df["date"].iloc[-1].date())
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()})
