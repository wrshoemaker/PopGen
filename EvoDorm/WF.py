# packages
from __future__ import division
import numpy as np
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse
from collections import Counter


# global variables
active_size = 50
dormant_size = 950
pop_size = active_size + dormant_size
seq_length = 100
alphabet = ['A', 'T', 'G', 'C']
mutation_rate = 0.0001
# per gen per individual per site
generations = 400

c = 10

# population
base_haplotype = ''.join(["A" for i in range(seq_length)])
pop = {}
pop['Active'] = {}
pop['Dormant'] = {}
pop['Active'][base_haplotype] = active_size
pop['Dormant'][base_haplotype] = dormant_size
history = []





# mutation
def get_mutation_count():
    mean = mutation_rate * active_size * seq_length
    return np.random.poisson(mean)

def get_random_haplotype(sub_pop):
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
        frequencies = [x/float(dormant_size) for x in pop['Dormant'].values()]
        print dormant_size
        total = sum(frequencies)
        frequencies = [x / total for x in frequencies]
        return np.random.choice(haplotypes, p=frequencies)

def get_mutant(haplotype):
    site = np.random.randint(seq_length)
    possible_mutations = list(alphabet)
    possible_mutations.remove(haplotype[site])
    mutation = np.random.choice(possible_mutations)
    new_haplotype = haplotype[:site] + mutation + haplotype[site+1:]
    return new_haplotype

def mutation_event():
    haplotype = get_random_haplotype('Active')
    if pop['Active'][haplotype] > 1:
        pop['Active'][haplotype] -= 1
        new_haplotype = get_mutant(haplotype)
        if new_haplotype in pop['Active']:
            pop['Active'][new_haplotype] += 1
        else:
            pop['Active'][new_haplotype] = 1

def mutation_step():
    mutation_count = get_mutation_count()
    for i in range(mutation_count):
        mutation_event()

# reproduce active pop, drift acts here
def get_offspring_counts():
	haplotypes = pop['Active'].keys()
	frequencies = [x/float(active_size) for x in pop['Active'].values()]
	total = sum(frequencies)
	frequencies = [x / total for x in frequencies]
	return list(np.random.multinomial(active_size, frequencies))

def offspring_step():
    counts = get_offspring_counts()
    for (haplotype, count) in zip(pop['Active'].keys(), counts):
        if (count > 0):
            pop['Active'][haplotype] = count
        else:
            del pop['Active'][haplotype]

def dormancy_step():
    if dormant_size <= 0:
        pass
    else:
        K = active_size / dormant_size
        dormancy_rate = int(round(c, 0))
        resuscitation_rate = int(round((K*c), 0))
        for i in range(0, dormancy_rate):
            new_haplotype = get_random_haplotype('Active')
            pop['Active'][new_haplotype] -= 1
            if new_haplotype in pop['Dormant']:
                pop['Dormant'][new_haplotype] += 1
            else:
                pop['Dormant'][new_haplotype] = 1
        for i in range(0, resuscitation_rate):
            new_haplotype = get_random_haplotype('Dormant')
            pop['Dormant'][new_haplotype] -= 1
            if new_haplotype in pop['Active']:
                pop['Active'][new_haplotype] += 1
            else:
                pop['Active'][new_haplotype] = 1


def time_step():
    mutation_step()
    offspring_step()
    dormancy_step()

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    #z = x.copy()
    #z.update(y)
    x = Counter(x)
    y = Counter(y)
    z = x + y
    #print sum(Counter(z).values())
    return z

def simulate():
    haplotypes_active = pop['Active']
    haplotypes_dormant = pop['Dormant']
    #print haplotypes_active, haplotypes_dormant
    pop_merged = merge_two_dicts(haplotypes_dormant, haplotypes_active)
    #print pop_merged
    clone_pop = dict(pop_merged)
    history.append(clone_pop)
    for i in range(generations):
        time_step()
        haplotypes_active = pop['Active']
        haplotypes_dormant = pop['Dormant']
        pop_merged = merge_two_dicts(haplotypes_dormant, haplotypes_active)
        clone_pop = pop_merged
        #print sum(clone_pop.values())
        history.append(clone_pop)



