#!/usr/bin/env python3

import sys
import operator
import subprocess
import glob
import os
from collections import defaultdict

def main():
    peer_updates = defaultdict(int)
    peer_announcements = defaultdict(int)
    peer_withdrawals = defaultdict(int)
    origin_announcements = defaultdict(int)
    origins_counter = defaultdict(int)
    
    as_paths = defaultdict(int)
    total_as_paths = 0
    as_paths_counter = defaultdict(int)
    
    prefixes = defaultdict(int)
    total_prefixes = 0
    prefixes_counter = defaultdict(int)
    
    as_paths_prefixes = defaultdict(int)
    total_as_paths_prefixes = 0
    as_paths_prefixes_counter = defaultdict(int)
    
    file_counter = 0
    show_max = 15
    directories = []
    enc='iso-8859-15'
    
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
                        if fields[0] == "peer_update":
                            peer_updates[fields[1]] += int(fields[2])
                        elif fields[0] == "peer_announcement":
                            peer_announcements[fields[1]] += int(fields[2])
                        elif fields[0] == "peer_withdrawal":
                            peer_withdrawals[fields[1]] += int(fields[2])
                        elif fields[0] == "origin_announcement":
                            origin_announcements[fields[1]] += int(fields[2])
                            origins_counter[fields[1]] += 1
                        elif fields[0] == "prefix":
                            prefixes[fields[1]] += int(fields[2])
                            prefixes_counter[fields[1]] += 1
                        elif fields[0] == "total_prefixes":
                            total_prefixes += int(fields[1])
                        elif fields[0] == "as_path":
                            as_paths[fields[1]] += int(fields[2])
                            as_paths_counter[fields[1]] += 1
                        elif fields[0] == "total_as_paths":
                            total_as_paths += int(fields[1])
                        elif fields[0] == "as_path_prefix":
                            as_paths_prefixes[fields[1]] += int(fields[2])
                            as_paths_prefixes_counter[fields[1]] += 1
                        elif fields[0] == "total_as_paths_prefixes":
                            total_as_paths_prefixes += int(fields[1])
                            
                    input_file.close()
    
    top_peer_updates = sorted(peer_updates.items(), key=lambda x:x[1], reverse=True)
    top_peer_announcements = sorted(peer_announcements.items(), key=lambda x:x[1], reverse=True)
    top_peer_withdrawals = sorted(peer_withdrawals.items(), key=lambda x:x[1], reverse=True)
    
    top_origin_announcements = sorted(origin_announcements.items(), key=lambda x:x[1], reverse=True)
    top_origins_counter = sorted(origins_counter.items(), key=lambda x:x[1], reverse=True)
    
    top_as_paths = sorted(as_paths.items(), key=lambda x:x[1], reverse=True)
    top_as_paths_counter = sorted(as_paths_counter.items(), key=lambda x:x[1], reverse=True)
    
    top_prefixes = sorted(prefixes.items(), key=lambda x:x[1], reverse=True)
    top_prefixes_counter = sorted(prefixes_counter.items(), key=lambda x:x[1], reverse=True)
    
    top_as_paths_prefixes = sorted(as_paths_prefixes.items(), key=lambda x:x[1], reverse=True)
    top_as_paths_prefixes_counter = sorted(as_paths_prefixes_counter.items(), key=lambda x:x[1], reverse=True)
    
    if any(top_peer_updates):
        print(">> Top", show_max, "Updates from Peers")
        for x in range(0, min(show_max, len(top_peer_updates))):
            percentage = (100/sum(peer_updates.values()))*int(top_peer_updates[x][1])
            print("%02d. AS: %s\tAmount: %s (%.2f%%)" % (x+1, top_peer_updates[x][0], top_peer_updates[x][1], percentage))
        
        print("\n>> Top", show_max, "Announcements from Peers")
        for x in range(0, min(show_max, len(top_peer_announcements))):
            percentage = (100/sum(peer_announcements.values()))*int(top_peer_announcements[x][1])
            print("%02d. AS: %s\tAmount: %s (%.2f%%)" % (x+1, top_peer_announcements[x][0], top_peer_announcements[x][1], percentage))
        
        print("\n>> Top", show_max, "Withdrawals from Peers")
        for x in range(0, min(show_max, len(top_peer_withdrawals))):
            percentage = (100/sum(peer_withdrawals.values()))*int(top_peer_withdrawals[x][1])
            print("%02d. AS: %s\tAmount: %s (%.2f%%)" % (x+1, top_peer_withdrawals[x][0], top_peer_withdrawals[x][1], percentage))
        
        print("\n>> Top", show_max, "Announcements from Origin")
        for x in range(0, min(show_max, len(top_origin_announcements))):
            percentage = (100/sum(origin_announcements.values()))*int(top_origin_announcements[x][1])
            print("%02d. AS: %s\tAmount: %s (%.2f%%)" % (x+1, top_origin_announcements[x][0], top_origin_announcements[x][1], percentage), end='\t\t')
            percentage = (int(top_origins_counter[x][1])/file_counter)*100
            print("%02d. AS: %s Days: %s (%.2f%%)" % (x+1, top_origins_counter[x][0], top_origins_counter[x][1], percentage))
        
        print("\n>> Top", show_max, "AS Paths")
        for x in range(0, min(show_max, len(top_as_paths))):
            percentage = (100/total_as_paths)*int(top_as_paths[x][1])
            print("%02d. Amount: %s (%.2f%%)\tAS_PATH: %s" % (x+1, top_as_paths[x][1], percentage, top_as_paths[x][0]), end='\t\t')
            percentage = (int(top_as_paths_counter[x][1])/file_counter)*100
            print("%02d. AS_PATH: %s\tDays: %s (%.2f%%)" % (x+1, top_as_paths_counter[x][0], top_as_paths_counter[x][1], percentage))
        
        print("\n>> Top", show_max, "Prefixes")
        for x in range(0, min(show_max, len(top_prefixes))):
            percentage = (100/total_prefixes)*int(top_prefixes[x][1])
            print("%02d. Amount: %s (%.2f%%)\tPrefix: %s" % (x+1, top_prefixes[x][1], percentage, top_prefixes[x][0]), end='\t\t')
            percentage = (int(top_prefixes_counter[x][1])/file_counter)*100
            print("%02d. Prefix: %s\tDays: %s (%.2f%%)" % (x+1, top_prefixes_counter[x][0], top_prefixes_counter[x][1], percentage))
        
        print("\n>> Top", show_max, "AS Path:Prefixes")
        for x in range(0, min(show_max, len(top_as_paths_prefixes))):
            percentage = (100/total_as_paths_prefixes)*int(top_as_paths_prefixes[x][1])
            print("%02d. Amount: %s (%.2f%%)\tAS Path Prefix: %s" % (x+1, top_as_paths_prefixes[x][1], percentage, top_as_paths_prefixes[x][0]), end='\t\t')
            percentage = (int(top_as_paths_prefixes_counter[x][1])/file_counter)*100
            print("%02d. AS: %s\tDays: %s (%.2f%%)" % (x+1, top_as_paths_prefixes_counter[x][0], top_as_paths_prefixes_counter[x][1], percentage))
        
    else:
        print("No files read")
    
if __name__ == '__main__':
    main()
