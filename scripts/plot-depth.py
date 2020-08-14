import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import math

reads = open('results.txt', 'r')
lines = reads.readlines()[1:]
reads.close()

chromosomes = {}
current = ""

for line in lines:
    temp = line.split()

    if current != temp[0]:
        current =  temp[0]
        chromosomes[current] = []

    chromosomes[current].append(temp[2])

N = len(chromosomes)
cols = 4
rows = int(math.ceil(N / cols))

gs = gridspec.GridSpec(rows, cols)
fig = plt.figure()
    
for key, n in zip(chromosomes, range(N)):
    pos = chromosomes[key]
    y = np.array(pos)
    x = np.arange(start=1, stop=y.size + 1, step=1)

    ax = fig.add_subplot(gs[n])
    ax.plot(x, y)
    ax.yaxis.set_ticks([0, 50, 100])

    # filename = "plots/" + key + ".svg"
    # fig = plt.plot(x, y)

    # print(min(pos))
    # plt.yticks(np.arange(start=int(min(y)), stop=int(max(y)), step=10))

    # plt.locator_params(axis='y', nticks=10)
    # plt.xlabel('Genome')
    # plt.ylabel('Read Depth')

    # plt.savefig(filename)
    # plt.clf()

plt.savefig('plots/lmao1.svg', dpi=1200)
