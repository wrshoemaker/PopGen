from __future__ import division
import os, math
import  matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm

mydir = os.path.expanduser("~/GitHub/PopGen/nasa/")


def nasa_fig():
    fig = plt.figure()

    ax1 = fig.add_subplot(211)
    # Plot between -10 and 10 with .001 steps.
    x_axis1 = np.arange(-15, 15, 0.001)
    x_axis2 = np.arange(0, 30, 0.001)
    x_axis3 = np.arange(10, 40, 0.001)
    # Mean = 0, SD = 2.

    ax1.plot(x_axis1, norm.pdf(x_axis1,0,2), 'k', label="Ancestor")
    ax1.plot(x_axis2, norm.pdf(x_axis2,15,2), 'b:', label='Spore forming')
    ax1.plot(x_axis3, norm.pdf(x_axis3,25,2), 'r--', label="Non-spore forming")
    ax1.set_xlim([-15,47])
    plt.xlabel('Fitness (i.e., growth rate)', fontsize = 12)
    plt.ylabel('Number of individuals', fontsize = 11)
    plt.legend(loc = 'upper right', fontsize = 8)
    plt.xticks([])
    plt.yticks([])
    ax1.arrow(0, 0.1, 15, 0, width=0.004, \
        head_width=0.02, head_length=2,  length_includes_head=True, \
        shape='full', color = 'b', alpha = 0.8)

    ax1.arrow(0, 0.075, 25, 0, width=0.004, \
        head_width=0.02, head_length=2,  length_includes_head=True, \
        shape='full', color = 'r', alpha = 0.8)
    #ax1.text(2.45, 0.115, "Rate of adaptive evolution", fontsize=10, fontweight='bold')
    ax1.text(-0.5, 0.22, r'$T_{0}$', fontsize=10, fontweight='bold', color= 'k')
    ax1.text(14.5, 0.22, r'$T_{1}$', fontsize=10, fontweight='bold', color = 'b')
    ax1.text(24.5, 0.22, r'$T_{1}$', fontsize=10, fontweight='bold', color = 'r')
    ax1.text(-13.5, 0.22, "a)", fontsize=12, fontweight='bold')

    ax1.set_ylim([0, 0.25])

    ax2 = fig.add_subplot(212)
    loc1, scale1, size1 = (-2, 1, 175)
    loc2, scale2, size2 = (2, 0.2, 50)
    x2 = np.concatenate([np.random.normal(loc=loc1, scale=scale1, size=size1),
                          np.random.normal(loc=loc2, scale=scale2, size=size2)])
    x_eval = np.linspace(x2.min() - 1, x2.max() + 1, 500)
    kde2 = stats.gaussian_kde(x2, bw_method='silverman')
    ax2.plot(x_eval, kde2(x_eval), 'b:', label='Spore forming', alpha = 0.8)
    zip_x_y = zip(x_eval, kde2(x_eval))
    new_y = []
    for item in zip_x_y:
        if (item[0] < 0) and (item[1] > 0.08):
            new_y.append(0.08)
        else:
            new_y.append(item[1])
    ax2.plot(x_eval, new_y, 'r--', label="Non-spore forming", alpha = 0.8)
    ax2.text(-5.8, 0.23, "b)", fontsize=12, fontweight='bold')
    #ax2.text(-5.83, 0.23, "v)", fontsize=12, fontweight='bold')
    #plt.title(r'$Bacillus$' + ' fitness landscape', fontsize = 16)
    #ax2.title.set_text(r'$Bacillus$' + ' fitness landscape', font = 14)
    #ax2.set_title(r'$Bacillus$' + ' fitness landscape', fontsize = 16)
    plt.xlabel('Genotype', fontsize = 12)
    plt.ylabel('Fitness (i.e., growth rate)', fontsize = 11)
    plt.xticks([])
    plt.yticks([])
    #plt.legend(loc = 'upper right')


    fig_name = mydir + 'fig2.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()

nasa_fig()
