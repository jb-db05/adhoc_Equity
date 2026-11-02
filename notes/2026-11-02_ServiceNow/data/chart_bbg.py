import sys, openpyxl, datetime as dt
import matplotlib; matplotlib.use('Agg'); import matplotlib.patches
import matplotlib.pyplot as plt, matplotlib.dates as md
from matplotlib import font_manager as fm
S=sys.argv[1]
for f in ['nunito1','nunito2','nunito3','nunito4']: fm.fontManager.addfont(f'{S}/fonts/{f}.ttf')
SPACE,BLUEBERRY,TIGER,GOLD='#202945','#4B5F80','#FF6C0E','#FFC545'
plt.rcParams.update({'font.family':'Nunito','font.size':10.5,'text.color':SPACE,'axes.edgecolor':SPACE,
 'axes.labelcolor':SPACE,'xtick.color':SPACE,'ytick.color':SPACE})
ws=openpyxl.load_workbook(f'{S}/bbg/data.xlsx',data_only=True)['Sheet1']
r=sorted([x[:5] for x in ws.iter_rows(min_row=2,values_only=True) if x[0] and x[0]<=dt.datetime(2026,10,30)])
d=[x[0] for x in r]; p=[x[1] for x in r]; eps=[x[2] for x in r]; ma=[x[3] for x in r]
fig,ax=plt.subplots(figsize=(8.4,5.6),dpi=220)
ax2=ax.twinx()
ax.plot(d,eps,color=GOLD,lw=2.2)
ax2.plot(d,p,color=SPACE,lw=1.2); ax2.plot(d,ma,color=TIGER,lw=1.4)
for a in (ax,ax2): a.spines['top'].set_visible(False)
ax.set_ylim(0,5); ax2.set_ylim(0,250)
ax.set_ylabel('EXPECTED EPS, USD (LEFT)',fontweight='bold',style='italic',fontsize=9,color=SPACE)
ax2.set_ylabel('SHARE PRICE, USD (RIGHT)',fontweight='bold',style='italic',fontsize=9)
ax.set_xticks([dt.datetime(y,1,1) for y in range(2016,2027,2)]); ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
ax.set_xlim(d[0],dt.datetime(2028,7,1))
ax2.grid(axis='y',color='#D9D9D9',lw=0.6); ax.set_axisbelow(True); ax2.set_axisbelow(True)
ax2.annotate(f'USD {p[-1]:.2f}',(d[-1],p[-1]),xytext=(8,-8),textcoords='offset points',va='center',fontsize=9,fontweight='bold',
  bbox=dict(boxstyle='round,pad=0.3',fc='white',ec=SPACE,lw=1))
ax.annotate(f'USD {eps[-1]:.2f}',(d[-1],eps[-1]),xytext=(8,4),textcoords='offset points',va='center',fontsize=9,fontweight='bold',color=SPACE,
  bbox=dict(boxstyle='round,pad=0.3',fc='white',ec=GOLD,lw=1.4))
# legend (top left, square markers, bold uppercase name + light line)
items=[(SPACE,'SHARE PRICE','Weekly close (right)'),(TIGER,'40-WEEK AVERAGE','About 200 days (right)'),(GOLD,'EXPECTED EPS','Next twelve months, consensus (left)')]
for i,(c,n,s) in enumerate(items):
    y=0.97-i*0.085
    ax.add_patch(matplotlib.patches.Rectangle((0.02,y-0.028),0.022,0.028*1.5*0.66,transform=ax.transAxes,color=c,clip_on=False))
    ax.text(0.055,y,n,transform=ax.transAxes,color=c,fontsize=9,fontweight='bold',va='top')
    ax.text(0.055,y-0.035,s,transform=ax.transAxes,fontsize=8.5,fontweight=300,va='top')
fig.tight_layout(); fig.savefig(f'{S}/out/chart1.png',facecolor='white')
print(d[0],d[-1],p[-1],eps[-1])
