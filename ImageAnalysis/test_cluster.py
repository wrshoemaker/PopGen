from itertools import cycle
from time import time
from scipy import ndimage
import scipy as sp

dna = sp.misc.imread('/Users/WRShoemaker/github/PopGen/ImageAnalysis/test.jpg')


dnaf = ndimage.gaussian_filter(dna, 1)
T = 25
labeled, nr_objects = ndimage.label(dnaf > T) # `dna[:,:,0]>T` for red-dot case
print "Number of objects is %d " % nr_objects

import matplotlib.pyplot as plt
plt.imsave('labeled_dna.png', labeled)
