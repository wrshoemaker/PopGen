import pandas as pd
from scipy.stats import gaussian_kde
import numpy as np
import  matplotlib.pyplot as plt


#table = pd.read_csv("Vos_ Didelot_2009.csv", header=True, delim_whitespace=True)
table = pd.read_excel("Vos_ Didelot_2009.xlsx", header=False)

gnm = table[table.columns[9]].values
recom = table[table.columns[5]].values
gnmLog = np.log10(gnm)

CI_upper = table[table.columns[7]].values
CIs = np.subtract(CI_upper, recom)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#plt.scatter(gnmLog,recom)
plt.errorbar(gnmLog, recom, yerr=CIs,  fmt = 'o', color = 'k')

plt.xticks(fontsize = 6) # work on current fig
plt.yticks(fontsize = 6)
plt.ylabel('r/m', fontsize = 14)
plt.xlabel('log(Genome Size)', fontsize = 14)

plt.tight_layout()
output = "output_plot.png"
plt.savefig(output, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
#plt.xscale()
plt.close()
