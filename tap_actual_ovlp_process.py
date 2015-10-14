#!/usr/bin/env python
import sys

def rev_accum(data):
    i=-1
    count=0L
    output=[]
    for l in range(40000,0,-100):
        while abs(i) <= len(data):
            if data[i][0] < l:
                output.append([l,count])
                break
            count += data[i][0]*data[i][1]	# legnth of overlap multiplies the count; count is the total overlap
            i-=1
    return output

import fileinput

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: ", sys.argv[0], "genome_size_in_mb", "Nnucl_in_read"
        sys.exit(0);
    genome_size_in_mb=float(sys.argv[1])
    genome_size=genome_size_in_mb*1000000.
    Nnucl_in_read=float(sys.argv[2])
    data=[]
    for line in fileinput.input(sys.argv[3:]):
        fields=line.strip().split()
        data.append([long(fields[0]), long(fields[1])])
    tmp=rev_accum(data)
    f=(1./Nnucl_in_read)/(Nnucl_in_read/genome_size)
    for d in reversed(tmp):
        print d[0], d[1]*f


