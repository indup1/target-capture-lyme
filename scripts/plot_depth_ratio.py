 import bokeh
from bokeh.models import Panel, Tabs
from bokeh.plotting import figure, output_file, show
from operator import add

import numpy as np
import math

# Hybrid runs
runs = ['SRR2034333.1', 'SRR2034334.1', 'SRR2034335.1', 'SRR2034336.1', 'SRR2034337.1',
'SRR2034338.1',
'SRR2034339.1', 'SRR2034340.1', 'SRR2034341.1', 'SRR2034342.1']

# Normal method runs
# norm_runs = ['SRR9616106', 'SRR9616113', 'SRR9616115', 'SRR9616121', 'SRR9616125',
# 'SRR9616129', 'SRR9616130',
# 'SRR9616133', 'SRR9616136', 'SRR9616137']

norm_runs = ['10071001.l10071001.000H3LCYN.1', '10071002.l10071002.000H3LCYN.1',
'10071003.l10071003.000H3LCYN.1',
'10081001.l10081001.000H3LCYN.1', '10081004.l10081004.000H3LCYN.1']

# Function to parse .txt version of .bam file
def read_bam(filename):
    # Open file, read in lines
    path = "../depths/" + filename + ".txt" 
    reads = open(path)
    lines = reads.readlines()
    reads.close()
    # Dictionary to differentiate between plasmids
    chromosomes = {}
    current = ""

    # Loop through lines. If we see a new plasmid, change to that. 
    # Regardless, add next depth reading to plasmid.
    for line in lines: 
        temp = line.split()
        if current != temp[0]:
            current = temp[0]
            chromosomes[current] = []
        chromosomes[current].append(int(temp[2]))
    return chromosomes

# Lists of dictionaries for each run, hybrid and normal.
depths = [read_bam(run) for run in runs]
norm_depths = [read_bam(run) for run in norm_runs]
tab_list = []
print(depths[0].keys())
print(norm_depths[0].keys())
# Iterate through each plasmid
for key in depths[0]:
    # Find average depth for hybrids
    pos = [run[key] for run in depths] 
    total = [sum(x) for x in zip(*pos)] 
    average = [x/10 for x in total]

    # Set up ndarrays for plotting
    y = np.array(average)
    x = np.arange(start=1, stop=y.size + 1, step=1)

    # Find aerage depth for normal runs
    norm_pos = [run[key] for run in norm_depths] 
    norm_total = [sum(x) for x in zip(*norm_pos)] 
    norm_average = [x/5 for x in norm_total]

    # Set up ndarrays for plotting
    norm_y = np.array(norm_average)
    norm_x = np.arange(start=1, stop=norm_y.size + 1, step=1)

    # Find percentage of the time hybrid does better vs percentage normal does better.
    hybrid = 0
    normal = 0
    ratio = []
    for h, n in zip(y, norm_y):
        if h > n: 
            hybrid += 1
        elif n > h:
            normal += 1
        if n == 0 and h != 0: 
            ratio.append(h) 
        elif n==0 and h==0: 
            ratio.append(1)
        else: 
            ratio.append(h/n)

    print("HYBRID %: " + str(hybrid/len(y)))

    print("NORMAL %: " + str(normal/len(norm_y)))

    nd_ratio = np.array(ratio)

    p = figure(plot_width=600, plot_height=400, title='Ratio of average read depth of hybrid capture vs non-hybrid capture samples',
        x_axis_label='Read depth ratio', y_axis_label='Position in plasmid') 
    p.line(x, nd_ratio, line_width=2, color='blue')

    # p.line(x, y, line_width=2, color='red')
    # p.line(norm_x, norm_y, line_width=2, color='blue')

    tab = Panel(child=p, title=key) 
    tab_list.append(tab)

tabs = Tabs(tabs=tab_list)
show(tabs) 
output_file("plots/ratio.html")