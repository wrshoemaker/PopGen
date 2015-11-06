from __future__ import division
import numpy as np
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
import random

nucs = ['A', 'T', 'G', 'C']
def gen_haplotype(genome_size):
    return ''.join(random.choice('ACTG') for x in range(genome_size))

def generate_pop(size):
    popDict = {}
    haplotype = gen_haplotype()
    popDict[haplotype] = size
    return popDict


# So I guess I need to make the population global(or just not call it each iteration)

class Evolve(object):


    def __init__(self, size, genome_size, mut_rate, dorm_rate):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.size = int(size)
        self.genome_size = int(genome_size)
        self.mut_rate = float(mut_rate)
        self.dorm_rate = float(dorm_rate)

    population = generate_pop(self)

    def mutation_count(self):
        mean =  (self.mut_rate * self.size * self.genome_size)
        return np.random.poisson(mean)

    def get_random_haplotype(self):
        haplotypes = self.generate_pop().keys()
        frequencies = [x/float(self.size) for x in self.generate_pop().values()]
        total = sum(frequencies)
        frequencies = [x / total for x in frequencies]
        return np.random.choice(haplotypes, p=frequencies)

    def get_mutant(self, haplotype):
        site = np.random.randint(seq_length)
        possible_mutations = list(nucs)
        possible_mutations.remove(haplotype[site])
        mutation = np.random.choice(possible_mutations)
        new_haplotype = haplotype[:site] + mutation + haplotype[site+1:]
        return new_haplotype

    def mutation_event(self):
        haplotype = self.get_random_haplotype()
        population = self.generate_pop()
        print haplotype
        print population
        if population[haplotype] > 1:
            population[haplotype] -= 1
            new_haplotype = self.get_mutant(haplotype)
            if new_haplotype in pop:
                population[new_haplotype] += 1
            else:
                population[new_haplotype] = 1


evolve_test = Evolve(100, 5,0.001, 1.4)

print evolve_test.mutation_event()
