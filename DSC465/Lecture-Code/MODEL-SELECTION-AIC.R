
### START

source("https://bioconductor.org/biocLite.R")
biocLite("GEOquery")
library(GEOquery)
library(MuMIn)
library(MASS)

#### input 

# perceived social isolation (PSI)
# UCLA Loneliness Scale

psi = c(32,33,40,23,41,39,44,32,39,33,NA,36,23,37,39,30,29,NA,42,NA,34,41,35,54,33,55,40, 
35, 45, 41, 42, 31, 30, 37, 27, 25, 27, 46, 62, 32, 45, 35, 39, 40, 43, 42,50, 38, 
33, NA, 31, 32, 49, 35, 34, 25, 42, 31, 30, 33, 37, 35, 35, 36, 30, 30, 37, 49, NA, 
58, 23, 22, 38, 33, 38, 45, 36, 57, 45, 47, 36, 47, 28, 31, 28, 35, 37, 26, 35, 37, 
40, NA, 46, 43, NA, 27, 20, 34)

# get data from GEO


gse65213.fn = getGEOfile("GSE65213")[[1]]
gse65213 = getGEO(filename = gse65213.fn, GSEMatrix = TRUE)

junk = gse65213@gsms
names(junk)
j1 = junk[[1]]@dataTable@table
j2 = junk[[2]]@dataTable@table
gnames = j1[,1]

ge = sapply(junk, function(obj) {as.double(obj@dataTable@table[,2])})

### add gene names to data

rownames(ge) = gnames


# there seems to be unusual values in subject in = 69

par(mfrow=c(2,1))
boxplot(ge[1:15,])
which(ge[1,] > 2000)
ge2 = ge[,-69]
psi2 = psi[-69]
boxplot(ge2[1:15,])

# remove missing values

ind = !is.na(psi2)
psi3 = psi2[ind]
ge3 = ge2[,ind]

# look for correlated genes using Spearman (rank) correlation 

f0 = function(x) {cor.test(x,psi3,method='spearman')$p.value}
pv = apply(ge3, 1, f0)
hist(pv,nclass=250)

# Select 10 most correlated (+ve or -ve)

gene.sel = sort.list(pv)[1:10]

par(mfrow=c(2,5),mar=c(4,4,2,2))
for (i in 1:10) {
  x = ge3[gene.sel[i],]
  plot(x,psi3,xlab=rownames(ge3)[gene.sel[i]],ylab='PSI',pch=20,cex=0.5)
  
  xy = na.omit(cbind(x,psi3))
  xy = xy[sort.list(xy[,1]),]
  lines(ksmooth(xy[,1],xy[,2],bandwidth=IQR(xy[,1]),kernel='normal'),col='red')
}

### remove anomaly

gene.sel2 = gene.sel[-7]

par(mfrow=c(2,5),mar=c(4,4,2,2))
for (i in 1:9) {
  x = ge3[gene.sel2[i],]
  plot(x,psi3,xlab=rownames(ge3)[gene.sel2[i]],ylab='PSI',pch=20,cex=0.5)
  
  xy = na.omit(cbind(x,psi3))
  xy = xy[sort.list(xy[,1]),]
  lines(ksmooth(xy[,1],xy[,2],bandwidth=IQR(xy[,1]),kernel='normal'),col='red')
}

ge4 = ge3[gene.sel2,]

main.data = data.frame(psi3, t(ge4))
names(main.data)[1] = 'psi'
head(main.data)

# check distributional assumptions

par(mfrow=c(3,3),mar=c(4,4,2,2))
for (i in 1:9) { boxplot(main.data[,i]) }


# look at model

fit = lm(psi ~ .,data=main.data,na.action=na.fail)
summary(fit)$coef 

# AICc = AIC +2(k+1)(k+2)/(n-k-2)

junk = dredge(fit, rank = "AIC")
fit.aic = get.models(junk, 1)[[1]]
junk = dredge(fit, rank = "AICc")
fit.aicc = get.models(junk, 1)[[1]]
junk = dredge(fit, rank = "BIC")
fit.bic = get.models(junk, 1)[[1]]

st1 = system.time(fit.stepaicf <- stepAIC(fit,direction='forward'))
st2 = system.time(fit.stepaicb <- stepAIC(fit,direction='backward'))

st1
st2


summary(fit.aic)$coef
summary(fit.aicc)$coef
summary(fit.bic)$coef
summary(fit.stepaicf)$coef
summary(fit.stepaicb)$coef

pm = cbind(predict(fit.aic), predict(fit.aicc), predict(fit.bic), predict(fit.stepaicf), predict(fit.stepaicb))
colnames(pm) = c('AIC','AICc','BIC','AICf', 'AICb')
pairs(pm)


# split data and repeat

set.seed(1)

n = dim(main.data)[1]

samp = sample(n)
samp

main.data3 = main.data[samp[1:45],]
main.data4 = main.data[samp[46:91],]

fitA = lm(psi ~ .,data=main.data3,na.action=na.fail)
summary(fitA)$coef 
junk = dredge(fitA, rank = "AIC")
fitA.aic = get.models(junk, 1)[[1]]
junk = dredge(fitA, rank = "AICc")
fitA.aicc = get.models(junk, 1)[[1]]
junk = dredge(fitA, rank = "BIC")
fitA.bic = get.models(junk, 1)[[1]]

fitA.stepaicf = stepAIC(fitA,direction='forward')
fitA.stepaicb = stepAIC(fitA,direction='backward')


fitB = lm(psi ~ .,data=main.data4,na.action=na.fail)
summary(fitB)$coef 
junk = dredge(fitB, rank = "AIC")
fitB.aic = get.models(junk, 1)[[1]]
junk = dredge(fitB, rank = "AICc")
fitB.aicc = get.models(junk, 1)[[1]]
junk = dredge(fitB, rank = "BIC")
fitB.bic = get.models(junk, 1)[[1]]

fitB.stepaicf = stepAIC(fitB,direction='forward')
fitB.stepaicb = stepAIC(fitB,direction='backward')


summary(fitA.bic)$coef
summary(fitB.bic)$coef

#######################

###
### is the gene selection reliable?
###

### original selection

f0 = function(x) {cor.test(x,psi3,method='spearman')$p.value}
pv0= apply(ge3, 1, f0)
              

### split data and repeat gene selection for each training data set          

f0 = function(x) {cor.test(x,psi3[1:45],method='spearman')$p.value}
pv1= apply(ge3[,1:45], 1, f0)
f0 = function(x) {cor.test(x,psi3[46:91],method='spearman')$p.value}
pv2= apply(ge3[,46:91], 1, f0)

### capture gene names

sort(pv0)[1:20]
gene.names0 = names(sort(pv0)[1:20])
sort(pv1)[1:20]
gene.names1 = names(sort(pv1)[1:20])
sort(pv2)[1:20]
gene.names2 = names(sort(pv2)[1:20])

### what selected genes are common?

intersect(gene.names0,gene.names1)
intersect(gene.names0,gene.names2)
intersect(gene.names1,gene.names2)

### STOP

