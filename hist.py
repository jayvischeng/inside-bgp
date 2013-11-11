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
    origin_announcements = defaultdict(int)
    origins_counter = defaultdict(int)
    enc='iso-8859-15'
    
    counter = "prefix" # origin_announcement prefix as_path
    measurement = "days" # days updates
    
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
                            origin_announcements[fields[1]] += int(fields[2])
                            origins_counter[fields[1]] += 1
                    input_file.close()
    
    top_origin_announcements = sorted(origin_announcements.items(), key=lambda x:x[1], reverse=True)
    top_origins_counter = sorted(origins_counter.items(), key=lambda x:x[1], reverse=True)
    histlist = []
    
    if any(top_origin_announcements):
        for x in range(0, len(top_origin_announcements)):
            percentage = (100/sum(origin_announcements.values()))*int(top_origin_announcements[x][1])
            #print("%02d. AS: %s\tAmount: %s (%.2f%%)" % (x+1, top_origin_announcements[x][0], top_origin_announcements[x][1], percentage))
            if measurement == "days":
                histlist.append(top_origins_counter[x][1])
            elif measurement == "updates":
                histlist.append(top_origin_announcements[x][1])
    else:
        print("No files read")

    print(histlist)
    mean = int(sum(histlist)/len(histlist))
    median = histlist[int(len(histlist)/2)]
    percent_5 = histlist[int(len(histlist)/20)]
    percent_95 = histlist[int(19*(len(histlist)/20))]
    print(">> Average: %d" % mean)
    print(">> Median: %d" % median)
    print(">> First 5%%: %d - %d" % (histlist[0], percent_5))
    print(">> Last 5%%: %d - %d" % (percent_95, histlist[-1]))
    if measurement == "days":
        plt.title("Active Days Distribution")
        plt.xlabel("Amount of %s" % counter)
        plt.ylabel("Days")
    elif measurement == "updates":
        plt.title("%s Distribution" % counter)
        plt.xlabel("Amount of %s" % counter)
        plt.ylabel("Amount of updates")
        plt.yscale('log')
    plt.plot(histlist)
    plt.grid(True)
    #plt.show()
    plt.savefig('hist.png', bbox_inches='tight')

if __name__ == '__main__':
    main()
