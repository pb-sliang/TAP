#!/bin/bash

usage () { echo "Usage: $0 -g genome_size_in_MB"; exit 1;}

while getopts "hg:" o ; do
   case "${o}" in
       h)
           usage
           ;;
       g)
           genome_size_in_mb=${OPTARG}
           ;;
       *)
           usage
           ;;
    esac
done

if [ -z "$genome_size_in_mb" ]; then
    dir=`pwd`
    if [ ! -f $dir/genome_size.txt ] ; then
        echo "no genome_size file"
        exit 1
    fi
    genome_size_in_mb=`cat genome_size.txt`
fi

if [ "$genome_size_in_mb" == 0. ]; then
echo "Usage: $0 -g genome_size_in_MB\n OR set a genome_size.txt file"; exit 1;
fi


# run in a dir from falcon
db=0-rawreads/raw_reads.db

DBstats -u -b100  $db > len_distr.txt
tap_ideal_ovlp.py len_distr.txt > ideal_ovlp.txt

Nnucl_in_read=`head -1 ideal_ovlp.txt | awk '{print $2}'`

lasdir=0-rawreads/las_files
for f_ovlp in `ls $lasdir/`
do
LA4Falcon -m $db $lasdir/$f_ovlp 
done | tap_len_ovlp.py | tap_actual_ovlp_process.py $genome_size_in_mb $Nnucl_in_read > actual_ovlp.txt 

#gnuplot /home/sliang/repeat/param_tuning_alignmt/gp_script
