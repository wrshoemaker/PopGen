import os, argparse, random, math
from collections import Counter
from itertools import product
from itertools import izip_longest


mydir = os.path.dirname(os.path.realpath(__file__))
mydir = str(mydir[:-6]) + 'data/'

print mydir
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

    #def translateDnaAllFrames(self, dna):
    #    '''Translates dna sequence in 3 forward frames. \
    #        Translates from the opposite end if reverseTL == True \
    #        Returns a list of of length 6 containing the translated dna. \
    #        The first 3 items are the translated DNA sequences from frames \
    #        1, 2, and 3, respectively. Items 4, 5, and 6 contain the reverse \
    #        compliment translations for frames 1, 2, and 3, respectively'''
    #    all_translations = []
    #
    #    for frame in range(1,4):
    #        all_translations.append(self.translateDnaFrame(dna))
    #    if self.reverseTL:
    #        dnaRC = self.revcomp(dna)
    #        for frame in range(1,4):
    #            all_translations.append(self.translateDnaFrame(dnaRC))
    #    return all_translations
    #
    def codonFrequency(self):
        dnaCodons = self.translateDnaFrame()
        codonCount = Counter(dnaCodons)
        codonTotal = sum(codonCount.values(), 0.0)
        for key in codonCount:
            codonCount[key] /= codonTotal
        return codonCount


## converted into codon usage table format
## converted into codon usage table format
## converted into codon usage table format
def CodonTableFormat(codon_usages, **kw):
    codon_num = 0
    out = ''
    nucleotides = ['A','T','C','G']
    key = [''.join(i) for i in product(nucleotides, repeat = 3)]
    for i in range(len(key)):
        if key[i] not in codon_usages.keys():
            codon_usages[key[i]] = 0.0
    for codon in sorted(codon_usages):
        freq = "%.2f" % (round(codon_usages[codon]*100,2)) + "%"
        if codon_num == 0:
            out += codon+": "+freq
        elif codon_num % 4 != 0:
            out += "\t"+codon+": "+freq
        else:
            out += "\n"+codon+": "+freq
        codon_num += 1
    return out


def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

fasta = mydir + 'coding/coding_train.fa'

class_test = classFASTA(fasta)
######### This command returns the nested list containing sequence names
######### and sequences to a flat list containing only sequences
#print class_test.readFASTA()
sequences = [ [x[1]] for x in class_test.readFASTA() ]
min_len =  len(min(sequences, key=len)[0])
#sequences_cut = [ [x[0][:min_len]] for x in sequences]


sequences_test = [ split(x[0], 3) for x in sequences ]
#print sequences_test
for x in sequences_test:
    for y in x:
        if len(y) != 3:
            x.remove(y)

sequences_test = list(map(list, izip_longest(*sequences_test)))
codonCount_test = [Counter(x) for x in sequences_test]

codon_list = ["TTT", "TTC", "TTA", "TTG",
    "TCT", "TCC", "TCA", "TCG",
    "TAT", "TAC", "TAA", "TAG",
    "TGT", "TGC", "TGA", "TGG",
    "CTT", "CTC", "CTA", "CTG",
    "CCT", "CCC", "CCA", "CCG",
    "CAT", "CAC", "CAA", "CAG",
    "CGT", "CGC", "CGA", "CGG",
    "ATT", "ATC", "ATA", "ATG",
    "ACT", "ACC", "ACA", "ACG",
    "AAT", "AAC", "AAA", "AAG",
    "AGT", "AGC", "AGA", "AGG",
    "GTT", "GTC", "GTA", "GTG",
    "GCT", "GCC", "GCA", "GCG",
    "GAT", "GAC", "GAA", "GAG",
    "GGT", "GGC", "GGA", "GGG"]

### Not sure what to do here.
# We got the codons counted. Do we chop off sequence lengths?
####


for x in codonCount_test:
    list_x = list(x.items())
    print type(x)
    #if len(x) == 2:
        #print "what"
    if None in x:
        print "nonnneee"
        codonCount_test.remove(x)
    #for y in list_x:
    #    if y[0] == None:
    #        print "what", len(list_x)
    #    if (len(list_x) == 2) and y[0] == None:
    #        print x
    #        codonCount_test.remove(x)
#print codonCount_test
#print codonCount_test
    #print list_x
#    if (len(list_x) == 2) and (None in list_x):
#        pass
#    else:
#        print list_x
    #for y in list_x:
    #    if (y[0] == None) and len(list_x) == 2:
    #        codonCount_test.remove(x)

#print codonCount_test



# tranform the codon usage dictionary to an optional output table
codon_usages = dnaTranslation(mydir,concatenated_seq, args.reading_frame, reverseTL = args.feature).codonFrequency()
codon_table = CodonTableFormat(codon_usages)

# simulate a randomized sequence based on known nucleotide frequency
myseq = dnaTranslation(mydir,concatenated_seq, args.reading_frame, reverseTL = args.feature).dna
random_seq = SeqSimulator(myseq)
random_usages = dnaTranslation(mydir,random_seq, args.reading_frame, reverseTL = args.feature).codonFrequency()
random_table = CodonTableFormat(random_usages)
