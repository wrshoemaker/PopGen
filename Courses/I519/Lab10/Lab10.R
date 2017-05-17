###############################
# bioconductor

rm(list=ls())
getwd()
setwd('~/github/PopGen/I519/Lab10/microarray/Affy/')
getwd()

#source("https://bioconductor.org/biocLite.R")
#biocLite("affy")
biocLite("GEOquery")
biocLite("limma")
biocLite("marray")


#install.packages("GEOquery", dependencies=TRUE)
#install.packages("OLIN", dependencies=TRUE)
#install.packages("affy", dependencies=TRUE)
# library(GEOquery)
# library(marray)
# library(OLIN)
library(affy)
library(GEOquery)
library(limma)
library(marray)

# change dir to the affy folder under the downloaded dataset
dir()

affy <- ReadAffy()
affy 
pData(affy) # access the phenotype data and meta-data if available
pm(affy[,1]) 
mm(affy[,1])
sampleNames(affy)
index <- c(1,2,3,100,1000)
index
probeNames(affy)[index] # check some of the probe names
geneNames(affy)[1:3] # gene name, not really :-)
pm(affy)[index,]
hist(affy)
par(mfrow = c(2,2)) # prepare for the plotting
image(affy)
MAplot(affy[,1:3], pairs=TRUE)
# Target degradation plots
deg <- AffyRNAdeg(affy) 
summaryAffyRNAdeg(deg)
par(mfrow = c(1,1))
plotAffyRNAdeg(deg)
#### normalization remove from the intensity measures any systematic trends which arise from the microarray technology;
## rather than from differences between the probes or between the target RNA samples hybridized to the arrays. 
affy.norm <- normalize(affy)
### more normlizations
affy.exp <- expresso(affy, normalize.method="loess", bgcorrect.method="rma", pmcorrect.method="pmonly", summary.method="avgdiff")
# save the output
#exprs2excel(affy.exp, file="affynorm.csv")
write.exprs(affy.exp, file="affynorm.csv", sep=",")



# open gpr files

filenames <- c('../cDNA/HYB_12821154_balanced_0001_results.gpr',
               '../cDNA/HYB_12821191_balanced_results.gpr',
               '../cDNA/HYB_12824547_balanced_results.gpr')
data<-read.GenePix(filenames)
data
