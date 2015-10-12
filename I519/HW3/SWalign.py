#!/usr/bin/env python
from __future__ import division
from sys import argv
import os
import optparse
import argparse
import math
#from datetime import datetime
#import time

# Read the BLOSUM table
def read_BLOSUM(fname):
    d = {}
    lines = open(fname, "rt").readlines()
    content = [x for x in lines if not x.startswith('#')]
    alpha = content[0].rstrip('\n\r').split()
    assert(len(alpha) == len(content)-1)
    for r in content[1:]:
        r = r.rstrip('\n\r').split()
        a1 = r[0]
        for a2, score in zip(alpha, r[1:]):
            d[(a1, a2)] = int(score)
    return d

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

#sigma = 1
#epsilon = 11

def SW_affine_gap(r1, r2, output_format, output_name, sigma, epsilon, B62):
    d_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    i_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    s_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    traceback = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    max_score = -1
    max_i, max_j = 0, 0
    for i in xrange(1, len(r1)+1):
        for j in xrange(1, len(r2)+1):
            #d_mat[i][j] = max([d_mat[i-1][j] - epsilon, s_mat[i-1][j] - sigma])
            #i_mat[i][j] = max([i_mat[i][j-1] - epsilon, s_mat[i][j-1] - sigma])
            d_mat[i][j] = max([d_mat[i-1][j] - sigma, s_mat[i-1][j] - (sigma + epsilon)])
            i_mat[i][j] = max([i_mat[i][j-1] - sigma, s_mat[i][j-1] - (sigma + epsilon)])
            s_mat_scores = [d_mat[i][j], s_mat[i-1][j-1] + B62[r1[i-1], r2[j-1]], i_mat[i][j], 0]
            s_mat[i][j] = max(s_mat_scores)
            traceback[i][j] = s_mat_scores.index(s_mat[i][j])
            if s_mat[i][j] > max_score:
                max_score = s_mat[i][j]
                max_i, max_j = i, j
    # Start at the high score
    i, j = max_i, max_j
    # Slice the AA sequences starting where the max score is
    r1_aligned, r2_aligned = r1[:i], r2[:j]
    # Need to include insertion
    align_symbl = []
    r1_with_indels = []
    r2_with_indels = []

    while traceback[i][j] != 3 and i*j != 0:
        if traceback[i][j] == 0:
            r1_with_indels.insert(0,r1_aligned[i-1])
            r2_with_indels.insert(0,'-')
            align_symbl.insert(0,' ')
            i -= 1
        elif traceback[i][j] == 1:
            r1_with_indels.insert(0,r1_aligned[i-1])
            r2_with_indels.insert(0,r2_aligned[j-1])
            if str(r1_aligned[i-1]) == str(r2_aligned[j-1]):
                align_symbl.insert(0,'|')
            else:
                align_symbl.insert(0,'.')
            i -= 1
            j -= 1
        elif traceback[i][j] == 2:
            r2_with_indels.insert(0,r2_aligned[j-1])
            r1_with_indels.insert(0,'-')
            align_symbl.insert(0,' ')
            j -= 1

    r1_aligned = r1_aligned[i:]
    r2_aligned = r2_aligned[j:]

    r1_with_indels_str = ''.join(r1_with_indels)
    align_symbl_str = ''.join(align_symbl)
    r2_with_indels_str = ''.join(r2_with_indels)
    OUT = open(str(mydir) + "/" + output_name,'w+')


    # Calculate alignment score
    alignment_length = int(max(len(r1_with_indels), len(r2_with_indels)))
    match_count = int(align_symbl.count('|'))
    identity_score = (match_count/alignment_length) * 100
    align_len_print = "Input seqs: seq1 (len=%s); seq2 (len=%s)" % \
                    (str(len(r1)), str(len(r2)))
    align_score_print = "Alignment length=" + str(alignment_length) + \
                "; identity=" + str(round(identity_score, 2)) + "%"
    print "Your best alignment score is " + str(max_score)
    print align_len_print
    print align_score_print
    print r1_with_indels_str
    print align_symbl_str
    print r2_with_indels_str
    if output_format == 'FASTA':
        seq1_name = '>seq1'
        seq2_name = '>seq2'
        print>> OUT, seq1_name
        print>> OUT, r1_with_indels_str
        print>> OUT, seq2_name
        print>> OUT, r2_with_indels_str
    else:
        print>> OUT, align_len_print
        print>> OUT, align_score_print
        print>> OUT, r1_with_indels_str
        print>> OUT, align_symbl_str
        print>> OUT, r2_with_indels_str
    return str(max_score), r1_aligned, r2_aligned


#alignment = SW_affine_gap("GGBBAABB", "GABBAGB")

if __name__ == '__main__':
    #startTime = datetime.now()
    #start_time = time.time()
    parser = argparse.ArgumentParser(description = "Run Smith-Waterman AA alignment")
    parser.add_argument('-i', type = str, default = "twoseq.fasta", help = "FATA formatted input file")
    parser.add_argument('-f', type = str, default = "FASTA", help = "FASTA or PLAIN")
    parser.add_argument('-o', type = str, default = "twoseq-aligned.fasta", help = "Alignment output")
    parser.add_argument('-s', type = int, default = 11, help = "sigma, gap start penalty")
    parser.add_argument('-e', type = int, default = 1, help = "epsilon, gap extension penalty")
    parser.add_argument('-m', type = str, default = "BLOSUM62.txt", help = "File path for BLOSUM matrix")

    params = parser.parse_args()

    input_fasta = params.i
    output_format = params.f.upper()
    output_name = params.o
    sigma = math.fabs(params.s)
    epsilon = math.fabs(params.e)
    blosum = params.m

    mydir = os.path.dirname(os.path.realpath(__file__))
    B62_text = mydir + '/' + blosum
    B62 = read_BLOSUM(B62_text)

    r1, r2 = [fasta[1] for fasta in readFASTA(input_fasta)]
    #r1 = "GAATTCAGTTA"
    #r2 = "GGATCGA"
    alignment = SW_affine_gap(r1, r2, output_format, output_name, sigma, epsilon, B62)
    #print datetime.now() - startTime
    #print("--- %s seconds ---" % (time.time() - start_time))
