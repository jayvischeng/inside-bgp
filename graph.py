#!/usr/bin/env python3

import datetime as dt
import sys
import operator
import subprocess
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from collections import defaultdict

def main():
    top = defaultdict(list)
    total_announcements = []
    announcements = defaultdict(list)
    filenames = []
    enc='iso-8859-15'
    
    city = "amsterdam"
    graph_type = "origin_announcement" # prefix as_path_prefix as_path origin_announcement
    start_date = 2005
    end_date = 2013
    
    if graph_type == "prefix":
        # Amsterdam
        display = ['208.31.3.0/24', '63.100.105.0/24', '130.36.35.0/24', '130.36.34.0/24', '209.140.24.0/24', '199.181.158.0/23', '2001:67c:1ec::/48', '202.92.235.0/24', '192.12.120.0/24', '62.24.238.0/24']
        # Sao Paulo
        #display = ['192.58.232.0/24', '2001:67c:1ec::/48', '206.105.75.0/24', '208.16.110.0/24', '69.38.178.0/24', '194.63.9.0/24', '84.205.66.0/24', '208.78.30.0/24', '2001:7fb:ff02::/48', '208.68.168.0/21']
        graph_type_total = "total_prefixes"
    elif graph_type == "as_path_prefix":
        # Amsterdam
        #display = ['3549 701 32528:130.36.35.0/24', '3549 701 32528:130.36.34.0/24', '3549 701 7260 4595:199.181.158.0/23', '3549 1239 19398:63.100.105.0/24', '3549 1239 19398:208.31.3.0/24', '8758 6939 3549 29607:2001:67c:1ec::/48', '7018 701 32528:130.36.34.0/24', '7018 701 32528:130.36.35.0/24', '1103 3549 701 7260 4595:199.181.158.0/23', '9304 6453 701 32528:130.36.35.0/24']
        #display = ['9304 852 32233:64.178.136.0/21', '9304 6327 32233:64.178.136.0/21']
        # Sao Paulo
        #display = ['22548 3549 29838:208.78.30.0/24', '22548 3549 29838:208.68.168.0/21', '16735 6939 3549 29607:2001:67c:1ec::/48', '28571 22548 3549 29607:2001:67c:1ec::/48', '14840 18881 3549 29607:2001:67c:1ec::/48', '16735 6762 209 6629:192.58.232.0/24', '53070 3549 29838:208.78.30.0/24', '53070 3549 29838:208.68.168.0/21', '28289 53131 16735 6939 3549 29607:2001:67c:1ec::/48', '14840 18881 3549 3356 21371 35054:2a03:bd80::/32']
        display = ['22548 3549 29838:208.78.30.0/24', '22548 3549 29838:208.68.168.0/21']
        graph_type_total = "total_as_paths_prefixes"
    elif graph_type == "as_path":
        # Amsterdam
        display = ['3549 7018', '3549 701 32528', '3549 701 7260 4595', '3549 3561 9829', '3549 6453 4755 9829', '7018 3561 9829', '3549 1239 19398', '3549 7018 2386', '3549 4134', '3549 6453 4755']
        # Sao Paulo
        #display = ['22548 3549 29838', '53070 3549 29838', '1916 11537 22388 7660 24287 24490 55824 2697', '53070 8167 1239 4837 4808', '53070 8167 6453 4837 4808', '16735 6762 3216 3216 8402', '22548 3549 3356 32955', '1916 11537 22388 7660 24287 24489 24490 55824 2697', '16735 3549 2914 33788 36998', '53070 3549 3356 32955']
        graph_type_total = "total_as_paths"
    elif graph_type == "origin_announcement":
        # Amsterdam
        #display = ['17974', '9829', '8151', '9583', '7018', '8452', '20115', '4755', '9498', '4134']
        display = ['2118']
        # Sao Paulo
        #display = ['8402', '9829', '6629', '28573', '17974', '1273', '7552', '12654', '647', '4808']
        graph_type_total = "total_origin_announcements"
    
    for element in display:
        top[element] = False
    
    for date in glob.glob(city+"/graph_data/*.graph"):
        filenames.append(date)
    filenames.sort()
    
    for filename in filenames:
        input_file = open(filename, "r", encoding=enc)
        print(filename)
        for line in input_file:
            fields = line.strip().split("|")
            if fields[0] == graph_type:
                if fields[1] in top:
                    announcements[fields[1]].append(fields[2])
                    top[fields[1]] = True
            if fields[0] == graph_type_total:
                total_announcements.append(fields[1])
        input_file.close()
        for element in display:
            if top[element] == False:
                announcements[element].append('0')
            top[element] = False
    
    dates = []
    for i in range(start_date,end_date+1):
        dates.append("01-06-%d" % i)
        for j in range(1, 14):
            dates.append("")
        dates.append("15-06-%d" % i)
        for j in range(15, 31):
            dates.append("")
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks(range(len(dates)))
    ax.xaxis.set_ticklabels(dates)
    
    total_announcements = list(map(int, total_announcements))
    ax.plot(total_announcements, label=('Total'))
    
    for key, val in announcements.items():
        val = list(map(int, val))
        cc = np.corrcoef(total_announcements, val)
        cc = cc[0][1]
        #if cc > 0.83:
        print("AS: %s\tCC: %s" % (key, cc))
        ax.plot(val, label=key)
    
    legend = plt.legend(loc='upper right', shadow=True)
    for label in legend.get_lines():
        label.set_linewidth(4.0)
    
    plt.xlabel('Year')
    plt.ylabel('Amount')
    plt.yscale('log')
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='major')
    plt.title(city.title())
    plt.show()
    
if __name__ == '__main__':
    main()
