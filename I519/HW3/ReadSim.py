#!/usr/bin/env python
from __future__ import division
from sys import argv, exit
import random
import os
from pprint import pprint
import math


mydir = os.path.dirname(os.path.realpath(__file__))

def readFASTA(fileFASTA):
    '''Checks for fasta by file extension'''
    file_lower = fileFASTA.lower()
    '''Check for three most common fasta file extensions'''
    if file_lower.endswith('.txt') or file_lower.endswith('.fa') or \
    file_lower.endswith('.fasta') or file_lower.endswith('.fna'):
        with open(fileFASTA, "r") as f:
            return ParseFASTA(f)

def ParseFASTA(fileFasta):
    '''Gets the sequence name and sequence from a FASTA formatted file'''
    fasta_list=[]
    for line in fileFasta:
        if line[0] == '>':
            try:
                fasta_list.append(current_dna)
        	#pass if an error comes up
            except UnboundLocalError:
                pass
            current_dna = [line.lstrip('>').rstrip('\n'),'']
        else:
            current_dna[1] += "".join(line.split())
    fasta_list.append(current_dna)
    return fasta_list


def random_reads(genome, read_len, cov):
    genome_split = genome.split('.')
    read_len = int(read_len)
    cov = int(cov)
    OUT = open(str(mydir) + "/" +  str(genome_split[0]) +'_'+ "reads_" + str(read_len) +'_' + 'cov_' + str(cov) + '.fna','w+')
    genomeParsed = readFASTA(genome)
    name = genomeParsed[0][0]
    just_genome = genomeParsed[0][1]
    #just_genome = 'AAACCCGGGTTT'
    ''' Below we calculate how many reads we need, given the genome size, \
    the read length, and coverage'''
    genome_size = len(just_genome)
    genome_set = set(range(0,genome_size))
    print "Your genome size is " + str(genome_size) + ' bp'
    sites = range(0, genome_size)
    if read_len > genome_size:
        print "Your read length is longer than the genome"
        print "Exiting script"
        exit()
    read_number = (cov / read_len) * genome_size
    read_number_round = round(read_number,0)
    print "Generating " + str(int(read_number_round)) + " reads now"
    sample_size = 0
    read_tuples = []
    while sample_size < read_number:
        header = ">read_" + str(sample_size)
        print>> OUT, header
        start = random.randint(0,genome_size-1)
        start_plus_read = start + read_len
        if start_plus_read <= genome_size:
            read = just_genome[start:start + read_len]
            #print read
            print>> OUT, read
            range1 = (start, read_len+start)
            read_tuples.append(range1)
        else:
            difference = start_plus_read - genome_size
            read = just_genome[start:] + just_genome[:difference]
            print>> OUT, read
            #print range(start, read_len+start)
            range2 =  range(start, genome_size) + range(0,difference)
            for element in range2:
                if element in sites:
                    sites.remove(element)

        sample_size += 1
    print "Estimating coverage..."
    #no_coverage = [genome_set.difference(set(range(read_tuple[0], read_tuple[1])))
    #                for read_tuple in read_tuples]
    sites_covered = [(set(range(read_tuple[0], read_tuple[1])))
                    for read_tuple in read_tuples]
    set_sites_covered = set.union(*sites_covered)
    sites_not_covered = genome_set - set_sites_covered
    not_covered_list = list(sites_not_covered)
    poisson_coverage = round(math.exp(-cov), 4) * 100
    if len(not_covered_list) == 0:
        print "Every site is covered!"
    else:
        percent_not_covered = (len(not_covered_list)/genome_size) * 100
        print str(len(not_covered_list)) + " sites aren't covered"
        print str(round(percent_not_covered, 2)) + "% of the genome isn't covered."
        print "The Poisson distribution estimates that %s percent of sites aren't covered" % poisson_coverage
        #print "The following sites aren't covered: "
        #print '[%s]' % ', '.join(map(str, not_covered_list))

genm = argv[1]
read_len = argv[2]
cov = argv[3]


random_reads(genm, read_len, cov)
