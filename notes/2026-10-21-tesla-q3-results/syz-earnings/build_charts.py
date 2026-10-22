"""build_charts.py: Chart 1 (surprise vs. consensus) and Chart 2 (price vs. EPS and P/E) for the Tesla update.
Usage: python3 build_charts.py <bloomberg_daily.xlsx> <out_dir>"""
import sys

import pandas as pd

import syz_charts as sc

PARAMS = {
    "ticker": "TSLA",
    "asof": "21 Oct 2026",
    "last_date": "2026-10-21",      # pre-results close; later rows are dropped
    # automotive gross margin excluding regulatory credits, %
    "auto_gm": [("Q2 2026 reported", 16.3), ("Q3 2026 consensus", 16.7), ("Q3 2026 reported", 18.1)],
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
    # Chart 1, trading-update variant: the decisive line (automotive gross margin excl. credits) in absolute terms
    labels = [l for l, _ in p["auto_gm"]]
    sc.bar_chart(f"{out}/Chart1_TSLA_auto_gross_margin.png", labels, [v for _, v in p["auto_gm"]],
                 f"{p['ticker']}: automotive gross margin excluding regulatory credits", "% of automotive revenue",
                 sc.source_line("company filings", p["asof"], "Consensus: pre-results analyst estimates"),
                 colors=[sc.BLUEB, sc.BLUEB, sc.ORANGE], fmt="{:.1f}%", zero_line=False)
    sc.crop_for_pdf(f"{out}/Chart1_TSLA_auto_gross_margin.png", f"{out}/c1_crop.png", "bar")
    df = load_daily_as_weekly(src, p["last_date"])
    stats = sc.price_eps_pe_chart(
        f"{out}/Chart2_TSLA_price_eps_pe.png", df, "Tesla", f"{p['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "TSLA US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale", "P/E shaded vs. its 2020-26 average"),
        ccy="USD")
    sc.crop_for_pdf(f"{out}/Chart2_TSLA_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print("window", df["date"].iloc[0].date(), "to", df["date"].iloc[-1].date())
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()})
