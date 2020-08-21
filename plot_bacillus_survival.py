from __future__ import division
import math, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


mydir = os.path.expanduser("~/GitHub/PopGen")

df = pd.read_csv(mydir + '/bacillus_survival_muri.csv', sep = ',')

df['N_all'] = df['nt'] * (10** df['nt-dil'] )
df['N_heat'] = df['ht'] * (10** df['ht-dil'] )



df['N_veg'] = df['N_all'] - df['N_heat']
df['days'] = df['time'] / 24

df['N_heat'] = df.apply(lambda x: x.N_heat * 3.5 if x.time <2136  else x.N_heat, axis=1)


df_spo0a = df.loc[df['strain'] == 'Spo_0A']
df_wt = df.loc[df['strain'] == 'KBS0812']


fig = plt.figure(figsize = (9, 6))
fig.tight_layout(pad = 2.8)

# Scatterplot on main ax
ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=1)

ax1.scatter(df_wt.days.values, df_wt.N_veg.values, alpha = 0.5, c ='#175ac6', label = 'Vegetative')
ax1.scatter(df_wt.days.values, df_wt.N_heat.values, alpha = 0.5, c ='red', label = 'Spores')
ax1.set_title('')

ax1.set_ylim([0.8, 4000000000])
ax1.set_title(r'$\mathit{B. \,subtilis} \; \mathrm{sp. \,KBS0812}$',fontsize = 14)

ax1.set_yscale('log',basey=10)
ax1.set_ylabel('Cell density (CFUs/mL)', fontsize = 12)
ax1.legend(loc='lower right')


ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=1)

ax2.scatter(df_spo0a.days.values, df_spo0a.N_veg.values, alpha = 0.5, c ='#175ac6', label = 'Vegetative')

ax2.set_title(r'$\mathit{B. \,subtilis} \; \Delta \mathrm{spo0A}$',fontsize = 14)

ax2.set_ylim([0.8, 4000000000])
ax2.set_yscale('log', basey=10)
ax2.set_ylabel('Cell density (CFUs/mL)', fontsize = 12)
#ax2.legend(loc='upper right')

ax2.set_xlabel('Days', fontsize = 16)


plt.tight_layout()
fig_name = mydir + '/bacillus_survival_muri.png'
fig.savefig(fig_name, bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
plt.close()
