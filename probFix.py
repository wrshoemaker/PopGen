from __future__ import division
import math, os
import  matplotlib.pyplot as plt
import numpy as np

mydir = os.path.expanduser("~/github/PopGen")


def probFix(N):
    S = (1/N) *2
    fig = plt.figure()
    Ns = []
    probs = []
    S_array = np.arange(-S,S,S/1000)
    for s in S_array:
        Ns.append(N * s)
        if s >0:
            prob = (2*s) / (1 - math.exp(-2*N*s))
        elif s < 0:
            prob = (2*-s) / (math.exp(2*N*-s) -1)
        else:
            prob = 1/N
        probs.append(prob * N)
    plt.plot(np.asarray(Ns), np.asarray(probs))
    plt.axhline(y=1, c = '#808080', ls='--')
    plt.xlabel('Scaled selection coefficient (' + r'$N_{e}s$' + '', fontsize=18)
    plt.ylabel('Relative fixation probability', fontsize=16)
    fig.savefig(mydir + '/probFix.png', bbox_inches='tight',  dpi = 600)
    plt.close()


probFix(10000000)
