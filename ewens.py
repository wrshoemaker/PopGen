from __future__ import division
import pandas as pd
import os, math, re, operator


def product_list(my_list):
    return reduce(operator.mul, my_list, 1)

def ewens(a, n, theta):
    # test to make sure sum(j * a_J ) = n
    sum_a = 0

    for j, a_j  in   enumerate(a):
        j = j+1
        sum_a += a_j * j
    if sum_a != n:
        print 'Error: alleles do not sum to n'
    if theta == 0:
        term1 = 0
    else:
        term1 = math.factorial(n) / product_list([theta + i for i in range(0,n)])
    term2_sum = 1
    for j, a_j in enumerate(a):
        #print a_j
        j = j+1
        iter_j = (theta ** a_j) / (math.factorial(a_j) * (j**a_j))
        term2_sum *= iter_j
    return term1 * term2_sum
    #return term2_sum

#
def pick(total):

    def inner(highest, total):
        if total == 0:
            yield result
            return
        if highest == 1:
            result[0] = total
            yield result
            result[0] = 0
            return
        for i in reversed(range(total // highest + 1)):
            result[highest - 1] = i
            newtotal = total - i * highest
            for y in inner(min(highest - 1, newtotal),
                             newtotal):
                yield y

    result = [0] * total
    for x in inner(total, total):
        yield x
n = 10
theta = 0.8
sum1 = 0
for x in pick(n):
    e = ewens(x, n, theta)
    print x
    print e
    sum1 += e

print sum1
