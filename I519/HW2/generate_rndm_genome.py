#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math
import random

def readFASTA(fileFASTA):
    '''Checks for fasta by file extension'''
    file_lower = fileFASTA.lower()
    '''Check for three most common fasta file extensions'''
    if file_lower.endswith('.txt') or file_lower.endswith('.fa') or file_lower.endswith('.fasta') or file_lower.endswith('.fna'):
        with open(fileFASTA, "r") as f:
            return ParseFASTA(f)
    else:
        print 'File does not end with .txt, .fasta, .fa, or .fna'
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
            current_dna[1] += line.rstrip('\n')
    fasta_list.append(current_dna)
    return fasta_list
def seqType(fileFASTA):
    fileParsed = readFASTA(fileFASTA)
    seq_dict = {}
    for x in fileParsed:
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
            "your DNA or RNA, or a very peptide chain with little diversity")

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
sampleMassDist = (0.2, 0.4, 0.3, 0.1)

print roll(sampleMassDist)

def rndmGenome(fileFASTA):
    fileParsed = readFASTA(fileFASTA)
    for x in fileParsed:
        name = x[0]
        setX = set(str(x[1]))
        lenx = len(x[1])
        letters = dict(collections.Counter(x[1]))
        letters.update((y, round((z/lenx),4)) for y, z in letters.items())
        letters = collections.OrderedDict(sorted(letters.items()))
        print letters
        print letters['A']
        #''.join(random.choice('acgt') for x in range(10))

    #print fileParsed[0]
    #if len(fileParsed) > 1:
    #    print "More than one sequence in FASTA file"
    #else:
    #    seq = fileParsed[0]
        #name = x[0]
        #setX = set(str(x[1]))
        #lenx = len(x[1])
        #letters = dict(collections.Counter(x[1]))
        #letters.update((y, round((z/lenx),4)) for y, z in letters.items())


list_FASTA = rndmGenome(argv[1])
#list_FASTA = seqType(argv[1])
