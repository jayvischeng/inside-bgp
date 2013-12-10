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
    show = defaultdict(list)
    total_announcements = []
    total_ipv4 = []
    total_ipv6 = []
    announcements = defaultdict(list)
    filenames = []
    enc='iso-8859-15'
    n_files = 10

    city = "amsterdam"
    graph_type = "prefix" # prefix as_path_prefix as_path origin_announcement
    start_year = 2013
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
    
    days = 0
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
                    print(len(path) * '---', update_file)
                    input_file = open(os.path.join(root,update_file), "r", encoding=enc)
                    ipv4 = 0
                    ipv6 = 0
                    for line in input_file:
                        fields = line.strip().split("|")
                        if fields[0] == graph_type:
                            if len(announcements[fields[1]]) == 0:
                                announcements[fields[1]] = [0] * n_files
                                    
                            announcements[fields[1]][days] = fields[2]
                            
                            if (graph_type == "prefix"):
                                if ":" in fields[1]:
                                    ipv6 += int(fields[2])
                                else:
                                    ipv4 += int(fields[2])
                        if fields[0] == graph_type_total:
                            total_announcements.append(fields[1])
                    total_ipv4.append(ipv4)
                    total_ipv6.append(ipv6)
                    input_file.close()
                    days += 1
    
    dates = []
    for year in range(start_year, end_year+1):
        # dates.append("01-01-%d" % year)
        # for j in range(1, 30):
        #     dates.append("")
        # dates.append("01-02-%d" % year)
        # for j in range(1, 28):
        #     dates.append("")
        # dates.append("01-03-%d" % year)
        # for j in range(1, 29):
        #     dates.append("")
        dates.append("01-04-%d" % year)
        for j in range(1, 30):
            dates.append("")
        dates.append("01-05-%d" % year)
        for j in range(1, 30):
            dates.append("")
        # dates.append("01-06-%d" % year)
        # for j in range(1, 30):
        #     dates.append("")
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xticks(range(len(dates)))
    ax.xaxis.set_ticklabels(dates)

    total_announcements = list(map(int, total_announcements))
    
    print(total_announcements)

    ax.plot(total_announcements, label=('Total'))
    
    # if (graph_type ==  "prefix"):
    #     total_ipv4 = list(map(int, total_ipv4))
    #     total_ipv6 = list(map(int, total_ipv6))
    #     ax.plot(total_ipv4, label=('ipv4'))
    #     ax.plot(total_ipv6, label=('ipv6'))
    
    # full_time = [0] * days
    # full_time_amount = 0
    # part_time = [0] * days
    # part_time_amount = 0
    prefix_count = [0] * n_files
    full_time_prefix_count = [0] * n_files
    test_set = [0] * n_files
    test_set2 = [0] * n_files
    for key, val in announcements.items():
        val = list(map(int, val))
        for day in range(0,days):
            if val[day] != 0:
                prefix_count[day] += 1
            if val.count(0) < 2:
                full_time_prefix_count[day] += 1
            if val[day] < 30:
                test_set[day] += val[day]
                test_set2[day] += 1

        #cc = np.corrcoef(total_announcements, val)
        #cc = cc[0][1]
        #print("AS: %s\tCC: %s" % (key, cc))
        # if 0 not in val or val.count(0) < 6:
        #     full_time_amount += 1
        #     full_time = [a+b for a,b in zip(full_time, val)]
        # else:
        #     part_time_amount += 1
        #     part_time = [a+b for a,b in zip(part_time, val)]

    # ax.plot(full_time, label="Full Time Talkers")
    # ax.plot(part_time, label="part time talking")
    print(prefix_count)
    print(full_time_prefix_count)
    ax.plot(prefix_count, label=('Prefix Count'))
    # ax.plot(full_time_prefix_count, label=('Full Time Prefixes'))
    ax.plot(test_set, label=('Test Set'))
    ax.plot(test_set2, label=('Test Set Count'))
    # print("amount of as always talking:", full_time_amount)
    # print("amount of as sometimes talking:", part_time_amount)
    
    legend = plt.legend(loc='upper right', fancybox=True)
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
    fig.savefig('graph.png', bbox_inches='tight', dpi=200)
    
if __name__ == '__main__':
    main()
