import pandas as pd
import numpy as np
import matplotlib as mpl

stroopdata = pd.read_csv('stroopdata.csv')

mpl.use('pgf')
pgf_with_lualatex = {
    "text.usetex": True,
    "pgf.rcfonts": False,   # Do not set up fonts from rc parameters.
    "pgf.texsystem": "lualatex",
    "pgf.preamble": [
        r'\usepackage[no-math]{fontspec}',
        r'\usepackage{newtxtext,newtxmath}',
        ]
}
mpl.rcParams.update(pgf_with_lualatex)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(6.0, 7.5), dpi=100)

#fig = plt.subplots(figsize=(6.0, 4.5), dpi=100)
ax = fig.add_subplot(111)

x = stroopdata['Incongruent']

histICS = ax.hist(x,
        bins = 6,
        color='b',
        alpha=0.8,
        label='Histogram of ICS Sample'
       )

# add some text for labels, title, pretty legend, axes ticks
plt.xlabel('Time (s)')
plt.ylabel('$\#$ of Subjects in bin')
plt.title(r'\textbf{Histogram of ICS with 6 Bins}')

leg = plt.legend(loc=2,fancybox=True, fontsize=14)
leg.get_frame().set_alpha(0.5)

xind = [ round(i,2) for i in histICS[1] ]
plt.xticks( histICS[1], xind, rotation=-90)
plt.savefig("figure.pdf")
