#!/usr/bin/python3.4
'''
contains:
    * describe data for part 1 of P1
    * bar, and two histogram graphs for part 4
    * statistics calculations for parts 5 and 6

options:
    -data - build latex tables
    -graphs - build graphics
todo:
'''
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-f", "--figures", help="generate figures for P1",
                    action="store_true")
parser.add_argument("-r", "--removeFiles", help="remove extraneous files",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
if args.figures:
    print("generating figures")
    figures = True
if args.removeFiles:
    remove_trash = True

import re
import numpy as np
import pandas as pd
import matplotlib as mpl
from math import ceil

# use fancy LaTeX backend for fonts
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


stroopdata = pd.read_csv('stroopdata.csv')
stroopdata.describe()

def df_describe():
    # descriptive statistics
    table = stroopdata.describe().to_latex()
    data_describe = 'data_describe.tex'
    f = open(data_describe, 'w')
    f.write( table )
    f.close()

def bar_graph():
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
    plt.xlabel('Subject \#')
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

# P1 histogram
def p1_histogram(x: pd.core.series.Series, Label: str, Title: str, Output: str):
    fig = plt.figure(figsize=(6.0, 7.5), dpi=100)
    ax = fig.add_subplot(111)

    histICS = ax.hist(x,
            bins = 6,
            color='b',
            alpha=0.8,
            label=Label
           )

    # add some text for labels, title, pretty legend, axes ticks
    plt.xlabel('Time (s)')
    plt.ylabel('$\#$ of Subjects in bin')
    plt.title(Title)

    leg = plt.legend(loc=2,fancybox=True, fontsize=14)
    leg.get_frame().set_alpha(0.5)

    xind = [ round(i,2) for i in histICS[1] ]
    plt.xticks( histICS[1], xind, rotation=-90)
    plt.savefig(Output)

if figures:
    # Create ICS histogram
    x = stroopdata['Incongruent']
    Label = 'Histogram of ICS Data'
    Title = r"\textbf{Histogram of ICS with 6 Bins}"
    Output = "histogram-ics.pdf"
    p1_histogram(x, Label, Title, Output)

    # Create CCS histogram
    x = stroopdata['Congruent']
    Label = 'Histogram of CCS Data'
    Title = r"\textbf{Histogram of CCS with 6 Bins}"
    Output = "histogram-ccs.pdf"
    p1_histogram(x, Label, Title, Output)

    # ICS histogram removing outliers
    x = stroopdata['Incongruent'].where(stroopdata['Incongruent'] < 30)
    x = x.dropna().sort_values()
    Label = 'Histogram of ICS Data Removing Outliers'
    Title = r"\textbf{Histogram of ICS removal of outliers}"
    Output = "histogram-ics-no-outliers.pdf"
    p1_histogram(x, Label, Title, Output)

if remove_trash:
    def purge(dir, pattern):
        for file in os.listdir(dir):
            if re.search(pattern, file):
                os.remove(os.path.join(dir, file))
    purge(".", "*.bbl")
