from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os, decimal

mydir = os.path.expanduser("~/github/PopGen/")

def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """
    Returns a string representation of the scientific
    notation of the given number formatted for use with
    LaTeX or Mathtext, with specified number of significant
    decimal digits and precision (number of decimal digits
    to show). The exponent to be used can also be specified
    explicitly.
    """
    if not exponent:
        exponent = int(np.floor(np.log10(abs(num))))
    coeff = round(num / float(10**exponent), decimal_digits)
    if not precision:
        precision = decimal_digits

    return r"{0:.{2}f}\cdot10^{{{1:d}}}".format(coeff, exponent, precision)

def plotPi(theta2 = 0, generations = False):
    N = 1000
    theta1s = [2* N* 0.0000005, 2* N*0.00000005, 2* N*0.000000005]
    fig, ax = plt.subplots()
    colors = ['#FF6347', '#FFA500', '#87CEEB']
    K = np.logspace(-3, 3, num = 1000, base=10.0)
    M = [(N/k) for k in K]
    for i, theta1 in enumerate(theta1s):
        y = []
        for K_i in K:
            term1 = theta1 + (theta1 / K_i)
            term2 = (1 + (1 / K_i))  * (theta2 / K_i)
            pi = term1 + term2
            y.append(pi)
        #plt.plot(x, np.asarray(y), 'k-', color = colors[i], label= r'$\theta = $' + str(theta1))
        theta1_SN = sci_notation(theta1)
        plt.plot(M, np.asarray(y), 'k-', color = colors[i], label= r'$\theta = {{{}}}$'.format(theta1_SN), linewidth=3)
    ax.set_ylabel('Expected nucleotide diversity, ' + r'$\mathbf{E}[\pi]$', fontsize=20)
    ax.set_ylim([0.000001, 1])
    ax.set_xscale('log', basex=10)
    ax.set_yscale('log', basey=10)
    #ax.set_ylim(-6, 0)

    ax.legend(loc='upper left')
    if generations == True:
        plt.axvline(N, linestyle='dashed', color = 'darkgrey', linewidth=3)
        ax.set_xlabel('Time in seed bank (generations), '+ r'$log_{10}$' , fontsize=20)
        fig.savefig(mydir + 'pi_SB_gens.png', \
                bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    else:
        ax.set_xlabel('Seed bank size, ' + r'$M$', fontsize=20)
        fig.savefig(mydir + 'pi_SB.png', \
                bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()

def Pfix():
    K = np.logspace(-3, 3, num = 1000, base=10.0)
    fig, ax = plt.subplots()
    y = 1
    x = 0
    pfix = []
    for K_i in K:
        num = y + (x*K_i)
        den = 1 + K_i
        pfix.append(num/den)
    print pfix
    print K
    plt.plot(K, np.asarray(pfix), 'k-', color = '#87CEEB', linewidth=3)
    ax.set_xlim([0.001, 1000])
    ax.set_xscale('log', basex=10)
    ax.set_ylim([0, 1])
    ax.set_xlabel('Relative seed bank size, N/M', fontsize=20)
    ax.set_ylabel('Fixation probability', fontsize=20)
    fig.savefig(mydir + 'K_SB.png', \
            bbox_inches = "tight", pad_inches = 0.4, dpi = 600)

#plotPi(generations = False)
#plotPi(generations = True)
Pfix()
