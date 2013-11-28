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
    prefixes = ["77.76.168.0/24"]
    as_paths = []
    pivots = []

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
                            if fields[2] == "A" and len(fields) > 6 and fields[5] in prefixes:
                                as_path = fields[6].strip().split(" ")
                                as_path_no_dup = []
                                for index, as_number in enumerate(as_path):
                                    if as_path[0:index].count(as_number) == 0:
                                        as_path_no_dup.append(as_number)
                                as_path_no_dup.reverse()
                                as_paths.append(as_path_no_dup)
                    input_file.close()
    
    print("")

    for index, as_path in enumerate(as_paths):
        print(index, "\t", as_path)

    for base_index, base_as_path in enumerate(as_paths[0:]):
        for cmp_index, cmp_as_path in enumerate(as_paths[base_index+1:]):
            for index, as_number in enumerate(cmp_as_path):
                if index < len(base_as_path) and as_number != base_as_path[index]:
                    #print("%d pivots on %d: %s" % (base_index, cmp_index+base_index+1, cmp_as_path[index-1]))
                    if pivots.count(cmp_as_path[index-1]) == 0:
                        pivots.append(cmp_as_path[index-1])
                    break
    print(pivots)
    
if __name__ == '__main__':
    main()
