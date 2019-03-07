from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mydir = os.path.expanduser("~/GitHub/PopGen/")


def eqn_system(N, B, S, Y=0.01, k=0.01, Ks=0.1, alpha = 0.95, beta=0.5, gamma=0.85, sigma=0.1):
    mu = Y * k * (S / (S+Ks) )
    N_dot = (mu * N) - (sigma * N)
    S_dot = (alpha * beta * B) - (N * k * (S / (S+Ks) ))
    B_dot = (gamma * sigma * N) - (alpha * B)
    print(S_dot)
    return N_dot, S_dot, B_dot



dt = 0.01
stepCnt = 100000

# Need one more for the initial values
Ns = np.empty((stepCnt + 1,))
Ss = np.empty((stepCnt + 1,))
Bs = np.empty((stepCnt + 1,))

# Setting initial values
Ns[0], Ss[0], Bs[0] = (100, 1000000000, 0)

# Stepping through "time".
for i in range(stepCnt):
    # Derivatives of the X, Y, Z state
    N_dot, S_dot, B_dot = eqn_system(Ns[i], Ss[i], Bs[i])
    Ns[i + 1] = Ns[i] + (N_dot * dt)
    Ss[i + 1] = Ss[i] + (S_dot * dt)
    Bs[i + 1] = Bs[i] + (B_dot * dt)


fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(Ns, Ss, Bs, lw=0.5)
ax.set_xlabel("Population size")
ax.set_ylabel("Substrate (mol)")
ax.set_zlabel("Necromass (mol)")
ax.set_title("Necromass recycling")

fig.tight_layout()
fig.savefig(mydir + '/ode.png', bbox_inches = "tight", pad_inches = 0.4, dpi = 600)
plt.close()
