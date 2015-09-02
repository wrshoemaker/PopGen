#!/usr/bin/env python
from __future__ import division
import numpy as np

p = 0.1
m = 0.1
s = 0.5
f = 10

matrixVal = np.matrix([[p, m], [f, s]])
nInitial = np.array([100,100000])
# 2) annual mortality rate for larvae is

print np.dot(matrixVal, nInitial)
x_free = np.zeros(10001)
x_free[0] = 1
x = x_free.copy()




def PopProj(M, N, gens):
    x_free = np.zeros(10001)
    #x_free[0] = N
    np.insert(x_free, 0, N)
    for x in range(0,gens):
        print x_free[0]
        if x == 0:
            x_dot = np.dot(M, N)
        elif x == 10000:
            n_next = x_free[x-1]
            print np.dot(M, n_next)
        else:
            n_next = x_free[x-1]
            pNew = np.dot(M, n_next)
            pFreq.insert(x, pNew)
