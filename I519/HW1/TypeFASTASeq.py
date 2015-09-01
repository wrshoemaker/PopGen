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
    if len(fasta_list) > 1:
        return fasta_list
    else:
        fasta_list_flat = [item for sublist in fasta_list for item in sublist]
        return fasta_list_flat

def seqType(fileFASTA):
    #setDNA = set('ACGT')
    #setRNA = set('ACGU')
    #setPep = set('ARNDCEQGHILKMFPSTWYV')
    fileParsed = readFASTA(fileFASTA)
    justSeqs = fileParsed[1::2]
    seq_dict = {}
    for x in justSeqs:
        setX = set(str(x))
        lenx = len(x)
        letters = dict(collections.Counter(x))
        letters.update((x, round((y/lenx),4)) for x, y in letters.items())
        if len(setX) > 4:
            print "Protein: " + str(letters)
        elif len(setX) == 4 and 'U' in setX:
            print "RNA: " + str(letters)
        elif len(setX) == 4 and 'T' in setX:
            print "DNA: " + str(letters)
        else:
            print ("You either have a character that is not a nucleotide in "
            "your DNA or RNA, or a very peptide chain with little diversity")



list_FASTA = seqType(argv[1])
