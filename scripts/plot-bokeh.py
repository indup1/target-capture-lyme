from bokeh.models import Panel, Tabs
from bokeh.plotting import figure, output_file, show

import numpy as np
import math

norm_reads = open('n_results.txt', 'r')
norm_lines = norm_reads.readlines()[1:]
norm_reads.close()

norm_chromosomes = {}
current = ""

for line in norm_lines:
    temp = line.split()

    if current != temp[0]:
        current =  temp[0]
        norm_chromosomes[current] = []

    norm_chromosomes[current].append(temp[2])

hybrid_reads = open('h_results.txt', 'r')
hybrid_lines = hybrid_reads.readlines()[1:]
hybrid_reads.close()

hybrid_chromosomes = {}
current = ""

for line in hybrid_lines:
    temp = line.split()

    if current != temp[0]:
        current = temp[0]
        hybrid_chromosomes[current] = []

    hybrid_chromosomes[current].append(temp[2])

tab_list = []

for n_key, h_key in zip(norm_chromosomes, hybrid_chromosomes):
    pos = norm_chromosomes[n_key]
    pos1 = hybrid_chromosomes[h_key]

    n_y = np.array(pos)
    n_x = np.arange(start=1, stop=n_y.size + 1, step=1)

    h_y = np.array(pos1)
    h_x = np.arange(start=1, stop=h_y.size + 1, step=1)

    p = figure(plot_width=600, plot_height=400)
    p.line(n_x, n_y, line_width=2, color="blue")
    p.line(h_x, h_y, line_width=2, color="red")

    tab = Panel(child=p, title=h_key)
    tab_list.append(tab)

tabs = Tabs(tabs=tab_list)

show(tabs)
output_file("plots/lmao2.html")
