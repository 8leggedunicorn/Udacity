import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
fig = plt.subplots()

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

## add some text for labels, title and axes ticks
plt.xlabel('Subject')
plt.ylabel('Time (s)')
plt.title('Scores for CCS and ICS')
plt.xticks(index + bar_width, range(1,25))
plt.legend()
plt.tight_layout()
plt.savefig('bar_graph.pdf')
