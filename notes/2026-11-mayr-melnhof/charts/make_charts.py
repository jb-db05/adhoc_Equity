"""Syz-style charts for the Mayr-Melnhof ad-hoc opinion. Usage: python make_charts.py <MMK Chart.xlsx> <outdir>"""
import sys, datetime as dt, statistics as st, openpyxl
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

SPACE, BLUE, TIGER, MANGO, GOLD, MINT, GREY = '#202945', '#4B5F80', '#FF6C0E', '#FFA400', '#FFC545', '#3BAF90', '#D9D9D9'
F = '/root/.fonts/nunito{}.ttf'
try:
    LIGHT, REG, BOLD, XB = (fm.FontProperties(fname=F.format(i)) for i in (1, 2, 3, 4))
except Exception:
    LIGHT = REG = BOLD = XB = fm.FontProperties(family='DejaVu Sans')
plt.rcParams.update({'text.color': SPACE, 'axes.edgecolor': SPACE, 'xtick.color': SPACE, 'ytick.color': SPACE,
                     'axes.linewidth': .8, 'xtick.major.width': .8, 'ytick.major.width': .8})

def fp(base, size): p = base.copy(); p.set_size(size); return p

def style(ax):
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.grid(axis='y', color=GREY, lw=.6); ax.set_axisbelow(True)
    for l in ax.get_xticklabels() + ax.get_yticklabels(): l.set_fontproperties(fp(REG, 9))

def tag(ax, x, y, text, color=SPACE):
    ax.annotate(text, (x, y), xytext=(6, 0), textcoords='offset points', va='center', fontproperties=fp(XB, 9.5),
                color=color, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1.2), annotation_clip=False)

def load(path):
    ws = openpyxl.load_workbook(path, data_only=True).active
    rows = sorted(r for r in ws.iter_rows(min_row=2, values_only=True) if r[0])
    return rows

def chart_price_pe(rows, out):
    d = [r[0] for r in rows]; px = [r[1] for r in rows]; ma = [r[3] for r in rows]; pe = [r[4] for r in rows]
    last = rows[-1]; start10 = last[0] - dt.timedelta(days=3652)
    pe10 = [r[4] for r in rows if r[0] >= start10]; avg, sd = st.mean(pe10), st.pstdev(pe10)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7.2), dpi=200, sharex=True, gridspec_kw=dict(height_ratios=[1.7, 1], hspace=.12))
    # price panel
    a1.plot(d, px, color=SPACE, lw=1.4, label='Share price')
    a1.plot(d, ma, color=TIGER, lw=1.4, label='40-week moving average')
    pk = max(rows, key=lambda r: r[1]); lo = min(rows, key=lambda r: r[1])
    a1.scatter([pk[0]], [pk[1]], s=22, color=SPACE, zorder=5)
    a1.annotate(f'Peak EUR {pk[1]:.0f}\n{pk[0]:%B %Y}', (pk[0], pk[1]), xytext=(10, 6), textcoords='offset points',
                fontproperties=fp(BOLD, 9), va='bottom', color=SPACE)
    a1.scatter([lo[0]], [lo[1]], s=22, color=TIGER, zorder=5)
    a1.annotate(f'Low EUR {lo[1]:.2f} on {lo[0]:%-d %b %Y}\nlowest since 2014', (lo[0], lo[1]), xytext=(-8, -8), textcoords='offset points',
                ha='right', va='top', fontproperties=fp(BOLD, 9), color=TIGER)
    deal = dt.datetime(2026, 11, 9)
    a1.axvline(deal, color=BLUE, lw=.9, ls=(0, (3, 2)))
    a1.annotate('KPS deal\n9 Nov 2026', (deal, 150), xytext=(-6, 0), textcoords='offset points', ha='right',
                fontproperties=fp(BOLD, 9), color=BLUE)
    tag(a1, last[0], last[1], f'{last[1]:.2f}'); tag(a1, last[0], last[3] + 9, f'{last[3]:.1f}', TIGER)
    a1.set_ylim(35, 215); style(a1)
    a1.set_ylabel('EUR', fontproperties=fp(BOLD, 9), style='italic')
    leg = a1.legend(loc='upper left', frameon=False, prop=fp(BOLD, 9.5))
    for t, c in zip(leg.get_texts(), (SPACE, TIGER)): t.set_color(c)
    # P/E panel
    a2.fill_between([start10, last[0]], avg - sd, avg + sd, color=BLUE, alpha=.10, lw=0)
    a2.axhline(avg, color=BLUE, lw=1, ls=(0, (4, 2)))
    a2.plot(d, pe, color=SPACE, lw=1.3)
    a2.text(d[0] + dt.timedelta(days=20), 19.2, f'Dashed line: 10-year average {avg:.1f}x', fontproperties=fp(BOLD, 9), color=BLUE)
    a2.text(d[0] + dt.timedelta(days=20), 17.6, f'Shaded band: plus or minus one standard deviation ({avg - sd:.1f}x to {avg + sd:.1f}x)', fontproperties=fp(LIGHT, 8.5), color=BLUE)
    tag(a2, last[0], last[4], f'{last[4]:.1f}x', TIGER)
    a2.set_ylim(4, 21); style(a2)
    a2.set_ylabel('FORWARD P/E', fontproperties=fp(BOLD, 9), style='italic')
    a2.xaxis.set_major_locator(mdates.YearLocator(2)); a2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    for l in a2.get_xticklabels(): l.set_fontproperties(fp(REG, 9))
    a1.set_xlim(d[0], last[0] + dt.timedelta(days=60))
    fig.savefig(out, facecolor='white', bbox_inches='tight', pad_inches=.15); plt.close(fig)
    return avg, sd

