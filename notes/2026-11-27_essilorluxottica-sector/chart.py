import datetime as d, openpyxl
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as md
from matplotlib.patches import Rectangle
SPACE,TIGER='#202945','#FF6C0E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':SPACE,'axes.edgecolor':SPACE,'axes.labelcolor':SPACE,'xtick.color':SPACE,'ytick.color':SPACE})
wb=openpyxl.load_workbook('/root/.claude/uploads/9746c044-5665-561c-b0e4-2be86e403ba7/6a764bf9-EL.xlsx',read_only=True)
rows=sorted(r for r in wb.active.iter_rows(min_row=2,values_only=True))
p=[r for r in rows if r[0]>=d.datetime(2024,11,27) and r[1] and r[2]]
b=p[0]; print(b[:3],p[-1][:3])
x=[r[0] for r in p]; pr=[r[1]/b[1]*100 for r in p]; ep=[r[2]/b[2]*100 for r in p]
print(pr[-1],ep[-1])
fig,ax=plt.subplots(figsize=(10,3.3),dpi=180); fig.subplots_adjust(left=.07,right=.76,top=.88,bottom=.17)
ax.plot(x,pr,color=SPACE,lw=1.4); ax.plot(x,ep,color=TIGER,lw=1.6); ax.axhline(100,color='#D9D9D9',lw=.8,zorder=0)
ax.xaxis.set_major_formatter(md.DateFormatter('%b %y')); ax.xaxis.set_major_locator(md.MonthLocator(interval=3))
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.set_xlabel('DATE',fontweight='bold',style='italic',fontsize=8); ax.set_ylabel('REBASED, 27 NOV 2024 = 100',fontweight='bold',style='italic',fontsize=8)
ax.set_title('EL FP: share price and expected earnings',fontsize=12)
for v,c in ((pr[-1],SPACE),(ep[-1],TIGER)):
    ax.annotate(f'{v:.0f}',(x[-1],v),xytext=(8,0),textcoords='offset points',va='center',fontsize=9,fontweight='bold',bbox=dict(boxstyle='round,pad=0.3',fc='white',ec=c,lw=1.2),annotation_clip=False)
for i,(c,n,t) in enumerate([(SPACE,'SHARE PRICE','Daily close'),(TIGER,'EXPECTED EPS','Consensus, next 12 months')]):
    yy=.78-i*.2; fig.patches.append(Rectangle((.80,yy-.01),.014,.03,transform=fig.transFigure,color=c))
    fig.text(.822,yy,n,fontweight='bold',fontsize=8,color=c,va='center'); fig.text(.822,yy-.06,t,fontsize=7.5,va='center')
fig.savefig('chart1_price_vs_eps.png',facecolor='white')
