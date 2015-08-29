from __future__ import division
import random
#output a random base

def random_sequence(L):
    dna = ["A","G","C","T"]
    sequence = ''
    L = int(L)
    for i in range(0,L):
        sequence += random.choice(dna)
    return sequence

what = random_sequence(100)
print what[3]
