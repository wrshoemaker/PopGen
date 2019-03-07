from __future__ import division
import math, random, itertools, os
import numpy as np
#import scipy as sp
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt


mydir = os.path.expanduser("~/GitHub/PopGen/")


def regression_sim(iter=1000, confidence=0.95):
    ns = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    # log scale
    b0 = 6
    b1 = -0.8
    n_all = []
    ci95_all = []
    for n in ns:
        for i in range(iter):
            X = np.asarray([20, 40, 60, 80, 100, 120] * n)
            sigma2 = X**1.3
            eps = np.random.randn(len(X) ) * np.sqrt(sigma2)
            Y = b0+ (b1* X) + eps
            slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
            Y_diff = Y - slope
            MSE_sqrt = math.sqrt( sum(Y_diff ** 2) / ( len(X) -2 ) )
            #print(slope)
            MSE_sqrt_slope = MSE_sqrt / (  math.sqrt(  sum( (X - np.mean(X) ) **2   )  )   )
            #print(MSE_sqrt_slope)
            CI95 = stats.t.ppf((1 + confidence) / 2. ,  len(X)-2)  * MSE_sqrt_slope
            n_all.append(n)
            ci95_all.append(CI95)


    fig = plt.figure()
    plt.scatter(n_all, ci95_all, c='#175ac6', marker = 'o', s = 70, \
        edgecolors='#244162', linewidth = 0.6, alpha = 0.5, zorder=2)#, edgecolors='none')
    plt.xlabel("Sample size", fontsize = 16)
    plt.ylabel("95% Confidence interval", fontsize = 14)
    fig.tight_layout()
    fig.savefig(mydir + '/regression_sim.png', bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()




def brownian(x0, n, dt, delta, out=None):
    """
    Generate an instance of Brownian motion (i.e. the Wiener process):

        X(t) = X(0) + N(0, delta**2 * t; 0, t)

    where N(a,b; t0, t1) is a normally distributed random variable with mean a and
    variance b.  The parameters t0 and t1 make explicit the statistical
    independence of N on different time intervals; that is, if [t0, t1) and
    [t2, t3) are disjoint intervals, then N(a, b; t0, t1) and N(a, b; t2, t3)
    are independent.

    Written as an iteration scheme,

        X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)


    If `x0` is an array (or array-like), each value in `x0` is treated as
    an initial condition, and the value returned is a numpy array with one
    more dimension than `x0`.

    Arguments
    ---------
    x0 : float or numpy array (or something that can be converted to a numpy array
         using numpy.asarray(x0)).
        The initial condition(s) (i.e. position(s)) of the Brownian motion.
    n : int
        The number of steps to take.
    dt : float
        The time step.
    delta : float
        delta determines the "speed" of the Brownian motion.  The random variable
        of the position at time t, X(t), has a normal distribution whose mean is
        the position at time t=0 and whose variance is delta**2*t.
    out : numpy array or None
        If `out` is not None, it specifies the array in which to put the
        result.  If `out` is None, a new numpy array is created and returned.

    Returns
    -------
    A numpy array of floats with shape `x0.shape + (n,)`.

    Note that the initial value `x0` is not included in the returned array.
    """

    x0 = np.asarray(x0)

    # For each element of x0, generate a sample of n numbers from a
    # normal distribution.
    r = norm.rvs(size=x0.shape + (n,), scale=delta*math.sqrt(dt))

    # If `out` was not given, create an output array.
    if out is None:
        out = np.empty(r.shape)

    # This computes the Brownian motion by forming the cumulative sum of
    # the random samples.
    np.cumsum(r, axis=-1, out=out)

    # Add the initial condition.
    out += np.expand_dims(x0, axis=-1)

    return out

def plot_split(T1=2, T2=3):
    # The Wiener process parameter.
    delta = 2
    # Number of steps.
    N = 500
    # Time step size
    dt1 = T1/N
    dt2 = T2/N
    # Number of realizations to generate.
    m = 1
    # Create an empty array to store thte realizations.
    x1 = np.empty((m,N+1))
    # Initial values of x.
    x1[:, 0] = 50

    b_out1 = brownian(x1[:,0], N, dt1, delta, out=x1[:,1:])

    x2 = np.empty((2,N+1))
    x2[:, 0] = b_out1[:,-1]
    b_out2 = brownian(x2[:,0], N, dt2, delta, out=x2[:,1:])

    #print(np.shape(b_out1))
    #print(np.shape(b_out2))

    t1 = list(range(500))
    t2 = list(range(500, 1000))
    print()
    fig = plt.figure()

    plt.plot(t1, b_out1[0,:], c = 'k')
    plt.plot(t2, b_out2[0,:], c = 'b')
    plt.plot(t2, b_out2[1,:], c = 'r')

    plt.xlabel('Time')
    plt.ylabel('Trait value')

    plt.tight_layout()
    fig_name = mydir + 'trait_diverge.png'
    fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
    plt.close()



plot_split()


#regression_sim()
