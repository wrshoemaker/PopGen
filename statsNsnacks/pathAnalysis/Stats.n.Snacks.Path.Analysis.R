##############################################
# set working directory and read in data

rm(list = ls())
getwd()
setwd("~/github/PopGen/statsNsnacks/pathAnalysis/")


data<-read.csv("plankton.field.data.csv") # Read in the data.  Each row is a lake sampled in a particular year.
data$Year=as.factor(data$Year) # Make sure R interprets "Year" as a factor, not a continuous variable

#################################
# Look at some bivariate plots.  
# Remember, path analysis is philosophically different from normal statistical tests: 
# Instead of testing a null hypothesis, we are testing a specific hypothetical model, based on prior evidence and/or theory
# So, we start by looking at some univariate patterns to guide our creation of a path model
# All of these relationships are further supported by previous theoretical and empirical work

# First, different community metrics seem to effect disease.  Look at two:

plot(data$D.size,data$M.prev)
# D.size is size (in mm) of adult Daphnia.  It is a robust index of fish predation.  
# Smaller size = more intense predation.
# M.prev is average prevalence of fungal infections in our focal Daphnia host 
# Index of fish predation (left on x axis) appears to decrease infection prevalence
plot(data$C.freq,data$M.prev)
# C.freq is frequency of a spore predator in the host community (Ceriodaphnia).  
# It reduces disease by vacuuming spores without getting sick, and by competing with focal hosts.
# Frequency of small spore predators appears to decrease infection prevalence

# Second, look at some other ways these community drivers are related:

plot(data$Refuge,data$D.size)
# Refuge (hypolimnetic refuge) is a layer of the lake where Daphnia hosts can escape fish predation
# Smaller refuges mean more fish predation
plot(data$D.size,data$C.freq)
# Ceriodaphnia spore predators are small than focal Daphnia hosts, and hence less conspicuous to fish predators
# more fish predation increases frequency of small spore predators
plot(data$Refuge,data$C.freq)
# Smaller refuges (hence more intense fish predation) means more small spore predators

#######################################

# Questions for path analysis:
# Do fish directly reduce disease, or indirectly reduce disease via changes in spore predators?
# How do these direct and indirect effects compare in effect size?
# Does refuge size matter more for disease by setting up fish or spore predators?

# Test a hypothesized causal path model with lavaan:

library(lavaan)   # This is the package for sem (including path analysis)

# library(MVN) # This is a package for testing the multivariate normal distribution
# Check to see if the data are multivariate normal.  Mine are not.  That's okay...
# If data are not multivariate normal, then use robust estimator or bootstrapping for parameter errors

mod1 = 'M.prev ~ C.freq + D.size    # Define a hypothetical model.  Infection prevalence is driven by...
C.freq ~ D.size + Refuge            # Frequency of small spore predators is driven by...
D.size ~ Refuge'                    # Fish predation index is driven by...

mod1.fit = sem(mod1, data=data, estimator= "MLM")        # Choose the MLM robust estimator
summary(mod1.fit, standardized=TRUE, fit.measures=TRUE)  # Ask for standardized parameter estimates and model fit stats

mod1.fit = sem(mod1, data=data, test="bollen.stine", se="boot", bootstrap=1000) # Or alternatively, bootstrap 
summary(mod1.fit, standardized=TRUE, fit.measures=TRUE)


#######################################
# Try out a much more complex model

library(lavaan.survey)   # This is a handy package for clustered sample design
# Really, it is useful for any data that are not all completely independent observations 
# Here, I use to because I sampled the same lakes in different years

mod2 = 'M.prev ~ C.freq + D.size + Chaob2 + O.freq + Simpsons
Simpsons ~ O.freq + C.freq + P.freq
C.freq ~ D.size + Refuge + Chaob2
P.freq ~ D.size + Refuge + Chaob2
P.freq ~~ C.freq                          # ~~ means you are hypothesizing a correlation, not a causal effect
P.freq ~~ O.freq
C.freq ~~ O.freq
D.size ~~ Chaob2
D.size ~ Refuge'
mod2.est = sem(mod2, data=data, estimator= "MLM")
weighting = svydesign(ids = ~Lake, probs = ~1, data = data)     # Same lake sampled in different years may not be independent
mod2.fit = lavaan.survey(mod2.est, weighting, estimator = "MLM")
summary(mod2.fit, standardized=TRUE, fit.measures=TRUE)
residuals(mod2.est)$cov                                    
resid(mod2.est, type = "standardized")                          
# It can be useful to check out the residual covariance matrix.  Big values indicate important missing links.

# Try fiddling with this model structure and see what happens to model fit indices, 
# parameter estimates, and the residual covariance matrix






