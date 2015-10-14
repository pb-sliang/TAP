#!/usr/bin/env python
import sys
import math

#from matplotlib import pyplot


def readDBstats(fn):
    length_=[]
    nread_=[]
    with open(fn,"r") as infile:
        for line in infile:
            if "Bin:" in line:
                break;
        for line in infile:
            fields= line.strip().split()
            length_.append( int(fields[0].replace(",","").replace(":","")) )
            nread_.append( int(fields[1].replace(",","")) )
    length=list(reversed(length_))
    nread=list(reversed(nread_))
    return length,nread
            

def integral(length, nread, ovlp):
    for i in range(len(length)-1):
        cutoff=length[i]
        o=0.
        for j in range(1,len(length)):
            if length[j-1] < cutoff:
                continue
            al=(length[j-1]+length[j])/2.
            o += (al-cutoff)*nread[j-1]
        o+=(length[-1]-cutoff)*nread[-1]
        ovlp.append(o*o)


if __name__ == "__main__":
    length, nread = readDBstats(sys.argv[1])
    ovlp=[]
    integral(length, nread, ovlp)
    print '#', math.sqrt(ovlp[0])
    for i in range(len(ovlp)):
        print length[i], ovlp[i]/ovlp[0]
    #pyplot.yscale('log')
    #pyplot.plot(length,ovlp)
    #pyplot.show()
    #savefig('arab.pdf')
    
