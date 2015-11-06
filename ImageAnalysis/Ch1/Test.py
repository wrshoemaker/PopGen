from PIL import Image
import os
import numpy as np
import pylab as pl
import imtools as it
from scipy.ndimage import filters
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

# THis returns a PIL image
pil_im = Image.open('../data/empire.jpg')
# Concert image to black & white
im_bw = np.array(Image.open('../data/empire.jpg').convert('L'))

# Save image as a new format
outfile = "pil_im.jpg"
pil_im.save(outfile)

out = pil_im.rotate(90)
out.save(outfile)

# matplotlib

im = np.array(Image.open('../data/empire.jpg'))

pl.imshow(im)

x = [100,100,400,400]
y = [200,500,200,500]

pl.plot(x,y, 'r*')
pl.plot(x[:2],y[:2])
title = "Plotting: 'empire.jpg'"
pl.title(title)
pl.axis('off')
pl.savefig('foo.png')

pl.figure()
pl.hist(im_bw.flatten(),128)
pl.savefig('hist.png')
#pl.gray()
#pl.contour(im_bw, origin="image")
#pl.axis('equal')
#pl.axis('off')

#im = np.array(Image.open('../data/AquaTermi_lowcontrast.jpg').convert('L'))
#im2,cdf = it.histeq(im)

## Test PCA
# put file names in list
font_list = it.get_imlist('../data/a_thumbs')
# open an image to get a size
im = np.array(Image.open(font_list[0]))
m,n = im.shape[0:2] # get size of the images
imnbr = len(font_list) # get the number of images

# create matrix to store all flattened images
immatrix = np.array([np.array(Image.open(im)).flatten()
            for im in font_list],'f')

# perform PCA
V,S, immean = it.pca(immatrix)

# show some images (mean and 7 first modes)
pl.figure()
pl.gray()
pl.subplot(2,4,1)
pl.imshow(immean.reshape(m,n))
for i in range(7):
    pl.subplot(2,4,i+2)
    pl.imshow(V[i].reshape(m,n))

pl.savefig('pca_dicking_around.png')

# Make 3x4 image
plt.figure()
plt.gray()
sigma = 5
im = np.array(Image.open('me.jpg').convert('L'))
print im
imx = np.zeros(im.shape)
filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)

imy = np.zeros(im.shape)
print imy
what = filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
print what

plt.savefig('me_test.png')
