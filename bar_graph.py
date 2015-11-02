import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save

stroopdata = pd.read_csv('stroopdata.csv')
stroopdata.describe()

fig, ax = plt.subplots()

index = np.arange(stroopdata.shape[0])
bar_width = 0.35

opacity = 0.6

rects1 = plt.bar(index, stroopdata['Congruent'],
                 bar_width,
                 alpha=opacity,
                 color='k',
                 label='CCS Sample')

rects2 = plt.bar(index + bar_width, stroopdata['Incongruent'],
                 bar_width,
                 alpha=opacity,
                 color='b',
                 label='ICS Sample')

# add some text for labels, title and axes ticks
plt.xlabel('Subject')
plt.ylabel('Time (s)')
plt.title('Scores for CCS and ICS')
plt.xticks(index + bar_width, range(1,25))
plt.legend()

plt.tight_layout()
#plt.show()
#tikz_save('bar_graph.tex');
plt.savefig('bar_graph.pdf')
