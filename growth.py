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
    data_start = defaultdict(int)
    data_end = defaultdict(int)
    differences = defaultdict(int)
    enc='iso-8859-15'
    
    counter = "origin_announcement" # origin_announcement prefix as_path
    
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
                            if directory == directories[0]:
                                data_start[fields[1]] += int(fields[2])
                                data_end[fields[1]] += int(fields[2])
                            elif directory == directories[1]:
                                data_end[fields[1]] += int(fields[2])
                    input_file.close()
    
    for key, value in data_start.items():
        difference = data_end[key] - value
        percentage = data_end[key]*(100/value)
        print("%s: %s -> %s (%s, %.2f%%)" % (key, value, data_end[key], difference, percentage))
        differences[key] = difference
        #print(differences[key])
    
    sorted_differences = sorted(differences.items(), key=lambda x:x[1], reverse=True)
    print("\n>> Top 10 Rising")
    for x in range(0, 10):
        percentage = data_end[sorted_differences[x][0]]*(100/data_start[sorted_differences[x][0]])
        print("%d: %s (+%s, %.2f%%) " % (x+1, sorted_differences[x][0], sorted_differences[x][1], percentage))
    print("\n>> Bottom 10 Rising")
    for x in range(len(sorted_differences)-10, len(sorted_differences)):
        percentage = data_end[sorted_differences[x][0]]*(100/data_start[sorted_differences[x][0]])
        print("%d: %s (+%s, %.2f%%) " % (x+1, sorted_differences[x][0], sorted_differences[x][1], percentage))
    
    start_only = 0
    for key in data_start:
        if data_start[key] == data_end[key]:
            start_only += 1
    
    end_only = 0
    for key in data_end:
        if data_start[key] == 0:
            end_only += 1
    
    print("")
    print(">> Only in start set: %d" % start_only)
    print(">> Only in end set:   %d" % end_only)
    
    core = 0
    core_updates_start = 0
    core_updates_end = 0
    for key in data_end:
        if data_start[key] != data_end[key] and data_start[key] != 0:
            core += 1
            core_updates_start += data_start[key]
            core_updates_end += data_end[key] - data_start[key]
    
    print("")
    print(">> Amount of AS in both:  %d" % core)
    print(">> Amount of AS in start: %d" % (len(data_start)-end_only))
    print(">> Amount of AS in end:   %d" % (len(data_end)-start_only))
    
    print("")
    print(">> Amount of core updates start: %d" % core_updates_start)
    print(">> Amount of core updates end:   %d" % core_updates_end)
    percentage = core_updates_end*(100/core_updates_start)
    print(">> Difference:                   %d (%.2f%%)" % ((core_updates_end - core_updates_start), percentage))
    
    differences_list = []
    for element in sorted_differences:
        differences_list.append(element[1])
    
    plt.title("AS Growth Distribution")
    plt.xlabel("Amount of AS")
    plt.ylabel("Growth")
    plt.yscale('log')
    plt.plot(differences_list)
    plt.grid(True)
    #plt.show()
    plt.savefig('growth.png', bbox_inches='tight')
    
if __name__ == '__main__':
    main()
