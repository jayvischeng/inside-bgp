#!/usr/bin/env python3

import codecs
import sys
import operator
import subprocess
import glob
import os
from collections import defaultdict

def main():
    top_n = 1000
    directories = []
    enc='iso-8859-15'
    
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
            peer_updates = defaultdict(int)
            peer_announcements = defaultdict(int)
            peer_withdrawals = defaultdict(int)
            origin_announcements = defaultdict(int)
            as_paths = defaultdict(int)
            prefixes = defaultdict(int)
            as_paths_prefixes = defaultdict(int)
            
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
                            peer_updates[fields[4]] += 1
                            if fields[2] == "A" and len(fields) > 6:
                                peer_announcements[fields[4]] += 1
                                as_path = fields[6].strip().split(" ")
                                origin_announcements[as_path[-1]] += 1
                                as_paths[fields[6]] += 1
                                prefixes[fields[5]] += 1
                                as_path_prefix = "%s:%s" % (fields[6], fields[5])
                                as_paths_prefixes[as_path_prefix] += 1
                            elif fields[2] == "W":
                                peer_withdrawals[fields[4]] += 1
                    input_file.close()

            if not not peer_updates and not not peer_announcements and not not peer_withdrawals:
                filename = directory+"/graph_data/"+os.path.basename(root)+".graph"
                print(">> Writing to: %s" % filename)
                try: 
                    os.makedirs(directory+"/graph_data")
                except OSError:
                    if not os.path.isdir(directory+"/graph_data"):
                        raise
                output_file = open(filename, "w", encoding=enc)
                
                top_peer_updates = sorted(peer_updates.items(), key=lambda x:x[1], reverse=True)
                top_peer_announcements = sorted(peer_announcements.items(), key=lambda x:x[1], reverse=True)
                top_peer_withdrawals = sorted(peer_withdrawals.items(), key=lambda x:x[1], reverse=True)
                top_origin_announcements = sorted(origin_announcements.items(), key=lambda x:x[1], reverse=True)
                top_as_paths = sorted(as_paths.items(), key=lambda x:x[1], reverse=True)
                top_prefixes = sorted(prefixes.items(), key=lambda x:x[1], reverse=True)
                top_as_paths_prefixes = sorted(as_paths_prefixes.items(), key=lambda x:x[1], reverse=True)
                
                for x in range(0, len(top_peer_updates)):
                    output_file.write("peer_update|%s|%s\n" % (str(top_peer_updates[x][0]), str(top_peer_updates[x][1])))
                output_file.write("total_peer_updates|%s\n" % sum(peer_updates.values()))
                for x in range(0, len(top_peer_announcements)):
                    output_file.write("peer_announcement|%s|%s\n" % (str(top_peer_announcements[x][0]), str(top_peer_announcements[x][1])))
                output_file.write("total_peer_announcements|%s\n" % sum(peer_announcements.values()))
                for x in range(0, len(top_peer_withdrawals)):
                    output_file.write("peer_withdrawal|%s|%s\n" % (str(top_peer_withdrawals[x][0]), str(top_peer_withdrawals[x][1])))
                output_file.write("total_peer_withdrawals|%s\n" % sum(peer_withdrawals.values()))
                for x in range(0, len(top_origin_announcements)):
                    output_file.write("origin_announcement|%s|%s\n" % (str(top_origin_announcements[x][0]), str(top_origin_announcements[x][1])))
                output_file.write("total_origin_announcements|%s\n" % sum(origin_announcements.values()))
                for x in range(0, top_n):
                    output_file.write("as_path|%s|%s\n" % (top_as_paths[x][0], top_as_paths[x][1]))
                output_file.write("total_as_paths|%s\n" % sum(as_paths.values()))
                for x in range(0, top_n):
                    output_file.write("prefix|%s|%s\n" % (top_prefixes[x][0], top_prefixes[x][1]))
                output_file.write("total_prefixes|%s\n" % sum(prefixes.values()))
                for x in range(0, top_n):
                    output_file.write("as_path_prefix|%s|%s\n" % (top_as_paths_prefixes[x][0], top_as_paths_prefixes[x][1]))
                output_file.write("total_as_paths_prefixes|%s\n" % sum(as_paths_prefixes.values()))
                
                output_file.close()
    
if __name__ == '__main__':
    main()
