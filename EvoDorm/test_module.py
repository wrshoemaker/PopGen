from __future__ import division
import EvoDorm as ed
import timeit
import EvoDorm_test as edt
import os

mutation_rate = 10
active_size = 100
dormant_size = 0
seq_length = 100
generations = 1000
c = 0
LH_strat = 'W'
good_freq = 0.5

#mut_count = ed.get_mutation_count(mutation_rate, active_size, seq_length)
#pop = {}
#pop = edt.generate_pop(active_size, dormant_size, seq_length)
#pop['Active']['AAATTTGGGA'] = 10
#pop['Active']['ACATTTGGGA'] = 10
#pop['Active']['ATATTTGGGA'] = 10
#pop['Active']['GTTTTTGGGA'] = 10
#pop['Active']['AAGAA'] = 1
#pop['Active']['AAAAT'] = 1


#print ed.tajimas_theta(ed.merge_two_dicts(pop['Active'], pop['Dormant']))
#test_pop = {'TCA': 1, 'GTC': 1, 'CGA': 1}

#sim = ed.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c)
#what =  edt.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c, False,LH_strat, good_freq)
#pop2 = edt.merge_two_dicts(what['Active'], what['Dormant'])


#print pop
#print ed.fu_and_li_D(pop, seq_length)
#print edt.tajimas_theta(pop2)
#print edt.wattersons_theta(pop2, seq_length)
#print edt.fu_and_li_D(pop2, seq_length)
#print edt.tajimas_D(pop2, seq_length)
#print ed.fu_and_li_D(pop, seq_length)
#print ed.fu_and_li_theta(pop, seq_length)

#print ed.tajimas_D(what[-1], seq_length)


#ed.tajimas_theta_plot(what, generations)


mydir = os.path.dirname(os.path.realpath(__file__))



def generate_Tajimas_D(mutation_rate, generations, seq_length, active_size, dormant_size, history, LH_strat, good_freq):
    for x in range(50,10000, 50):
        active_size_i = 10000 - x
        dormant_size_i = x
        OUT = open(mydir + "/G" + str(generations) + "_S" + str(seq_length) + "_A" + \
            str(active_size) + '_D' + str(dormant_size_i) + '.txt','w+')
        for iteration in range(0,1000, 1):
            pop = edt.generate_pop(active_size_i, dormant_size_i, seq_length)
            pop_sim = edt.simulate(pop, mutation_rate, generations, seq_length, active_size_i, dormant_size_i, 0.1, False, LH_strat, good_freq)
            pop_merged = edt.merge_two_dicts(pop_sim['Active'], pop_sim['Dormant'])
            FD = edt.fu_and_li_D(pop_merged, seq_length)
            TD = edt.tajimas_D(pop_merged, seq_length)
            WT = edt.wattersons_theta(pop_merged, seq_length)
            PI = edt.tajimas_theta(pop_merged)
            print dormant_size_i, iteration, WT, PI, FD, TD
            print>> OUT, dormant_size_i, WT, PI, TD, FD
        OUT.close()

generate_Tajimas_D(1, 10, 10, 100, dormant_size, False, LH_strat, good_freq)

#print min(timeit.Timer('a=s[:]; timsort(a)', setup=setup).repeat(7, 1000))
