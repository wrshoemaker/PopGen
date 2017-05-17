#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math
import random
import os

#mydir = os.path.expanduser("~/github/PopGen/I519/HW2/")

def read_fasta(file_fasta):
    '''Checks for fasta by file extension'''
    file_lower = file_fasta.lower()
    '''Check for three most common fasta file extensions'''
    if file_lower.endswith('.txt') or file_lower.endswith('.fa') or file_lower.endswith('.fasta') or file_lower.endswith('.fna'):
        with open(file_fasta, "r") as f:
            return parse_fasta(f)
    else:
        print 'File does not end with .txt, .fasta, .fa, or .fna'
def parse_fasta(file_fasta):
    '''Gets the sequence name and sequence from a FASTA formatted file'''
    fasta_list=[]
    for line in file_fasta:
        if line[0] == '>':
            try:
                fasta_list.append(current_dna)
        	#pass if an error comes up
            except UnboundLocalError:
                pass
            current_dna = [line.lstrip('>').rstrip('\n'),'']
        else:
            current_dna[1] += line.rstrip('\n')
    fasta_list.append(current_dna)
    return fasta_list

def seq_type(file_fasta):
    file_parsed = read_fasta(file_fasta)
    seq_dict = {}
    for x in file_parsed:
        name = x[0]
        setX = set(str(x[1]))
        lenx = len(x[1])
        letters = dict(collections.Counter(x[1]))
        letters.update((y, round((z/lenx),4)) for y, z in letters.items())
        if len(setX) > 4:
            print str(name) + " contains a protein sequence with the following AA frequencies: " + str(letters)
        elif len(setX) <= 4 and 'U' in setX:
            print str(name) + " contains RNA with the following nucleotide frequencies: " + str(letters)
        elif len(setX) <= 4 and 'T' in setX:
            print str(name) + " contains DNA with the following nucleotide frequencies: " + str(letters)
        else:
            print ("You either have a character that is not a nucleotide in "
            "your DNA or RNA, or a peptide chain with very little diversity")

# This function will take a dictionary
def roll(massDist):
    randRoll = random.random() # in [0,1)
    sum = 0
    result = 1
    for mass in massDist:
        sum += mass
        if randRoll < sum:
            return result
        result+=1
sample_mass_dist = (0.2, 0.4, 0.3, 0.1)

def choose_by_weight(weights):
    weights = map(float, weights)
    rndm = random.random() * sum(weights)
    for i, j in enumerate(weights):
        rndm -= j
        if rndm < 0:
            return i

def blocks(s, n):
    """Produce n-character chunks from s."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

def rndmGenome(file_fasta):
    fileParsed = read_fasta(file_fasta)
    gen_ref = ''
    for x in fileParsed:
        gen_ref += x[1]
    setX = set(str(gen_ref))
    lenX = len(gen_ref)
    letters = dict(collections.Counter(gen_ref))
    letters.update((y, round((z/lenX),4)) for y, z in letters.items())
    letters = collections.OrderedDict(sorted(letters.items()))
    nuc_freqs = [x[1] for x in letters.items()]
    gen_rndm = ''
    for i in range(0,lenX):
        j = choose_by_weight(nuc_freqs)
        if j == 0:
            gen_rndm += 'A'
        elif j == 1:
            gen_rndm += 'C'
        elif j == 2:
            gen_rndm += 'G'
        elif j == 3:
            gen_rndm += 'T'
        else:
            print "You have a non-nucleotide character in the genome."

    setY = set(str(gen_rndm))
    lenY = len(gen_rndm)
    letters_rndm = dict(collections.Counter(gen_rndm))
    letters_rndm.update((y, round((z/lenY),4)) for y, z in letters_rndm.items())
    letters_rndm = collections.OrderedDict(sorted(letters_rndm.items()))
    file_name = str(argv[1]).split('.')
    #OUT = open(mydir + file_name[0] +'_random.' + file_name[1],'w+')
    OUT = open("./" + file_name[0] +'_random.' + file_name[1],'w+')
    fasta_header = ">" + file_name[0] +'_random'
    print>> OUT, fasta_header
    for block in blocks(gen_rndm, 80):
        print>> OUT, block
    print "Your biological genome has relative nucleotide frequencies of:"
    print letters.items()
    print "Your random genome has relative nucleotide frequencies of:"
    print letters_rndm.items()


rndmGenome(argv[1])
