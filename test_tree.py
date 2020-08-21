
#from Bio import Phylo


#tree = Phylo.read("/Users/WRShoemaker/Downloads/rep_set_v13.tre", "newick")

#myclade = tree.find_clades("OTU_97.17922").next()

#print(myclade)


from skbio import read
from skbio import TreeNode
from io import StringIO
#open_filehandle = StringIO('(a, b);')
tree = read("/Users/WRShoemaker/Downloads/rep_set_v13.tre", format='newick', into=TreeNode)
#tree = read("/Users/WRShoemaker/GitHub/LTDE/data/tree/RAxML_bestTree.ltde", format='newick', into=TreeNode)
print(tree.find('OTU_97.36544'))

#print(tree)
print(tree.ascii_art())
