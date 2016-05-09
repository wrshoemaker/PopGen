################################################################################
#                                                                              #
# Stats-n-Snacks Lession 3: Multivariate Statistics                            #
#                                                                              #
# Written by Nathan Wisnoski and Mario Muscarella                              #
#                                                                              #
# Last Update: 24 Apr 2016                                                     #
#                                                                              #
################################################################################

# Initial Setup
rm(list = ls())

# Load Packages
require("vegan")
# If package isn't installed, run:
# install.packages("vegan")

################################################################################
# Part I: Bumpus Bird Data
#
# More Info on Data: 
#    https://www.fieldmuseum.org/science/blog/hermon-bumpus-and-house-sparrows
#
################################################################################

# Load Data
bumpus <- read.delim(file = "https://www.fieldmuseum.org/sites/default/files/plowther/2014/09/24/bumpus.txt", 
                     header = F, sep = "")

# Rename Columns
colnames(bumpus) <- c("Bump.num", "Sex","Age", "Survival", "Total.Length",
                      "Alar.Extent", "Weight", "Head.length", "Humerus.length", 
                      "Femur.length", "Tibiotarsus.length",  "Skull.width",
                      "Sternum.length")

# Summarize Data
summary(bumpus)

# Subset only Body Measurements
bumpus.body.F <- bumpus[which(bumpus$Sex == "f"), c(5:12)]
bumpus.body.M <- bumpus[which(bumpus$Sex == "m"), c(5:12)]
summary(bumpus.body.F)

# Test for Multicollinearity
cor.test(bumpus.body.F$Head.length, bumpus.body.F$Humerus.length)
plot(bumpus.body.F)

# PCA --- What are we trying to predict here again? 
bump.pca <- princomp(bumpus.body.F, na.action = na.omit)

# How much variation is explained by each principal component?
summary(bump.pca) 

# Why is 94% of variation captured by first axis?

# Transformations and Scaling
# Defaults of scale function are to center on mean and scale by SD
bumpus.body.F2 <- apply(bumpus.body.F, 2, scale)

# PCA --- What are we trying to predict here again? 
bump.pca <- princomp(bumpus.body.F2, na.action = na.omit)

# You can also use options in princomp to center and scale
# But we prefer to do separately so that we have more control

# How much variation is explained by each principal component?
summary(bump.pca)

pc1 <- bump.pca$scores[,1]
pc2 <- bump.pca$scores[,2]

plot (pc1, pc2)

# What do the axes represent
cor(cbind(pc1, pc2, bumpus.body.F2))[c(3:10),c(1:2)]

################################################################################
# Part II: Dutch Dune Community Data
#
# More Info on Data: 
#    Jongman R.H., Ter Braak C.J.F. & van Tongeren O.F.R. (eds) (1995): 
#    Data analysis in community and landscape ecology. 
#    Cambridge University Press
#
################################################################################

# Load Data
data(dune)
data(dune.env)

# Summary of Env
summary(dune.env)
dim(dune)


# Tranformations
## PA
dune.pa <- decostand(dune, method = "pa")

## Others: Relative Abundance and Hellinger 
dune.rel <- decostand(dune, method = "total")
dune.hel <- decostand(dune, method = "hellinger")

# Resemblance Matrix (AKA: Distance Matrix)
dune.dist <- vegdist(dune, method = "bray")
# Is this similarity or dissimilarity 

# Check the diagonals -> What does a distance of 0 mean?
dune.dist <- vegdist(dune, method = "bray", diag = T)

# Create Resemblance Matrix (Both Rel and Hel)
duneREL.dist <- vegdist(dune.rel, method = "bray")
duneHEL.dist <- vegdist(dune.hel, method = "bray")

# Visualization: Ordination
dune.pcoa <- cmdscale(duneHEL.dist, eig = T, k = 2)
dune.nmds <- metaMDS(duneHEL.dist, k = 2, autotransform = F) # Why no transform? - B/c Hellinger

# Are these good representations of the original data?
## PCoA: Percent Explained
var1 <- round(dune.pcoa$eig[1] / sum(dune.pcoa$eig),3) * 100
var2 <- round(dune.pcoa$eig[2] / sum(dune.pcoa$eig),3) * 100

## nMDS: Stress
strss <- round(dune.nmds$stress, 3)

# What are eigenvalues and eigenvectors
str(dune.pcoa)

# Plot Ordination Results
## PCoA
## Vanilla Plot
plot(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2])

