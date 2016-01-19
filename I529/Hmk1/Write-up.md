# I529: Homework 1

### Will Shoemaker

### Section 1

Three DNA sequences with the same nucleotide composition were genreated with nucleotide lengths of 10, 100, and 1,000 (Table1). Each sequence was run through the programs RANSEQ1 and RANSEQ2. RANSEQ1 generates random sequences with the per-base probability of a nucleotide being chosen obtained by the input DNA sequence. RANSEQ2 permutates the input sequence, generating a rearranged sequence. Both programs output their results to a user-chosen file in FASTA format. The results of both programs suggest that a permutation-based approach is innapropriate if one is interested in retaining the element of stochasticity present in the random sequence generation method. However, if one wants a deterministic approach with regards to nucleotide frequency, then a permutation-based method may be useful. 

While not taken into account here, it is also important to factor in the length of the input sequence. Storing a large genome in active memory and rearranging it may require a lot of time and computational power. 

![My Figure](input_table_cropped.pdf)
Table 1: The nucleotide frequencies of the DNA sequence used as input in the programs RANSEQ1 and RANSEQ2. 



![My Figure](freq_table_cropped.pdf)
Table 2: The mean and standard deviation of each nucleotide for random and permutated generated sequences. Each sequence generation method was run with three different input sequence lengths (N). 


### Section 2

#### 1

The probability of having the genetic disease is $$P(disease) = 1*10^{-7} $$. The test is 100% sensitive and 99.99% specific, so $$ P(positive\mid disease ) = 1$$ and $$P(negative\mid no\; disease ) = 0.9999$$, respectively.

From here we can find the probability that someone who has gotten a positive result on the test has the disease. 

$$P(disease\mid positive) = \frac{P(positive\mid disease) * P(disease)}{P(positive)}$$

Then calculate the probability of a positive result:

$$P(positive) = (P(positive\mid disease) * P( disease))  +  (P(positive\mid no\; disease) * P(no\; disease))$$

$$ = (1* (1*10^{-7})) + (0.9999999 * 0.0001) $$


$$ = 0.0001$$

Then get the conditional probability

$$P(disease\mid positive) = \frac{1.0 * (1*10^{-7})}{0.0001} $$

$$  = 0.001 $$

There is a very low probability of having the disease if the test is positive. Excluding the possibility of multiple tests or repeating the test, I would not want to take this test, as it conveys little information regarding whether or not I'd have the disease.

#### add multiple testing part

