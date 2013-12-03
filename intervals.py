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
    interval_vars = []

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
                                data_type = fields[5]
                                if len(timestamps[data_type]) == 0:
                                    timestamps[data_type].append(timestamp)
                                timestamps[data_type].append(timestamp - timestamps[data_type][0])
                    input_file.close()

    #timestamps.pop(0)
    for key in timestamps:
        timestamps[key].pop(0)
    # print(timestamps)
    data = []

    for prefix in timestamps:
        for index, timestamp in enumerate(timestamps[prefix]):
            intervals[prefix].append(timestamp - timestamps[prefix][max(0, index-1)])
        amount = len(intervals[prefix])
        timestamp_var = numpy.var(timestamps[prefix])
        interval_var = round(numpy.var(intervals[prefix]))
        interval_vars.append(interval_var)

    #print(sorted(interval_vars))
    # print(data)
    # print("Median: %d" % (timestamps[round(len(timestamps)/2)]))
    # print("Updates: %d" % (len(timestamps)))
    # print("x", tuple(x[0] for x in data))

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.title("Interval Histogram")
    plt.xlabel("Interval Variance")
    plt.ylabel("Amount of Prefixes")
    # plt.xscale('log')
    plt.yscale('symlog')
    plt.hist(interval_vars, bins=20)
    fig.savefig('intervals.png', bbox_inches='tight', dpi=200)

if __name__ == '__main__':
    main()
