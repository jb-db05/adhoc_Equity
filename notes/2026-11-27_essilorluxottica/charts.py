import pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as md
SPACE,BLUE,TIGER,MANGO,GOLD='#202945','#4B5F80','#FF6C0E','#FFA400','#FFC545'
plt.rcParams.update({'font.family':['DejaVu Sans'],'font.size':9,'text.color':SPACE,'axes.edgecolor':SPACE,
 'axes.labelcolor':SPACE,'xtick.color':SPACE,'ytick.color':SPACE})
d=pd.read_excel('/root/.claude/uploads/2e00f016-c895-5e5a-adef-7641daa52428/32d527cd-EL.xlsx').sort_values('Date')
d.columns=['date','px','eps','pe','m40','m200']; d=d.set_index('date')
def style(ax,ylab):
    for s in('top','right'):ax.spines[s].set_visible(False)
    ax.set_ylabel(ylab,fontweight='bold',style='italic',fontsize=8)
    ax.grid(axis='y',color='#D9D9D9',lw=.5); ax.tick_params(length=3)
def lab(ax,x,y,t):
    ax.annotate(t,(x,y),xytext=(6,0),textcoords='offset points',va='center',fontsize=8.5,fontweight='bold',
      bbox=dict(boxstyle='round,pad=.3',fc='white',ec=SPACE,lw=1),annotation_clip=False)
def leg(ax,items):
    ax.legend(handles=[plt.Line2D([],[],color=c,lw=2,ls=s,label=l) for l,c,s in items],loc='upper center',
      bbox_to_anchor=(.5,-.12),ncol=len(items),frameon=False,fontsize=8)
# 1 price
x=d[d.index>='2024-11-27']; fig,ax=plt.subplots(figsize=(10,2.9),dpi=180)
ax.plot(x.px.dropna().index,x.px.dropna(),color=SPACE,lw=1.3); ax.plot(x.m40.dropna().index,x.m40.dropna(),color=GOLD,lw=1.2); ax.plot(x.m200.dropna().index,x.m200.dropna(),color=TIGER,lw=1.4)
ax.axvline(pd.Timestamp('2026-10-20'),color=BLUE,ls='--',lw=1); ax.text(pd.Timestamp('2026-10-14'),300,'Q3 revenue\n20 Oct 2026',ha='right',va='top',fontsize=8,color=BLUE)
ax.set_title('EL FP: share price over two years',fontsize=11,fontweight='light'); style(ax,'EUR')
ax.xaxis.set_major_formatter(md.DateFormatter('%b %y')); ax.xaxis.set_major_locator(md.MonthLocator(interval=3))
lab(ax,x.index[-1],x.px.iloc[-1],f'{x.px.iloc[-1]:.2f}'); leg(ax,[('Close',SPACE,'-'),('40-day average',GOLD,'-'),('200-day average',TIGER,'-')])
fig.subplots_adjust(right=.9,bottom=.28); fig.savefig('chart1_price.png',facecolor='white'); plt.close()
# 2 PE
y=d[(d.index>='2016-11-27')].dropna(subset=['pe']); avg=y.pe.mean(); fig,ax=plt.subplots(figsize=(10,2.9),dpi=180)
ax.plot(y.pe.dropna().index,y.pe.dropna(),color=BLUE,lw=1.1); ax.axhline(avg,color=TIGER,ls='--',lw=1.3)
ax.set_title('EL FP: forward P/E over ten years',fontsize=11,fontweight='light'); style(ax,'TIMES')
ax.xaxis.set_major_locator(md.YearLocator()); ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
ax.set_xlim(pd.Timestamp('2016-11-27'),pd.Timestamp('2026-12-15'));lab(ax,y.index[-1],y.pe.iloc[-1],f'{y.pe.iloc[-1]:.1f}x'); ax.text(pd.Timestamp('2016-12-15'),avg+1.6,f'Ten-year average {avg:.1f}x',color=TIGER,fontsize=8.5,fontweight='bold',bbox=dict(fc='white',ec='none',pad=1))
leg(ax,[('Price / consensus EPS, next 12 months',BLUE,'-'),('Ten-year average',TIGER,'--')]); fig.subplots_adjust(right=.9,bottom=.28)
fig.savefig('chart2_pe.png',facecolor='white'); plt.close()
# 3 EPS
z=d[d.index>='2024-11-27'].dropna(subset=['eps']); fig,ax=plt.subplots(figsize=(10,2.9),dpi=180)
ax.plot(z.index,z.eps,color=SPACE,lw=1.5,label='EPS')
ax.set_title('EL FP: consensus earnings per share, next twelve months',fontsize=11,fontweight='light'); style(ax,'EUR')
ax.set_ylim(6.5,8.5); ax.xaxis.set_major_formatter(md.DateFormatter('%b %y')); ax.xaxis.set_major_locator(md.MonthLocator(interval=3))
lab(ax,z.index[-1],z.eps.iloc[-1],f'{z.eps.iloc[-1]:.2f}'); leg(ax,[('Consensus EPS, next 12 months',SPACE,'-')]); fig.subplots_adjust(right=.9,bottom=.28)
fig.savefig('chart3_eps.png',facecolor='white'); plt.close()
print(avg, z.eps.min(), z.eps.max(), z.eps.iloc[0])
