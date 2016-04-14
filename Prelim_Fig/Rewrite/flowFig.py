from __future__ import division
import pylab as plt
import FlowCytometryTools
from FlowCytometryTools import test_data_dir, test_data_file, FCMeasurement, FCPlate, ThresholdGate, PolyGate
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth, DBSCAN,MiniBatchKMeans,spectral_clustering
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KernelDensity
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
#import FlowFunctions as ff
import scipy.signal as signal
import pandas as pd
from scipy.sparse import hstack
import numpy as np
from scipy.stats import gaussian_kde


plate = FCPlate.from_dir(ID='Demo Plate', path= '/Users/WRShoemaker/github/Task2/FlowCyto/20151203/CTC_FVD_Hoechst_test120315/', parser='name')
plate = plate.transform('hlog', channels=['FSC-A', 'SSC-A', 'PI (B)-A', 'Alexa Fluor 488-A', 'Pacific Blue-A'])
plate = plate.dropna()
gate = ThresholdGate(2000.0, 'Pacific Blue-A', region='below')
gated_sample_beads_A3= plate['A3'].gate(gate)

plateData = plate['A3'].data[['Pacific Blue-A', 'PI (B)-A']]

CTCnumpy = gated_sample_beads_A3[['PI (B)-A']].values
DNAnumpy = gated_sample_beads_A3[['Pacific Blue-A']].values

def get_kdens_choose_kernel(xlist,expand, kernel = 0.5):
    """ Finds the kernel density function across a vector of values """
    xlist = xlist[np.logical_not(np.isnan(xlist))]
    density = gaussian_kde(xlist)
    n = len(xlist)
    if expand == False:
        xs = np.linspace(min(xlist),max(xlist),n)
    else:
        xs = np.linspace(min(xlist - expand),max(xlist + expand),n)
    #xs = np.linspace(0.0,1.0,n)
    density.covariance_factor = lambda : kernel
    density._compute_covariance()
    D = [xs,density(xs)]
    return D

def CV_KDE(oneD_array, expand = 1000):
    # remove +/- inf
    oneD_array = oneD_array[np.logical_not(np.isnan(oneD_array))]
    grid = GridSearchCV(KernelDensity(),
                    {'bandwidth': np.logspace(0.1, 5.0, 30)},
                    cv=50) # 20-fold cross-validation
    grid.fit(oneD_array[:, None])
    x_grid = np.linspace(np.amin(oneD_array), np.amax(oneD_array), 10000)
    # add nothing to the end of grid and pdf so you can get a nice looking kde
    kde = grid.best_estimator_
    pdf = np.exp(kde.score_samples(x_grid[:, None]))
    # returns grod for x-axis,  pdf, and bandwidth
    return_tuple = (x_grid, pdf, kde.bandwidth)
    return return_tuple

#returnKDE = get_kdens_choose_kernel(CTCnumpy, 1000, kernel = 0.05 )
#returnKDE = CV_KDE(CTCnumpy)


#km = KMeans(n_clusters=2, init='k-means++', n_init=10,
#            max_iter=300, tol=1e-04, random_state=0)

X = StandardScaler().fit_transform(plateData)

##############################################################################
# Compute DBSCAN

km = MiniBatchKMeans(n_clusters=2, init='k-means++', n_init=10,
            max_iter=300, tol=1e-04, random_state=0)
#km = spectral_clustering(X, n_clusters=2, eigen_solver='arpack')


y_km = km.fit_predict(X)
plt.scatter(X[y_km==0,0], X[y_km==0,1], s=25,
            c='green', marker='s', label='Active')
plt.scatter(X[y_km==1,0], X[y_km==1,1], s=25,
            c='red', marker='o', label='Dormant')

#plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1],
#            s=200, marker='*', c='red', label='centroids')

plt.legend()
plt.grid()
plt.tight_layout()
#plt.savefig('./figures/centroids.png', dpi=300)
plt.show()

#plt.savefig('./figures/centroids.png', dpi=300)
#plt.show()


#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.scatter(DNAnumpy, CTCnumpy)
#ax.set_xlim([-1000,4000])

#plt.plot(returnKDE[0], returnKDE[1],color = 'b', linestyle = '-', label="N = 1000, B = 1")
output = 'testKDE.png'
plt.savefig(output)
#plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
