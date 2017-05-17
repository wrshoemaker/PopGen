# Running RANSEQ1 & RANSEQ2

Note: Both programs are written in Python 2.7, no external dependencies.

### RANSEQ1

RANSEQ1 is a random sequence generator that calculates the nucleotide frequency of the input sequence and uses that to generate random sequencs with a length equal to the input sequence and outputs it to a file.

### RANSEQ2

RANSEQ1 is a permutation sequence generator that permutes the input sequence and outputs that to a file.

### Input/Output

There are three arguments, the same for each program. Both take a FASTA file with a single sequence as input and output the sequences in  a FASTA format.

| -i  | Path for input FASTA file                 |
|-----|---------------------------------|
| -o  | Path for output FASTA file                |
| -N  | Number of sequences to generate |

### Example 

For RANSEQ1

python RANSEQ1 –i inputfiles –n N –o outputfiles

For RANSEQ2 

python RANSEQ2 –i inputfiles –n N –o outputfiles
