from __future__ import division
import os, math, re
import  matplotlib.pyplot as plt
import numpy as np

mydir = os.path.expanduser("~/github/PopGen")


def generateDist(mu = 0.00000005):
    #N_list = [100000, 1000000, 10000000, 100000000, 1000000000]
    N_list = [10000]
    for N in N_list:
        theta = 2*mu * N
        list_values = [(theta/i) for i in range (1,N+1)]
        print list_values[0:10]
        #print theta
        #freqs = np.linspace(1/N, (1-(1/N)), 100)
        #print freqs
        #print (1-freqs) ** (theta-1)
        #phi = (theta / freqs) * ((1-freqs) ** (theta-1))
        #print phi
        plt.hist(list_values, bins=50, normed=True)
        plt.savefig(mydir + '/test.png', bbox_inches='tight',  dpi = 600)

generateDist()
