from __future__ import division
import math
import random

def poisson(mean):
    sum_p = -math.log(random.random())
    i = 0
    while sum_p < mean:
        sum_p += -math.log(random.random())
        i = i + 1
    return i

U = 2

print poisson(U)
