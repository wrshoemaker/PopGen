from __future__ import division
import numpy as np
import itertools
import math
import matplotlib.pyplot as plt
import pylab
import matplotlib as mpl
import argparse
from collections import Counter

def generate_base_haplotype(seq_length):
    base_haplotype = ''.join(["A" for i in range(seq_length)])
    return base_haplotype

def generate_pop(active_size, dormant_size, seq_length):
    base_haplotype = generate_base_haplotype(seq_length)
    pop = {}
    pop['Active'] = {}
    pop['Dormant'] = {}
    pop['Active'][base_haplotype] = active_size
    pop['Dormant'][base_haplotype] = dormant_size
    return pop

# mutation
def get_mutation_count(mutation_rate, active_size, seq_length):
    mean = mutation_rate * active_size * seq_length
    return np.random.poisson(mean)

def get_random_haplotype(pop, sub_pop):
    # Need random haplotype for active only
    if sub_pop == 'Active':
        haplotypes = pop['Active'].keys()
        active_size_step = sum(pop['Active'].values())
        frequencies = [x/float(active_size_step) for x in pop['Active'].values()]
        total = sum(frequencies)
        frequencies = [x / total for x in frequencies]
        return np.random.choice(haplotypes, p=frequencies)
    elif sub_pop == 'Dormant':
        haplotypes = pop['Dormant'].keys()
        dormant_size_step = sum(pop['Dormant'].values())
        frequencies = [x/float(dormant_size_step) for x in pop['Dormant'].values()]
        total = sum(frequencies)
        frequencies = [x / total for x in frequencies]
        return np.random.choice(haplotypes, p=frequencies)

def get_mutant(haplotype, seq_length):
    alphabet = ['A', 'T', 'G', 'C']
    site = np.random.randint(seq_length)
    possible_mutations = list(alphabet)
    possible_mutations.remove(haplotype[site])
    mutation = np.random.choice(possible_mutations)
    new_haplotype = haplotype[:site] + mutation + haplotype[site+1:]
    return new_haplotype

def mutation_event(pop, seq_length):
    sub_pop = 'Active'
    haplotype = get_random_haplotype(pop, sub_pop)
    if pop['Active'][haplotype] > 1:
        pop['Active'][haplotype] -= 1
        new_haplotype = get_mutant(haplotype, seq_length)
        if new_haplotype in pop['Active']:
            pop['Active'][new_haplotype] += 1
        else:
            pop['Active'][new_haplotype] = 1

def mutation_step(pop, mutation_rate, active_size, seq_length):
    mutation_count = get_mutation_count(mutation_rate, active_size, seq_length)
    for i in range(mutation_count):
        mutation_event(pop, seq_length)

# reproduce active pop, drift acts here
def get_offspring_counts(pop, active_size):
    haplotypes = pop['Active'].keys()
    frequencies = [x/float(active_size) for x in pop['Active'].values()]
    total = sum(frequencies)
    frequencies = [x / total for x in frequencies]
    return list(np.random.multinomial(active_size, frequencies))

def offspring_step(pop, active_size):
    counts = get_offspring_counts(pop, active_size)
    for (haplotype, count) in zip(pop['Active'].keys(), counts):
        if (count > 0):
            pop['Active'][haplotype] = count
        else:
            del pop['Active'][haplotype]


def dormancy_step(pop, active_size, dormant_size, c):
    if dormant_size <= 0:
        pass
    else:
        K = active_size / dormant_size
        dormancy_rate = int(round(c, 0))
        resuscitation_rate = int(round((K*c), 0))
        for i in range(0, dormancy_rate):
            new_haplotype = get_random_haplotype(pop, 'Active')
            pop['Active'][new_haplotype] -= 1
            if new_haplotype in pop['Dormant']:
                pop['Dormant'][new_haplotype] += 1
            else:
                pop['Dormant'][new_haplotype] = 1
        for i in range(0, resuscitation_rate):
            new_haplotype = get_random_haplotype(pop, 'Dormant')
            pop['Dormant'][new_haplotype] -= 1
            if new_haplotype in pop['Active']:
                pop['Active'][new_haplotype] += 1
            else:
                pop['Active'][new_haplotype] = 1

def time_step(pop, mutation_rate, seq_length, active_size, dormant_size, c):
    mutation_step(pop, mutation_rate, active_size, seq_length)
    offspring_step(pop, active_size)
    dormancy_step(pop, active_size, dormant_size, c)

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    #z = x.copy()
    #z.update(y)
    x = Counter(x)
    y = Counter(y)
    z = x + y
    return z


def simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c):
    history = []
    new_pop = []
    haplotypes_active = pop['Active']
    haplotypes_dormant = pop['Dormant']
    pop_merged = merge_two_dicts(haplotypes_dormant, haplotypes_active)
    history.append(pop_merged)
    for i in range(generations):
        time_step(pop, mutation_rate, seq_length, active_size, dormant_size, c)
        haplotypes_active = pop['Active']
        haplotypes_dormant = pop['Dormant']
        pop_merged = merge_two_dicts(haplotypes_dormant, haplotypes_active)
        history.append(pop_merged)
    return history


def simulate_last(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c):
    '''Accepts a nested dictioanry of active and dormant sub-pops containing  haplotypes and counts'''
    haplotypes_active = pop['Active']
    haplotypes_dormant = pop['Dormant']
    pop_merged = merge_two_dicts(haplotypes_dormant, haplotypes_active)
    #print old_pop
    #print new_pop

    for i in range(generations):
        time_step(pop, mutation_rate, seq_length, active_size, dormant_size, c)
    return pop


# Genetic diversity parameters

def a1(n):
    '''Given n, this function returns the (n-1)th harmonic number'''
    n = int(n)
    return sum((1.0/d) for d in range(1,n))

def a2(n):
    '''Given n, this function returns the (n-1)th squared harmonic number'''
    n = int(n)
    return sum((1.0/(d**2)) for d in range(1,n))

def b1(n):
    '''Creates b1 for the variance of Tajima's theta'''
    n = int(n)
    return ((n+1) /  (3*(n-1)))

def b2(n):
    '''Creates b2 for the variance of Tajima's theta'''
    n = int(n)
    num = ((n**2) + n + 3) * 2
    den = 9 * n * (n-1)
    return num / den

def c1(n):
    n = int(n)
    '''Creates c1 for the variance of Tajima's theta'''
    return b1(n) - (1 / a1(n))

def c2(n):
    n = int(n)
    '''Creates c2 for the variance of Tajima's theta'''
    return b2(n) - ((n+2) / (a1(n) * n)) + (a2(n) / (a1(n) ** 2 ))

def e1(n):
    n = int(n)
    return c1(n) / a1(n)

def e2(n):
    n = int(n)
    return c2(n) / ( (a1(n) ** 2) + a2(n) )

def cn(n):
    n = int(n)
    num = ( 2 * n * a1(n) ) - (4 * (n-1))
    den = (n-1) * (n-2)
    return num / den

def vD(n):
    n = int(n)
    chunk1 = (a1(n) ** 2) / ( a2(n) + (a1(n) ** 2) )
    chunk2 = cn(n) - ((n + 1) / (n - 1))
    return 1 + (chunk1 * chunk2)

def uD(n):
    n = int(n)
    return a1(n) - 1 - vD(n)

def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

# AKA # of segregating sites
def wattersons_theta(pop, seq_length):
    '''Accepts a single dictionary of a population where keys are haplotypes'''
    '''and values are the counts'''
    reference = generate_base_haplotype(seq_length)
    seq_number = sum(pop.values())
    list_of_seqs =  list(flatten(pop.keys()))
    list_of_seqs.insert(0, reference)
    site_freq_spec = zip(*list_of_seqs)
    set_sfs = [set(sublist) for sublist in site_freq_spec]
    K = 0
    for site in set_sfs:
        if len(site) > 1:
            K += 1
    theta = K / a1(seq_number)
    return theta

def fu_and_li_theta(pop, seq_length):
    reference = generate_base_haplotype(seq_length)
    seq_number = sum(pop.values())
    # a haplotype occuring once is a prerequisite for a singleton
    # Select haplotypes that occur only once
    singletons = []
    for key, value in pop.iteritems():
        if value == 1:
            singletons.append(key)
    singletons.insert(0, reference)
    site_freq_spect = zip(*singletons)
    what = zip(*singletons)
    '''Indicates that there's a singleton'''
    site_freq_spec = [x for x in zip(*singletons) if x.count(x[0]) == (len(x) -1) ]
    n_1 = len(site_freq_spec)
    return n_1

def get_distance(seq_a, seq_b):
    diffs = 0
    length = len(seq_a)
    assert len(seq_a) == len(seq_b)
    for chr_a, chr_b in zip(seq_a, seq_b):
        if chr_a != chr_b:
            diffs += 1
    #return diffs / float(length)
    return diffs

# AKA Pi
def tajimas_theta(population):
    '''Accepts a single dictionary of a population where keys are haplotypes \
        and values are the counts'''
    pop_size = sum(population.values())
    haplotypes = population.keys()
    haplotype_count = len(haplotypes)
    diversity = 0
    for i in range(haplotype_count):
        haplotype_a = haplotypes[i]
        frequency_a = population[haplotype_a] / float(pop_size)
        for j in range(0, i):
            #for j in range(haplotype_count):
            haplotype_b = haplotypes[j]
            #frequency_b = population[haplotype_b] / float(pop_size)
            #frequency_pair = frequency_a * frequency_b
            #diversity += frequency_pair * get_distance(haplotype_a, haplotype_b)
            diversity += (get_distance(haplotype_a, haplotype_b))
    return (diversity * (2 / (pop_size * (pop_size-1))))

