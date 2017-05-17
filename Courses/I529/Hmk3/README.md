# README for PreProStr_ghmm.py

PreProStr_ghmm is python script which contains a Generalized Hidden Markov Model that predicts the secondary structure of an amino acid sequence. 

### Commands

	
* Input test data must be FASTA formatted.

		input test data = -i


* Input training data must be formatted like the files [here](https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/protein-secondary-structure/)
	
		input training data = -t


* Output format is the same as the input format.

		output = -o 


### Example

	python PredProStr_ghmm.py -i ../data/test.fasta -t ../data/protein-secondary-structure.test.txt -o ../data/output_test.txt
