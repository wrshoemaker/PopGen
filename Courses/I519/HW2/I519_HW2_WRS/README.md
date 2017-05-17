# Instructions

### BioTranslator.py
This program is a six-frame translator for a FASTA formatted file containing DNA sequences. To use the program, enter Python, the program name, your FASTA file containing DNA sequences, and a file containing the codon table you want to use onto the command line as follows:

	python BioTranslator.py sampleseq.txt codon.txt
	
### SimuGenome.py
This program takes an input of a FASTA file of a genome (complete or fragmented) and generates a random genome with the nucleotide frequencies of the input. It returns the nucleotide frequencies of the input and output to the screen along with a FASTA formatted file containing the random genome. To run the program, enter python, the program name, and the name of your FASTA formatted file containing DNA as follows:

	python SimuGenome.py sampleseq.txt