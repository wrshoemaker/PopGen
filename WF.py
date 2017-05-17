from __future__ import division
import numpy as np
from scipy.misc import comb


def WF(N = 10):
    # m is the transition matrix for the wright-fisher markov chain
    m=np.zeros((N+1,N+1))
    for i in np.arange(N+1):
        for j in np.arange(N+1):
            m[j,i]=comb(N,j)*(i/N)**j*((N-i)/N)**(N-j)
    return m

print WF() ** 1000