# plot diversity
def get_distance(seq_a, seq_b):
    diffs = 0
    length = len(seq_a)
    assert len(seq_a) == len(seq_b)
    for chr_a, chr_b in zip(seq_a, seq_b):
        if chr_a != chr_b:
            diffs += 1
    return diffs / float(length)

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

def get_diversity_trajectory():
    trajectory = [get_diversity(generation) for generation in history]
    return trajectory

def diversity_plot(xlabel="generation"):
    mpl.rcParams['font.size']=14
    trajectory = get_diversity_trajectory()
    plt.plot(trajectory, "#447CCD")
    plt.ylabel("diversity")
    plt.xlabel(xlabel)

# plot divergence
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

def divergence_plot(xlabel="generation"):
    mpl.rcParams['font.size']=14
    trajectory = get_divergence_trajectory()
    plt.plot(trajectory, "#447CCD")
    plt.ylabel("divergence")
    plt.xlabel(xlabel)

# plot trajectories
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

def stacked_trajectory_plot(xlabel="generation"):
    colors_lighter = ["#A567AF", "#8F69C1", "#8474D1", "#7F85DB", "#7F97DF", "#82A8DD", "#88B5D5", "#8FC0C9", "#97C8BC", "#A1CDAD", "#ACD1A0", "#B9D395", "#C6D38C", "#D3D285", "#DECE81", "#E8C77D", "#EDBB7A", "#EEAB77", "#ED9773", "#EA816F", "#E76B6B"]
    mpl.rcParams['font.size']=18
    haplotypes = get_all_haplotypes()
    trajectories = [get_trajectory(haplotype) for haplotype in haplotypes]
    plt.stackplot(range(generations), trajectories, colors=colors_lighter)
    plt.ylim(0, 1)
    plt.ylabel("frequency")
    plt.xlabel(xlabel)

# plot snp trajectories
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
    colors = ["#781C86", "#571EA2", "#462EB9", "#3F47C9", "#3F63CF", \
    "#447CCD", "#4C90C0", "#56A0AE", "#63AC9A", "#72B485", "#83BA70", \
    "#96BD60", "#AABD52", "#BDBB48", "#CEB541", "#DCAB3C", "#E49938", \
    "#E68133", "#E4632E", "#DF4327", "#DB2122"]
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

#if __name__=="__main__":
#    parser = argparse.ArgumentParser(description = "run wright-fisher simulation with mutation and genetic drift")
#    parser.add_argument('--active_size', type = int, default = 50.0, help = "Active population size")
#    parser.add_argument('--dormant_size', type = int, default = 50.0, help = "Dormant population size")
#    parser.add_argument('--mutation_rate', type = float, default = 0.0001, help = "mutation rate")
#    parser.add_argument('--seq_length', type = int, default = 100, help = "sequence length")
#    parser.add_argument('--dorm_rate', type = int, default = 1, help = "Rate individual's enter dormant state")
#    parser.add_argument('--generations', type = int, default = 500, help = "generations")
#    parser.add_argument('--summary', action = "store_true", default = False, help = "don't plot trajectories")

#    params = parser.parse_args()
#    active_size = params.active_size
#    dormant_size = params.dormant_size
#    mutation_rate = params.mutation_rate
#    seq_length = params.seq_length
#    generations = params.generations
#    c = params.dorm_rate
#    pop_size = active_size + dormant_size
simulate()

#    base_haplotype = ''.join(["A" for i in range(seq_length)])
#    pop = {}
#    pop['Active'] = {}
#    pop['Dormant'] = {}
#    pop['Active'][base_haplotype] = active_size
#    pop['Dormant'][base_haplotype] = dormant_size
#    history = []

plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
    #if params.summary:
    #    plt.subplot2grid((2,1), (0,0))
    #    diversity_plot()
    #    plt.subplot2grid((2,1), (1,0))
    #    divergence_plot()
    #else:
plt.subplot2grid((3,2), (0,0), colspan=2)
stacked_trajectory_plot(xlabel="")
plt.subplot2grid((3,2), (1,0), colspan=2)
snp_trajectory_plot(xlabel="")
plt.subplot2grid((3,2), (2,0))
diversity_plot()
plt.subplot2grid((3,2), (2,1))
divergence_plot()
name = "A" + str(active_size) + "_D" + str(dormant_size) + "_M" + str(mutation_rate) + "_G" + str(generations) + "_R" + str(c) + ".png"
plt.savefig(name)
