from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt


x_iter = 1000
x = np.linspace(0.0, 1.0, num=x_iter)
def prob_fixation(y, K, x_iter):
    '''
    x = freq in active population
    y = freq in dorm population
    K = relative seed bank size (n/M)
    '''
    x_range = np.linspace(0.0, 1.0, num=x_iter)
    g = np.vectorize(lambda x: (y + (x * K) )  / (1 + K) )
    return g(x_range)

line1 = prob_fixation(0.5, 0.01, x_iter)
line2 = prob_fixation(0.5, 0.1, x_iter)
line3 = prob_fixation(0.5, 1.0, x_iter)
line4 = prob_fixation(0.5, 10.0, x_iter)
line5 = prob_fixation(0.5, 100.0, x_iter)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


plt.plot(x, line1)
plt.plot(x, line2,  color = 'b')
plt.plot(x, line3)
plt.plot(x, line4)


plt.tight_layout()

output = "dorm_fix_prob.png"
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