def chart_sotp(price, out, shares=20.0, net_cash=(0.8, 0.85, 0.9), stake=0.4, special=(0.5, 0.6)):
    nc_lo, nc, nc_hi = (x * 1000 / shares for x in net_cash); st_ = stake * 1000 / shares; bp = price - nc - st_
    fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
    w = .56; xs = [0, 1, 2, 3.25]
    # waterfall: net cash, stake, Board & Paper, share price
    ax.bar(xs[0], nc, w, color=SPACE)
    ax.bar(xs[1], st_, w, bottom=nc, color=BLUE)
    ax.bar(xs[2], bp, w, bottom=nc + st_, color=TIGER)
    ax.bar(xs[3], price, w, color='white', edgecolor=SPACE, lw=1.6)
    for a, b in ((0, 1), (1, 2), (2, 3)):
        y = [nc, nc + st_, price][a]
        ax.plot([xs[a] + w / 2, xs[b] - w / 2], [y, y], color=SPACE, lw=.7, ls=(0, (2, 2)))
    # net cash range whisker
    ax.errorbar(xs[0], nc, yerr=[[nc - nc_lo], [nc_hi - nc]], color=GOLD, capsize=6, lw=1.6, capthick=1.6)
    # special distribution bracket inside the net cash bar
    s_lo, s_hi = (x * 1000 / shares for x in special)
    ax.bar(xs[0] - w / 2 - .07, s_hi, .05, color=MANGO); ax.plot([xs[0] - w / 2 - .12, xs[0] - w / 2 - .02], [s_lo, s_lo], color='white', lw=1.5)
    ax.annotate(f'of which planned\nspecial distribution\nEUR {s_lo:.0f} to {s_hi:.0f}', (xs[0] - w / 2 - .1, s_hi / 2), xytext=(-8, 0),
                textcoords='offset points', ha='right', va='center', fontproperties=fp(BOLD, 9), color=MANGO)
    lab = dict(ha='center', fontproperties=fp(XB, 15))
    ax.text(xs[0], nc / 2, f'{nc:.1f}', color='white', va='center', **lab)
    ax.text(xs[1], nc + st_ / 2, f'{st_:.1f}', color='white', va='center', **lab)
    ax.text(xs[2], nc + st_ + bp / 2, f'{bp:.1f}', color='white', va='center', **lab)
    ax.text(xs[3], price / 2, f'{price:.2f}', color=SPACE, va='center', **lab)
    ax.text(xs[2], price + 2.5, f'About EUR {bp * shares / 1000:.2f}bn\nfor the whole business', ha='center', va='bottom',
            fontproperties=fp(BOLD, 9), color=TIGER)
    ax.text(xs[1], nc + st_ + 2.5, f'{(nc + st_) / price:.0%} of the\nshare price', ha='center', va='bottom', fontproperties=fp(BOLD, 9), color=BLUE)
    ax.set_xticks(xs, ['Net cash after\nclosing', '30% stake in\nPackaging', 'Implied value of\nBoard & Paper', 'Share price\n11 Nov 2026'])
    style(ax); ax.grid(False); ax.spines['left'].set_visible(False); ax.set_yticks([])
    for l in ax.get_xticklabels(): l.set_fontproperties(fp(BOLD, 10))
    ax.set_xlim(-1.35, 3.7); ax.set_ylim(0, price * 1.2)
    fig.savefig(out, facecolor='white', bbox_inches='tight', pad_inches=.15); plt.close(fig)
    return nc, st_, bp

if __name__ == '__main__':
    rows = load(sys.argv[1]); out = sys.argv[2]
    print('P/E avg, sd:', chart_price_pe(rows, f'{out}/chart_price_pe.png'))
    print('SOTP per share:', chart_sotp(rows[-1][1], f'{out}/chart_sotp.png'))
