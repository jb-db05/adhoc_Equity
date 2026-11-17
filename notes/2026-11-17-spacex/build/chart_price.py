import sys, datetime as dt, openpyxl, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.patches import Rectangle
xl, out = sys.argv[1], sys.argv[2]
SPACE, TIGER = '#202945', '#FF6C0E'
plt.rcParams.update({'font.family': 'Nunito', 'font.size': 11, 'text.color': SPACE, 'axes.edgecolor': SPACE,
    'axes.labelcolor': SPACE, 'xtick.color': SPACE, 'ytick.color': SPACE, 'axes.linewidth': 0.9})
def d(x): return x if isinstance(x, dt.datetime) else dt.datetime(1899, 12, 30) + dt.timedelta(days=x)
ws = openpyxl.load_workbook(xl, data_only=True)['Sheet1']
rows = sorted((d(r[0]), r[3], r[4]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None and r[3] is not None)
rows = [r for r in rows if r[0] >= dt.datetime(2026, 6, 12)]   # 11 June is the IPO price, not a traded close
dates = [r[0] for r in rows]; px = [r[1] for r in rows]
ma = [(r[0], r[2]) for r in rows if r[2] is not None]
fig = plt.figure(figsize=(10, 4.6), dpi=200)
ax = fig.add_axes([0.08, 0.13, 0.6, 0.74])
ax.plot(dates, px, color=SPACE, lw=1.6)
ax.plot([m[0] for m in ma], [m[1] for m in ma], color=TIGER, lw=1.6)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.yaxis.grid(True, color='#D9D9D9', lw=0.6); ax.set_axisbelow(True); ax.tick_params(length=4, width=0.8)
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_ylim(90, 220); ax.set_xlim(dates[0] - dt.timedelta(days=2), dates[-1] + dt.timedelta(days=2))
ax.set_ylabel('USD', fontweight='bold', style='italic', fontsize=10)
ax.annotate(f'{px[-1]:.2f}', xy=(dates[-1], px[-1]), xytext=(8, 0), textcoords='offset points', va='center', fontweight='bold',
    fontsize=10, color=SPACE, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=SPACE, lw=1), annotation_clip=False)
fig.text(0.38, 0.93, 'Share price and 40-day moving average', ha='center', fontweight='light', fontsize=13)
items = [(SPACE, 'SHARE PRICE', f'Daily close, last USD {px[-1]:.2f}'), (TIGER, '40-DAY AVERAGE', f'Simple average, last USD {ma[-1][1]:.2f}')]
for i, (col, name, sub) in enumerate(items):
    yy = 0.74 - i * 0.135
    fig.patches.append(Rectangle((0.745, yy - 0.012), 0.018, 0.034, transform=fig.transFigure, color=col, figure=fig))
    fig.text(0.775, yy, name, color=col, fontweight='bold', fontsize=11, va='bottom')
    fig.text(0.775, yy - 0.012, sub, color=SPACE, fontweight='light', fontsize=10, va='top')
fig.savefig(out, facecolor='white')
print(dates[0].date(), px[0], dates[-1].date(), px[-1], ma[0][0].date(), ma[-1][1], len(px))
