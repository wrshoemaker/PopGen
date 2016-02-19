from __future__ import division
import os, argparse, random, math
from collections import Counter
from itertools import product
import scipy
from scipy.stats import chisquare

mydir = os.path.dirname(os.path.realpath(__file__))
mydir = str(mydir[:-6]) + 'data/'

class classFASTA:

    def __init__(self, fileFASTA):
        self.fileFASTA = fileFASTA

    def readFASTA(self):
        '''Checks for fasta by file extension'''
        file_lower = self.fileFASTA.lower()
        '''Check for three most common fasta file extensions'''
        if file_lower.endswith('.txt') or file_lower.endswith('.fa') or \
        file_lower.endswith('.fasta') or file_lower.endswith('.fna'):
            with open(self.fileFASTA, "r") as f:
                return self.ParseFASTA(f)
        else:
            print "Not in FASTA format."

    def ParseFASTA(self, fileFASTA):
        '''Gets the sequence name and sequence from a FASTA formatted file'''
        fasta_list=[]
        for line in fileFASTA:
            if line[0] == '>':
                try:
                    fasta_list.append(current_dna)
            	#pass if an error comes up
                except UnboundLocalError:
                    #print "Inproper file format."
                    pass
                current_dna = [line.lstrip('>').rstrip('\n'),'']
            else:
                current_dna[1] += "".join(line.split())
        fasta_list.append(current_dna)
        '''Returns fasa as nested list, containing line identifier \
            and sequence'''
        return fasta_list

class dnaTranslation:

    '''This class takes the fasta in as a nested list object. \
        This object is created using the above class classFASTA. \
        Codon tables are imported and are in the location  \
        ../data/codon.txt \
        AA sequence is returned as a string.'''

    def __init__(self, myDir, dna, frame, reverseTL = False):
        self.myDir = myDir + 'codon.txt'
        self.frame = frame
        self.reverseTL = reverseTL
        self.dna = dna

    def importAAtable(self):
        table = {}
        aa_list = [[item.strip() for item in line.rstrip('\r\n').split('= ', 1)[-1]] \
            for line in open(self.myDir)]
        aa_list_zip = map(list, zip(*aa_list))
        for x in aa_list_zip:
             x[2:5] = [''.join(x[2:5])]
             table[str(x[2])] = str(x[0])
        return table

    def translateCodon(self, codon):
        AAtable = self.importAAtable()
        return AAtable.get(codon.upper(), 'x')

    def splitSeqToCodons(self):
        codons = []
        for i in range(self.frame - 1, len(self.dna)-2, 3):
            codon = self.dna[i:i+3]
            codons.append(codon)
        return codons

    def revcomp(self):
        bases = 'ATGCTACG'
        comp_dict = {bases[i]:bases[i+4] for i in range(4)}
        seq = reversed(self.dna)
        list_rev_comp = [comp_dict[base] for base in seq]
        return ''.join(list_rev_comp)

    def translateDnaFrame(self):

        ''''Translates a dna sequence of a specified frame'''
        if self.reverseTL == True:
            self.dna = self.revcomp()
        codons = self.splitSeqToCodons()
        return codons
        #amino_acids = ''
        #for codon in codons:
        #    amino_acids = amino_acids + self.translateCodon(codon)
        #return amino_acids

    def codonFrequency(self):
        dnaCodons = self.translateDnaFrame()
        codonCount = Counter(dnaCodons)
        codonTotal = sum(codonCount.values(), 0.0)
        for key in codonCount:
            codonCount[key] /= codonTotal
        return codonCount


## converted into codon usage table format

## simulate randomized sequence
def SeqSimulator(myseq):
    randomized_seq = list(myseq)
    random.shuffle(randomized_seq)
    Simulated_sequence = ''.join(randomized_seq)
    return Simulated_sequence

def revcomp_quick_fix(dna):
    bases = 'ATGCTACG'
    comp_dict = {bases[i]:bases[i+4] for i in range(4)}
    seq = reversed(dna)
    list_rev_comp = [comp_dict[base] for base in seq]
    return ''.join(list_rev_comp)

def markov_random_table(seqs_list, **kw):
    '''
    This function takes a nested list of sequences and outputs a dictionary of
    expected codon-codon transition frequencues using only the nucleotide
    frequencies (i.e. our random expectation)
    '''
    concatenated_seq = ''.join(seqs_list)
    nucs_freq = Counter(concatenated_seq)
    nucleotides = ['A','T','C','G']
    codons = [''.join(i) for i in product(nucleotides, repeat = 3)]
    codon_trans = ['-'.join(i) for i in product(codons, repeat = 2)]
    freq_table = {}
    for key in codon_trans:
        freq_table[key] = 0
    for key, value in nucs_freq.items():
        nucs_freq[key] = value / len(concatenated_seq)
    # now calculate expected codon frequencies
    for x in codon_trans:
        x_list =  list(x)
        c1 = nucs_freq[x_list[0]] * nucs_freq[x_list[1]] * nucs_freq[x_list[2]]
        c2 = nucs_freq[x_list[4]] * nucs_freq[x_list[5]] * nucs_freq[x_list[6]]
        freq_table[x] = c1*c2
    return freq_table


