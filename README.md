# TAP 
Tuning assembler parameters (TAP) by computing on small fraction of the data and estimate overlap due to repeats.

This program is designed to help choosing daligner parameters in the first step of Falcon assembler. 
Particularly the minimum overlap required for an alignment (daligner -l parameter).
The aim is to reduce alignment due to repeats without sacreficing quality of the alignment.
 
A few example of use cases are:
(1) Estimate amount of repetitive sequences and other high copy-number component such as chloroplast, mitochondrion
(2) Estimate the speedup at a given cutoff
(3) The speedup should be balanced by the lost of coverage due to exclusion of shorter reads


# Installation
The program assume that the Falcon has been installed in your system. To install TAP,

git clone https://github.com/pb-sliang/TAP.git

Then activate FALCON virtual environment
( for example, 
source ~/FALCON-integrate/fc_env/bin/activate
or
. ~/FALCON-integrate/fc_env/bin/activate
)

cd TAP

sh setup.sh     # this will copy python scripts to FALCON virtual environment $VIRTUAL_ENV/bin

# Running TAP
To run TAP, first run FALCON on a small number of ZMW cells, however, in a directory different from where you normally run FALCON on the full data set:
(1) prepare a input.fofn file containing a small number of cells in order to speed up computation.
(2) prepare a configuration file (for example ecoli.cfg) containing FALCON parameters. 
(3) run FALCON by 
fc_run.py ecoli.cfg 
where ecoli.cfg is the configuration file containing some of the parameters to be tuned.
Set length_cutoff to a small value (for example length_cutoff = 500). 
(4) after FALCON has finished and .las file generated, run TAP programs by 
tap.sh. Note that tap.sh should be run in the same directory where FALCON was run (on a small number of cells) in the directory containing 0-rawreads subdirectory. tap.sh generates two text files in the current directory reporting the results of the calculation:
ideal_ovlp.txt and actual_ovlp.txt. File ideal_ovlp.txt is the expected overlaps computed from the the read length distribution
assuming the genome contains no repeats. File actual_ovlp.txt is from the daligner overlap normalized to so it can be directly
compared to ideal_ovlp.txt. In both files, the first column is the minimum overlap length, below which the overlap will not be counted. The secon column is the normalized overlap. (this will be the right hand size of the equaltion above for ideal_ovlp.txt and the left side of the euqation for actual_ovlp.txt). These two files can be plotted together using plot_ovlp script to gnuplot:

gnuplot plot_ovlp

This generates a file plot_ovlp.ps. The name of the file and the details of the plot are set in plot_ovlp.




# Additional details
A more detailed explanation of the program is below.

The reason for increaseing the miminum required overlapfor an alignment is that when this minimum exceeds the length of the repeat, the repeat will no longer be aligned. The computation is reduced because the length of overlap is computed in seeding stage, which is only a small part of overall computation.

Requiring a minimum overlap is not without drawbacks. It leads to a reduction in effective coverage since short reads can never be aligned and are in effect removed from assembly. Reduction of coverage may be detrimental to the contiguity of final assembly. The amount of reduction will obviously depend on the distribution of read length.

The expected alignment for a non-repetitive genome can be derived assuming that reads are drawn randomly from the genome. The expression can be written in closed form as is an integral over the distribution of read length.

The expected pairwise overlap is
N_o(L)/(X N_n) = (\int_L^\infty (x - L) f(x) dx / l_a)^2

Here, L is the minimum overlap length; N_o (L) is total pairwise overlap length; X is the per site coverage; N_n is the total number of nucleotides in the reads. Note that N_o(L), X, and N_n should be computed on the same partial data set. When L=0, the right hand side is equal to 1. The left hand side can be interpreted as square of the fold of reduction in effective coverage due to requirement of increased overlap length. l_a=N_n/N_r is the average read length. (N_r is the total number of reads).

Note that N_o (L) can be measured from a fraction of data. If the factor X*N_n for the same fraction is used, then this can be directly comparable to the right-hand side. 

To recap, the ideal overlap is what the pairwise overlap should be as a function of minimum overlap length if the genome has no repeats. It is computed from the distribution of read length for the data. The actual overlap is computed on a partial data set (to ease the computation). Since the reads are distributed randomly among files, the partial data should be a good approximation to the entire data set. It is scaled to be directly comparable to the ideal overlap.
Some of ways of using these curves

(1) the actual overlap is proportional to Daligner computation time. Since there is no adjustable parameter, the two curves are directly comparable. The curve should be above the ideal overlap due to repeats. The folds over the ideal curve is a measure of extra computation due to presence of repeats. It is usually 100 to 1000 folds for a large genome.

(2) we can use actual overlap curve to figure out computation saving when minimum allowed overlapping length is increased. Simply compare overlap at the desired length cutoff and the zero cutoff.

(3) When increasing minimum overlap length, computational saving needs to be balanced with the reduction in effective coverage which can be detrimental to assembly. A reasonable rule of thumb is to use Lander-Waterman criteria. For example, in order for the mean contig length to be one Mbp, the coverage should be 10X for human genome according to Lander-Waterman criteria. We the ideal overlap curve, we can read off the folds of reduction by comparing the y-axis at the desired cutoff to zero cutoff and take square root.
