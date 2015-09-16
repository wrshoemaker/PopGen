#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math
from distutils.util import strtobool

AAtable = {
      'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
      'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
      'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
      'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
      'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
      'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
      'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
      'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
      'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
      'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
      'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
      'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
      'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
      'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
      'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
      'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'}

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
            current_dna[1] += line.rstrip('\n')
    fasta_list.append(current_dna)
    return fasta_list

def revcomp(seq):
    bases = 'ATGCTACG'
    compDict = {bases[i]:bases[i+4] for i in range(4)}
    seq = reversed(seq)
    listRevComp = [compDict[base] for base in seq]
    return ''.join(listRevComp)

my_dna = 'CTCGCCATTAACCGTTTCAGCCCCAGGTGCCTTTCTTGAGGC'

def translateSeq(seq):
    seqRC = revcomp(seq)
    pass

s_protein = ''
all_tl = []
#for i in range(1,4):
    #all_tl.append(translate_dna_single(dna, frame))
#    for j in range(i,len(my_dna)+i,3):
#        if AAtable[my_dna[j:j+3]] != '*':
#            s_protein += AAtable[my_dna[j:j+3]]
#print s_protein
def translate_codon(codon):
    return AAtable.get(codon.upper(), 'x')

def split_into_codons(dna, frame):
    codons = []
    for i in range(frame - 1, len(dna)-2, 3):
        codon = dna[i:i+3]
        codons.append(codon)
    return codons


# a function to translate a dna sequence in a single frame
def translate_dna_single(dna, frame=1):
    codons = split_into_codons(dna, frame)
    amino_acids = ''
    for codon in codons:
        amino_acids = amino_acids + translate_codon(codon)
    return amino_acids

# a function to translate a dna sequence in 3 forward frames
def translate_dna(dna, reverseTL = False):
    all_translations = []
    for frame in range(1,4):
        all_translations.append(translate_dna_single(dna, frame))
    if reverseTL:
        dnaRC = revcomp(dna)
        for frame in range(1,4):
            all_translations.append(translate_dna_single(dnaRC, frame))
    return all_translations

# to do, change variable names, format translation



def format_translation(dna):
    what = translate_dna(my_dna, reverseTL=True)
    print what[0]
    print dna
    print revcomp(dna)


print format_translation(my_dna)
