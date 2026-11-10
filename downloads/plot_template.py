#!/usr/bin/env python3
"""MMIFusion plotting template (MIT). pip install matplotlib
Run: python plot_template.py
The data below are illustrative, not experimental results.
"""
import matplotlib.pyplot as plt

x=[1,2,3,4,5]
series={
    'Method A (demo)': [0.58,0.66,0.71,0.74,0.76],
    'Method B (demo)': [0.56,0.62,0.67,0.71,0.74],
    'Method C (demo)': [0.53,0.58,0.64,0.68,0.71],
}
colors=['#253B53','#BF5545','#619282']
markers=['o','s','^']; styles=['-','--',':']
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(5.2,3.5),layout='constrained')
for (label,y),color,marker,style in zip(series.items(),colors,markers,styles):
    ax.plot(x,y,label=label,color=color,marker=marker,linestyle=style,linewidth=1.8,markersize=5)
ax.set(xlabel='Experimental setting (replace)',ylabel='Metric (replace)',xticks=x,title='Illustrative data — replace before use')
ax.grid(alpha=.18);ax.legend(frameon=False)
fig.savefig('mmifusion_plot.pdf',bbox_inches='tight')
fig.savefig('mmifusion_plot.png',dpi=300,bbox_inches='tight')
print('Saved mmifusion_plot.pdf and mmifusion_plot.png')
