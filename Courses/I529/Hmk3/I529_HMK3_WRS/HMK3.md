# Homework 3

### Section 1

### Section 2

1) 

![alt text](./HMM_model/Slide1.jpg)

2) AR-HMMs

+ 1) A standard viterbi algorithm that takes into account the hidden state as well as a subset of previous observations. From the descriptin, it should be a small modification of the k-step HMM.
	
+ 2) Here I would think that state frequencies could be used, with the addition of estimating the set of parameters for the long-range and short-range dependance  a distribution. 

+ 3) For an HMM you need the state and emission parameters. For an AR-HMM you need state parameters, transistion parameters, state means, state variances, and state autoregressive parameters.

3)

+ 1) I would use a HMM with a sliding window of size m and compare the the log-likelihood of the two phylogenetic trees. 

+ 2) Since the second tree isn't known, I would generate a null tree based off of the sequence data. The log-likelihood would then be compared with the known phylogenetic tree as the alternative hypothesis and the null phylogenteic tree as the null hypothesis.

### Section 3