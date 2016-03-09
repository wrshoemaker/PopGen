#!/usr/bin/env python
from __future__ import division
import itertools, collections, os, math, re, argparse, operator
from collections import defaultdict



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

def addPseudocounts(nestedDict):
    '''
    This function takes a list of states as an argument.
    It returns a nested dictionary with pseudo-counts
    '''
    AAs = 'ARNDCQEGHILKMFPSTWYV'
    AAsList = list(AAs)
    for x in nestedDict.keys():
        for y in AAsList:
            nestedDict[x][y] += 1
    return nestedDict

def isplit(iterable,splitters):
    return [list(g) for k,g in \
        itertools.groupby(iterable,lambda x:x in splitters) if not k]

class getParams:

    def __init__(self, inTrain):
        self.inTrain = inTrain

    def initialParams(self):
        initial_state_list = []
        for line in self.inTrain:
            # get the state transitions and emission freqs
            initial_state = line[0].split()
            initial_state_list.append(initial_state[1])
        lettersInit = dict(collections.Counter(initial_state_list))
        lettersInit.update((y, math.log(round((z/len(initial_state_list)),5))  ) for y, z in lettersInit.items())
        lettersInit = collections.OrderedDict(sorted(lettersInit.items()))
        return lettersInit

    def stateParams(self):
        transition_state_list = []
        for line in self.inTrain:
            for x in range(0, len(line)-1):
                xFrom = line[x]
                xTo = line[x+1]
                if xFrom == '<end>' or xTo == '<end>':
                    continue
                xFrom = xFrom.split()
                xTo = xTo.split()
                stateTrans = str(xFrom[1]) + '>' +  str(xTo[1])
                transition_state_list.append(stateTrans)
        lettersState = dict(collections.Counter(transition_state_list))
        lettersState.update((y, math.log(round((z/len(transition_state_list)),5))  ) \
            for y, z in lettersState.items())
        lettersState = collections.OrderedDict(sorted(lettersState.items()))
        return lettersState

    def emissionParams(self):
        emissionDict = defaultdict(lambda: defaultdict(int))
        for line in self.inTrain:
            for x in range(0, len(line)-1):
                xFrom = line[x]
                xTo = line[x+1]
                if xFrom == '<end>' or xTo == '<end>':
                    continue
                xFrom = xFrom.split()
                xTo = xTo.split()
                # use xFrom to get AA counts for each state
                emissionDict[xFrom[1]][xFrom[0]] += 1
        pseudoCountDict = addPseudocounts(emissionDict)
        for key1, value1 in pseudoCountDict.iteritems():
            denom = sum(value1.values())
            for key2, value2 in value1.items():
                value1[key2] = math.log(value2 / denom)
        return pseudoCountDict

    def lengthParams(self):
        length_dict = defaultdict(lambda: defaultdict(int))
        stateKeys = self.emissionParams().keys()
        for line in splitLines:
            listStates = [x[-1] for x in line if x[-1] != '>']
            count = 0
            for x,y in enumerate(listStates):
                if ( x == 0 ):
                    count = 0
                elif (listStates[x] ==  listStates[x-1] ):
                    count += 1
                elif (listStates[x] !=  listStates[x-1] ):
                    length_dict[y][str(count+1)] += 1
                    count = 0
        for key1, value1 in length_dict.iteritems():
            maxKey = max(value1.keys(), key=int)
            # add pseudocounts

            for x in range(1,int(maxKey)+1):
                value1[str(x)] += 1
            denom = sum(value1.values())
            for key2, value2 in value1.items():
                 value1[key2] = round(math.log(value2 / denom), 5)
        return length_dict


def stateLength(stateList):
    '''
    Takes a list as an argument. Returns a tuple of the state identity
    and the number of the same states that occur in a row.
    '''
    stateList = stateList[::-1]
    count = 0
    if len(stateList) > 1:
        for x in range(0, len(stateList)-1 ):
            if stateList[x] == stateList[x+1]:
                count += 1
            else:
                break
    count += 1
    stateLast = stateList[count-1]
    returnTuple = (stateLast, count)
    return returnTuple

def viterbi(IN, lengthParams, emissionParams, stateParams, initialParams):
    stateList = []
    likelihood = 0.0
    if len(initialParams) == 1:
        stateList.append(initialParams.keys()[0])
        likelihood += initialParams[initialParams.keys()[0]]
    count = 0
    possibleStates = emissionParams.keys()
    for x, currentEmission in enumerate(IN):
        if ( x == 0 ):
            continue
        else:
            priorEmission = IN[x-1]
            priorState = stateList[x-1]
            bestDict = {}
            for key, value in stateParams.iteritems():
                lenState = []
                count = 0
                priorList = stateList[:x-1]
                if key[0] == priorState:
                    if len(priorList) > 0:
                        stateTuple = stateLength(priorList)
                        if str(stateTuple[1]) in lengthParams[stateTuple[0]]:
                            currentValue = value + emissionParams[key[-1]][currentEmission] + \
                                lengthParams[stateTuple[0]][str(stateTuple[1])]
                            bestDict[key[-1]] = currentValue
                        else:
                            if key[0] == key[-1]:
                                continue
                            else:
                                currentValue = value + emissionParams[key[-1]][currentEmission]
                                bestDict[key[-1]] = currentValue
                    else:
                        currentValue = value + emissionParams[key[-1]][currentEmission]
                        bestDict[key[-1]] = currentValue
                if bool(bestDict) == False:
                    continue
                else:
                    likelihood += max(bestDict.iteritems(), key=operator.itemgetter(1))[1]
                    stateList.append(max(bestDict.iteritems(), key=operator.itemgetter(1))[0])
    print len(stateList)
    return likelihood



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "GHMM")
    parser.add_argument('-i', '--fasta_file', required=True)
    parser.add_argument('-t', '--training_file', required=True)
    parser.add_argument('-o', '--out_file', required=True)
    args = parser.parse_args()
    IN = args.fasta_file
    TRAIN = args.training_file
    OUT = args.out_file
    #IN = '../data/protein-secondary-structure.test.txt'

    mydir = os.path.dirname(os.path.realpath(__file__))
    mydir = str(mydir[:-6]) + 'data/'
    IN = mydir + '/' + IN
    TRAIN = mydir + '/' + TRAIN

    lines = [line.rstrip('\n') for line in open(TRAIN)]
    lines = [item for item in lines if '#' not in item]
    lines = filter(None, lines)
    splitLines = isplit(lines,'<>')
    splitLinesClass = getParams(splitLines)

    lengthParams = splitLinesClass.lengthParams()
    emissionParams = splitLinesClass.emissionParams()
    stateParams = splitLinesClass.stateParams()
    initialParams = splitLinesClass.initialParams()

    print lengthParams
    class_test = classFASTA(IN)
    sequences = [ x[1] for x in class_test.readFASTA() ]
    INsequence = sequences[0]
    #print lengthParams
    print len(INsequence)
    print viterbi(INsequence, lengthParams, emissionParams, stateParams,initialParams)
