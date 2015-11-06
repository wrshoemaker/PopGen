import numpy as np
import scipy.ndimage as ndimage
import scipy.misc as misc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import filters
import matplotlib.gridspec as gridspec

im = ndimage.imread('me.jpg', flatten = False)
im = ndimage.interpolation.rotate(im, 270)

imx = np.zeros(im.shape,dtype=np.float64)
filters.sobel(im,1,imx)

imy = np.zeros(im.shape,dtype=np.float64)
filters.sobel(im,0,imy)


magnitude=np.sqrt(imx**2+imy**2)

plt.figure(figsize = (4,4))
gs1 = gridspec.GridSpec(4, 4)
gs1.update(wspace=0.0025, hspace=0.0025)

for i in range(16):
    ax1 = plt.subplot(gs1[i])
    plt.axis('off')
    ax1.set_aspect('equal')

    if i == 0:
        im_plt = ndimage.gaussian_filter(im, sigma = (0, 0, 0), order=0)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 1:
        im_plt = ndimage.gaussian_filter(im, sigma = (4, 4, 0), order=0)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 2:
        im_plt = ndimage.gaussian_filter(im, sigma = (10, 10, 0), order=0)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 3:
        im_plt = ndimage.gaussian_filter(im, sigma = (15, 15, 0), order=0)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 4:
        im_plt = ndimage.gaussian_filter(im, sigma = (0, 0, 0), order=1)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 5:
        im_plt = ndimage.gaussian_filter(im, sigma = (1.5, 1.5, 0), order=1)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 6:
        im_plt = ndimage.gaussian_filter(im, sigma = (2, 2, 0), order=1)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 7:
        im_plt = ndimage.gaussian_filter(im, sigma = (5, 5, 0), order=1)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 8:
        im_plt = ndimage.gaussian_filter(im, sigma = (0, 0, 0), order=2)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 9:
        im_plt = ndimage.gaussian_filter(im, sigma = (1.5, 1.5, 0), order=2)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 10:
        im_plt = ndimage.gaussian_filter(im, sigma = (2, 2, 0), order=2)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 11:
        im_plt = ndimage.gaussian_filter(im, sigma = (5, 5, 0), order=2)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 12:
        im_plt = ndimage.gaussian_filter(im, sigma = (0, 0, 0), order=3)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 13:
        im_plt = ndimage.gaussian_filter(im, sigma = (1.5, 1.5, 0), order=3)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 14:
        im_plt = ndimage.gaussian_filter(im, sigma = (2, 2, 0), order=3)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    elif i == 15:
        im_plt = ndimage.gaussian_filter(im, sigma = (5, 5, 0), order=3)
        #im_plt = ndimage.filters.gaussian_gradient_magnitude(im, sigma = 5)
        plt.imshow(im_plt,cmap=plt.cm.gray)
    plt.axis('off')

plt.savefig("me_bw.png", bbox_inches='tight',dpi = 600, pad_inches = 0.4)
