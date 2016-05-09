from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt
import math
from scipy.special import expi



p_iter = 1000
N = 1000
p = np.linspace(1/N, (1-1/N), num=p_iter)

def prob_fixation(N, p_iter, B=1):
    '''
    N = population size
    p_iter = number of floats to take in allele freq range (0,1)
    '''
    x_range = np.linspace(1/N, (1-1/N), num = p_iter)
    g = np.vectorize(lambda x: np.log10((-2 * N * (B ** 2)* \
    	( ( (1-x) * np.log(1-x) ) + ( (x) * np.log(x) )   ) )))
    return g(x_range)

line1 = prob_fixation(N, p_iter)
line2 = prob_fixation(N, p_iter, 10)
line3 = prob_fixation(N, p_iter, 100)
line4 = prob_fixation(N, p_iter, 1000)
#line5 = prob_fixation(N, p_iter, 5)

fig = plt.figure()

ax = fig.add_subplot(2, 1, 1)


plt.plot(p, line1,color = 'b', linestyle = '-', label=r'$N = 1000,\, \beta = 1$')
plt.plot(p, line2, color = 'b',linestyle = '--', label=r'$N = 1000,\, \beta = 10$')
plt.plot(p, line3, color = 'b',linestyle = '-.', label=r'$N = 1000,\, \beta = 100$')
plt.plot(p, line4, color = 'b',linestyle = ':', label=r'$N = 1000,\, \beta = 1,000$')
#plt.plot(p, line5, color = 'b', linestyle = ' ', label="N = 1000, B = 5")

plt.tight_layout()
plt.ylabel(r'$log_{10}(\bar{t}(p))$', fontsize = 18, rotation = 90)
plt.xlabel(r'$Allele \,frequency, (p)$', fontsize = 18)
plt.legend(loc='upper right', prop={'size':10})

#fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)




p_iter = 1000
S = 1
p = np.linspace(0, S, num=p_iter)
N = 1000

def prob_fixation_select(s, p_iter, N, B=1):
    s_range = np.linspace(0, s, num = p_iter)
    g = np.vectorize(lambda s: np.log10(  ((2*B *N) / (s * (np.exp(2*B*s) -1)  )  ) \
        *  ((np.exp(2*B*s) + 1) * math.e  - expi(2*B*s) + np.log(2*B*s) \
        + np.exp(2*B*s) * (-expi(-2*B*s) + np.log(2*B*s))))  )
    return g(s_range)

line1 = prob_fixation_select(S, p_iter, N)
line2 = prob_fixation_select(S, p_iter, N, B = 10)
line3 = prob_fixation_select(S, p_iter, N, B = 100)
#line4 = prob_fixation(S, p_iter, 1000)
#line5 = prob_fixation(S, p_iter, 5)

ax = fig.add_subplot(2, 1, 2)


plt.plot(p, line1, color = 'b', linestyle = '-', label=r'$N = 1000,\, \beta = 1$')
plt.plot(p, line2, color = 'b',linestyle = '--', label=r'$N = 1000,\, \beta = 10$')
plt.plot(p, line3, color = 'b',linestyle = '-.', label=r'$N = 1000,\, \beta = 100$')
#plt.plot(p, line4, color = 'b',linestyle = ':', label="B = 1,000")
#plt.plot(p, line5, color = 'b', linestyle = ' ', label="N = 1000, B = 5")

plt.tight_layout()
plt.ylabel(r'$log_{10}(\bar{t^{*}})$', fontsize = 18, rotation = 90)
plt.xlabel(r'$Selection\, coefficient,(s)$', fontsize = 18)
output = "time_fixation_select_both.png"
plt.legend(loc='upper right', prop={'size':10})

#fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
