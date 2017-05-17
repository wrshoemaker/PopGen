rm(list = ls())
getwd()
setwd('~/github/PopGen/I519/Project/')

source("https://bioconductor.org/biocLite.R")
biocLite("muscle")
biocLite("msa")

#require("muscle")
require('msa')

mySequences <- readAAStringSet("./AAs.fa")
myFirstAlignment <- msa(mySequences)
print(myFirstAlignment)

msaPrettyPrint(myFirstAlignment, output="asis", showNames="none",
               showLogo="none", alFile = 'what.aln', askForOverwrite=FALSE, verbose=FALSE)
