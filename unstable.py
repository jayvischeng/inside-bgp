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
    unstable_prefixes = defaultdict(list)
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

                    for line in input_file:
                        fields = line.strip().split("|")
                        if fields[0] == counter:
                            unstable_prefixes[update_file].append((fields[1]))
                    input_file.close()

        
    print(">> Unstable prefixes per day")
    total_unpref_start = 0
    total_start = 0
    for x in unstable_prefixes_start:
        print("%d" % len(unstable_prefixes_start[x]), end=', ')
        total_unpref_start += len(unstable_prefixes_start[x])
        total_start += 1
    print("\n>> Average prefixes/day start: %d" % (total_unpref_start/total_start))
    
    plt.title("Prefix Instability")
    plt.xlabel("Year")
    plt.ylabel("Amount of prefixes")
    plt.yscale('symlog')
    plt.plot(unstable_prefixes)
    plt.grid(True)
    #plt.show()
    plt.savefig('unpref.png', bbox_inches='tight')
    
if __name__ == '__main__':
    main()
