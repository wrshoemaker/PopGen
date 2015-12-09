from __future__ import division
import math
import os
#def import_pdb(pdb_file):
import re
import collections
import argparse


def euclidean_distance(x,y):
  return math.sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

#print euclidean_distance([0,3,4,5],[7,6,3,-1])

mydir = os.path.dirname(os.path.realpath(__file__))

file_path = mydir + '/' + '1FDL-clean.pdb'

def read_pdb(file_path):
    '''Returns the pdb file as an object of a list of strings
    with no white space and commas between all values'''
    with open(file_path, 'r') as f_in:
        line_list = []
        lines = (','.join(re.findall('\"[^\"]*\"|\S+', line)) for line in f_in) # All lines including the blank ones
        lines = (line for line in lines if line)
        for line in lines:
            line_list.append(line)
        return line_list


cutoff = 6

#ContactOrder(protein_length, )

# do, write a function that pulls all of the AA into a dictionary.
# AA position is the key, a paired tuple of AA, the atom and euclidean distance are the values

def sort_pdb(file_path):
    '''Returns  PDB as a dictionary wher keys are the positions of
    the AA residues and the values are a list containing tuples
    containing cartesian coordinates and AA type'''
    pdb_file = read_pdb(file_path)
    atom_count = 0
    #residue_count = []
    atom_dict = {}
    residue_count = 0
    for line in pdb_file:
        # add '1' to final count, enumerate starts at zero
        line = line.split(',')
        #atom_count = 0
        if str(line[0]).upper() == 'ATOM':
            atom_count += 1
            # AA number = (AA type, cartesian coordinates)
            residue_position = int(line[5])
            #print residue_position
            if residue_count <= residue_position:
                residue_count = residue_position

            # residue position, residue type, x, y, z
            atom_dict[atom_count] = (int(line[5]), line[3], float(line[6]), float(line[7]), float(line[8]))
            #if residue_position not in aa_dict:
            #    aa_dict[residue_position] = [(line[3], float(line[6]), float(line[7]), float(line[8])) ]
            #else:
            #    aa_dict[residue_position].append( (line[3], float(line[6]), float(line[7]), float(line[8])) )

        #elif str(line[0]).upper() == 'SEQRES':
        #    residue_count.append(int(line[3]))
    #aa_dict = collections.OrderedDict(sorted(aa_dict.items()))
    #print atom_count

    #print residue_count[0]
    #print residue_count
    return atom_dict, residue_count, atom_count

def calculateContactOrder(file_path, cutoff):
    sort_pdb_result = sort_pdb(file_path)
    atom_dict = sort_pdb_result[0]
    N = sort_pdb_result[1]
    atom_count = sort_pdb_result[2]
    #print atom_dict
    #print len_dict
    residues_sep = 0
    residue_set = set()
    #print atom_dict
    for i in range(1, len(atom_dict) +1):
        for j in range(1, i):
            residue_i = atom_dict[i][0]
            residue_j = atom_dict[j][0]
            ij_tuple = (residue_i , residue_j)
            if ij_tuple in residue_set:
                pass
            else:
                xyz1 = atom_dict[i][2:]
                xyz2 = atom_dict[j][2:]
                euc_dist = euclidean_distance(xyz1,xyz2)
                #print euc_dist
                if euc_dist <= cutoff:
                    residue_set.add((residue_i , residue_j ))
                    position_diff = abs(residue_i - residue_j )
                    #if position_diff >= 0:
                    residues_sep += position_diff
                    #S_ij += 1
    L = len(residue_set)
    #print S_ij
    CO = (residues_sep  ) * (1 / ( L  * N ) )
    print "There are " + str(N) + " residues"
    print "There are " + str(atom_count) + " residues"
    print "CO = " + str(CO)
    #return CO

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Run randomized motif approach")
    parser.add_argument('-p', type = str, default = "1FDL-clean.pdb", help = "PDB file")
    parser.add_argument('-d', type = int, default = 5, help = "cutoff")

    params = parser.parse_args()

    mydir = os.path.dirname(os.path.realpath(__file__))

    input_fasta = mydir + '/' + params.p
    cutoff = params.d
    calculateContactOrder(input_fasta, cutoff)
