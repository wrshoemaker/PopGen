#!/usr/bin/env python
from __future__ import division
from sys import argv
from itertools import groupby
import collections
import math
from distutils.util import strtobool
import argparse


#AAtable = {
#      'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
#      'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
#      'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
#      'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
#      'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
#      'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
#      'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
#      'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
#      'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
#      'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
#      'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
#      'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
#      'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
#      'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
#      'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
#      'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'}

def read_fasta(file_fasta):
    '''Checks for fasta by file extension'''
    file_lower = file_fasta.lower()
    '''Check for three most common fasta file extensions'''
    if file_lower.endswith('.txt') or file_lower.endswith('.fa') or file_lower.endswith('.fasta'):
        with open(file_fasta, "r") as f:
            return parse_fasta(f)

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

def revcomp(seq):
    bases = 'ATGCTACG'
    comp_dict = {bases[i]:bases[i+4] for i in range(4)}
    seq = reversed(seq)
    list_rev_comp = [comp_dict[base] for base in seq]
    return ''.join(list_rev_comp)

def translate_seq(seq):
    seq_rc = revcomp(seq)
    pass

def import_aa_table(codon_table):
    table = {}
    #data = [[item.strip() for item in line.rstrip('\r\n').split('= ', 1)[-1]] \
    #    for line in open(argv[2])]
    #aa_list = [[item.strip() for item in line.rstrip('\r\n').split('= ', 1)[-1]] \
    #    for line in open(argv[2])]
    aa_list = [[item.strip() for item in line.rstrip('\r\n').split('= ', 1)[-1]] \
        for line in open(codon_table)]
    aa_list_zip = map(list, zip(*aa_list))
    for x in aa_list_zip:
         x[2:5] = [''.join(x[2:5])]
         table[str(x[2])] = str(x[0])
    #return aa_list_zip
    return table


def translate_codon(codon):
    AAtable = import_aa_table(argv[2])
    return AAtable.get(codon.upper(), 'x')

def split_seq_to_codons(dna, frame):
    codons = []
    for i in range(frame - 1, len(dna)-2, 3):
        codon = dna[i:i+3]
        codons.append(codon)
    return codons


# a function to translate a dna sequence in a single frame
def translate_dna_frame(dna, frame=1):
    codons = split_seq_to_codons(dna, frame)
    amino_acids = ''
    for codon in codons:
        amino_acids = amino_acids + translate_codon(codon)
    return amino_acids

# a function to translate a dna sequence in 3 forward frames
def translate_dna(dna, reverseTL = False):
    all_translations = []
    for frame in range(1,4):
        all_translations.append(translate_dna_frame(dna, frame))
    if reverseTL:
        dnaRC = revcomp(dna)
        for frame in range(1,4):
            all_translations.append(translate_dna_frame(dnaRC, frame))
    return all_translations


def format_translation(dna):
    dna = read_fasta(dna)
    for x in dna:
        single_seq = translate_dna(x[1], reverseTL=True)
        print ">" + x[0]
        print "DNA: " + x[1]
        print ' +3:   ' + "  ".join(single_seq[2])
        print ' +2:  ' + "  ".join(single_seq[1])
        print ' +1: ' + "  ".join(single_seq[0])
        print "   : " +revcomp(x[1])
        print ' -1: ' + "  ".join(single_seq[3])
        print ' -2:  ' + "  ".join(single_seq[4])
        print ' -3:   ' + "  ".join(single_seq[5])

if __name__=="__main__":
        import_aa_table(argv[2])
        format_translation(argv[1])
        #parser = argparse.ArgumentParser(description = "six-frame DNA translator")
        #parser.add_argument('--dna_fasta', type = str, default = argv[1], help = "FASTA formatted DNA file")
        #parser.add_argument('--codon_table', type = str, default = argv[2], help = "Codon table")
        #params = parser.parse_args()

        #dna_fasta = params.dna_fasta
        #codon_table = params.codon_table

        #import_aa_table(codon_table)
        #format_translation(dna_fasta)

#format_translation(argv[1])
