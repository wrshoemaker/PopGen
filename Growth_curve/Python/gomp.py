from __future__ import division
import pandas as pd
import numpy as np
import scipy.signal
import scipy.stats as stats
from statsmodels.base.model import GenericLikelihoodModel
import  matplotlib.pyplot as plt

import os, re

np.random.seed(123456789)

mydir = os.path.expanduser("~/GitHub/PopGen/Growth_curve/")


# Modified Gompertz Equation
def m_gop(t, b0, A, umax, L):
    t = np.asarray(t)
    term = -np.exp(((umax*np.exp(1)) / A) * (L - t) + 1)
    return b0 + (A*np.exp(term))

# function to generate confidence intervals based on Fisher Information criteria
def CI_FIC(results):
    # standard errors = square root of the diagnol of a variance-covariance matrix
    ses = np.sqrt(np.absolute(np.diagonal(results.cov_params())))
    cfs = results.params
    lw = cfs - (1.96*ses)
    up = cfs +(1.96*ses)
    return (lw, up)


class modifiedGompertz(GenericLikelihoodModel):
    def __init__(self, endog, exog, **kwds):
        super(modifiedGompertz, self).__init__(endog, exog, **kwds)
        #print len(exog)

    def nloglikeobs(self, params):
        b0 = params[0]
        A = params[1]
        umax = params[2]
        L = params[3]
        z = params[4]
        # probability density function (pdf) is the same as dnorm
        exog_pred = m_gop(self.endog, b0 = b0, A = A, umax = umax, L = L)
        # need to flatten the exogenous variable
        LL = -stats.norm.logpdf(self.exog.flatten(), loc=exog_pred, scale=np.exp(z))
        return LL

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, method="bfgs", **kwds):

        if start_params is None:
            b0_start = 1
            A_start = 2
            umax_start = 0.5
            L_start = 0.8
            z_start = 0.8

            start_params = np.array([b0_start, A_start, umax_start, L_start, z_start])

        return super(modifiedGompertz, self).fit(start_params=start_params,
                                maxiter=maxiter, method = method, maxfun=maxfun,
                                **kwds)

def cleanData(path_IN, path_OUT, wells = 48):
    IN = open(path_IN, 'r')
    OUT = open(path_OUT, 'w')
    for line in IN:
        line_clean = line.strip().split('\t')
        if len(line_clean) == wells + 2:
            if line_clean[0] == 'Time':
                line_clean[1] = 'Temp_C'
            print>> OUT, '\t'.join(line_clean)
    OUT.close()


def checkTemp(df):
    temp_min = min(df['Temp_C'])
    temp_max = max(df['Temp_C'])
    temp_diff = temp_max - temp_min
    if temp_diff > 3:
        print "Temperature difference greater than 3C, check for temperature effects"


def modGompGrowth(IN_file_name, interceptGuess=0.1, delta = 0.05, synergy=True, \
    temp = True, smooth = True):
    IN = pd.read_csv(mydir + 'data/clean/'+ IN_file_name, sep = '\t')
    IN['Time'] = pd.to_datetime(IN['Time'], format='%H:%M:%S')
    IN['Minutes'] = IN['Time'].dt.hour * 60 + IN['Time'].dt.minute
    OUT = open(mydir + 'data/params/' +  IN_file_name.split('.')[0] + '_params.txt', 'w')
    print>> OUT, 'Sample', 'b0', 'A', 'umax', 'L', 'z', 'umax_lw', 'umax_up', \
            'umax_lw_FI', 'umax_up_FI'
    t = IN['Minutes'].values / 60
    #t =  IN['Time'].values
    for column in IN:
        if IN[column].name == 'Time' or IN[column].name == 'Temp_C' or IN[column].name == 'Minutes':
            continue
        if IN[column].name != 'A2':
            continue
        # growth curve
        s = IN[column].values
        s_name = IN[column].name
        if max(s) - min(s) < delta:
            print "Observed change in OD is not greater than " +  str(delta) + \
                  " in well " + IN[column].name
            continue
        if smooth == True:
            taps = [1/11] * 11
            s_2 = scipy.signal.lfilter(taps, 1.0, s)
            s_2[0:5] = s[0:5]
            s_2[5:-5] = s_2[10:]
            s_2[-6:] = s[-6:]
        else:
            s_2 = s
        s_2_max =  np.argmax(s_2)
        if len(s_2) < s_2_max + 20:
            t_trim = t
            s_trim = s_2
        else:
            t_trim = t[:s_2_max + 20]
            s_trim = s_2[:s_2_max + 20]


        # we're going to loop through the following combination of
        # parameter values
        umax_start_list = [0.05,0.1,1]
        L_start_list = [-5,-0.5,0.1,5,10,20]
        z_start_list = [-2,-0.5]
        # and while keeping the following initial values constant
        b0_start = interceptGuess
        A_start = max(s_trim)
        #A_start = 1.5
        model = modifiedGompertz(t_trim, s_trim)
        results = []
        for umax_start in umax_start_list:
            for L_start in L_start_list:
                for z_start in z_start_list:
                    # b0, A, umax, L, z
                    start_params = [b0_start, A_start, umax_start, L_start, z_start]
                    #result = model.fit(start_params = start_params, method="lbfgs", optim_args={'bounds':[(0,1), (A_start,10), (0,5), (-20,20), (-20, 20)]})
                    result = model.fit(start_params = start_params, method="lbfgs", bounds= [(-1,1), (A_start * 0.66,10), (0,5), (-20,20), (-20, 20)] )
                    #result = model.fit(start_params = start_params, method="lbfgs", optim_args={'bounds':1e-6})
                    #if result.mle_retvals['warnflag'] == 0:
                    results.append(result)
        AICs = [result.aic for result in results]
        print AICs
        print min(AICs)
        best = results[AICs.index(min(AICs))]
        best_CI_FIC = CI_FIC(best)
        best_CI = best.conf_int()
        best_params = best.params
        print best_params
        #print best.mle_settings
        #boot_mean, boot_std, boot_samples = best.bootstrap(nrep=500, store=True)
        print>> OUT, IN[column].name, best_params[0], best_params[1], best_params[2], \
                best_params[3], best_params[4], best_CI[2][0], best_CI[2][1], \
                best_CI_FIC[0][2], best_CI_FIC[1][2]


        fig = plt.figure()
        plt.plot(best.endog, best.exog, c = 'black', lw = 2)
        y_pred = m_gop(best.endog, best_params[0], best_params[1], best_params[2], best_params[3])
        plt.plot(best.endog, y_pred, c = 'blue', lw = 2)
        #m_gop(t, b0, A, umax, L)
        fig.tight_layout()
        fig_name = mydir + 'figs/' + IN[column].name + '.png'
        fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
        plt.close()

    OUT.close()





#path_IN = mydir + 'data/raw/GrowthCurve_Example.txt'
#path_OUT = mydir + 'data/clean/GrowthCurve_Example_clean.txt'
#cleanData(path_IN, path_OUT)
path = 'GrowthCurve_Example_clean.txt'
#path = 'Pseudo.csv'
modGompGrowth(path, smooth = True)
