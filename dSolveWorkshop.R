#Analyze the trajectory of a beneficial allele among active and dormant populations
#dPN/dt=s*p*(1-p) - (mNM * PN) + (mMN * PM)
#dPM/dt= (mNM * PN) - (mMN * PM)

#Clear working environment
rm(list=ls())

#Open deSolve library
library(deSolve)

s = 0.01
mNM = 0.001
mMN = 0.001
N = 100000

#Define system of differential equations
evolution <- function(t,y,params){
  pN = y[1]; pM = y[2];
  with(
    as.list(params),
    {
      dpN <- s*pN*(1-pN) - (mNM * pN) + (mMN * pM)
      dpM <- (mNM * pN) - (mMN * pM)
      res <- c(dpN,dpM)
      list(res)
    }
  )
}

#Pick times vector to integrate along
times=seq(from=0,to=100,by=1)

#Simulate
evolution_out=rk(
  #Vector of initial conditions
  c(pN=1/N,pM=0),
  #Time vector to use
  times, 
  #Differential equation system to use
  evolution,
  #Vector of parameters to use
  c(s=s,mNM=mNM,mMN=mMN),
  #Method to use
  method="rk45dp7")


#Plot the data lazily and let R do all the work
plot(evolution_out)
