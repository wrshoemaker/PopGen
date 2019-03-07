from __future__ import division
import os
import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns

mydir = os.path.expanduser("~/GitHub/PopGen/")


df = pd.read_csv(mydir + 'muri2-libraries-metadata-plate4-longform.txt', sep = '\t')
df['Transfer_regime'] = df['Names'].map(lambda x: x[0])
#df1 = df[['strain','Half_life']]
#df1['Half_life_log'] = np.log10(df1.Half_life)

#f, ax = plt.subplots(figsize=(11, 15))

#ax.set_axis_bgcolor('#fafafa')
#plt.title("Box Plot of Transformed Data Set (Breast Cancer Wisconsin Data Set)")
#ax.set(xlim=(-.05, 1.05))
#ax = sns.boxplot(data = df1, orient = 'h', palette = 'Set2')
#ax = sns.boxplot(x="strain", y="Half_life_log", data=df1, orient = "v" )
#ax.set(xlabel='', ylabel=r'$t_{1/2},\, log_{10}$')
#ax.set_xlabel("",fontsize=0)
#ax.set_ylabel(r'$t_{1/2},\, log_{10}$',fontsize=30)
#for item in ax.get_xticklabels():
#    item.set_rotation(90)

#ax.figure.savefig(mydir + 'half_life_bp.png')
