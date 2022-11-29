import bokeh
from bokeh.models import Panel, Tabs
from bokeh.plotting import figure, output_file, show
from operator import add
from scipy.stats import ttest_ind

import numpy as np 
import math

# Hybrid runs
runs = ['SRR2034333.1', 'SRR2034334.1', 'SRR2034335.1', 'SRR2034336.1', 'SRR2034337.1',
'SRR2034338.1',
'SRR2034339.1', 'SRR2034340.1', 'SRR2034341.1', 'SRR2034342.1']

# Normal method runs
norm_runs = ['SRR9616106', 'SRR9616113', 'SRR9616115', 'SRR9616121', 'SRR9616125',
'SRR9616129', 'SRR9616130',
'SRR9616133', 'SRR9616136', 'SRR9616137']

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

# Loop through lines. If we see a new plasmid, change to that. Regardless, add next 
# depth reading to plasmid.
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

# Iterate through each plasmid
for key in depths[0]:
    # Find average depth for hybrids 
    pos = [run[key] for run in depths] 
    total = [sum(x) for x in zip(*pos)] 
    average = [x/10 for x in total]

    # Find average depth for normal runs
    norm_pos = [run[key] for run in norm_depths] 
    norm_total = [sum(x) for x in zip(*norm_pos)] 
    norm_average = [x/10 for x in norm_total]

    # Run paired t-test
    # res = ttest_ind(average, norm_average)

    print("PLASMID: " + key)
    # print("T-STATISTIC: " + str(res[0]), "P-VALUE: " + str(res[1])) 
    print(ttest_ind(average, norm_average)) 
    print("=================================")