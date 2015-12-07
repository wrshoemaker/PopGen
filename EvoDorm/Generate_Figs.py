from __future__ import division
import  matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.cm as cm

input_filename1 = '/Users/WRShoemaker/github/PopGen/EvoDorm/G500_S100_A100_D100.txt'
input_filename2 = "/Users/WRShoemaker/github/PopGen/EvoDorm/G500_S100_A100_D100_LS_good0.5.txt"
data1 = np.genfromtxt(input_filename1, dtype = "f8,f8,f8,f8,f8", names = ['c','WT','PI','TD', 'FD'], delimiter = " ")
data2 = np.genfromtxt(input_filename2, dtype = "f8,f8,f8,f8,f8", names = ['c','WT','PI','TD', 'FD'], delimiter = " ")

WT1 = list(((data1["WT"])))
c1 = list(((data1["c"])))
pi1 = list(((data1["PI"])))
td1 = list(((data1["TD"])))
fd1 = list(((data1["FD"])))
WT2 = list(((data2["WT"])))
c2 = list(((data2["c"])))
pi2 = list(((data2["PI"])))
td2 = list(((data2["TD"])))
fd2 = list(((data2["FD"])))

plt.subplot(3, 2, 1)
plt.scatter(c1,WT1,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([0,7])

plt.ylabel(r'$\hat{\theta}_{W}$', fontsize = 12, rotation = 0)
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
plt.title(r'$WF-Model$', fontsize = 12, rotation = 0)

plt.subplot(3, 2, 2)
plt.scatter(c2,WT2,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([0,7])

plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
#plt.title('WF-model', x = 0.54, y = 1.05, fontsize=16)
plt.title(r'$Stochastic\;Switching$', fontsize = 12, rotation = 0)


plt.subplot(3, 2, 3)
plt.scatter(c1,pi1,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([-0.05,.20])

plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
plt.ylabel(r'$\hat{\theta}_{T}$', fontsize = 12, rotation = 0)

plt.subplot(3, 2, 4)
plt.scatter(c2,pi2,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([-0.05,.20])

plt.xlabel('time (s)')
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)

plt.subplot(3, 2, 5)
plt.scatter(c1,td1,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([-3.0,-1.5])

plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)
plt.ylabel(r'$D_{T}$', fontsize = 12, rotation = 0)
plt.xlabel(r'$c$', fontsize = 12, rotation = 0)

plt.subplot(3, 2, 6)
plt.scatter(c2,td2,color='blue',s=5,edgecolor='none')
plt.xlim([0,100])
plt.ylim([-3.0,-1.5])

plt.xlabel(r'$c$', fontsize = 12, rotation = 0)
plt.tick_params(axis='x', labelsize=8)
plt.tick_params(axis='y', labelsize=8)




plt.savefig("fig.png")
