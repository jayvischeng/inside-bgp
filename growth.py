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
    unstable_prefixes_start = defaultdict(list)
    unstable_prefixes_end = defaultdict(list)
    enc='iso-8859-15'
    
    counter = "prefix" # origin_announcement prefix as_path
    
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
                                unstable_prefixes_start[update_file].append((fields[1]))
                            elif directory == directories[1]:
                                data_end[fields[1]] += int(fields[2])
                                unstable_prefixes_end[update_file].append((fields[1]))
                    input_file.close()

    for key, value in data_start.items():
        difference = data_end[key] - value
        percentage = data_end[key]*(100/value)
        differences[key] = difference
    
    print("")
    sorted_differences = sorted(differences.items(), key=lambda x:x[1], reverse=True)
    print(">> Top 10 Rising")
    for x in range(0, 10):
        percentage = data_end[sorted_differences[x][0]]*(100/data_start[sorted_differences[x][0]])
        print("%d: %s (+%s, %.2f%%) " % (x+1, sorted_differences[x][0], sorted_differences[x][1], percentage))
    print("")
    print(">> Bottom 10 Rising")
    for x in range(len(sorted_differences)-10, len(sorted_differences)):
        percentage = data_end[sorted_differences[x][0]]*(100/data_start[sorted_differences[x][0]])
        print("%d: %s (%s, %.2f%%) " % (x+1, sorted_differences[x][0], sorted_differences[x][1], percentage))
    
    print("")

    total_unpref_start = 0
    total_start = 0
    for x in unstable_prefixes_start:
        print("%d" % len(unstable_prefixes_start[x]), end=', ')
        total_unpref_start += len(unstable_prefixes_start[x])
        total_start += 1
    print("")
    print(">> Average prefixes/day start: %d" % (total_unpref_start/total_start))

    total_unpref_end = 0
    total_end = 0
    for y in unstable_prefixes_end:
        print("%d" % len(unstable_prefixes_end[x]), end=', ')
        total_unpref_end += len(unstable_prefixes_end[y])
        total_end += 1
    print("")
    print(">> Average prefixes/day end:   %d" % (total_unpref_end/total_end))
    
    only_start = 0
    updates_start = 0
    ipv6_start = 0
    ipv6_updates_start = 0
    for key in data_start:
        updates_start += data_start[key]
        if ":" in key:
            ipv6_start += 1
            ipv6_updates_start += data_start[key]
        if data_end[key] == 0:
            only_start += 1
    
    only_end = 0
    updates_end = 0
    ipv6_end = 0
    ipv6_updates_end = 0
    for key in data_end:
        updates_end += data_end[key]
        if ":" in key:
            ipv6_end += 1
            ipv6_updates_end += data_end[key]
        if data_start[key] == 0:
            only_end += 1
    
    print("")
    print(">> Only in start set: %d" % only_start)
    print(">> Only in end set:   %d" % only_end)
    
    core = 0
    core_updates_start = 0
    core_updates_end = 0
    for key in data_end:
        if data_start[key] != 0 and data_end[key] != 0:
            core += 1
            core_updates_start += data_start[key]
            core_updates_end += data_end[key]
    
    print("")
    print(">> Amount of prefixes in core:  %d" % core)
    print(">> Amount of prefixes in start: %d (ipv6: %d)" % (len(data_start)-only_end, ipv6_start))
    print(">> Amount of prefixes in end:   %d (ipv6: %d)" % (len(data_end)-only_start, ipv6_end))
    
    print("")
    print(">> Amount of updates start:      %d (ipv6: %d)" % (updates_start, ipv6_updates_start))
    print(">> Amount of updates end:        %d (ipv6: %d)" % (updates_end, ipv6_updates_end))
    percentage = updates_end*(100/updates_start)
    print(">> Difference:                   %d (%.2f%%)" % ((updates_end - updates_start), percentage))

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
    plt.yscale('symlog')
    plt.plot(differences_list)
    plt.grid(True)
    #plt.show()
    plt.savefig('growth.png', bbox_inches='tight')
    
if __name__ == '__main__':
    main()
