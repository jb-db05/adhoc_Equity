import datetime as d, openpyxl, statistics as st
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as md
from matplotlib.patches import Rectangle
SPACE,BLUEBERRY,TIGER,MANGO,GOLD='#202945','#4B5F80','#FF6C0E','#FFA400','#FFC545'
import matplotlib.font_manager as fm, os
for w in (300,400,700,800): fm.fontManager.addfont(os.path.expanduser(f'~/.fonts/NunitoSans-{w}.ttf'))
plt.rcParams.update({'font.family':'Nunito Sans','font.size':10,'text.color':SPACE,'axes.edgecolor':SPACE,
  'axes.labelcolor':SPACE,'xtick.color':SPACE,'ytick.color':SPACE})
wb=openpyxl.load_workbook('/root/.claude/uploads/9746c044-5665-561c-b0e4-2be86e403ba7/6a764bf9-EL.xlsx',read_only=True)
rows=sorted(r for r in wb.active.iter_rows(min_row=2,values_only=True))
def style(ax,xl,yl):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.tick_params(length=4); ax.set_xlabel(xl,fontweight='bold',style='italic',fontsize=8); ax.set_ylabel(yl,fontweight='bold',style='italic',fontsize=8)
def legend(fig,items,x=0.80,y=0.80):
    for i,(c,n,s) in enumerate(items):
        yy=y-i*0.17
        fig.patches.append(Rectangle((x,yy-0.01),0.014,0.025,transform=fig.transFigure,color=c))
        fig.text(x+0.022,yy,n,fontweight='bold',fontsize=8,color=c if c!=GOLD else MANGO,va='center')
        fig.text(x+0.022,yy-0.055,s,fontweight='normal',fontsize=7.5,va='center')
def lastlabel(ax,xv,yv,txt):
    ax.annotate(txt,(xv,yv),xytext=(8,0),textcoords='offset points',va='center',fontsize=9,fontweight='bold',
      bbox=dict(boxstyle='round,pad=0.3',fc='white',ec=SPACE,lw=1.2),annotation_clip=False)
# chart 1
s=d.datetime(2024,11,27); p=[r for r in rows if r[0]>=s and r[1]]
x=[r[0] for r in p]
fig,ax=plt.subplots(figsize=(10,2.85),dpi=180); fig.subplots_adjust(left=.07,right=.76,top=.88,bottom=.17)
ax.plot(x,[r[1] for r in p],color=SPACE,lw=1.4); ax.plot(x,[r[4] for r in p],color=GOLD,lw=1.3); ax.plot(x,[r[5] for r in p],color=TIGER,lw=1.3)
ax.axvline(d.datetime(2026,10,20),color=BLUEBERRY,ls='--',lw=1)
ax.text(d.datetime(2026,10,20),ax.get_ylim()[1]*0.995,'3Q26 revenue\n20 Oct 2026 ',ha='right',va='top',fontsize=8,color=BLUEBERRY)
ax.xaxis.set_major_formatter(md.DateFormatter('%b %y')); ax.xaxis.set_major_locator(md.MonthLocator(interval=3))
style(ax,'DATE','EUR'); ax.set_title('EL FP: share price over two years',fontsize=12,fontweight='normal')
lastlabel(ax,x[-1],p[-1][1],'172.15')
legend(fig,[(SPACE,'PRICE','Daily close'),(GOLD,'40-DAY AVERAGE','Simple moving average'),(TIGER,'200-DAY AVERAGE','Simple moving average')])
fig.savefig('chart1_price.png',facecolor='white'); plt.close()
# chart 2
s=d.datetime(2016,11,27); p=[r for r in rows if r[0]>=s and r[3]]; avg=st.mean(r[3] for r in p)
x=[r[0] for r in p]
fig,ax=plt.subplots(figsize=(10,2.85),dpi=180); fig.subplots_adjust(left=.07,right=.76,top=.88,bottom=.17)
ax.plot(x,[r[3] for r in p],color=SPACE,lw=1.3); ax.axhline(avg,color=TIGER,ls='--',lw=1.3)
ax.xaxis.set_major_locator(md.YearLocator(2)); ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
style(ax,'DATE','P/E (X)'); ax.set_title('EL FP: forward P/E over ten years',fontsize=12,fontweight='normal')
lastlabel(ax,x[-1],p[-1][3],f'{p[-1][3]:.1f}x')
legend(fig,[(SPACE,'FORWARD P/E','Next 12 months consensus'),(TIGER,'TEN-YEAR AVERAGE',f'{avg:.1f}x')],y=0.78)
fig.savefig('chart2_pe.png',facecolor='white'); plt.close(); print('avg',avg)
# chart 3
labs=['Group','North\nAmerica','EMEA','Asia-\nPacific','Wearables','Myopia\nmanagement']; v=[7.2,4.7,7.5,15.7,20,24]
cols=[BLUEBERRY,SPACE,SPACE,SPACE,TIGER,TIGER]
fig,ax=plt.subplots(figsize=(10,2.7),dpi=180); fig.subplots_adjust(left=.07,right=.76,top=.88,bottom=.22)
b=ax.bar(labs,v,color=cols,width=.6)
for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+.6,f'+{val:g}%',ha='center',fontsize=9,fontweight='bold')
ax.set_ylim(0,27); style(ax,'','GROWTH (%)'); ax.set_title('EssilorLuxottica: revenue growth in the third quarter of 2026',fontsize=12,fontweight='normal')
legend(fig,[(BLUEBERRY,'GROUP','Revenue EUR 7,486m'),(SPACE,'REGIONS','Constant exchange rates'),(TIGER,'GROWTH LINES','Wearables, myopia management')],y=0.8)
fig.savefig('chart3_q3growth.png',facecolor='white'); plt.close()
