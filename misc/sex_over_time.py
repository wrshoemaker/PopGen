from __future__ import division
import numpy as np
import scipy.stats as stats
import  matplotlib.pyplot as plt
import os

mydir = os.path.expanduser("~/GitHub/PopGen/misc")

x = np.asarray([1989, 1990, 1991, 1993, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2014])
# number of times having sex per year
y = np.asarray([59.5, 62, 61, 61.5, 59.8, 65.5, 59, 62.5, 64, 59.8, 57, 59.6, 55, 52.5 ])

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

# y = mx + b
# where y = 0 (i.e. no sex )
no_sex = -intercept / slope
print int(round(no_sex))
print p_value
print slope

fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

ax.plot(x, y, marker='o', alpha = 0.8, \
    linestyle='', ms=12, c = 'b')

plt.suptitle('How often Americans have sex over time', fontsize=20)
ax.text(2009, 65, r'$m = -0.271$', fontsize=16)
ax.text(2009, 64, r'$r^{2}=0.397$', fontsize=16)
ax.text(2009, 63, r'$p < 0.05$', fontsize=16)


#print r_value** 2
predict_y = intercept + slope * x
pred_error = y - predict_y
degrees_of_freedom = len(x) - 2
residual_std_error = np.sqrt(np.sum(pred_error**2) / degrees_of_freedom)
plt.plot(x, predict_y, 'k-')
plt.tick_params(axis='both', which='major', labelsize=10)
#plt.ylim([min(y)-0.1,max(y)+0.1])
#plt.xlim([min(x)-0.3,max(x)+ 0.05])
plt.ylabel('Average amount of sex', fontsize=20)
plt.xlabel('Year', fontsize=20)

fig.savefig(mydir + '/sex_fig.png', \
    bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
plt.close()
