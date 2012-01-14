#!/usr/bin/python

import sys
from datetime import datetime,timedelta
import shutil
import os.path
import numpy
import time

def parse_log_line(line):
    line = line.strip()
    name, strtime = line.split("\t")
    time = datetime.strptime(strtime,"%Y:%m:%d %H:%M:%S")
    return name, time

def main(exiflog):
    with open(exiflog,"r") as logf:
        files, times = zip(*map(parse_log_line, logf))      

    deltas = [float("inf")]
    for i in range(1,len(times)):
        td = times[i] - times[i-1]
        totalsec = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1000000.0 
        deltas.append(totalsec)

    sdeltas = sorted(deltas)
    # Average is a poor estimator here because of large outliers
    print "Median delta:",sdeltas[len(deltas)/2]
    median = sdeltas[len(deltas)/2]

    thresholds = [1.2,1.3,1.5,1.6,1.7,1.8,2,2.2,2.4,2.6,2.8,3,5,6,7,8,9,10,20,40]
    for thresh in thresholds:
        thresh = thresh*median
        breaks = len(filter(lambda x:x>thresh,deltas))
        print breaks,"possible breakpoints at threshold of",thresh,"seconds"
        
    thresh = 10*median
    print "Using threshold:",thresh
    for i in range(len(deltas)):
        if deltas[i] > thresh:
            frameno = int(os.path.basename(files[i]).split(".")[1])
            sys.stderr.write("%s,%d,%f\n"%(files[i],frameno,deltas[i]))

if __name__ == "__main__":
    main(sys.argv[1])
