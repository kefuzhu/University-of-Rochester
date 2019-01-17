
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

junk = exprs(gse65213@gsms)
junk = gse65213@gsms
names(junk)
j1 = junk[[1]]@dataTable@table
j2 = junk[[2]]@dataTable@table
gnames = j1[,1]

ge = sapply(junk, function(obj) {as.double(obj@dataTable@table[,2])})

### add gene names to data

rownames(ge) = gnames

# there seems to be unusual values in subject in = 69

boxplot(ge[1:10,])
which(ge[1,] > 2000)
ge2 = ge[,-69]
psi2 = psi[-69]

# remove missing values

ind = !is.na(psi2)
psi3 = psi2[ind]
ge3 = ge2[,ind]

# look for correlated genes using Spearman (rank) correlation 

f0 = function(x) {cor.test(x,psi3,method='spearman')$p.value}
pv = apply(ge3, 1, f0)
hist(pv,nclass=50)

library ( glmnet )

gene.sel = sort.list(pv)[1:25]
ge5 = ge3[gene.sel,]
main.data = t(ge5)
head(main.data)


### RSS + lambda*[alpha*L1 + (1-alpha)*L2]

# leave predictors unstandardized for now

grid =10^seq(10 , -2 , length =100)
fit.ridge = glmnet(main.data, psi3, alpha=0)
class(fit.ridge)
isS4(fit.ridge)
names(fit.ridge)

# dev.ratio = 1 - dev/nulldev (like R^2)

par(mfrow=c(1,1))
plot(fit.ridge$lambda, fit.ridge$dev.ratio)

# one complete set of coefficients for each lambda

fit.ridge$lambda
coef(fit.ridge)[1:5,1:5]

print(fit.ridge)[1:5,]
coef(fit.ridge)[,2]
coef(fit.ridge, s = 1.1)

# use cross validation

fit.ridge.cv = cv.glmnet(main.data, psi3, alpha=0)
plot(fit.ridge.cv)
fit.ridge.cv$lambda.min
fit.ridge.cv$lambda.1se

coef.0 = coef(fit.ridge, s = 0)
coef.min = coef(fit.ridge, s = fit.ridge.cv$lambda.min)
coef.1se = coef(fit.ridge, s = fit.ridge.cv$lambda.1se)
coef.large = coef(fit.ridge, s = 1000)

par(mfrow=c(1,3))

plot(coef.0[-1], coef.min[-1])
abline(0,1)
plot(coef.min[-1], coef.1se[-1])
abline(0,1)
plot(coef.1se[-1], coef.large[-1])
abline(0,1)

##### lets look at the predictors again

par(mfrow=c(1,1))
boxplot(main.data)
min(main.data)

gmed = apply(main.data,2,median,na.rm=T)
giqr = apply(main.data, 2, IQR, na.rm = TRUE)
plot(abs(coef.1se[-1]),gmed)

# large gene expressions = small coefficients

# standardize predictors

main.data2 = scale(main.data, center = gmed, scale = giqr)
plot(main.data2[,1],main.data[,1])
boxplot(main.data2)

fit.ridge2 = glmnet(main.data2, psi3, alpha=0)
fit.ridge2.cv = cv.glmnet(main.data2, psi3, alpha=0)
fit.ridge2.cv$lambda.min
fit.ridge2.cv$lambda.1se

# relative importance of predictors easier to assess when standardized

par(mfrow=c(1,1))
plot(fit.ridge,label=T)
plot(fit.ridge2,label=T,xvar='lambda')

sort.list(gmed)

#################
# now try LASSO
#################

par(mfrow=c(1,1))
fit.lasso2 = glmnet(main.data2, psi3, alpha=1)
fit.lasso2.cv = cv.glmnet(main.data2, psi3, alpha=1)
plot(fit.lasso2.cv)
fit.lasso2.cv$lambda.min
fit.lasso2.cv$lambda.1se


# get coefficients from Ridge Regr and LASSO

coef2.0 = coef(fit.ridge2, s = 0)
coef2.min = coef(fit.ridge2, s = fit.ridge2.cv$lambda.min)
coef2.1se = coef(fit.ridge2, s = fit.ridge2.cv$lambda.1se)
coef2.large = coef(fit.ridge2, s = 1000)

coef3.0 = coef(fit.lasso2, s = 0)
coef3.min = coef(fit.lasso2, s = fit.lasso2.cv$lambda.min)
coef3.1se = coef(fit.lasso2, s = fit.lasso2.cv$lambda.1se)
coef3.large = coef(fit.lasso2, s = 1000)

