import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import statsmodels.api as sm

rndm_10 = pd.read_csv('./freq_rndm_output_10.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)
rndm_100 = pd.read_csv('./freq_rndm_output_100.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)
rndm_1000 = pd.read_csv('./freq_rndm_output_1000.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)

perm_10 = pd.read_csv('./freq_perm_output_10.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)
perm_100 = pd.read_csv('freq_perm_output_100.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)
perm_1000 = pd.read_csv('freq_perm_output_1000.txt', sep = ' ',
    names = ['line', 'a', 'c', 'g', 't'], header = None)


data_frames = [rndm_10, perm_10, rndm_100, perm_100, rndm_1000, perm_1000]
entropy_arrays = []
for x in data_frames:
    x['H'] = x.apply(lambda row: \
        stats.entropy((row['a'], row['c'], row['g'],  row['t']), base = 2), axis=1)
    entropy_arrays.append(x['H'].values)
    print np.mean(x['a'].values), np.mean(x['c'].values), \
        np.mean(x['g'].values), np.mean(x['t'].values)
    print np.std(x['a'].values), np.std(x['c'].values), \
        np.std(x['g'].values), np.std(x['t'].values)
