import numpy as np
import scipy.ndimage as ndimage


im = ndimage.imread('me.jpg', flatten = False)

im_plt = ndimage.gaussian_filter(im, sigma = (0, 0, 0), order=0)

print(im[0][0])
