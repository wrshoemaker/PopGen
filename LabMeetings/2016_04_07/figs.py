from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt
import math
import scipy.integrate as integrate
import decimal

N  = 100000
gamma = 0
u = 0.0000001
#f = lambda x : ( np.exp(-x * N * (gamma*s)) * ((1-x) ** (-u*N) )  )
#I = integrate.quad(f, 0, 1- (1/N) )

p_iter = 10000
Nstart = 3
Nend = 8

p = np.logspace(Nstart, Nend, num=p_iter)

def numerator(Ni, s, u, gamma):
    f = lambda x : ( np.exp(-x * Ni * (gamma+s)) * ((1-x) ** (-u*Ni) )  )
    I = integrate.quad(f, 0, 1- (1/Ni) )
    print Ni, I[0], I[1]
    return I[0]

def prob_fixation(N, s, u, gamma, p_iter, Nstart, Nend):
    '''
    N = population size
    s = selection coefficient
    u = deactivation rate of gene
    gamma = direct contact transfer rate
    p_iter = number of floats to take in allele freq range (0,1)
    '''
    x_range = np.logspace(Nstart, Nend, num = p_iter)
    f = lambda x : ( np.exp(-x * N * (gamma+s)) * ((1-x) ** (-u*N) )  )
    g = np.vectorize(lambda y:  (1 /  (y * numerator(y, s, u, gamma))))
    return np.log10(g(x_range))

line1 = prob_fixation(N, 0, u, gamma, p_iter, Nstart, Nend)
#line2 = prob_fixation(N, -0.0000001, u, gamma, p_iter, Nstart, Nend)
#line3 = prob_fixation(N, 0.0000001, u, gamma, p_iter, Nstart, Nend)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
p = np.log10(p)
plt.plot(p, line1,color = 'b', linestyle = '-', label="N = 1000, B = 1")
#plt.plot(p, line2,color = 'b', linestyle = '--', label="N = 1000, B = 1")
#plt.plot(p, line3,color = 'b', linestyle = '-.', label="N = 1000, B = 1")

plt.tight_layout()
plt.ylabel(r'$\bar{t}(p)$', fontsize = 18, rotation = 90)
plt.xlabel(r'$p$', fontsize = 18)
output = "dorm_fix_prob.png"
plt.legend(loc='upper left', prop={'size':10})

#fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
