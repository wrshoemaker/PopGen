#!/usr/bin/env python
from __future__ import division
from sys import argv
import os
import optparse
import argparse
import math
import collections
import itertools

def readFASTA(fileFASTA):
    '''Checks for fasta by file extension'''
    file_lower = fileFASTA.lower()
    '''Check for three most common fasta file extensions'''
    if file_lower.endswith('.txt') or file_lower.endswith('.fa') or file_lower.endswith('.fasta'):
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

def kmer_count2(dna, k, minimum_percentage):
    dna = str(dna)
    total_kmers = len(dna) - k + 1
    minimum_count = (total_kmers * minimum_percentage) / 100
    #print("min count is " + str(minimum_count))
    # first assemble dict of kmer counts
    kmer2count = {}
    for x in range(len(dna)+1-k):
        kmer = dna[x:x+k]
        kmer2count[kmer] = kmer2count.get(kmer, 0) + 1

    # now select just the high-count kmers
    for kmer, count in kmer2count.items():
        if count < minimum_count:
            del kmer2count[kmer]
    #print(len(kmer2count))
    return(kmer2count)



def freq_nucleotides(dna):
    setX = set(str(dna))
    lenX = len(dna)
    letters = dict(collections.Counter(dna))
    letters.update((y, round((z/lenX),4)) for y, z in letters.items())
    return letters

def exptected_kmers(dna, k):
    '''takes a dictionary as input'''
    nuc_freq = freq_nucleotides(dna)
    len_dna = len(dna)
    bases=['A','T','G','C']
    k_mer_freq_dict = {}
    possible_k_mers = [''.join(p) for p in itertools.product(bases, repeat=k)]
    for x in possible_k_mers:
         k_mer_freq_dict_value = round(nuc_freq.get(x[0]) * nuc_freq.get(x[1]) * len_dna, 0)
         k_mer_freq_dict[x] = k_mer_freq_dict_value
    return k_mer_freq_dict
    
if __name__ == '__main__':
    #startTime = datetime.now()
    #start_time = time.time()
    parser = argparse.ArgumentParser(description = "Run DiNuc")
    parser.add_argument('-i', type = str, default = "genome.fa")
    params = parser.parse_args()

    input_fasta = params.i
    mydir = os.path.dirname(os.path.realpath(__file__))

    file_fasta = mydir + '/' + input_fasta
    fasta_input = readFASTA(file_fasta)
    seq = fasta_input[0][1]
    #print seq
    test = kmer_count2(seq, 2, 0)
    print "The observed 2-mer count is:"
    print test
    print "The expected 2-mer count is:"
    print exptected_kmers(seq, 2)
