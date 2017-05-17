from scipy.stats import norm
import math

def x(r, n, d):
    return (r * math.sqrt(n)) /  (2*d)


print norm.cdf(x(0.1, 20, 5))
