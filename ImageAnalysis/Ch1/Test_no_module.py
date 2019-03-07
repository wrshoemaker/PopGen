import numpy as np
import scipy.ndimage as ndimage
import scipy.misc as misc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

img = ndimage.imread('regs.png', flatten = False)
#img = Image.open('me.jpg').convert('L')
#img = ndimage.interpolation.rotate(img, 270)

plt.figure()

plt.axis('off')
plt.subplot(4, 3, 1)
#ax.set_adjustable('box-forced')
img1 = ndimage.gaussian_filter(img, sigma=(0, 0, 0), order=0)
plt.imshow(img1, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')
#ax.set_adjustable('box-forced')

plt.subplot(4, 3, 2)
img2 = ndimage.gaussian_filter(img, sigma=(2, 2, 0), order=0)
plt.imshow(img2, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 3)
img3 = ndimage.gaussian_filter(img, sigma=(5, 5, 0), order=0)
plt.imshow(img3, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 4)
img4 = ndimage.gaussian_filter(img, sigma=(10, 10, 0), order=0)
plt.imshow(img4, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')


plt.subplot(4, 3, 5)
img5 = ndimage.gaussian_filter(img, sigma=(0, 0, 0), order=1)
plt.imshow(img5, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 6)
img6 = ndimage.gaussian_filter(img, sigma=(2, 2, 0), order=1)
plt.imshow(img6, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 7)
img7 = ndimage.gaussian_filter(img, sigma=(5, 5, 0), order=1)
plt.imshow(img7, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 8)
img8 = ndimage.gaussian_filter(img, sigma=(10, 10, 0), order=1)
plt.imshow(img8, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')



plt.subplot(4, 3, 9)
img9 = ndimage.gaussian_filter(img, sigma=(0, 0, 0), order=2)
plt.imshow(img9, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 10)
img10 = ndimage.gaussian_filter(img, sigma=(2, 2, 0), order=2)
plt.imshow(img10, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 11)
img11 = ndimage.gaussian_filter(img, sigma=(5, 5, 0), order=2)
plt.imshow(img11, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')

plt.subplot(4, 3, 12)
img12 = ndimage.gaussian_filter(img, sigma=(10, 10, 0), order=2)
plt.imshow(img12, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)

#plt.imshow(img, interpolation='nearest')
# Note the 0 sigma for the last axis, we don't wan't to blurr the color planes together!
#plt.imshow(img, interpolation='nearest', cmap = "Greys_r", vmin = 0, vmax = 255)
plt.axis('off')
plt.savefig("regs_bw.png", bbox_inches='tight',dpi = 600, pad_inches = 0.4)
