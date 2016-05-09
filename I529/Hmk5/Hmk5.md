# Homework 5
### Will Shoemaker

**1)**

-1 We start with random emission symbols as a sequence and calculate the probability with our HMM.

-2 We then select a random sequence, remove the random motif and recalculate model parameters.

-3 calculate the maximal total emission probability given the HMM with updated parameters 

-4 Update the model and continue iterating 

**2)**

-1 Here we have three conditional probability distributions (CPD).

 ![Alt text](./Presentation1/Slide1.jpg). 

-2 The module network does not represent the same dependence structure found in the original Bayesian network. This is in part due to the two addditional assumptions of modular networks. 1)  the priors of the parent nodes and the parameters of a modula are independant of the set of variables assigned to the module and 2) the prior on the module assignment function is proportional to the the product of local terms. This means that moving variables between modules does not change how we assign other variables. 

-3 A Bayesian network with a well-described distribution must be acylic, so if we take a Bayesian network and turn it into a module network we expect that it will be acylic as well.

**3)**

We should be able to just use maxmum likelihood.

 ![Alt text](./Presentation1/Slide3.jpg). 


**4)**

 ![Alt text](./Presentation1/Slide2.jpg). 


**5)**

-1 Because this is a network, to bredict $$X_{2}$$, the number of combination that we need to calculate the probabilities for is constrained. This problem constrains the number of possible seasons to two choices through the distribution $$P(X_{2} = salmon\mid X_{1})$$. We also know that the fish is thin. So, we have to calculate $$2 * 2 * 3 * 1 = 12$$ probabilities. We are asking $$P(X_{2} \mid X_{4} = thin, X_{1}, X{3})$$ From here the probability that we have a salmon is ~ 0.986, so we likely have a salmon. 

-2 Again, the number of calculations are constrained. We want to know $$P(X_{1} \mid X_{4} = thin, X_{3} = medium, X{2})$$ using the prior $$P(X{1})= (0.25,0.25,0.25, 0.25)$$. So we need a total of 4 * 2 * 1* 1 = 8 calculations. It is most likely winter with probability ~0.372