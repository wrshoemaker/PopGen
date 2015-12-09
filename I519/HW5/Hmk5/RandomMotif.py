from __future__ import division
import random
import collections
from operator import itemgetter
import itertools
import operator
import argparse
import os

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


def randomSubstring(string, k):
    sliced = len(string) - k + 1
    start = random.randrange(0, sliced, 1)
    return string[start: (k+start)]

def multipleKmers(list_seqs, k):
    list_kmers = []
    for x in list_seqs:
        substring = randomSubstring(x, k)
        list_kmers.append(substring)
    return list_kmers

def profileMatrix(list_seqs, k):
    ''' Takes a nested list of sequences, generates a random k-mer for each
    sequence, and turns those k-mers into a profile matrox returned as a list
    of dictionaries using Python's counter function.
    '''
    N = len(list_seqs)
    list_kmers = multipleKmers(list_seqs, k)
    zipped_list_kmers = zip(*list_kmers)
    for i in xrange(len(zipped_list_kmers)):
        zipped_list_kmers[i] = collections.Counter(zipped_list_kmers[i])
        for key, value in zipped_list_kmers[i].items():
            zipped_list_kmers[i][key] = value / N
    return zipped_list_kmers

def hamming1(str1, str2):
  return sum(itertools.imap(str.__ne__, str1, str2))

def kmerProb(list_seqs, k):
    length = len(list_seqs[0])
    profile = profileMatrix(list_seqs, k)
    #test = list_seqs[0]
    #print test
    max_score_list = []
    for seq in list_seqs:
        max_score = ('blank', 0)
        for y in range(0, (length - k +1)):
            seq_k =  seq[0 + y : y + k]
            #print test_k
            #print profile_test
            score = 1
            for i in range(k):
                profile_i = profile[i]
                seq_k_i = seq_k[i]
                #print test_k_i, profile_test_i
                score *= profile_i[seq_k_i]
            if score >= max_score[1]:
                max_score = (seq_k, score)
        max_score_list.append(max_score)
    return max_score_list

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def findConsensus(list_kmers):
    list_kmers = zip(*list_kmers)
    consensus = ''
    for x in list_kmers:
        consensus += str(most_common(x))
    return consensus


def motifScore(list_seqs, k):
    max_score_list = kmerProb(list_seqs, k)
    kmers = [item[0] for item in max_score_list]
    consensus = findConsensus(kmers)
    score = 0
    for x in kmers:
        score += hamming1(x, consensus)
    return score, max_score_list

def iterate(list_seqs, k, loops):
    loop_zero = motifScore(list_seqs, k)
    BestScore = loop_zero[0]
    BestMotif = loop_zero[1]
    for x in range(0, loops):
        loop_result = motifScore(list_seqs, k)
        if loop_result[0] <= BestScore:
            BestScore = loop_result[0]
            BestMotif = loop_result[1]
    print "The best score is " + str(BestScore)
    return BestMotif



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Run randomized motif approach")
    parser.add_argument('-i', type = str, default = "Dna.fasta", help = "FATA formatted input file")
    parser.add_argument('-k', type = int, default = 5, help = "k-mer length")

    params = parser.parse_args()

    mydir = os.path.dirname(os.path.realpath(__file__))

    input_fasta = mydir + '/' + params.i
    kmer_length = params.k

    r1 = [fasta[1] for fasta in readFASTA(input_fasta)]


    run_algorithm = iterate(r1, kmer_length, 10000)
    kmers_output = [item[0] for item in run_algorithm]
    print "Below are the k-mers"
    print kmers_output
