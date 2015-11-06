from __future__ import division
import EvoDorm as ed

mutation_rate = 0.01
active_size = 1000
dormant_size = 0
seq_length = 5
generations = 10000
c = 1.5

#mut_count = ed.get_mutation_count(mutation_rate, active_size, seq_length)
pop = {}
pop = ed.generate_pop(active_size, dormant_size, seq_length)
#pop['Active']['AAATTTGGGA'] = 10
#pop['Active']['ACATTTGGGA'] = 10
#pop['Active']['ATATTTGGGA'] = 10
#pop['Active']['GTTTTTGGGA'] = 10
#pop['Active']['AAGAA'] = 1
#pop['Active']['AAAAT'] = 1


#print ed.tajimas_theta(ed.merge_two_dicts(pop['Active'], pop['Dormant']))

#pop = ed.merge_two_dicts(pop['Active'], pop['Dormant'])

#sim = ed.simulate(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c)
what =  ed.simulate_last(pop, mutation_rate, generations, seq_length, active_size, dormant_size, c)
pop = ed.merge_two_dicts(what['Active'], what['Dormant'])
#print 2 * active_size * mutation_rate
#print ed.wattersons_theta(what[-1], seq_length)
print ed.tajimas_theta(pop)
#print ed.tajimas_D(what[-1], seq_length)

#ed.tajimas_theta_plot(what, generations)
