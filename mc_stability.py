from __future__ import division
import numpy as np

total = 100000

unstable_node = 0
unstable_spirals = 0
centers = 0
stable_spirals = 0
stable_node = 0
non_isolated_fixed_points = 0
saddle_points = 0
stars_and_degenerate_nodes = 0

for x in range(total):
    a,b,c,d = np.random.uniform(low=0.0, high=1.0, size=4)
    tau = a+d
    delta = (a*d) - (b*c)

    if delta < 0:
        saddle_points += 1
    elif delta == 0:
        centers +=1
    elif tau == 0:
        non_isolated_fixed_points += 1
    elif (tau**2) - 4*delta == 0:
        stars_and_degenerate_nodes += 1

    elif (tau**2 > 4*delta) and tau > 0:
        unstable_node += 1
    elif (tau**2 > 4*delta) and tau < 0:
        stable_node += 1

    elif (tau**2 < 4*delta) and tau > 0:
        unstable_spiral += 1
    elif (tau**2 < 4*delta) and tau < 0:
        stable_spiral += 1
    else:
        print(tau, delta)


print("Unstable nodes " + str(unstable_node/total))
print("Unstable spirals " + str(unstable_spirals/total))
print("Centers " + str(centers/total))
print("Stable spirals " + str(stable_spirals/total))
print("Stable nodes " + str(stable_node/total))
print("Non isolated fixed points " + str(non_isolated_fixed_points/total))
print("Saddle points " + str(saddle_points/total))
print("Stars and degenerate nodes " + str(stars_and_degenerate_nodes/total))

print(unstable_node + unstable_spirals + centers+stable_spirals + stable_node+non_isolated_fixed_points + saddle_points+stars_and_degenerate_nodes)
