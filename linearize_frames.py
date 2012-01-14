#!/usr/bin/python

import EXIF
import os.path
import sys

from datetime import datetime,timedelta
from itertools import izip
from math import ceil
from math import log10
from multiprocessing import Pool

def getDigTime(filename):
    with open(filename,'rb') as f:
        tags = EXIF.process_file(f)
        digitized = datetime.strptime(str(tags['EXIF DateTimeOriginal']),"%Y:%m:%d %H:%M:%S")
    # Get frame number as first elt
    print "processed",filename
    return digitized

def jpegfiles(directory):
    srcdir = os.path.abspath(directory)
    files = []
    for dirname, dirnames, filenames in os.walk(srcdir):
        for filename in filenames:
            if filename[-3:].upper() == 'JPG':
                files.append(os.path.join(dirname, filename))
    return files

def link_linear(sorted_files, tgtdir):
    ndigits = ceil(log10(len(sorted_files)))
    tgtdir = os.path.abspath(tgtdir)
    out_names = []
    fileformat = "frame.%%0%dd.jpg" % ndigits
    if not os.path.exists(tgtdir):
        os.mkdir(tgtdir)
    for idx, src in enumerate(sorted_files):
        base = os.path.split(src)[1]
        tgt = os.path.join(tgtdir, fileformat % idx)
        out_names.append(tgt)
        print "linking",base,"to",tgt
        os.symlink(src, tgt)
    return out_names

def main(srcdir, tgtdir, exiflog):
    srcfiles = jpegfiles(srcdir)[:100]
    pool = Pool()
    digtimes = pool.map(getDigTime, srcfiles)
    sorted_files = [fn for time, fn in sorted(zip(digtimes, srcfiles))]
    out_names = link_linear(sorted_files, tgtdir)
    with open(exiflog,"w") as logf:
        for time, name in izip(digtimes, out_names):
            strtime = time.strftime("%Y:%m:%d %H:%M:%S")
            logf.write("%s\t%s\n" % (name, strtime))

    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
