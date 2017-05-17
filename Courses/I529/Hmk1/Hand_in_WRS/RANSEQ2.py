#!/usr/bin/env python
from __future__ import division
from sys import argv, exit
import random
import os
from pprint import pprint
import math
from random import shuffle
import argparse
import collections

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
            	"Not in a FASTA format!"
                pass
            current_dna = [line.lstrip('>').rstrip('\n'),'']
        else:
            current_dna[1] += "".join(line.split())
    fasta_list.append(current_dna)
    return fasta_list

def blocks(s, n):
    """Produce n-character chunks from s."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

def permute_sequence(input_fasta, output_fasta, nmbr_gnms, freq_output = False):
    fileParsed = readFASTA(input_fasta)
    gen_ref = fileParsed[0][1].upper()
    gen_name = fileParsed[0][0]
    setX = set(str(gen_ref))
    lenX = len(gen_ref)
    letters = dict(collections.Counter(gen_ref))
    letters.update((y, round((z/lenX),4)) for y, z in letters.items())
    letters = collections.OrderedDict(sorted(letters.items()))
    nuc_freqs = [x[1] for x in letters.items()]
    print letters.items()
    #file_name = str(argv[1]).split('.')
    OUT1 = open(output_fasta, 'w+')
    l = list(gen_ref)
    if freq_output == True:
        OUT2 = open("./freq_perm_output.txt",'w+')
        print>> OUT2, 0 ,nuc_freqs[0],nuc_freqs[1],nuc_freqs[2],nuc_freqs[3]
    for i in range(int(nmbr_gnms)):
        random.shuffle(l)
        gen_perm = ''.join(l)
        setY = set(str(gen_perm))
        lenY = len(gen_perm)
        letters_perm = dict(collections.Counter(gen_perm))
        letters_perm.update((y, round((z/lenY),4)) for y, z in letters_perm.items())
        letters_perm = collections.OrderedDict(sorted(letters_perm.items()))
        fasta_header = ">" + gen_name +'_random_' + str(i)
        print>> OUT1, fasta_header
        for block in blocks(gen_perm, 80):
            print>> OUT1, block
        if freq_output == True:
            freqs_list = [x[1] for x in letters_perm.items()]
            print>> OUT2, (i+1), freqs_list[0], freqs_list[1], freqs_list[2], freqs_list[3]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Generate random genome")
    parser.add_argument('-i', type = str, default = "example_input.fa", \
        help = "FATA formatted input file")
    parser.add_argument('-N', type = int, default = 1, \
        help = "Read output number")
    parser.add_argument('-o', type = str, default = "example_output.fa", \
        help = "FATA formatted output file")
    parser.add_argument('-f', type = bool, default = False, \
        help = "Output nucleotide frequencies to a file")

    params = parser.parse_args()
    mydir = os.path.dirname(os.path.realpath(__file__))

    input_fasta = mydir + '/' + params.i
    nmbr_gnms = params.N
    freq_output = params.f
    output_fasta = params.o
    permute_sequence(input_fasta, output_fasta,nmbr_gnms, freq_output = freq_output)
