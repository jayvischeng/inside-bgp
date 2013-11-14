#!/usr/bin/env python3

import datetime as dt
import sys
import operator
import subprocess
import glob
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from collections import defaultdict

def main():
    top = defaultdict(list)
    total_announcements = []
    total_ipv4 = []
    total_ipv6 = []
    announcements = defaultdict(list)
    filenames = []
    enc='iso-8859-15'
    
    city = "amsterdam"
    graph_type = "origin_announcement" # prefix as_path_prefix as_path origin_announcement
    start_year = 2007
    end_year = 2013 
    
    if graph_type == "prefix":
        display = ['84.205.74.0/24', '2001:7fb:fe0a::/48']
        graph_type_total = "total_prefixes"
    elif graph_type == "as_path_prefix":
        display = ['']
        graph_type_total = "total_as_paths_prefixes"
    elif graph_type == "as_path":
        display = ['']
        graph_type_total = "total_as_paths"
    elif graph_type == "origin_announcement":
        display = ['3549', '3257', '12880']
        graph_type_total = "total_origin_announcements"
    
    for element in display:
        top[element] = False
    
    for year in range(start_year, end_year+1):
        for date in glob.glob(city+"/graph_data/"+str(year)+"/*.graph"):
            filenames.append(date)
    filenames.sort()
    
    for filename in filenames:
        input_file = open(filename, "r", encoding=enc)
        print(filename)
        ipv4 = 0
        ipv6 = 0
        for line in input_file:
            fields = line.strip().split("|")
            if fields[0] == graph_type:
                if fields[1] in top:
                    announcements[fields[1]].append(fields[2])
                    top[fields[1]] = True
                if ":" in fields[1]:
                    ipv6 += int(fields[2])
                else:
                    ipv4 += int(fields[2])
            if fields[0] == graph_type_total:
                total_announcements.append(fields[1])
        total_ipv4.append(ipv4)
        total_ipv6.append(ipv6)
        input_file.close()
        for element in display:
            if top[element] == False:
                announcements[element].append('0')
            top[element] = False
    
    dates = []
    for year in range(start_year, end_year+1):
        dates.append("01-01-%d" % year)
        for j in range(1, 30):
            dates.append("")
        dates.append("01-02-%d" % year)
        for j in range(1, 28):
            dates.append("")
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks(range(len(dates)))
    ax.xaxis.set_ticklabels(dates)
    
    total_announcements = list(map(int, total_announcements))
    total_ipv4 = list(map(int, total_ipv4))
    total_ipv6 = list(map(int, total_ipv6))
    ax.plot(total_announcements, label=('Total'))
    ax.plot(total_ipv4, label=('ipv4'))
    ax.plot(total_ipv6, label=('ipv6'))
    
    for key, val in announcements.items():
        val = list(map(int, val))
        cc = np.corrcoef(total_announcements, val)
        cc = cc[0][1]
        print("AS: %s\tCC: %s" % (key, cc))
        ax.plot(val, label=key)
    
    legend = plt.legend(loc='best', fancybox=True)
    legend.get_frame().set_alpha(0.5)
    for label in legend.get_lines():
        label.set_linewidth(4.0)
    
    plt.xlabel('Year')
    plt.ylabel('Amount')
    plt.yscale('log')
    plt.gcf().autofmt_xdate()
    plt.grid(True, which='major')
    plt.title(city.title())
    #plt.show()
    fig.savefig('graph.png', bbox_inches='tight')
    
if __name__ == '__main__':
    main()
