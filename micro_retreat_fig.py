from __future__ import division
import os, math
import  matplotlib.pyplot as plt
import numpy as np

mydir = os.path.expanduser("~/GitHub/PopGen/")


def make_plot(s = 0.05, U_b = 0.001):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    t_est = 3

    x = range(1, 101)
    y = [((0.5 * np.exp(s * (x_i -t_est ) )) / s) for x_i in x]
    ax.plot(x, y, color = '#FF6347')
    ax.set_yscale('log', basey=10)
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 1000])
    ax.axhline(y = int(1/s), color='#87CEEB', ls = '--', lw = 3)
    ax.axvline(x = 1, color='#87CEEB', ls = '--', lw = 3)
    ax.axvline(x = t_est, color='#87CEEB', ls = '--', lw = 3)
    #ax.set_yscale('log', basey=10)
    #ax.set_ylim([0, 3])

    fig_name = mydir + 'micro_retreat.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()


make_plot()
