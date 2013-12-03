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
    n_files = 0
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
                    n_files += 1
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
                                # as_path = fields[6].strip().split(" ")
                                timestamp = int(fields[1])
                                data_type = fields[5]
                                # data_type = as_path[-1]
                                # if len(timestamps[data_type]) == 0:
                                    # timestamps[data_type].append(timestamp)
                                timestamps[data_type].append(timestamp)
                    input_file.close()

    for key in timestamps:
        timestamps[key] = sorted(timestamps[key])
    
    data_red = []
    data_green = []

    seconds = n_files * 5 * 60

    for prefix in timestamps:
        amount = len(timestamps[prefix])
        timestamp_var = numpy.var(timestamps[prefix])
        data_point = (timestamp_var, amount)
        if timestamps[prefix][-1] - timestamps[prefix][0] > (0.98*seconds):
            data_red.append(data_point)
        else:
            data_green.append(data_point)

    n_red = len(data_red)
    n_green = len(data_green)
    total = n_red + n_green
    print("Red:   %d (%.2f%%)" % (n_red, 100*n_red/total))
    print("Green: %d (%.2f%%)" % (n_green, 100*n_green/total))
    print("Total: %d" % total)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.title("Prefix Clustering")
    plt.xlabel("Timestamp Variance")
    plt.ylabel("Amount of Announcements")
    # plt.xscale('log')
    plt.yscale('symlog')
    x_red = tuple(x[0] for x in data_red)
    y_red = tuple(y[1] for y in data_red)
    plt.plot(x_red, y_red, 'r,')
    x_green = tuple(x[0] for x in data_green)
    y_green = tuple(y[1] for y in data_green)
    plt.plot(x_green, y_green, 'g,')
    fig.savefig('cluster.png', bbox_inches='tight', dpi=200)

if __name__ == '__main__':
    main()