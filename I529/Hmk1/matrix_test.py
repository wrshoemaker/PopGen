import numpy as np
from numpy import linalg as LA

mat = np.matrix( \
[[0.6, 0, 0, 0.6, 0, 0, 0.6, 0, 0],
[0.2, 0, 0, 0.2, 0, 0, 0.2, 0, 0],
[0.2, 0, 0, 0.2, 0, 0, 0.2, 0, 0],
[0, 0.2, 0, 0, 0.3, 0, 0, 0.2, 0],
[0, 0.6, 0, 0, 0.5, 0, 0, 0.6, 0],
[0, 0.2, 0, 0, 0.2, 0, 0, 0.2, 0],
[0, 0, 0.2, 0, 0, 0.2, 0, 0, 0.2],
[0, 0, 0.2, 0, 0, 0.2, 0, 0, 0.1],
[0, 0, 0.6, 0, 0, 0.6, 0, 0, 0.7]])

initial_state = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0])

mat =  LA.matrix_power(mat, 6)

mult =  np.dot(mat, initial_state)

print mult[:,1] + mult[:,4] + mult[:,7]

#print mat[1].sum() + mat[4].sum() + mat[7].sum()
