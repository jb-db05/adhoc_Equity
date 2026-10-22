"""syz_charts.py: Syz earnings chart kit (white-background report charts, Research Comment format)."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

FONT_DIR = "/home/claude/fonts"
ORANGE, AMBER, GOLD = "#FF6C0E", "#FFA400", "#FFC545"
NAVY, BLUEB = "#202945", "#4B5F80"
MINT, TEAL, SKY, PEACH, MULB = "#3BAF90", "#9DD9D2", "#79D6FF", "#E6A4AD", "#AC5D85"
GREY, AXIS_TXT, SPINE, GRID = "#8A8F98", "#5A5F68", "#D6D9DE", "#EDEFF2"
SYZ_GRAD = LinearSegmentedColormap.from_list("syz", [ORANGE, GOLD])
DASH = (0, (5, 4))


def setup_fonts():
    for w in ["Light", "Regular", "SemiBold", "Bold", "ExtraBold"]:
        fm.fontManager.addfont(f"{FONT_DIR}/Nunito-{w}.ttf")
    plt.rcParams["font.family"] = "Nunito"
    plt.rcParams["font.weight"] = "bold"          # Nunito Bold everywhere; ExtraBold for titles
    plt.rcParams["axes.titleweight"] = "bold"


def style_ax(ax, grid_axis="y"):
    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(SPINE)
    ax.tick_params(colors=AXIS_TXT, labelsize=9.5, length=3)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, zorder=0)


def header(fig, title, subtitle, footnote, title_y=0.945, sub_y=0.906, bar_y=0.886, foot_y=0.032, rule=True):
    """Standalone-PNG header: navy title, optional grey subtitle + orange->gold rule, grey source footnote."""
    fig.patch.set_facecolor("white")
    fig.text(0.07, title_y, title, fontsize=16.5, fontweight="extra bold", color=NAVY, ha="left")
    if subtitle:
        fig.text(0.07, sub_y, subtitle, fontsize=10.5, color=AXIS_TXT, ha="left")
    if rule:
        bar = fig.add_axes([0.07, bar_y, 0.89, 0.006])
        bar.imshow(np.linspace(0, 1, 256).reshape(1, -1), aspect="auto", cmap=SYZ_GRAD)
        bar.set_axis_off()
    fig.text(0.07, foot_y, footnote, fontsize=8, color=GREY, ha="left", fontweight="normal")


def source_line(provider, asof, *notes):
    """No full stop at the end, ever."""
    return " · ".join([f"Source: Syz Research, {provider}", f"As of {asof}", *[n for n in notes if n]])


def legend(ax, loc="upper left", ncol=1):
    leg = ax.legend(loc=loc, frameon=False, fontsize=10.5, ncol=ncol, handlelength=2.2)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")
    return leg


def _fmt_thousands(v, _):
    return f"{v:,.0f}"


def _log_ticks(ax, lo, hi, subs=(1, 2, 5)):
    """1-2-5 ladder on a log axis, clipped to the data range (e.g. 1, 2, 5, 10, 20, 50)."""
    ticks = [m * 10 ** e for e in range(int(np.floor(np.log10(lo))) - 1, int(np.ceil(np.log10(hi))) + 2)
             for m in subs]
    ticks = [t for t in ticks if lo * 0.9 <= t <= hi * 1.35]
    ax.set_yticks(ticks); ax.set_yticks([], minor=True)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}"))


# ---------------------------------------------------------------- data loader (Bloomberg weekly export)
def load_bloomberg_sheet(path, sheet=0):
    """Bloomberg export, one row per week, newest first, header row 1:
    Date | <Ticker> - Last Price (R1) | <Ticker> - BEst EPS (L1) | Moving Average(Simple,40,0) | <Ticker> - BEst P/E Ratio
    Column order is matched by keyword, not position. Returns a DataFrame sorted oldest -> newest."""
    df = pd.read_excel(path, sheet_name=sheet)
    df = df.dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    out = pd.DataFrame({
        "date": pd.to_datetime(df[pick("date")]),
        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
        "ma40": pd.to_numeric(df[pick("moving average")], errors="coerce"),
        "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return out


# ---------------------------------------------------------------- archetype: price vs. consensus EPS + P/E panel
def price_eps_pe_chart(path, df, name, title, footnote, ccy="EUR", pe_avg_from=None,
                       p1_title=None, p2_title=None):
    """Reference earnings chart. Top: share price (Blueberry, rhs, log) + 40-week MA (dashed) + 12m-forward
    EPS (Orange, lhs, log). Bottom: 12m-forward P/E (Orange) vs. its long-run average (dashed navy), shaded
    orange above / blue-grey below. df from load_bloomberg_sheet(). Returns the numbers quoted in the labels."""
    x = mdates.date2num(df["date"])
    p1_title = p1_title or f"Share price and consensus 12m-forward EPS (log scale)"
    p2_title = p2_title or "12m-forward P/E"
    start_year, end_year = df["date"].iloc[0].year, df["date"].iloc[-1].year
    pe_series = df["pe"] if pe_avg_from is None else df.loc[df["date"] >= pe_avg_from, "pe"]
    pe_avg = float(pe_series.mean())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.5, 8.6), dpi=200, sharex=True,
                                   gridspec_kw={"height_ratios": [2.45, 1], "hspace": 0.16})
    fig.subplots_adjust(top=0.875, bottom=0.085, left=0.075, right=0.925)

    # --- top panel: EPS on the left axis, price + MA on a twin right axis, both log
    style_ax(ax1)
    ax1.set_yscale("log")
    ax1.plot(x, df["eps"], color=ORANGE, linewidth=2.1, zorder=3, label=f"12m-forward EPS, {ccy} (lhs)")
    ax1.set_ylabel(f"12m-forward EPS ({ccy}, log scale)", fontsize=10, color=ORANGE, fontweight="bold")
    ax1.tick_params(axis="y", colors=ORANGE)
    _log_ticks(ax1, float(df["eps"].min()), float(df["eps"].max()))
    ax1.set_title(p1_title, fontsize=12, fontweight="bold", color=NAVY, loc="left", pad=8)

    axr = ax1.twinx()
    axr.set_yscale("log")
    axr.spines[["top"]].set_visible(False)
    axr.spines[["right", "left", "bottom"]].set_color(SPINE)
    axr.plot(x, df["price"], color=BLUEB, linewidth=1.9, zorder=4, label=f"Share price, {ccy} (rhs)")
    axr.plot(x, df["ma40"], color=BLUEB, linewidth=1.3, linestyle=DASH, zorder=3, label="40-week moving average (rhs)")
    axr.set_ylabel(f"Share price ({ccy}, log scale)", fontsize=10, color=AXIS_TXT, fontweight="bold")
    axr.tick_params(axis="y", colors=AXIS_TXT, labelsize=9.5, length=3)
    _log_ticks(axr, float(df["price"].min()), float(df["price"].max()), subs=(1, 2.5, 5))
    ax1.set_zorder(axr.get_zorder() + 1); ax1.patch.set_visible(False)

    # end labels
    last_p, last_e = float(df["price"].iloc[-1]), float(df["eps"].iloc[-1])
    axr.plot(x[-1], last_p, "o", color=BLUEB, ms=5, zorder=5)
    axr.annotate(f"{last_p:,.0f}", (x[-1], last_p), xytext=(10, 10), textcoords="offset points",
                 color=BLUEB, fontsize=10.5, fontweight="bold")
    ax1.plot(x[-1], last_e, "o", color=ORANGE, ms=5, zorder=5)
    ax1.annotate(f"{last_e:,.1f}", (x[-1], last_e), xytext=(10, -22), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")

    # one legend combining both axes
    h1, l1 = axr.get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels()
    leg = ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=10.5, handlelength=2.4)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")

    # --- bottom panel: P/E vs. average
    style_ax(ax2)
    pe = df["pe"].to_numpy(float)
    ax2.plot(x, pe, color=ORANGE, linewidth=1.9, zorder=3, label="12m-forward P/E")
    ax2.axhline(pe_avg, color=NAVY, linestyle=DASH, linewidth=1.3, zorder=2,
                label=f"Average since {pe_series.index.map(lambda i: df['date'][i]).min().year}: {pe_avg:.1f}x")
    ax2.fill_between(x, pe, pe_avg, where=pe >= pe_avg, interpolate=True, color=ORANGE, alpha=0.12, zorder=1)
    ax2.fill_between(x, pe, pe_avg, where=pe < pe_avg, interpolate=True, color=BLUEB, alpha=0.14, zorder=1)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}x"))
    ax2.set_title(p2_title, fontsize=12, fontweight="bold", color=NAVY, loc="left", pad=8)
    ax2.plot(x[-1], pe[-1], "o", color=ORANGE, ms=5, zorder=4)
    ax2.annotate(f"{pe[-1]:.1f}x", (x[-1], pe[-1]), xytext=(10, -4), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")
    legend(ax2, loc="upper left", ncol=2)

    ax2.xaxis.set_major_locator(mdates.YearLocator(1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.set_xlim(x[0] - 30, x[-1] + 330)

    header(fig, title, None, footnote, title_y=0.955, foot_y=0.028, rule=False)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)
    return {"price": last_p, "eps": last_e, "pe": float(pe[-1]), "pe_avg": pe_avg,
            "pe_premium_pct": (float(pe[-1]) / pe_avg - 1) * 100,
            "above_ma": last_p > float(df["ma40"].iloc[-1]), "ma40": float(df["ma40"].iloc[-1])}


# ---------------------------------------------------------------- generic single-series bar (KPI vs. consensus etc.)
def bar_chart(path, labels, values, title, subtitle, footnote, colors=None, fmt="{:+.1f}%", ylabel="",
              zero_line=True, highlight_negative=True):
    """Simple bar archetype for page 1 (e.g. beat/miss by line, revisions by segment). Positive = Blueberry,
    negative = Tiger Orange (bearish tag colour), unless colors is given."""
    vals = np.asarray(values, float)
    if colors is None:
        colors = [ORANGE if (highlight_negative and v < 0) else BLUEB for v in vals]
    fig, ax = plt.subplots(figsize=(12.5, 5.0), dpi=200)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.07, right=0.96)
    style_ax(ax)
    ax.tick_params(labelsize=12)
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.62, linewidth=0, zorder=3)
    if zero_line:
        ax.axhline(0, color=NAVY, linewidth=1.0, zorder=2)
    for b, v in zip(bars, vals):
        ax.annotate(fmt.format(v), (b.get_x() + b.get_width() / 2, v),
                    xytext=(0, 5 if v >= 0 else -13), textcoords="offset points",
                    ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=12.5, color=NAVY, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11.5, color=AXIS_TXT, fontweight="bold")
    header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- PDF embedding
CROPS = {"price_eps_pe": (0.085, 0.045), "bar": (0.165, 0.055)}


def crop_for_pdf(src, dst, kind):
    """Strip the standalone header/footnote: in the PDF, titles are typeset in HTML."""
    top, bot = CROPS[kind]
    im = Image.open(src); w, h = im.size
    im.crop((0, int(h * top), w, int(h * (1 - bot)))).save(dst)
