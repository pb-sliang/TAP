#!/bin/sh

dir=`pwd`
if [ ! -f $dir/genome_size.txt ] ; then
    echo "no genome_size file"
    exit 1
fi
genome_size_in_mb=`cat genome_size.txt`

# run in a dir from falcon
db=0-rawreads/raw_reads.db

DBstats -u -b100  $db > len_distr.txt
ideal_ovlp.py len_distr.txt > ideal_ovlp.txt

Nnucl_in_read=`head -1 ideal_ovlp.txt | awk '{print $2}'`

lasdir=0-rawreads/las_files
for f_ovlp in `ls $lasdir/`
do
LA4Falcon -m $db $lasdir/$f_ovlp 
done | len_ovlp.py | actual_ovlp_process.py $genome_size_in_mb $Nnucl_in_read > actual_ovlp.txt 

#gnuplot /home/sliang/repeat/param_tuning_alignmt/gp_script
