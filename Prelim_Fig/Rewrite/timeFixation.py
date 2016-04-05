from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt
import math


p_iter = 1000
N = 1000
p = np.linspace(1/N, (1-1/N), num=p_iter)

def prob_fixation(N, p_iter, B=1):
    '''
    N = population size
    p_iter = number of floats to take in allele freq range (0,1)
    '''
    x_range = np.linspace(1/N, (1-1/N), num = p_iter)
    g = np.vectorize(lambda x: (-2 * N * (B ** 2)* \
    	( ( (1-x) * np.log(1-x) ) + ( (x) * np.log(x) )   ) ))
    return g(x_range)

line1 = prob_fixation(N, p_iter)
line2 = prob_fixation(N, p_iter, 2)
line3 = prob_fixation(N, p_iter, 3)
line4 = prob_fixation(N, p_iter, 4)
line5 = prob_fixation(N, p_iter, 5)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


plt.plot(p, line1,color = 'b', linestyle = '-', label="N = 1000, B = 1")
plt.plot(p, line2, color = 'b',linestyle = '--', label="N = 1000, B = 2")
plt.plot(p, line3, color = 'b',linestyle = '-.', label="N = 1000, B = 3")
plt.plot(p, line4, color = 'b',linestyle = ':', label="N = 1000, B = 4")
#plt.plot(p, line5, color = 'b', linestyle = ' ', label="N = 1000, B = 5")

plt.tight_layout()
plt.ylabel(r'$\bar{t}(p)$', fontsize = 18, rotation = 90)
plt.xlabel(r'$p$', fontsize = 18)
output = "dorm_fix_prob.png"
plt.legend(loc='upper left', prop={'size':10})

#fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
