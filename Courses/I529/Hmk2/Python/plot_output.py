from __future__ import division
import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt
import collections

#pos = pd.read_csv("../data/test.txt", header=True, delim_whitespace=True)
#neg = pd.read_csv("../data/out_neg.txt", header=True, delim_whitespace=True)

coding = pd.read_csv("../data/coding_test_out.txt", header=True, delim_whitespace=True)
non_coding = pd.read_csv("../data/non_coding_test_out.txt", header=True, delim_whitespace=True)

coding_LL = coding[coding.columns[1]].values
non_coding_LL = non_coding[non_coding.columns[1]].values

coding_TP = sum(x >= 0 for x in coding_LL)
coding_FP = sum(x < 0 for x in coding_LL)

non_coding_TP = sum(x < 0 for x in non_coding_LL)
non_coding_FP = sum(x >= 0 for x in non_coding_LL)

print coding_TP / len(coding_LL)
print non_coding_TP / len(non_coding_LL)

def get_kdens_choose_kernel(xlist,expand, kernel = 0.5):
    """ Finds the kernel density function across a vector of values """
    xlist = xlist[np.logical_not(np.isnan(xlist))]
    density = gaussian_kde(xlist)
    n = len(xlist)
    if expand == False:
        xs = np.linspace(min(xlist),max(xlist),n)
    else:
        xs = np.linspace(min(xlist - expand),max(xlist + expand),n)
    #xs = np.linspace(0.0,1.0,n)
    density.covariance_factor = lambda : kernel
    density._compute_covariance()
    D = [xs,density(xs)]
    return D

#pos_LL = pos[pos.columns[1]].values
#neg_LL = neg[neg.columns[2]].values
#all_LL = np.hstack((neg_LL, pos_LL))

#kde_data = get_kdens_choose_kernel(pos_LL, 20, kernel = 0.4)
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#zip_kde = zip(kde_data[0], kde_data[1])

#negative_zip = [x for x in zip_kde if x[0] <= 0]
#positive_zip = [x for x in zip_kde if x[0] >= 0]

#negative_unzip = zip(*negative_zip)
#positive_unzip = zip(*positive_zip)

#ax.plot(negative_unzip[0], negative_unzip[1], c='black')
#ax.plot(positive_unzip[0], positive_unzip[1], c='black')
#ax.fill_between(negative_unzip[0], negative_unzip[1],1e-6,color='red', alpha=0.5)
#ax.fill_between(positive_unzip[0], positive_unzip[1],1e-6,color='green', alpha=0.5)

#plt.xticks(fontsize = 6) # work on current fig
#plt.yticks(fontsize = 6)
#plt.ylabel('Probability Density', fontsize = 14)
#plt.xlabel('Likelihood', fontsize = 14)

#plt.tight_layout()
#output = "../figures/output_plot.png"
#plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
#plt.close()
