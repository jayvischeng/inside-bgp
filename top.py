#!/usr/bin/env python

import sys
import operator
import subprocess
import glob
import os

def inverse(x):
    return 1.0 / x

def main():
    total = {}
    announcements = {}
    withdrawals = {}
    show = 10
    
    for date in sys.argv:
        if date != sys.argv[0]:
            print(">> Parsing updates")
            for update_file in glob.glob(date+"/*.bz2"):
                print(update_file+".parsed")
                # Check if file is already parsed
                try:
                    with open(update_file+".parsed"): pass
                except IOError:
                    subprocess.call(["bgpdump", "-m", update_file, "-O", update_file+".parsed"])
                input_file = open(update_file+".parsed", "r").read()

                # Count updates in file
                for message in input_file.splitlines():
                    fields = message.strip().split("|")
                    if fields[4] in total:
                        total[fields[4]] += 1
                    else:
                        total[fields[4]] = 1
                    if fields[2] == "A":
                        if fields[4] in announcements:
                            announcements[fields[4]] += 1
                        else:
                            announcements[fields[4]] = 1
                    elif fields[2] == "W":
                        if fields[4] in withdrawals:
                            withdrawals[fields[4]] += 1
                        else:
                            withdrawals[fields[4]] = 1
            print(">> Parsing finished")

    
    top_talkers = sorted(total.items(), key=lambda x:x[1], reverse=True)
    top_announcements = sorted(announcements.items(), key=lambda x:x[1], reverse=True)
    top_withdrawals = sorted(withdrawals.items(), key=lambda x:x[1], reverse=True)
    
    print("Top", show, "Talkers")
    for x in range(0, show):
        print(x+1, "AS:", top_talkers[x][0], "Total:", top_talkers[x][1])
    print("Top", show, "Announcements")
    for x in range(0, show):
        print(x+1, "AS:", top_announcements[x][0], "Total:", top_announcements[x][1])
    print("Top", show, "Withdrawals")
    for x in range(0, show) :
        print(x+1, "AS:", top_withdrawals[x][0], "Total:", top_withdrawals[x][1])
    
if __name__ == '__main__':
    main()