#def zfsw_theta(pop):

#def fay_and_wu_theta(population)

def tajimas_D(population, seq_length):
    #population = merge_two_dicts(pop['Active'], pop['Dormant'])
    pop_size = sum(population.values())
    theta = wattersons_theta(population, seq_length)
    pi = tajimas_theta(population)
    S_n = theta * a1(pop_size)
    num = pi - theta
    den = math.sqrt( (e1(pop_size) * S_n) + (e2(pop_size) * S_n * (S_n-1)) )
    D_T = num / den
    return D_T

def fu_and_li_D(population, seq_length):
    pop_size = sum(population.values())
    theta = wattersons_theta(population, seq_length)
    a1_pop = a1(pop_size)
    S_n = theta * a1_pop
    num = S_n - ( a1_pop * fu_and_li_theta(population, seq_length) )
    den = math.sqrt((uD(pop_size) * S_n) + (vD(pop_size) * (S_n ** 2)))
    return num / den


# Measure the genetic diversity in the simulation
def get_wattersons_theta_trajectory(history, seq_length):
    trajectory = [wattersons_theta(generation, seq_length) for generation in history]
    return trajectory

def wattersons_theta_plot(history, seq_length, xlabel="generation"):
    mpl.rcParams['font.size']=14
    trajectory = get_wattersons_theta_trajectory(history, seq_length)
    plt.plot(trajectory, "#447CCD")
    plt.ylabel(r'$\hat{\theta}_{W}$', rotation=0, fontsize = 18)
    #ax.set_ylabel(r'MG-RAST 99%' '\n' r'$\alpha$', rotation=90, size=12)
    plt.xlabel(xlabel)
    plt.savefig('wattersons_theta.png')

def get_tajimas_theta_trajectory(history, seq_length):
    trajectory = [tajimas_theta(generation) for generation in history]
    return trajectory

def tajimas_theta_plot(history, seq_length, xlabel="generation"):
    mpl.rcParams['font.size']=14
    trajectory = get_tajimas_theta_trajectory(history, seq_length)
    plt.plot(trajectory, "#447CCD")
    plt.ylabel(r'$\hat{\theta}_{\pi}$', rotation=0, fontsize = 18)
    plt.xlabel(xlabel)
    plt.savefig('tajimas_theta.png')


def get_frequency(haplotype, generation, history):
    pop_at_generation = history[generation]
    pop_size = sum(pop_at_generation.values())
    if haplotype in pop_at_generation:
        return pop_at_generation[haplotype]/float(pop_size)
    else:
        return 0

def get_trajectory(haplotype, generations, history):
    trajectory = [get_frequency(haplotype, gen, history) for gen in range(generations)]
    return trajectory

def get_all_haplotypes(history, generations):
    haplotypes = set()
    for generation in history:
        for haplotype in generation:
            haplotypes.add(haplotype)
    return haplotypes

def stacked_trajectory_plot(history, generations, xlabel="generation"):
    colors_lighter = ["#A567AF", "#8F69C1", "#8474D1", "#7F85DB", "#7F97DF", "#82A8DD", "#88B5D5", "#8FC0C9", "#97C8BC", "#A1CDAD", "#ACD1A0", "#B9D395", "#C6D38C", "#D3D285", "#DECE81", "#E8C77D", "#EDBB7A", "#EEAB77", "#ED9773", "#EA816F", "#E76B6B"]
    mpl.rcParams['font.size']=18
    haplotypes = get_all_haplotypes(history, generations)
    trajectories = [get_trajectory(haplotype, generations, history) for haplotype in haplotypes]
    plt.stackplot(range(generations), trajectories, colors=colors_lighter)
    plt.ylim(0, 1)
    plt.ylabel("frequency")
    plt.xlabel(xlabel)
    plt.savefig('test_stacked_trajectory.png')


def get_tajimas_D_trajectory(history, seq_length):
    trajectory = [tajimas_D(generation, seq_length) for generation in history]
    return trajectory

def tajimas_D_plot(history, seq_length, xlabel="generation"):
    mpl.rcParams['font.size']=14
    trajectory = get_tajimas_D_trajectory(history, seq_length)
    plt.plot(trajectory, "#447CCD")
    plt.ylabel(r'$D_{T}$', rotation=0, fontsize = 18)
    plt.xlabel(xlabel)
    plt.savefig('tajimas_D.png')
