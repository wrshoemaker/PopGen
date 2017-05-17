from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
def SelectOneLocus(p, s, h, a, d, gens):
    pFreq = []
    V_A = []
    V_D = []
    h2 = []
    W11 = 1
    W12 = 1 - h*s
    W22 = 1 - s
    for x in range(0,gens):
        if x == 0:
            pFreq.insert(x, p)
            V_A_0 = 2*p*(1-p)*((a+(d*((1-p)*p)))**2)
            V_A.insert(x, V_A_0)
            V_D_0 = (2*d*p*(1-p))**2
            V_D.insert(x, V_D_0)
            z_bar = (p**2)*a + (2*p*(1-p)*d) + ((1-p)**2)*-a
            alpha1 = p*a + (1-p)*d - z_bar
            alpha2 = ((1-p) * (-a)) + (p * d) - z_bar
            h2_new = V_A_0 / ( ((p**2)*2*(alpha1**2)) + (2*p*(1-p)*((alpha1 + alpha2)**2)) + (((1-p)**2)*2*(alpha2**2)) )
            #h2.insert(x, h2_new)
            print type(V_A_0), type(z_bar), type(alpha1), type(alpha2)
        else:
            p_next = pFreq[x-1]
            W_mean = ((p_next**2)*W11) + (2*(1-p_next)*p_next*W12) + (((1-p_next)**2)* W22)
            pNew = (p_next*((p_next*W11) + ((1-p_next)*W12))) / W_mean
            pFreq.insert(x, pNew)
            V_A_0 = 2*p_next*(1-p_next)*((a+(d*((1-p_next)*p_next)))**2)
            V_D_0 = (2*d*p_next*(1-p_next))**2
            V_A.insert(x, V_A_0)
            V_D.insert(x, V_D_0)
            z_bar = (p_next**2)*a + (2*p_next*(1-p_next)*d) + ((1-p_next)**2)*(-a)
            alpha1 = (p_next*a) + ((1-p_next)*d) - z_bar
            alpha2 = ((1-p_next) * (-a)) + (p_next * d) - z_bar
            h2_new = V_A_0 / ( ((p_next**2)*2*(alpha1**2)) + (2*p_next*(1-p_next)*((alpha1 + alpha2)**2)) + (((1-p_next)**2)*2*(alpha2**2)) )
            h2.insert(x, h2_new)
            print h2_new
    plt.plot(pFreq)
    plt.plot(V_A)
    plt.plot(V_D)
    #plt.plot(h2)
    plt.xlabel('t, generations')
    plt.ylabel('p')
    plt.show()
    return plt


SelectOneLocus(0.01, 0.2, 1, 1, -1, 1000)
