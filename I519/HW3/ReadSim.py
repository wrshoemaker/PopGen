#!/usr/bin/env python
from __future__ import division
from sys import argv
import random

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
    #genomeParsed = readFASTA(genome)
    #name = genomeParsed[0][0]
    #just_genome = genomeParsed[0][1]
    just_genome = 'ACCCCCGGCGCATGCATATGCATGCTAGCATGGGGGGTTTTT'
    ''' Below we calculate how many reads we need, given the genome size, \
    the read length, and coverage'''
    genome_size = len(just_genome)
    read_number = (cov / read_len) * genome_size
    #print round(read_number,0)
    #reads = random.sample(just_genome, read_len)
    sample_size = 0
    while sample_size < read_number:
        start = random.randint(0,genome_size)
        slice_size = start + read_len
        ''' Todo: if slice positions go over genome size, start at the beginning'''
        if slice_size <= genome_size:
            read = just_genome[start:start + read_len]
            print read
        else:
            print "what"
        sample_size += 1


    #for x in geomeParsed:
    #    print x
        #name = genomeParsed[0][0]
        #genome = genomeParsed[0][1]
    #print genome
    #reads = random.sample(mylist, L)




genm = argv[1]
#read_len = argv[2]
#cov = argv[3]

#gnm = "/Users/WRShoemaker/github/PopGen/I519/HW3/NC_010698.fna"

random_reads(genm, 5, 1)
