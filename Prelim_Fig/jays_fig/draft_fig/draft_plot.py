from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt


N_iter = 1000
N = np.linspace(0.0, 1000000, num=N_iter)

def prob_fixation(s, M, N_iter):
    '''
    x = freq in active population
    y = freq in dorm population
    K = relative seed bank size (n/M)
    '''
    u = 0.000001
    N_range = np.linspace(0.0, 1000000, num=N_iter)
    Ne = np.vectorize(lambda N: N / (1 + (N* (2*N*u*s) *  ( ( N / (N+M)) **2  ) )   ))
    return Ne(N_range)


def prob_fixation_indep_rho(s, M, N_iter):
    '''
    x = freq in active population
    y = freq in dorm population
    K = relative seed bank size (n/M)
    '''
    u = 0.000001
    N_range = np.linspace(0.0, 1000000, num=N_iter)
    Ne = np.vectorize(lambda N: N / (1 + (N* (0.1) *  ( ( N / (N+M)) **2  ) )   ))
    return Ne(N_range)

line1 = prob_fixation(0.01, 10000, N_iter)
line2 = prob_fixation(0.01, 100000, N_iter)
line3 = prob_fixation(0.01, 1000000, N_iter)
line4 = prob_fixation(0.01, 10000000, N_iter)
#line5 = prob_fixation_indep_rho(0.01, 100000000, N_iter)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


plt.plot(N, line1,color = 'b', linestyle = '-', label=r'$M = 10,000$')
plt.plot(N, line2, color = 'b',linestyle = '--', label=r'$M = 100,000$')
plt.plot(N, line3, color = 'b',linestyle = '-.', label=r'$M = 1,000,000$')
plt.plot(N, line4, color = 'b',linestyle = ':', label=r'$M = 10,000,000$')
#plt.plot(N, line5, color = 'b', label="M = 100,000,000")

plt.tight_layout()
plt.ylabel(r'$N_{e}$', fontsize = 18)
plt.xlabel(r'$N$', fontsize = 18)
output = "dorm_draft.png"
plt.legend(loc='upper right', prop={'size':10})
max_y = max(line4) + 10000
plt.ylim([0,max_y])
#fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
