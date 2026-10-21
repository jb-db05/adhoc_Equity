"""Build the charts for the CATL ad-hoc opinion from a Bloomberg export.

Usage: python make_charts.py <bloomberg_export.xlsx> <output_dir>
Expected columns (Sheet1): Date, Last Price, BEst EPS, BEst P/E Ratio, SMAVG (40), SMAVG (200).
"""
import sys
import datetime as dt
import statistics as st

import openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches

SPACE, BLUEBERRY, TIGER, MANGO, GOLD, MINT = '#202945', '#4B5F80', '#FF6C0E', '#FFA400', '#FFC545', '#3BAF90'
plt.rcParams.update({'font.family': 'Nunito', 'font.size': 10, 'text.color': SPACE,
                     'axes.edgecolor': SPACE, 'axes.labelcolor': SPACE, 'xtick.color': SPACE, 'ytick.color': SPACE,
                     'axes.linewidth': 0.8})

src, out = sys.argv[1], sys.argv[2]
ws = openpyxl.load_workbook(src, data_only=True)['Sheet1']
rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None][::-1]

def series(col, start):
    return [(r[0], r[col]) for r in rows if r[col] is not None and r[0] >= start]

def style(ax, ylabel):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#D9D9D9', linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_ylabel(ylabel, fontweight='bold', style='italic', fontsize=8.5)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
    ax.tick_params(labelsize=8.5)

def legend(fig, items, x=0.815, y=0.80, step=0.19):
    for name, sub, colour in items:
        fig.patches.append(matplotlib.patches.Rectangle((x, y - 0.018), 0.012, 0.036, color=colour,
                                                        transform=fig.transFigure, figure=fig))
        fig.text(x + 0.022, y, name, color=colour, fontsize=8.5, fontweight='bold', va='center')
        fig.text(x + 0.022, y - 0.065, sub, color=SPACE, fontsize=7.5, fontweight=300, va='center')
        y -= step

def last_label(ax, d, v, text, colour=SPACE):
    ax.annotate(text, (d, v), xytext=(8, 0), textcoords='offset points', va='center', fontsize=8,
                fontweight='bold', color=colour,
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=colour, lw=1))

# Chart 1: share price with 40-day and 200-day averages
start = dt.datetime(2024, 1, 1)
px, ma40, ma200 = series(1, start), series(4, start), series(5, start)
fig = plt.figure(figsize=(10, 3.5), dpi=200)
ax = fig.add_axes([0.07, 0.17, 0.70, 0.72])
ax.plot(*zip(*px), color=SPACE, lw=1.1)
ax.plot(*zip(*ma40), color=BLUEBERRY, lw=1.1, ls='--')
ax.plot(*zip(*ma200), color=TIGER, lw=1.6)
ax.axhline(211.39, color=TIGER, lw=0.8, ls=':')
ax.text(px[0][0], 211.39 + 6, 'April 2025 low: CNY 211.4', fontsize=7.5, color=TIGER)
last_label(ax, px[-1][0], px[-1][1], f'{px[-1][1]:.1f}')
last_label(ax, ma200[-1][0], ma200[-1][1], f'{ma200[-1][1]:.1f}', TIGER)
style(ax, 'CNY')
ax.set_title('Share price and moving averages, January 2024 to October 2026', fontsize=10.5, fontweight=300)
legend(fig, [('SHARE PRICE', 'Daily close, CNY', SPACE), ('40-DAY AVERAGE', 'Short-term trend', BLUEBERRY),
             ('200-DAY AVERAGE', 'Long-term trend, now falling', TIGER)])
fig.savefig(f'{out}/chart1_price.png', facecolor='white')
plt.close(fig)

# Chart 2: forward P/E with its average and one standard deviation band since 2023
start = dt.datetime(2023, 1, 1)
pe = series(3, start)
vals = [v for _, v in pe]
mean, sd = st.mean(vals), st.pstdev(vals)
fig = plt.figure(figsize=(10, 3.1), dpi=200)
ax = fig.add_axes([0.07, 0.18, 0.70, 0.71])
ax.fill_between([pe[0][0], pe[-1][0]], mean - sd, mean + sd, color=MANGO, alpha=0.18, lw=0)
ax.plot(*zip(*pe), color=SPACE, lw=1.1)
ax.axhline(mean, color=TIGER, lw=1.2, ls='--')
last_label(ax, pe[-1][0], pe[-1][1], f'{pe[-1][1]:.1f}x')
style(ax, 'TIMES EARNINGS')
ax.set_title('Price-to-earnings ratio on current-year expected earnings, 2023 to October 2026', fontsize=10.5, fontweight=300)
legend(fig, [('P/E', 'Price / current-year consensus EPS', SPACE), ('AVERAGE SINCE 2023', f'{mean:.1f}x', TIGER),
             ('NORMAL RANGE', f'± 1 st. dev.: {mean - sd:.1f}x to {mean + sd:.1f}x', MANGO)])
fig.savefig(f'{out}/chart2_pe.png', facecolor='white')
plt.close(fig)
print(f'P/E average since 2023 {mean:.2f}, sd {sd:.2f}, last {pe[-1][1]:.2f}')

# Chart 3: share price and consensus EPS for 2026, rebased to 100 at the start of the year
# (the Bloomberg EPS series rolls to the next financial year each January, so the chart starts in 2026)
px, eps = series(1, dt.datetime(2025, 12, 31)), series(2, dt.datetime(2026, 1, 1))
fig = plt.figure(figsize=(10, 3.1), dpi=200)
ax = fig.add_axes([0.07, 0.18, 0.70, 0.71])
ax.plot([d for d, _ in px], [v / px[0][1] * 100 for _, v in px], color=SPACE, lw=1.1)
ax.plot([d for d, _ in eps], [v / eps[0][1] * 100 for _, v in eps], color=TIGER, lw=1.6)
ax.axhline(100, color=SPACE, lw=0.6)
last_label(ax, px[-1][0], px[-1][1] / px[0][1] * 100, f'{px[-1][1] / px[0][1] * 100:.0f}')
last_label(ax, eps[-1][0], eps[-1][1] / eps[0][1] * 100, f'{eps[-1][1] / eps[0][1] * 100:.0f}', TIGER)
style(ax, 'INDEX, END 2025 = 100')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xlim(px[0][0], px[-1][0] + dt.timedelta(days=4))
ax.set_title('Share price versus consensus 2026 earnings per share', fontsize=10.5, fontweight=300)
legend(fig, [('SHARE PRICE', 'Rebased to 100', SPACE), ('CONSENSUS EPS 2026', 'Bloomberg estimate, rebased', TIGER)])
fig.savefig(f'{out}/chart3_price_vs_eps.png', facecolor='white')
plt.close(fig)
peak = max(eps, key=lambda x: x[1])
print('EPS start', eps[0], 'peak', peak, 'last', eps[-1], f'{eps[-1][1] / peak[1] - 1:.1%}', 'px start', px[0], 'last', px[-1])
