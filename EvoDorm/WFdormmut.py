from __future__ import division
from sys import argv
from itertools import groupby
import collections
from collections import OrderedDict
import math
import random
import numpy as np
import itertools

#DNA = ''
#DNA+=weightedchoice([("C", 10], ("G", 20), ("A", 40"), ("T", 30)])

alphabet = ['A', 'T', 'G', 'C']
pop_size = 100
seq_length = 10
base_haplotype = "AAAAAAAAAA"
pop = {}
pop["AAAAAAAAAA"] = 100
#pop["AATTTAAAAA"] = 30
#pop["AAATAAAAAA"] = 30



mutation_rate = 0.005 # per gen per individual per site

def gen_haplotype(length):
    return ''.join(random.choice('ACTG') for x in range(length))

def gen_population(popsize, genomesize):
    popDict = {}
    haplotype = gen_haplotype(genomesize)
    popDict[haplotype] = popsize
    return popDict

#print gen_population(100,100)

def get_mutation_count():
    mean = mutation_rate * pop_size * seq_length
    return np.random.poisson(mean)



def get_random_haplotype():
    haplotypes = pop.keys()
    frequencies = [x/float(pop_size) for x in pop.values()]
    total = sum(frequencies)
    frequencies = [x / total for x in frequencies]
    return np.random.choice(haplotypes, p=frequencies)

check = get_random_haplotype()
print check
#site = np.random.randint(seq_length)
#possible_mutations = list(alphabet)
#possible_mutations.remove(check[site])

#print possible_mutations

def get_mutant(haplotype):
    site = np.random.randint(seq_length)
    possible_mutations = list(alphabet)
    possible_mutations.remove(haplotype[site])
    mutation = np.random.choice(possible_mutations)
    new_haplotype = haplotype[:site] + mutation + haplotype[site+1:]
    return new_haplotype

#test = get_random_haplotype()
#print get_mutant(test)

def mutation_event():
    haplotype = get_random_haplotype()
    if pop[haplotype] > 1:
        pop[haplotype] -= 1
        new_haplotype = get_mutant(haplotype)
        if new_haplotype in pop:
            pop[new_haplotype] += 1
        else:
            pop[new_haplotype] = 1


def mutation_step():
    mutation_count = get_mutation_count()
    for i in range(mutation_count):
        mutation_event()
#print mutation_event()
#print pop
generations = 5


# Adding genetic drift
def get_offspring_counts():
    haplotypes = pop.keys()
    frequencies = [x/float(pop_size) for x in pop.values()]
    return list(np.random.multinomial(pop_size, frequencies))

def offspring_step():
    counts = get_offspring_counts()
    for (haplotype, count) in zip(pop.keys(), counts):
        if (count > 0):
            pop[haplotype] = count
        else:
            del pop[haplotype]

# Combine

def time_step():
    mutation_step()
    offspring_step()

def simulate():
    for i in range(generations):
        time_step()
simulate()

print pop
# Reord
