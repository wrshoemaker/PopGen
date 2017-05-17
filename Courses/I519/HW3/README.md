# I519 homework 3 README
### Will Shoemaker 

### 1) Smith-Waterman algorithm

##### SWalign.py

This program is an implementation of the Smith-Waterman algorithm with an affine gap penalty. The program takes a FASTA formatted file containing two amino-acid sequences and an [NCBI formatted BLOSUM table](http://www.ncbi.nlm.nih.gov/Class/FieldGuide/BLOSUM62.txt), returning the optimal local alignment. The output can be returned as a file in either a FASTA format with indels, or as a plain text format identical to the on-screen output. 

The program runs as follows:

	python SWalign.py -i input.fasta -f FASTA -o output-alignment.fasta -s 11 -e 1 -m BLOSUM_table.txt
	
The flags pass the following arguments:

* -i  = The relative path to a FASTA-formatted file containing two AA sequences

* -f = The output format. Type "FASTA" for a fasta formatted output or "PLAIN" for a plain output format

* -o = The name of your output file

* -s = Sigma, your new gap penalty

*  -e = Epsilon, your gap extension penalty

* -m = The file path to your NCBI formatted BLOSUM scoring matrix.

### 2) Smith-Waterman implementation running time

Using a FASTA file containing two amino-acid sequences of length 200, I used Python's time module to calculate the length of time for completion of SWalign.py as ~ 0.114 seconds. 0.114 x 1,000,000 iterations = 114,000 seconds, which is 1,900 minutes, which is ~ **32 hours**. So with this algorithm it would take over a day to compare a query sequence of 200 AA against a database that contains 1,000,000 sequences of 200 AA. 

### 3) Genome sequencing simulator

##### ReadSim.py

This program simulates genome sequencing. It takes a FASTA formatted genome, read length as input. It prints the total number and proportion of sites not covered to the screen and prints the simulated reads to a FASTA-formatted file. It also calculates what percent of sites aren't covered under the Poisson distribution.

The program runs as follows:

	python ReadSim.py genome.fna read_length coverage

Below is an example:
 
	python ReadSim.py genome.fna 100 1

The output file name depends on the input file name and contains information on the coverage and read length. For example, if your genome had the file name  "genome.fna" and you specified a read length of 100 and coverage of 1, your simulated reads would be in this file .

	genome_reads_100_cov_1.fna
	
