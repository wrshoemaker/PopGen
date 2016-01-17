#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math
import random
import os
import argparse

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

def rndmGenome(file_fasta, iterations, gnm_output, output_freqs = False):
    fileParsed = readFASTA(file_fasta)
    gen_ref = fileParsed[0][1]
    gen_name = fileParsed[0][0]
    setX = set(str(gen_ref))
    lenX = len(gen_ref)
    letters = dict(collections.Counter(gen_ref))
    letters.update((y, round((z/lenX),4)) for y, z in letters.items())
    letters = collections.OrderedDict(sorted(letters.items()))
    nuc_freqs = [x[1] for x in letters.items()]
    file_name = str(argv[1]).split('.')
    #OUT1 = open("./" + file_name[0] +'_output.' + file_name[1],'w+')
    OUT1 = open(gnm_output, 'w+')
    if output_freqs == True:
        OUT2 = open("./freq_rndm_output.txt",'w+')
        print>> OUT2, 0 ,nuc_freqs
    for i in range(int(iterations)):
        gen_rndm = ''
        for j in range(0,lenX):
            k = choose_by_weight(nuc_freqs)
            if k == 0:
                gen_rndm += 'A'
            elif k == 1:
                gen_rndm += 'C'
            elif k == 2:
                gen_rndm += 'G'
            elif k == 3:
                gen_rndm += 'T'
            else:
                print "You have a non-nucleotide character in the genome."

        setY = set(str(gen_rndm))
        lenY = len(gen_rndm)
        letters_rndm = dict(collections.Counter(gen_rndm))
        letters_rndm.update((y, round((z/lenY),4)) for y, z in letters_rndm.items())
        letters_rndm = collections.OrderedDict(sorted(letters_rndm.items()))
        #OUT = open(mydir + file_name[0] +'_random.' + file_name[1],'w+')
        fasta_header = ">" + gen_name +'_random_' + str(i)
        print>> OUT1, fasta_header
        for block in blocks(gen_rndm, 80):
            print>> OUT1, block
        if output_freqs == True:
            freqs_list = [x[1] for x in letters_rndm.items()]
            print>> OUT2, (i+1), freqs_list
    print "The biological genome has relative nucleotide frequencies of:"
    print letters.items()
    #print "Your random genome has relative nucleotide frequencies of:"
    #print letters_rndm.items()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Generate random genome")
    parser.add_argument('-i', type = str, default = "example_input.fa", \
        help = "FATA formatted input file")
    parser.add_argument('-n', type = int, default = 1, \
        help = "Read output number")
    parser.add_argument('-o', type = str, default = "example_output.fa", \
        help = "FATA formatted output file")
    parser.add_argument('-f', type = bool, default = False, \
        help = "Output nucleotide frequencies to a file")


    params = parser.parse_args()
    mydir = os.path.dirname(os.path.realpath(__file__))

    input_fasta = mydir + '/' + params.i
    nmbr_gnms = params.n
    freq_output = params.f
    gnm_output = params.o
    rndmGenome(input_fasta, nmbr_gnms, gnm_output, \
        output_freqs = freq_output)