## Cool Kid Plot
par(mar = c(5, 5, 3, 2) + 0.1)
plot(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
     xlim = c(-0.4,0.25), ylim = c(-0.4,0.55),
     xlab = paste("PCoA 1 (", var1, "%)", sep = ""),
     ylab = paste("PCoA 2 (", var2, "%)", sep = ""), 
     pch = 19, cex = 2.0, type = "n", cex.lab = 1.5, cex.axis = 1.2, axes = F)
points(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
       pch=19, cex=2, bg="wheat", col="wheat")
text(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
     cex = 0.5, labels = row.names(dune.pcoa$points))
axis(side = 1, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 2, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1,
     at = c(-0.4, -0.2, 0, 0.2, 0.4))
axis(side = 3, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 4, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1,
     at = c(-0.4, -0.2, 0, 0.2, 0.4))
abline(h = 0, v = 0, lty = 3)
box(lwd = 2)


## NMDS
par(mar = c(5, 5, 3, 2) + 0.1)
plot(dune.nmds$points[ ,1], dune.nmds$points[ ,2],
     xlim = c(-0.45,0.3), ylim = c(-0.35,0.52),
     xlab = paste("NMDS 1"),
     ylab = paste("NMDS 2"), 
     pch = 19, cex = 2.0, type = "n", cex.lab = 1.5, cex.axis = 1.2, axes = F)
points(dune.nmds$points[ ,1], dune.nmds$points[ ,2],
       pch=19, cex=2, bg="wheat", col="wheat")
text(dune.nmds$points[ ,1], dune.nmds$points[ ,2],
     cex = 0.5, labels = row.names(dune.pcoa$points))
axis(side = 1, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 2, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1, 
     at = c(-0.2, 0, 0.2, 0.4))
axis(side = 3, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 4, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1, 
     at = c(-0.2, 0, 0.2, 0.4))
abline(h = 0, v = 0, lty = 3)
legend("topright", legend = paste("stress = ", strss), bty = "n", cex = 0.8)
box(lwd = 2)


# Why didn't we use PCA and Why you shouldn't either

# Correspondence Analysis (CA) (Unconstrained Ordination)
dune.ca <- vegan::cca(dune)
dune.ca.explainvar1 <- round(dune.ca$CA$eig[1] / sum(dune.ca$CA$eig), 3) * 100
dune.ca.explainvar2 <- round(dune.ca$CA$eig[2] / sum(dune.ca$CA$eig), 3) * 100

# But we also have some environmental data, so we can use constrained ordination, but
# "CCA is a good choice if the user has clear and strong a priori hypotheses 
# on constraints and is not interested in the major structure in the data set."


# Create Env. Matrix (This is super inelegant) 
dune.env2 <- dune.env[,c("A1", "Moisture", "Manure")]
str(dune.env2)
dune.env2$Moisture <- as.numeric(dune.env2$Moisture)
dune.env2$Manure <- as.numeric(dune.env2$Manure)
dune.env2 <- as.matrix(dune.env2)
  

# CCA & RDA (Constrained Ordination)
# CCA
dune.cca <- vegan::cca(dune ~ dune.env2)
dune.cca.explainvar1 <- round(dune.cca$CCA$eig[1] /
                              sum(c(dune.cca$CCA$eig, dune.cca$CA$eig)), 3) * 100
dune.cca.explainvar2 <- round(dune.cca$CCA$eig[2] /
                              sum(c(dune.cca$CCA$eig, dune.cca$CA$eig)), 3) * 100

# CCA Plot
par(mar = c(5, 5, 4, 4) + 0.1)
plot(scores(dune.cca, display = "wa"), xlim = c(-1.5, 3.2), ylim = c(-2.5, 2),
     xlab = paste("CCA 1 (", dune.cca.explainvar1, "%)", sep = ""), 
     ylab = paste("CCA 2 (", dune.cca.explainvar2, "%)", sep = ""), 
     pch = 16, cex = 2.0, type = "n", cex.lab = 1.5, cex.axis = 1.2, axes = FALSE)
axis(side=1, labels=T, lwd.ticks=2, cex.axis=1.2, las=1)
axis(side=2, labels=T, lwd.ticks=2, cex.axis=1.2, las=1)
abline(h=0, v=0, lty=3)
box(lwd=2)
points(scores(dune.cca, display = "wa"),
       pch=19, cex=2, bg="gray", col="gray")
text(scores(dune.cca, display = "wa"), cex=0.5,
     labels = row.names(scores(dune.cca, display = "wa")))
dune.cca.vectors <- scores(dune.cca, display = "bp")
row.names(dune.cca.vectors) <- colnames(dune.env2)
arrows(0, 0, dune.cca.vectors[, 1] * 2, dune.cca.vectors[, 2]*2,
       lwd = 2, lty = 1, length = 0.2, col = "red")
