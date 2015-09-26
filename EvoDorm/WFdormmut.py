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
pop = {"AAAAAAAAAA": pop_size}
history = []
def simulate():
    clone_pop = dict(pop)
    history.append(clone_pop)
    for i in range(generations):
        time_step()
        clone_pop = dict(pop)
        history.append(clone_pop)
simulate()
pop

# Analyze trajectories
def get_distance(seq_a, seq_b):
    diffs = 0
    length = len(seq_a)
    assert len(seq_a) == len(seq_b)
    for chr_a, chr_b in zip(seq_a, seq_b):
        if chr_a != chr_b:
            diffs += 1
    return diffs / float(length)

get_distance("AAAAAAAAAA", "AAAAAAAAAB")

def get_diversity(population):
    haplotypes = population.keys()
    haplotype_count = len(haplotypes)
    diversity = 0
    for i in range(haplotype_count):
        for j in range(haplotype_count):
            haplotype_a = haplotypes[i]
            haplotype_b = haplotypes[j]
            frequency_a = population[haplotype_a] / float(pop_size)
            frequency_b = population[haplotype_b] / float(pop_size)
            frequency_pair = frequency_a * frequency_b
            diversity += frequency_pair * get_distance(haplotype_a, haplotype_b)
    return diversity

get_diversity(pop)

def get_diversity_trajectory():
    trajectory = [get_diversity(generation) for generation in history]
    return trajectory

import matplotlib.pyplot as plt
import matplotlib as mpl
def diversity_plot():
    mpl.rcParams['font.size']=14
    trajectory = get_diversity_trajectory()
    plt.plot(trajectory, "#447CCD")
    plt.ylabel("diversity")
    plt.xlabel("generation")

# Analyze and plot divergence
def get_divergence(population):
    haplotypes = population.keys()
    divergence = 0
    for haplotype in haplotypes:
        frequency = population[haplotype] / float(pop_size)
        divergence += frequency * get_distance(base_haplotype, haplotype)
    return divergence

def get_divergence_trajectory():
    trajectory = [get_divergence(generation) for generation in history]
    return trajectory
def divergence_plot():
    mpl.rcParams['font.size']=14
    trajectory = get_divergence_trajectory()
    plt.plot(trajectory, "#447CCD")
    plt.ylabel("divergence")
    plt.xlabel("generation")

# Plot haplotype trajectories

def get_frequency(haplotype, generation):
    pop_at_generation = history[generation]
    if haplotype in pop_at_generation:
        return pop_at_generation[haplotype]/float(pop_size)
    else:
        return 0
def get_trajectory(haplotype):
    trajectory = [get_frequency(haplotype, gen) for gen in range(generations)]
    return trajectory

def get_all_haplotypes():
    haplotypes = set()
    for generation in history:
        for haplotype in generation:
            haplotypes.add(haplotype)
    return haplotypes

haplotypes = get_all_haplotypes()
for haplotype in haplotypes:
    plt.plot(get_trajectory(haplotype))
plt.show()

def stacked_trajectory_plot(xlabel="generation"):
    mpl.rcParams['font.size']=18
    haplotypes = get_all_haplotypes()
    trajectories = [get_trajectory(haplotype) for haplotype in haplotypes]
    plt.stackplot(range(generations), trajectories, colors=colors_lighter)
    plt.ylim(0, 1)
    plt.ylabel("frequency")
    plt.xlabel(xlabel)

# Plot SNP trajectories

def get_snp_frequency(site, generation):
    minor_allele_frequency = 0.0
    pop_at_generation = history[generation]
    for haplotype in pop_at_generation.keys():
        allele = haplotype[site]
        frequency = pop_at_generation[haplotype] / float(pop_size)
        if allele != "A":
            minor_allele_frequency += frequency
    return minor_allele_frequency

def get_snp_trajectory(site):
    trajectory = [get_snp_frequency(site, gen) for gen in range(generations)]
    return trajectory

def get_all_snps():
    snps = set()
    for generation in history:
        for haplotype in generation:
            for site in range(seq_length):
                if haplotype[site] != "A":
                    snps.add(site)
    return snps


def snp_trajectory_plot(xlabel="generation"):
    mpl.rcParams['font.size']=18
    snps = get_all_snps()
    trajectories = [get_snp_trajectory(snp) for snp in snps]
    data = []
    for trajectory, color in itertools.izip(trajectories, itertools.cycle(colors)):
        data.append(range(generations))
        data.append(trajectory)
        data.append(color)
    plt.plot(*data)
    plt.ylim(0, 1)
    plt.ylabel("frequency")
    plt.xlabel(xlabel)


# Scale up
pop_size = 50
seq_length = 100
generations = 500
mutation_rate = 0.0001

seq_length * mutation_rate

2 * pop_size * seq_length * mutation_rate

base_haplotype = ''.join(["A" for i in range(seq_length)])
pop.clear()
del history[:]
pop[base_haplotype] = pop_size

simulate()

plt.figure(num=None, figsize=(14, 14), dpi=80, facecolor='w', edgecolor='k')
plt.subplot2grid((3,2), (0,0), colspan=2)
stacked_trajectory_plot(xlabel="")
plt.subplot2grid((3,2), (1,0), colspan=2)
snp_trajectory_plot(xlabel="")
plt.subplot2grid((3,2), (2,0))
diversity_plot()
plt.subplot2grid((3,2), (2,1))
divergence_plot()