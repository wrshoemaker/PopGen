import numpy as np
import  matplotlib.pyplot as plt



def prob_fixation(y, K):
    '''
    x = freq in active population
    y = freq in dorm population
    K = relative seed bank size (n/M)
    '''
    x_range = np.arange(0,1,0.1)
    return x_range

#print prob_fixation(1,1)


print np.linspace(0.02, 2.0, num=20)
print np.logspace(0.02, 2.0, num=20)

list_test = [1,2,4,6]
print list_test
