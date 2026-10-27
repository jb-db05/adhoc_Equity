import sys, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
SPACE, BLUEBERRY, TIGER, MANGO, GOLD = '#202945', '#4B5F80', '#FF6C0E', '#FFA400', '#FFC545'
plt.rcParams.update({'font.family':'Nunito','font.size':10,'text.color':SPACE,'axes.edgecolor':SPACE,
 'axes.labelcolor':SPACE,'xtick.color':SPACE,'ytick.color':SPACE,'axes.linewidth':0.8})
src, out = sys.argv[1], sys.argv[2]
df = pd.read_excel(src); df.columns = ['date','px','eps','pe','ma40','ma200']
df = df.dropna(subset=['px']).sort_values('date').set_index('date')
def style(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#D9D9D9', lw=0.6); ax.set_axisbelow(True)

# Chart 1: price and 200-day average since 2023
d = df.loc['2023-01-01':]
fig, ax = plt.subplots(figsize=(10,4.6), dpi=180)
ax.plot(d.index, d.px, color=SPACE, lw=1.3, label='Share price')
ax.plot(d.index, d.ma200, color=TIGER, lw=1.6, label='200-day average')
for y,lab in [(43.67,'CAD 43.67 (7 Oct low)'),(48.40,'CAD 48.40 (17 Sep high)')]:
    ax.axhline(y, color=BLUEBERRY, lw=0.8, ls=(0,(4,3)))
    ax.text(d.index[0], y+0.5, lab, color=BLUEBERRY, fontsize=8.5, fontweight='bold')
last = d.px.iloc[-1]
ax.annotate(f'CAD {last:.2f}', xy=(d.index[-1], last), xytext=(8,-4), textcoords='offset points', fontsize=9, fontweight='bold',
            color=SPACE, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=SPACE, lw=1))
ax.set_title('Cenovus share price and 200-day average, Jan 2023 to 26 Oct 2026', fontsize=12, fontweight=300)
ax.set_ylabel('CAD PER SHARE', fontweight='bold', style='italic', fontsize=8.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,7])); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
ax.set_xlim(d.index[0], d.index[-1]+pd.Timedelta(days=75)); style(ax)
fig.tight_layout(); fig.savefig(f'{out}/chart1_price.png', facecolor='white'); plt.close(fig)

# Chart 2: forward EPS vs forward P/E since 2024
d = df.loc['2024-01-01':].copy(); d[['eps','pe']] = d[['eps','pe']].ffill()
fig, (a1,a2) = plt.subplots(2,1, figsize=(10,5.2), dpi=180, sharex=True, gridspec_kw={'hspace':0.18})
a1.plot(d.index, d.eps, color=TIGER, lw=1.8)
a1.set_ylabel('FWD EPS, CAD', fontweight='bold', style='italic', fontsize=8.5)
a1.set_title('Consensus forward EPS (top) and forward P/E (bottom), Jan 2024 to 26 Oct 2026', fontsize=12, fontweight=300)
pe = d.pe.where((d.pe>0)&(d.pe<40))
med = df.pe.loc['2021':].pipe(lambda s: s[(s>0)&(s<60)]).median()
a2.plot(d.index, pe, color=SPACE, lw=1.4)
a2.axhline(med, color=BLUEBERRY, lw=0.9, ls=(0,(4,3)))
a2.text(pd.Timestamp('2025-09-01'), med-2.6, f'Median since 2021: {med:.1f}x', color=BLUEBERRY, fontsize=8.5, fontweight='bold')
a2.set_ylabel('FWD P/E, X', fontweight='bold', style='italic', fontsize=8.5)
for a,s,fmt in [(a1,d.eps,'CAD {:.2f}'),(a2,d.pe,'{:.1f}x')]:
    a.annotate(fmt.format(s.iloc[-1]), xy=(d.index[-1], s.iloc[-1]), xytext=(8,-4), textcoords='offset points', fontsize=9,
               fontweight='bold', color=SPACE, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=SPACE, lw=1))
    style(a)
a2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10])); a2.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
a2.set_xlim(d.index[0], d.index[-1]+pd.Timedelta(days=60))
fig.subplots_adjust(left=0.08,right=0.93,top=0.92,bottom=0.08); fig.savefig(f'{out}/chart2_eps_pe.png', facecolor='white'); plt.close(fig)
print('median pe', med)
