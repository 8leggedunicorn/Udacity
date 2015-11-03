import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

stroopdata = pd.read_csv('stroopdata.csv')
stroopdata.describe()

# descriptive statistics
table = stroopdata.describe().to_latex()
data_describe = 'data_describe.tex'
f = open(data_describe, 'w')
f.write( table )
f.close()

data = stroopdata.max() - stroopdata.min()
file = "range.txt"
f = open(file, 'w')
f.write( str(data) )
f.close()

# bar graph
fig = plt.subplots(figsize=(6.0, 4.5), dpi=100)

#fig, ax = plt.subplots()
bar_width = 0.35
opacity = 0.6

index = list(range(0,stroopdata.count()[0]))
rects1 = plt.bar(index, stroopdata.sort_values(by='Congruent')['Congruent'],
                 bar_width,
                 alpha=opacity,
                 color='k',
                 label='CCS Sample')

index = [ i + bar_width for i in index]
rects2 = plt.bar(index, stroopdata.sort_values(by='Congruent')['Incongruent'],
                 bar_width,
                 alpha=opacity,
                 color='b',
                 label='ICS Sample')

plt.axhline(y = stroopdata.mean()[0],
            xmin=-1,
            xmax = 24,
            linewidth=2,
            color='k',
            ls = 'dotted',
            label='Average for CCS Sample')

plt.axhline(y = stroopdata.median()[0],
            xmin=-1,
            xmax = 24,
            linewidth=2,
            color='r',
            ls = 'dashed',
            label='Median for CCS Sample')

# add some text for labels, title, pretty legend, axes ticks
plt.xlabel('Subject #')
plt.ylabel('Time (s)')
plt.title('Scores for CCS and ICS')

leg = plt.legend(loc=2,fancybox=True, fontsize=14)
leg.get_frame().set_alpha(0.5)

ccs_sort = stroopdata.sort_values(by='Congruent')
xloc = list(range(1,ccs_sort.count()[0] +1 ))
xloc = [ i + bar_width - 1 for i in xloc]
xind = [ i + 1 for i in ccs_sort.index ]
ymin_graph = int(ceil(stroopdata.min()[0])) - 1
ymax_graph = int(ceil(stroopdata.max()[1])) + 1
#yind = list(range(ymin_graph, ymax_graph + 1,2))
yind = list(range(0, ymax_graph + 1,2))

#plt.ylim(ymin_graph, ymax_graph)
plt.ylim(0, ymax_graph)
plt.xticks( xloc, xind)
plt.yticks( yind, yind)

plt.tight_layout()
plt.savefig('bar_graph.pdf')
