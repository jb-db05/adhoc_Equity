import sys, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import glob, os
for f in glob.glob(os.path.expanduser('~/.fonts/Nunito-*.ttf')): fm.fontManager.addfont(f)
SPACE, BLUEBERRY, TIGER, MANGO, GOLD, MINT, GREY = '#202945', '#4B5F80', '#FF6C0E', '#FFA400', '#FFC545', '#3BAF90', '#D9D9D9'
plt.rcParams.update({'font.family': 'Nunito', 'font.size': 11, 'text.color': SPACE,
    'axes.edgecolor': SPACE, 'axes.labelcolor': SPACE, 'xtick.color': SPACE, 'ytick.color': SPACE})
rows = [  # label, growth, group
 ('Leather goods and saddlery', 11, 'core'),
 ('Ready-to-wear and accessories', -2, 'cyc'),
 ('Silk and textiles', 1, 'cyc'),
 ('Other Hermès sectors', -1, 'cyc'),
 ('Watches', -6, 'cyc'),
 ('Perfumes and beauty', 8, 'oth'),
 ('Other products', 11, 'oth'),
]
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
y = [0, 1.6, 2.6, 3.6, 4.6, 6.2, 7.2]
for (lab, g, grp), yy in zip(rows, y):
    c = BLUEBERRY if g >= 0 else TIGER
    alpha = 0.45 if grp == 'oth' else 1
    ax.barh(yy, g, color=c, height=0.62, alpha=alpha)
    ax.text(g + (0.3 if g >= 0 else -0.3), yy, f'{g:+d}%'.replace('-','−'), va='center', ha='left' if g >= 0 else 'right',
            fontweight='bold', color=c, fontsize=11)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
ax.axvline(0, color=SPACE, lw=1)
ax.axvline(4.3, color=SPACE, lw=1, ls='--')
ax.text(4.4, 8.05, 'Group +4.3%', fontsize=10, color=SPACE, va='center')
for yy, t in [(-0.75, 'SCARCITY ENGINE · 47% OF SALES'), (0.85, 'CYCLICAL ENGINE · RUNS WITH THE LUXURY SECTOR'), (5.45, 'SMALLER LINES')]:
    ax.text(-8.9, yy, t, fontsize=9.5, ha='right', fontweight='bold', color=TIGER if 'SCAR' in t else (BLUEBERRY if 'CYC' in t else '#8a93a6'), va='center')
ax.set_xlim(-8.6, 14); ax.set_ylim(8.4, -1.2)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.set_xlabel('GROWTH AT CONSTANT EXCHANGE RATES, Q3 2026 (%)', fontweight='bold', style='italic', fontsize=9.5)
fig.tight_layout()
fig.savefig(sys.argv[1], facecolor='white')
