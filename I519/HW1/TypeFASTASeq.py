#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math


def readFASTA(fileFASTA):
    '''Checks for fasta by file extension'''
    file_lower = fileFASTA.lower()
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
            except UnboundLocalError:
                pass
            current_dna = [line.lstrip('>').rstrip('\n'),'']
        else:
            current_dna[1] += line.rstrip('\n')
    fasta_list.append(current_dna)
    return fasta_list

def seqType(fileFASTA):
    #setDNA = set('ACGT')
    #setRNA = set('ACGU')
    #setPep = set('ARNDCEQGHILKMFPSTWYV')
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
        elif len(setX) == 4 and 'U' in setX:
            print str(name) + " contains RNA with the following nucleotide frequencies: " + str(letters)
        elif len(setX) == 4 and 'T' in setX:
            print str(name) + " contains DNA with the following nucleotide frequencies: " + str(letters)
        else:
            print ("You either have a character that is not a nucleotide in "
            "your DNA or RNA, or a very peptide chain with little diversity")



list_FASTA = seqType(argv[1])
