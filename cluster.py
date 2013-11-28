#!/usr/bin/env python3

import codecs
import sys
import operator
import subprocess
import glob
import os
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

def main():
    top_n = 1000
    directories = []
    enc='iso-8859-15'
    prefixes = ["177.154.214.0/24", "173.232.234.0/24", "95.58.190.0/23"]
    timestamps = defaultdict(list)
    intervals = defaultdict(list)

    for arg in sys.argv:
        if arg != sys.argv[0]:
            if not os.path.isdir(arg):
                print(">> Error: %s not found" % arg)
            else:
                directories.append(arg)
    if len(directories) == 0:
        directories = ["."]
    
    for directory in directories:
        for root, dir_names, files in os.walk(directory):
            
            
            path = root.split('/')
            print((len(path) - 1) * '---' , os.path.basename(root))
            for update_file in files:
                if update_file.endswith(".bz2") or update_file.endswith(".gz"):
                    update_file = os.path.join(root,update_file)
                    print(len(path) * '---', update_file)
                    try:
                        with open(update_file+".parsed"): pass
                    except IOError:
                        subprocess.call(["../libbgpdump-1.4.99.13/bgpdump", "-m", update_file, "-O", update_file+".parsed"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    input_file = codecs.open(update_file+".parsed", "r", encoding=enc)
                    
                    for message in input_file:
                        printable = True
                        fields = message.strip().split("|")
                        for i in range(0, len(fields)):
                            if not fields[i].isprintable():
                                printable = False
                        if printable == True and len(fields) > 4:
                            if fields[2] == "A" and len(fields) > 6:
                                #as_path = fields[6].strip().split(" ")
                                timestamp = int(fields[1])
                                measurement = fields[6]
                                if len(timestamps[measurement]) == 0:
                                    timestamps[measurement].append(timestamp)
                                timestamps[measurement].append(timestamp - timestamps[measurement][0])
                    input_file.close()

    #timestamps.pop(0)
    for key in timestamps:
        timestamps[key].pop(0)
    # print(timestamps)
    data = []

    for prefix in timestamps:
        # print("")
        # print("timestamps:", timestamps[x])
        # for index, timestamp in enumerate(timestamps[prefix]):
            # intervals[prefix].append(timestamp - timestamps[prefix][max(0, index-1)])
        # print("intervals:", sorted(intervals[x]))
        # print("amount of announcements:", len(intervals[x]))
        # print("mean interval:", numpy.mean(intervals[x]))
        # print("median interval:", numpy.median(intervals[x]))
        # print("std interval:", numpy.std(intervals[x]))
        # print("var interval:", numpy.var(intervals[x]))
        data_point = (numpy.var(timestamps[prefix]), len(timestamps[prefix]))
        #print(">>", prefix, data_point)
        data.append(data_point)

    # print(data)
    # print("Median: %d" % (timestamps[round(len(timestamps)/2)]))
    # print("Updates: %d" % (len(timestamps)))
    # print("x", tuple(x[0] for x in data))

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.title("Prefix Clustering")
    plt.xlabel("Timestamp Variance")
    plt.ylabel("Amount of Announcements")
    #plt.xscale('log')
    plt.yscale('log')
    x = tuple(x[0] for x in data)
    y = tuple(y[1] for y in data)
    plt.plot(x, y, 'r,')
    fig.savefig('cluster.png', bbox_inches='tight', dpi=200)

if __name__ == '__main__':
    main()
