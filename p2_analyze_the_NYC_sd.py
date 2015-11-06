#!/usr/bin/python3.4
'''
contains:
    This is a script meant to handle the generation and removal of the first
    project, The Stroop Effect, for Udacity's Data Analysis nanodegree.

todo:
'''
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-f", "--figures", help="generate figures for p1",
                    action="store_true")
parser.add_argument("-c", "--charts", help="generate data charts for p1",
                    action="store_true")
parser.add_argument("-r", "--removeFiles", help="remove extraneous files",
                    action="store_true")
buildPdfHelp="generate p1_stroop_effect.pdf or recompile if PDF exists"
parser.add_argument("-pdf", "--buildPdf", help=buildPdfHelp,
                    action="store_true")
args = parser.parse_args()

# initialize all switch variables to default false
charts = figures = remove_trash = buildPdf = False

if args.verbose:
    print("verbosity turned on")
if args.buildPdf:
    print("generating PDF")
    buildPdf = True
if args.figures:
    print("generating figures")
    figures = True
if args.charts:
    print("generating charts")
    charts = True
if args.removeFiles:
    remove_trash = True

import re
import numpy as np
import pandas as pd

"""
stroopdata = pd.read_csv('stroopdata.csv')
stroopdata.describe()
"""
chart_path = './charts'
figure_path = './figures'

if buildPdf:

    def run_command(Bin: str, Input: str):
        command = Bin + ' ' + Input
        print( "running", command )
        p = os.popen( command, "r" )
        while True:
            line = p.readline()
            if not line: break
            print ( line )

    # run TeX binary:
    TeXInput='p2_analyze_the_NYC_sd.tex'
    BibInput = os.path.splitext(TeXInput)[0]
    TeXBin = '/home/yigal/.bin/pdflatex'
    #PythonTexBin = '/home/yigal/.bin/pythontex'
    BibBin = '/home/yigal/.bin/biber'

    run_command(TeXBin, TeXInput)
    run_command(BibBin, BibInput)
    #run_command(PythonTexBin, TeXInput)
    run_command(TeXBin, BibInput)

    TeXOutput=os.path.splitext(TeXInput)[0] + '.pdf'

if charts:
    if not os.path.exists(chart_path):
        os.mkdir(chart_path)

    data_describe = 'data_describe.tex'
    data_describe = os.path.join(chart_path,data_describe)
    if not os.path.isfile(data_describe):
        def df_describe():
            # descriptive statistics
            table = stroopdata.describe().to_latex()
            f = open(data_describe, 'w')
            f.write( table )
            f.close()
            print(data_describe, "generated")
        df_describe()
    else:
        print(data_describe, "already generated")

if figures == True:
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

    def bar_graph(Output: str):
        # bar graph
        fig = plt.subplots(figsize=(6.0, 4.5), dpi=100)

        #fig, ax = plt.subplots()
        bar_width = 0.35
        opacity = 0.6

        # Set up CCS bars
        index = list(range(0,stroopdata.count()[0]))
        rects1 = plt.bar(index, stroopdata.sort_values(by='Congruent')['Congruent'],
                         bar_width,
                         alpha=opacity,
                         color='k',
                         label='CCS Sample')

        # Set up ICS bars
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
        plt.savefig(Output)
        #plt.savefig('')

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

    # Create figure directory if it doesn't exist:
    if not os.path.exists(figure_path):
        os.mkdir(figure_path)

    # Create ICS histogram if it doesn't exist:
    Output = "histogram-ics.pdf"
    Output = os.path.join(figure_path, Output)
    if not os.path.isfile(Output):
        print("generating", Output)
        x = stroopdata['Incongruent']
        Label = 'Histogram of ICS Data'
        Title = r"\textbf{Histogram of ICS with 6 Bins}"
        p1_histogram(x, Label, Title, Output)
    else:
        print("file", Output,"already exists")

    # Create CCS histogram if it doesn't exist:
    Output = "histogram-ccs.pdf"
    Output = os.path.join(figure_path, Output)
    if not os.path.isfile(Output):
        print("generating", Output)
        x = stroopdata['Congruent']
        Label = 'Histogram of CCS Data'
        Title = r"\textbf{Histogram of CCS with 6 Bins}"
        p1_histogram(x, Label, Title, Output)
    else:
        print("file", Output,"already exists")

    # Create ICS histogram wo outliers if it doesn't exist:
    Output = "histogram-ics-no-outliers.pdf"
    Output = os.path.join(figure_path, Output)
    if not os.path.isfile(Output):
        print("generating", Output)
        x = stroopdata['Incongruent'].where(stroopdata['Incongruent'] < 30)
        x = x.dropna().sort_values()
        Label = 'Histogram of ICS Data Removing Outliers'
        Title = r"\textbf{Histogram of ICS removal of outliers}"
        p1_histogram(x, Label, Title, Output)
    else:
        print("file", Output,"already exists")

    # Create bar graph if it doesn't exist:
    Output = 'bar_graph.pdf'
    Output = os.path.join(figure_path, Output)
    if not os.path.isfile(Output):
        print("generating", Output)
        bar_graph(Output)
    else:
        print("file", Output,"already exists")

if remove_trash:
    import shutil
    def purge(dir, pattern):
        for file in os.listdir(dir):
            if re.search(pattern, file):
                os.remove(os.path.join(dir, file))
                print("removed",os.path.join(dir, file))
        if os.path.isdir(chart_path):
            shutil.rmtree(chart_path)
            print('removed',chart_path, 'directory')
        if os.path.isdir(figure_path):
            shutil.rmtree(figure_path)
            print('removed',figure_path, 'directory')

    purge('.', "(argparse|.*\.(aux\.*|aux|bbl|bcf|blg|log|pdf|out|run.xml|txt))")
