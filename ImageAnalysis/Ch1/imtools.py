import os
import numpy as np
from PIL import Image
import pylab as pl


def get_imlist(path):
    """Returns a list of filenames for all jpg images in a directory"""
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

def imresize(im,sz):
    """ Resize an image array using PIL. """
    pil_im = Image.fromarray(uint8(im))
    return np.array(pil_im.resize(sz))

def imresize(im, sz):
    """ Resize an image array using PIL. """
    pil_im = Image.fromarray(uint8(im))
    return np.array(pil_im.resize(sz))

def histeq(im,nbr_bins=256):
    """ Histogram equalization of a grayscale image. """

    # get image histogram
    imhist,bins = pl.histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    im2 = np.interp(im.flatten(),bins[:-1],cdf)

    return im2.reshape(im.shape), cdf

def compute_average(imlist):
    """ Compute the average of a list of images. """

    # open first image and make into array of type float
    averageim = np.array(Image.open(imlist[0]), 'f')

    for imname in imlist[1:]:
        try:
            averageim += np.array(Image.open(imname))
        except:
            print imname + '...skipped'
    averageim /= len(imlist)

    # return average as uint8
    return np.array(averageim, 'uint8')

def pca(X):
    """ Principal Component Analysis input: X, matrix with training data
        stored as flattened arrays in rows return: projection matrix
        (with important dimensions first), variance and mean.
    """

    # get dimensions
    num_data,dim = X.shape

    # center data
    mean_X = X.mean(axis=0)
    X = X - mean_X

    if dim > num_data:
        # PCA - compact trick used
        M = np.dot(X,X.T) # covariance matrix
        e,EV = np.linalg.eigh(M) # eigenvalues and eigenvectors
        tmp = np.dot(X.T,EV).T # this is the compact trick
        V = tmp[::-1] # reverse since last eigenvectors are the ones we want
        S = sqrt(e)[::-1] # reverse since eigenvalues are in increasing order

        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA - SVD used
        U,S,V = np.linalg.svd(X)
        V = V[:num_data] # only makes sense to return the first num_data

    # return the projection matrix, the variance and the mean
    return V,S,mean_X
