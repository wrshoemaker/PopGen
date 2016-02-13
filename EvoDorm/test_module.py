from __future__ import division
import EvoDorm as ed
import timeit
import EvoDorm_test as edt
import os

mutation_rate = 100
active_size = 10
dormant_size = 0
seq_length = 10
generations = 100
c = 0
LH_strat = 'W'
good_freq = 0.5

#mut_count = ed.get_mutation_count(mutation_rate, active_size, seq_length)
#pop = {}
pop = edt.generate_pop(active_size, dormant_size, seq_length)
#pop['Active']['AAATTTGGGA'] = 10
#pop['Active']['ACATTTGGGA'] = 10
#pop['Active']['ATATTTGGGA'] = 10
#pop['Active']['GTTTTTGGGA'] = 10
#pop['Active']['AAGAA'] = 1
#pop['Active']['AAAAT'] = 1


#print ed.tajimas_theta(ed.merge_two_dicts(pop['Active'], pop['Dormant']))
#test_pop = {'TCA': 1, 'GTC': 1, 'CGA': 1}

#sim = ed.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c)
what =  edt.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c, False,LH_strat, good_freq)
print what
pop2 = edt.merge_two_dicts(what['Active'], what['Dormant'])
#print 2 * active_size * mutation_rate
#print pop
#print ed.fu_and_li_D(pop, seq_length)
print edt.tajimas_theta(pop2)
print edt.wattersons_theta(pop2, seq_length)
print edt.fu_and_li_D(pop2, seq_length)
print edt.tajimas_D(pop2, seq_length)
#print ed.fu_and_li_D(pop, seq_length)
#print ed.fu_and_li_theta(pop, seq_length)

#print ed.tajimas_D(what[-1], seq_length)


#ed.tajimas_theta_plot(what, generations)


mydir = os.path.dirname(os.path.realpath(__file__))



def generate_Tajimas_D(mutation_rate, generations, seq_length, active_size, dormant_size, history, LH_strat, good_freq):
    OUT = open(mydir + "/G" + str(generations) + "_S" + str(seq_length) + "_A" + str(active_size) + '_D' + str(dormant_size) + '_L' + str(LH_strat) + '_good' + str(good_freq) + '.txt','w+')
    for x in range(1, 100, 1):
        for y in range(0,10):
            pop = edt.generate_pop(active_size, dormant_size, seq_length)
            pop_sim = edt.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, x, False, LH_strat, good_freq)
            pop_merged = edt.merge_two_dicts(pop['Active'], pop['Dormant'])
            FD = edt.fu_and_li_D(pop_merged, seq_length)
            TD = edt.tajimas_D(pop_merged, seq_length)
            WT = edt.wattersons_theta(pop_merged, seq_length)
            PI = edt.tajimas_theta(pop_merged)
            print x, FD, TD
            print>> OUT, x, WT, PI, TD, FD
    #OUT.close()

#generate_Tajimas_D(mutation_rate, generations, seq_length, active_size, dormant_size, False, LH_strat, good_freq)

#print min(timeit.Timer('a=s[:]; timsort(a)', setup=setup).repeat(7, 1000))
