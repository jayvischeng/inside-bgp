#!/usr/bin/env python

import sys
import operator
import subprocess
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def main():
    top = [3549, 8492, 13030, 7018, 3130]
    announcements = defaultdict(list)
    filenames = []
    
    #for date in sys.argv:
        #if date != sys.argv[0]:
            #dates.append(date)
    #dates.sort()
    
    for date in glob.glob("2013*/output"):
        filenames.append(date)
    filenames.sort()
    print(filenames)
    
    for filename in filenames:
        input_file = open(filename, "r")
        for line in input_file:
            fields = line.strip().split("|")
            if fields[0] == "A":
                if int(fields[1]) in top:
                    announcements[fields[1]].append(fields[2])
        input_file.close()
    for key, val in announcements.items():
        print(key, val, "\n")
        plt.plot(val, label=(key))
    legend = plt.legend(loc='upper right', shadow=True)
    for label in legend.get_lines():
        label.set_linewidth(4.0)
    plt.show()
    
if __name__ == '__main__':
    main()
