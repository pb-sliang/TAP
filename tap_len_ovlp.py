#!/usr/bin/env python


import fileinput
histogram=[0L for i in range(1000000)]
for line in fileinput.input():
    fields=line.strip().split()
    a_bgn=long(fields[5])     # begining of a read
    a_end=long(fields[6])     # end of a read
    b_bgn=long(fields[9])     # begining of b read
    b_end=long(fields[10])    # end of b read
    #err_r=1.-float(fields[3])/100.
    ovlp= min(a_end-a_bgn, b_end-b_bgn)
    #if ovlp < 0 or err_r * ovlp < abs(a_end-a_bgn-(b_end-b_bgn)):
    if ovlp < 0 or ovlp > len(histogram):
        continue
    histogram[ovlp]+=1

for i in range(len(histogram)):
    if histogram[i]:
        print i, histogram[i]
