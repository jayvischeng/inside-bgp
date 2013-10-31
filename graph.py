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
    announcements = defaultdict(list)
    filenames = []
    enc='iso-8859-15'
    
    city = "stockholm"
    graph_type = "origin_announcement" # prefix as_path_prefix as_path origin_announcement
    start_date = 2007
    end_date = 2013
    
    if graph_type == "prefix":
        display = ['']
        graph_type_total = "total_prefixes"
    elif graph_type == "as_path_prefix":
        display = ['']
        graph_type_total = "total_as_paths_prefixes"
    elif graph_type == "as_path":
        display = ['']
        graph_type_total = "total_as_paths"
    elif graph_type == "origin_announcement":
        display = ['8151', '8452']
        graph_type_total = "total_origin_announcements"
    
    for element in display:
        top[element] = False
    
    for date in glob.glob(city+"/graph_data/2007/*.graph"):
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
        dates.append("01-01-%d" % i)
        for j in range(1, 30):
            dates.append("")
        dates.append("01-02-%d" % i)
        for j in range(1, 28):
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
    #plt.show()
    fig.savefig('foo.png', bbox_inches='tight')
    
if __name__ == '__main__':
    main()
