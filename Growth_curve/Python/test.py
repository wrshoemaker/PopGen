from __future__ import division

from matplotlib import  pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
from statsmodels.base.model import GenericLikelihoodModel

np.random.seed(123456789)


N = 1000
pi = 0.3
lambda_ = 2.
inflated_zero = stats.bernoulli.rvs(pi, size=N)
x = (1 - inflated_zero) * stats.poisson.rvs(lambda_, size=N)

# zero inflated poisson
def zip_pmf(x, pi=pi, lambda_=lambda_):
    if pi < 0 or pi > 1 or lambda_ <= 0:
        return np.zeros_like(x)
    else:
        return (x == 0) * pi + (1 - pi) * stats.poisson.pmf(x, lambda_)

class ZeroInflatedPoisson(GenericLikelihoodModel):
    def __init__(self, endog, exog=None, **kwds):
        if exog is None:
            exog = np.zeros_like(endog)

        super(ZeroInflatedPoisson, self).__init__(endog, exog, **kwds)

    def nloglikeobs(self, params):
        pi = params[0]
        lambda_ = params[1]
        #print self.exog.shape
        #print self.endog.shape
        #print len(-np.log(zip_pmf(self.endog, pi=pi, lambda_=lambda_)))
        return -np.log(zip_pmf(self.endog, pi=pi, lambda_=lambda_))

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
        if start_params is None:
            lambda_start = self.endog.mean()
            excess_zeros = (self.endog == 0).mean() - stats.poisson.pmf(0, lambda_start)

            start_params = np.array([excess_zeros, lambda_start])
        return super(ZeroInflatedPoisson, self).fit(start_params=start_params,
                                                    maxiter=maxiter, maxfun=maxfun, **kwds)

model = ZeroInflatedPoisson(x)
results = model.fit()

#print results