par(mfrow=c(2,2))

plot(coef2.0[-1],coef3.0[-1], xlab='Ridge',ylab = 'LASSO')
abline(h=0,col='green')
abline(a=0,b=1,col='blue')
title('lambda = 0')

plot(coef2.min[-1],coef3.min[-1], xlab='Ridge',ylab = 'LASSO')
abline(h=0,col='green')
abline(a=0,b=1,col='blue')
title('min MSE = 0')

plot(coef2.1se[-1],coef3.1se[-1], xlab='Ridge',ylab = 'LASSO')
abline(h=0,col='green')
abline(a=0,b=1,col='blue')
title('MSE + 1 SE')

plot(coef2.large[-1],coef3.large[-1], xlab='Ridge',ylab = 'LASSO')
abline(h=0,col='green')
abline(a=0,b=1,col='blue')
title('large lambda')

#### larger pvalues associated with 0 coefficient values, but not exclusively

boxplot(pv[gene.sel] ~ coef3.1se[-1]==0)


### how good at model selection is LASSO?

dim(main.data2)

set.seed(1)

par(mfrow=c(1,1))
randomData = matrix(rnorm(91*25),91,25)
fit.lasso99.cv = cv.glmnet(randomData, psi3, alpha=1)
plot(fit.lasso99.cv)
coef99.min = coef(fit.lasso99.cv, s = fit.lasso99.cv$lambda.min)
coef99.min
sum(coef99.min != 0)

#### try loop 

n = 100
nv = integer(n)
msev = numeric(n)
set.seed(1)
for (i in 1:n) {
  
  randomData = matrix(rnorm(91*25),91,25)
  fit.lasso99.cv = cv.glmnet(randomData, psi3, alpha=1)
  coef99.min = coef(fit.lasso99.cv, s = fit.lasso99.cv$lambda.min)
  nv[i] = sum(coef99.min != 0)-1
  msev[i] = min(fit.lasso99.cv$cvm)
}

### True NULL MSE 

var(psi3)

### Estimated null MSE via randomization

min(msev)
mean(msev)

boxplot(msev)
abline(h=var(psi3),col='green')

# there is still spurious variable selection 

table(nv)

### try permutation procedure

n = 100
nv = integer(n)
msepv = numeric(n)
set.seed(1)
for (i in 1:n) {
  
  psi3perm = psi3[sample(length(psi3))]
  fit.lasso99.cv = cv.glmnet(randomData, psi3perm, alpha=1)
  coef99.min = coef(fit.lasso99.cv, s = fit.lasso99.cv$lambda.min)
  nv[i] = sum(coef99.min != 0)-1
  msepv[i] = min(fit.lasso99.cv$cvm)
}

### Model test MSE much smaller than null MSE 

boxplot(list(msev,msepv,min(fit.lasso2.cv$cvm)))

### But this still doesn't control for selection bias!!!

### PC analysis

par(mfrow=c(1,1))
prc<-prcomp(main.data, scale=T)

# Scree plot

plot(prc)

#par(mai=c(4,6,4,4))

npc<-10
pca.matrix<-prc$x[,1:npc]
labelsx<-paste('PC',c(1:npc), sep='')
pairs(pca.matrix[,1:5], labels=labelsx, col=1, pch=20, main='"GSE65213"')

pairs(pca.matrix[,1:5], labels=labelsx, col=1 + (psi3 > median(psi3)), pch = 20,  main='GSE10245 (symbols for recurrent subjects  vary) [unscaled]')

# we can see loadings

prc$rotation

library(boot)

dfr = data.frame(psi3,pca.matrix)

cv.err = numeric(8)

fit1 = glm(psi3 ~ PC1, data=dfr )
cv.err[1] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2, data=dfr )
cv.err[2] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3, data=dfr )
cv.err[3] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3+PC4, data=dfr )
cv.err[4] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3+PC4+PC5, data=dfr )
cv.err[5] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3+PC4+PC5+PC6, data=dfr )
cv.err[6] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3+PC4+PC5+PC6+PC7, data=dfr )
cv.err[7] = cv.glm(dfr,fit1,K=91)$delta[1]
fit1 = glm(psi3 ~ PC1+PC2+PC3+PC4+PC5+PC6+PC7+PC8, data=dfr )
cv.err[8] = cv.glm(dfr,fit1,K=91)$delta[1]

plot(cv.err,type='b')

### first two principal components are sufficient

### STOP



