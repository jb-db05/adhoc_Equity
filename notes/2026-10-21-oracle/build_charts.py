"""Build the charts for the Oracle ad-hoc note from the author's Bloomberg export."""
import datetime as dt
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
import openpyxl

SPACE, BLUEBERRY, TIGER, MANGO, GOLD, MINT = '#202945', '#4B5F80', '#FF6C0E', '#FFA400', '#FFC545', '#3BAF90'
CLOSE = dt.date(2026, 10, 20)

family = 'Nunito' if any('Nunito' in f.name for f in font_manager.fontManager.ttflist) else 'DejaVu Sans'
plt.rcParams.update({'font.family': family, 'font.size': 10, 'text.color': SPACE,
                     'axes.edgecolor': SPACE, 'axes.labelcolor': SPACE, 'xtick.color': SPACE, 'ytick.color': SPACE,
                     'axes.linewidth': 0.8})

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
rows = [r for r in wb['Sheet1'].iter_rows(min_row=2, values_only=True) if r[0] and r[1] is not None]
rows = sorted((r for r in rows if r[0].date() <= CLOSE), key=lambda r: r[0])


def style(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.tick_params(direction='out', length=4, width=0.8)
    ax.grid(axis='y', color='#D9D9D9', linewidth=0.6)
    ax.set_axisbelow(True)


def legend(fig, items, top=0.80):
    """Legend on the right: square marker, bold uppercase name in the series colour, light line below."""
    y = top
    for colour, name, note in items:
        fig.add_artist(Rectangle((0.835, y - 0.018), 0.014, 0.036, transform=fig.transFigure, color=colour))
        fig.text(0.86, y, name.upper(), color=colour, fontsize=9.5, fontweight='bold', va='center')
        fig.text(0.86, y - 0.06, note, color=SPACE, fontsize=8.5, fontweight=300, va='center')
        y -= 0.20


def last_label(ax, x, y, text):
    ax.annotate(text, xy=(x, y), xytext=(8, 0), textcoords='offset points', va='center', fontsize=9,
                fontweight='bold', color=SPACE,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=SPACE, lw=1))


# Chart 1: share price and 200-day average since January 2024
r1 = [r for r in rows if r[0].date() >= dt.date(2024, 1, 1)]
d1 = [r[0] for r in r1]
fig, ax = plt.subplots(figsize=(10, 3.8), dpi=200)
fig.subplots_adjust(left=0.08, right=0.80, top=0.90, bottom=0.14)
ax.plot(d1, [r[1] for r in r1], color=SPACE, lw=1.3)
ax.plot([r[0] for r in r1 if r[5]], [r[5] for r in r1 if r[5]], color=TIGER, lw=1.6)
last_label(ax, d1[-1], r1[-1][1], f'{r1[-1][1]:.2f}')
style(ax)
ax.set_ylim(0, 360)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_title('Oracle share price and 200-day average', fontsize=12, fontweight=300)
ax.set_ylabel('USD', fontweight='bold', style='italic', fontsize=9)
legend(fig, [(SPACE, 'Share price', 'Daily close, USD'), (TIGER, '200-day average', 'Simple moving average')])
fig.savefig('chart1.png', facecolor='white')

# Chart 2: forward P/E over ten years with its median
start = dt.date(CLOSE.year - 10, CLOSE.month, CLOSE.day)
r2 = [r for r in rows if r[2] and r[0].date() > start]
median = statistics.median(r[2] for r in r2)
fig, ax = plt.subplots(figsize=(10, 3.8), dpi=200)
fig.subplots_adjust(left=0.08, right=0.80, top=0.90, bottom=0.14)
ax.plot([r[0] for r in r2], [r[2] for r in r2], color=TIGER, lw=1.3)
ax.axhline(median, color=BLUEBERRY, lw=1.3, ls=(0, (5, 3)))
last_label(ax, r2[-1][0], r2[-1][2], f'{r2[-1][2]:.1f}x')
style(ax)
ax.set_ylim(0, 50)
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_title('Oracle price to forward earnings', fontsize=12, fontweight=300)
ax.set_ylabel('P/E (X)', fontweight='bold', style='italic', fontsize=9)
legend(fig, [(TIGER, 'Forward P/E', 'Bloomberg consensus'), (BLUEBERRY, '10-year median', f'{median:.1f}x')])
fig.savefig('chart2.png', facecolor='white')

print(f'font={family} last price={r1[-1][1]} last P/E={r2[-1][2]:.2f} 10y median={median:.2f}')
