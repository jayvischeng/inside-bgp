#!/usr/bin/env python3

import sys
import operator
import subprocess
import glob
import os
from collections import defaultdict
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from numpy.random import normal
import numpy

def main():
    unstable_prefixes_days = []
    enc='iso-8859-15'
    
    counter = "prefix"
    
    file_counter = 0
    directories = []
    
    for arg in sys.argv:
        if arg != sys.argv[0]:
            if not os.path.isdir(arg):
                print(">> Error: %s not found" % arg)
            else:
                directories.append(arg)
    if len(directories) == 0:
        directories = ["graph_data"]
    
    for directory in directories:
        for root, dir_names, files in os.walk(directory):
            path = root.split('/')
            print((len(path) - 1) * '---' , os.path.basename(root))
            for update_file in files:
                if update_file.endswith(".graph"):
                    file_counter += 1
                    print(len(path) * '---', update_file)
                    input_file = open(os.path.join(root,update_file), "r", encoding=enc)

                    prefixes = []
                    for line in input_file:
                        fields = line.strip().split("|")
                        if fields[0] == counter:
                            prefixes.append(fields[1])
                    input_file.close()
                    length = max(len(prefixes), 100000)
                    unstable_prefixes_days.append(length)

    print(">> Unstable prefixes per day")
    total_prefixes = 0
    total_days = 0
    plot_data = []
    for x in unstable_prefixes_days:
        print("%d" % x, end=', ')
        plot_data.append(x)
        total_prefixes += x
        total_days += 1
    print("\n>> Average prefixes/day: %d" % (total_prefixes/total_days))
    
    dates = []
    for year in range(2013, 2013+1):
        dates.append("01-01-%d" % year)
        for j in range(1, 30):
            dates.append("")
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks(range(len(dates)))
    ax.xaxis.set_ticklabels(dates, rotation=45)
    
    plt.title("Prefix Instability")
    plt.xlabel("Month")
    plt.ylabel("Amount of prefixes")
    #plt.yscale('symlog')
    plt.plot(plot_data)
    #plt.grid(True)
    #plt.show()
    fig.savefig('unpref.png', bbox_inches='tight', dpi=200)
    
if __name__ == '__main__':
    main()