def markov_freq_table(seqs_list, **kw):
    '''
    This function takes a nested list of sequences and outputs a markov table
    of codon-codon transition frequencies as a dictionary.
    '''
    nucleotides = ['A','T','C','G']
    codons = [''.join(i) for i in product(nucleotides, repeat = 3)]
    codon_trans = ['-'.join(i) for i in product(codons, repeat = 2)]
    seq_len = len(seqs_list)
    markov_table = {}
    valid = 'ACTG'
    for key in codon_trans:
        markov_table[key] = 1
    for seq in seqs_list:
        modulo = len(seq) % 3
        seq = seq[:-modulo]
        seq = seq.upper()
        split_dna = [seq[i:i+3] for i in range(0, len(seq), 3)]
        for x in range(0, len(split_dna)-1):
            if (all(y in valid for y in split_dna[x]) and all(y in valid for y in split_dna[x+1]) ) == True:
                data_trans = split_dna[x] + '-' + split_dna[x+1]
                markov_table[data_trans] += 1
    #sum(d.values())
    values_sum = sum(markov_table.values())
    for key, value in markov_table.items():
        markov_table[key] =  value / values_sum
    return markov_table


class class_chi_square:

    def __init__(self, observed_values, expected_values):
        self.observed_values = observed_values
        self.expected_values = expected_values

    def gf(self, x):
        #Play with these values to adjust the error of the approximation.
        upper_bound=100.0
        resolution=1000000.0

        step=upper_bound/resolution

        val=0
        rolling_sum=0

        while val<=upper_bound:
            rolling_sum+=step*(val**(x-1)*2.7182818284590452353602874713526624977**(-val))
            val+=step

        return rolling_sum

    def ilgf(self, s,z):
        val=0

        for k in range(0,100):
            val+=(((-1)**k)*z**(s+k))/(math.factorial(k)*(s+k))
        return val

    def chisquarecdf(self, x,k):
        return 1 - self.ilgf(k/2,x/2)/self.gf(k/2)

    def chisquare(self):
        test_statistic=0

        #for observed, expected in zip(self.observed_values, self.expected_values):
        #    test_statistic+=(float(observed)-float(expected))**2/float(expected)
        for observed, expected in zip(self.observed_values, self.expected_values):
            test_statistic+= (2 * (math.log(observed) - math.log(expected)  )  )

        df=len(self.observed_values)-1

        return test_statistic, self.chisquarecdf(test_statistic,df)

def log_likelihood_ratio(seq, alt_table, null_table):
    '''
    This function takes a nucleotide sequence as a string,
    splits it, and calculates te log-likelihood.
    '''
    valid = 'ACTG'
    modulo = len(seq) % 3
    if modulo > 0:
        seq = seq[:-modulo]
    seq = seq.upper()
    split_dna = [seq[i:i+3] for i in range(0, len(seq), 3)]
    sum_ll = 0
    for x in range(0, len(split_dna)-1):
        if (all(y in valid for y in split_dna[x]) and all(y in valid for y in split_dna[x+1]) ) == True:
            data_trans = split_dna[x] + '-' + split_dna[x+1]
            #print math.log(alt_table[data_trans]) - math.log(null_table[data_trans])
            ll = math.log(alt_table[data_trans] ) -    math.log(null_table[data_trans])
            #print ll
            #if ll ==0:
            #    print math.log(  alt_table[data_trans] ), math.log( null_table[data_trans] )
            sum_ll += ll
    return sum_ll



def log_likelihood_ratio_list(input_seqs, alt_table, null_table):
    ll_list = []
    for x in input_seqs:
        ll = log_likelihood_ratio(x, alt_table, null_table)
        ll_list.append(ll)
    return ll_list




#### ====== read input FASTA file and write output files ======
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--train_fasta_file', required=True)
    parser.add_argument('-j', '--test_fasta_file', required=True)
    parser.add_argument('-o', '--out_table', required=True)
    parser.add_argument('-c', '--codon_table')
    parser.add_argument('-r', '--random_codon_table')
    parser.add_argument('-t','--threshold_likelihood', default=3)
    parser.add_argument('-f','--reading_frame', type = int, default=1)
    parser.add_argument('-rc', '--reverse_compliment', dest='feature', action='store_true')
    parser.set_defaults(feature=False)
    args = parser.parse_args()
    fasta_train = mydir + args.train_fasta_file
    class_train = classFASTA(fasta_train)

    fasta_test = mydir + args.test_fasta_file
    class_test = classFASTA(fasta_test)

    ######### This command returns the nested list containing sequence names
    ######### and sequences to a flat list containing only sequences
    sequences_train = [ x[1] for x in class_train.readFASTA() ]
    sequences_train = [x.upper() for x in sequences_train]
    sequences_train = sequences_train[:1000]

    ######### concatenated the sequences
    concatenated_seq_train = ''.join(sequences_train)

    ####### get table from training data##############
    trans_freq_table = markov_freq_table(sequences_train)
    ###### get random table from training data######
    trans_random_rable = markov_random_table(sequences_train)


    ###### Input test data #########
    sequences_test = [ x[1] for x in class_test.readFASTA() ]
    sequences_names = [ x[0] for x in class_test.readFASTA() ]
    sequences_test = [x.upper() for x in sequences_test]
    sequences_test = sequences_test[:500]
    ######### concatenated the sequences


    #test =  'GGGGGGGGCCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    #print log_likelihood_ratio(test, trans_freq_table, trans_random_rable)
    likelihood_values = log_likelihood_ratio_list(sequences_test, trans_freq_table, trans_random_rable)
    zipped =  zip(sequences_names, likelihood_values)
    name = mydir + args.out_table
    OUT =  open(name, 'w+')

    for x,y in enumerate(zipped):
        orf_name = "ORF" + str(x)
        print>> OUT, orf_name, y[1]