text(dune.cca.vectors[, 1] * 2, dune.cca.vectors[, 2] * 2, pos=c(4, 4, 1),
     labels = row.names(dune.cca.vectors), col = "red")


# Does the pattern look odd/horseshoe-shaped?


# RDA
dune.rda <- vegan::rda(dune ~ dune.env2)
dune.rda.explainvar1 <- round(dune.rda$CCA$eig[1] /
                                sum(c(dune.rda$CCA$eig, dune.rda$CA$eig)), 3) * 100
dune.rda.explainvar2 <- round(dune.rda$CCA$eig[2] /
                                sum(c(dune.rda$CCA$eig, dune.rda$CA$eig)), 3) * 100

# RDA Plot 
par(mar = c(5, 5, 4, 4) + 0.1)
plot(scores(dune.rda, display = "wa"), xlim = c(-2.5, 3.5), ylim = c(-3.3, 3.3),
     xlab = paste("RDA 1 (", dune.rda.explainvar1, "%)", sep = ""), 
     ylab = paste("RDA 2 (", dune.rda.explainvar2, "%)", sep = ""), 
     pch = 16, cex = 2.0, type = "n", cex.lab = 1.5, cex.axis = 1.2, axes = FALSE)
axis(side=1, labels=T, lwd.ticks=2, cex.axis=1.2, las=1)
axis(side=2, labels=T, lwd.ticks=2, cex.axis=1.2, las=1)
axis(side=3, labels=F, lwd.ticks=2, cex.axis=1.2, las=1)
axis(side=4, labels=F, lwd.ticks=2, cex.axis=1.2, las=1)
abline(h=0, v=0, lty=3)
box(lwd=2)
points(scores(dune.rda, display = "wa"),
       pch=19, cex=2, bg="gray", col="gray")
text(scores(dune.rda, display = "wa"), cex=0.5,
     labels = row.names(scores(dune.rda, display = "wa")))
dune.rda.vectors <- scores(dune.rda, display = "bp")
row.names(dune.rda.vectors) <- colnames(dune.env2)
arrows(0, 0, dune.rda.vectors[, 1] * 2, dune.rda.vectors[, 2]*2,
       lwd = 2, lty = 1, length = 0.2, col = "red")
text(dune.rda.vectors[, 1] * 2, dune.rda.vectors[, 2] * 2, pos=3,
     labels = row.names(dune.rda.vectors), col = "red")






# Statistical Tests with Continuous Predictors
dune.cca.fit <- envfit(dune.cca, dune.env2, perm = 999)
dune.rda.fit <- envfit(dune.rda, dune.env2, perm = 999)

# Mantel Test
dune.env.dist <- vegdist(scale(dune.env2),method = "euclid")
mantel(dune.dist,dune.env.dist)

# Statistical Tests with Categorical Predictors
## Plot by Management

dune.env$Management
library("wesanderson")
palette(wes_palette("Royal1")) 
par(mar = c(5, 5, 3, 2) + 0.1)
plot(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
     xlim = c(-0.4,0.25), ylim = c(-0.4,0.55),
     xlab = paste("PCoA 1 (", var1, "%)", sep = ""),
     ylab = paste("PCoA 2 (", var2, "%)", sep = ""), 
     pch = 19, cex = 2.0, type = "n", cex.lab = 1.5, cex.axis = 1.2, axes = F)
points(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
       pch=21, cex=2, bg=dune.env$Management, col="black")
text(dune.pcoa$points[ ,1], dune.pcoa$points[ ,2],
     cex = 0.5, labels = row.names(dune.pcoa$points))
axis(side = 1, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 2, labels = T, lwd.ticks = 2, cex.axis = 1.2, las = 1,
     at = c(-0.4, -0.2, 0, 0.2, 0.4))
axis(side = 3, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1, 
     at = c(-0.4, -0.2, 0, 0.2))
axis(side = 4, labels = F, lwd.ticks = 2, tck = -0.025, cex.axis = 1.2, las = 1,
     at = c(-0.4, -0.2, 0, 0.2, 0.4))
abline(h = 0, v = 0, lty = 3)
legend("topright", legend = levels(dune.env$Management), col = c(1:4), pch = 19, bty = "n")
box(lwd = 2)


# Statistical Tests with PERMANOVA
perm.rel <- adonis(dune.rel ~ dune.env$Management, method = "bray", permutations = 999)
perm.hel <- adonis(dune.hel ~ dune.env$Management, method = "bray", permutations = 999)

