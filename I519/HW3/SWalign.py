#!/usr/bin/env python
from __future__ import division
from sys import argv
import os

"""To do: fix the output so that it formats nicely"""


# Read the BLOSUM50 table
def read_BLOSUM50(fname):
    d = {}
    lines = open(fname, "rt").readlines()
    alpha = lines[0].rstrip('\n\r').split()
    assert(len(alpha) == len(lines)-1)
    for r in lines[1:]:
        r = r.rstrip('\n\r').split()
        a1 = r[0]
        for a2, score in zip(alpha, r[1:]):
            d[(a1, a2)] = int(score)
    return d


scriptdir = os.path.dirname(os.path.abspath(__file__))
B62_text = scriptdir + '/BLOSUM62.txt'
B62 = read_BLOSUM50(B62_text)

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

sigma = 11
epsilon = 1

def SW_affine_gap(r1, r2):
    d_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    i_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    s_mat = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    traceback = [[0 for j in xrange(len(r2)+1)] for i in xrange(len(r1)+1)]
    max_score = -1
    max_i, max_j = 0, 0
    for i in xrange(1, len(r1)+1):
        for j in xrange(1, len(r2)+1):
            print B62[r1[i-1], r2[j-1]]
            d_mat[i][j] = max([d_mat[i-1][j] - epsilon, s_mat[i-1][j] - sigma])
            i_mat[i][j] = max([i_mat[i][j-1] - epsilon, s_mat[i][j-1] - sigma])
            s_mat_scores = [d_mat[i][j], s_mat[i-1][j-1] + B62[r1[i-1], r2[j-1]], i_mat[i][j], 0]
            s_mat[i][j] = max(s_mat_scores)
            traceback[i][j] = s_mat_scores.index(s_mat[i][j])

            if s_mat[i][j] > max_score:
                max_score = s_mat[i][j]
                max_i, max_j = i, j
    #print S_lower
    #print S_middle
    #print S_upper
    #print backtrack
    # Initialize the indices to start at the position of the high score.
    i, j = max_i, max_j

    # Initialize the aligned strings as the input strings up to the position of the high score.
    r1_aligned, r2_aligned = r1[:i], r2[:j]

    # Backtrack to start of the local alignment starting at the highest scoring cell.
    # Note: the solution format specifically asks for substrings, so no indel insertion necessary.
    while traceback[i][j] != 3 and i*j != 0:
        if traceback[i][j] == 0:
            i -= 1
        elif traceback[i][j] == 1:
            i -= 1
            j -= 1
        elif traceback[i][j] == 2:
            j -= 1

    # Cut the strings at the ending point of the backtrack.
    print r1_aligned
    print r2_aligned
    #r1_aligned = r1_aligned[i:]
    #r2_aligned = r2_aligned[j:]

    return str(max_score), r1_aligned, r2_aligned


alignment = SW_affine_gap("AAGGB", "AAGGDFBA")
print '\n'.join(alignment)

#if __name__ == '__main__':
    #r1, r2 = [fasta[1] for fasta in readFASTA(argv[1])]
    #alignment = SW_affine_gap(r1, r2)
