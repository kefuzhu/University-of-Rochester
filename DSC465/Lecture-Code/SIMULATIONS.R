
#######
####### EXAMPLE 1: Bootstrap third order sample moment 
#######

### Sq =  Avg[(x - xbar)^3]

Sq = function(x) {mean(sqrt(x))}

### Simulate sample distribution from Chisq 4 df

nrep=1000
nsample=50
xmatrix = matrix(rchisq(nrep*nsample,df=4),nrep,nsample)
sq.sample.1 = apply(xmatrix,1,Sq)

### Examine distribution


par(mfrow=c(2,2)) # make room for all plots

hist(sq.sample.1,nclass=15,main='Sampling distribution')
mean(sq.sample.1)
sd(sq.sample.1)

### Basic bootstrap operation

boot.rep = function(x) {Sq(sample(x,replace=TRUE))}
boot.rep.sample = sapply(1:10000,function(i) boot.rep(xmatrix[1,]))
mean(boot.rep.sample)
sd(boot.rep.sample)

### Apply to each sample

boot.rep.sample.rep = apply(xmatrix, 1, function(x) {
                            z = sapply(1:1000, function(i) boot.rep(x))
                            return(c(mean(z),sd(z)))
})                     
                    
### Examine accuracy of bootstrap 


hist(boot.rep.sample.rep[1,],main="Bootstrap mean")
abline(v=mean(sq.sample.1),col='green',lwd=2)
legend('topleft',legend=c("True value"),col='green',lty=1,cex=1,bty='n')
hist(boot.rep.sample.rep[2,],main="Bootstrap standard error")
abline(v=sd(sq.sample.1),col='green',lwd=2)
legend('topleft',legend=c("True value"),col='green',lty=1,cex=1,bty='n')


#######
####### EXAMPLE 2: Two sample permutation test
#######

### make room for plots 

par(mfrow=c(2,3))

### Create 2 samples

set.seed(12345)
x = rgamma(10,5,1)
y = rgamma(20,8,1)
boxplot(x,y)

### Express in model form

grp = c(rep(0,10),rep(1,20))
xy = c(x,y)
cbind(xy,grp)
boxplot(xy~grp)

### Calculate sample means by group

tapply(xy,grp,function(x) mean(x))

# There are usually more than one way to do things 

c(mean(xy[grp==0]),mean(xy[grp==1]))

### Permute group labels

grp.perm = sample(grp)
grp.perm

# Permutation destroys group association with outcomes 

tapply(xy,grp,function(x) mean(x))
tapply(xy,grp.perm,function(x) mean(x))

### Create a null distributionfor the hypothesis of equal group distributions

perm.rep = sapply(1:1000, function(x) {
                            diff(tapply(xy,sample(grp),function(x) mean(x)))
})

# Observed statistic

obs.diff = diff(tapply(xy,grp,function(x) mean(x)))
hist(perm.rep,nclass=15)
abline(v=obs.diff,col="green")
legend('topleft',legend=c("Observed statistic"),col='green',lty=1,cex=1,bty='n')

# Note that p-value estimation should include the observed statistic

mean(obs.diff <= c(perm.rep,obs.diff))


################################################################
### Is this test accurate? Compare nominal to actual test size
################################################################

set.seed(12345)

###
### Now, simulate data with equal group distributions 
### Simulate nrep data sets, apply bootstrap to each one 
###

nrep=100
nsample=30
xmatrix = matrix(rgamma(nrep*nsample,6.5,1),nrep,nsample)

grp = c(rep(0,10),rep(1,20))

pval = NULL
for (i in 1:nrep) {
  xy = xmatrix[i,]
  obs.diff = diff(tapply(xy,grp,function(x) mean(x)))
  perm.rep = sapply(1:1000, function(x) {
                            diff(tapply(xy,sample(grp),function(x) mean(x)))
  })
  pval[i] = mean(obs.diff <= c(perm.rep,obs.diff))
}
  
### Under the NULL hypothesis, the p-values should be uniformly distributed

# Histogram

hist(pval,nclass=15)

# Examine cumulative distribution function of p-values, compare to the uniform distribution

plot(sort(pval),(1:nrep)/nrep,type='s')
abline(0,1,col='red',lwd=1)

#
# We want to compare nominal 5% significance level to the actual significance level. 
# The actual significance level can be estimated as a binomial parameter. 
# For nrep = 100, the standard error for this estimate is about sqrt(.05*0.95/100) = 0.0218.
# Margin of error of a 95% CI is 2*0.0218 > 4%. 
# So if 5% is the actual significance level, as wll as the nominal, we can expect to see the estimated 
# significance level to be 1% - 9%. 

mean(pval <= 0.05)

# To decrease a margin of error by a factor of 4, increase the sample size by a factor of 4^2 = 16. 

#######################################
### This can always be parallelized
#######################################

### Testing a bootstrap 

# load parallel library

library(parallel)

### Enclose entire procedure into a single function, with input equal to the number of simulation replications

fun.par = function(nrep) {
  nsample=30
  xmatrix = matrix(rgamma(nrep*nsample,6.5,1),nrep,nsample)
  grp = c(rep(0,10),rep(1,20))
  pval = rep(0,nrep)
  for (i in 1:nrep) {
    xy = xmatrix[i,]
    obs.diff = diff(tapply(xy,grp,function(x) mean(x)))
    perm.rep = sapply(1:1000, function(x) {
                          diff(tapply(xy,sample(grp),function(x) mean(x)))
    })
    pval[i] = mean(obs.diff <= c(perm.rep,obs.diff))
  }
  return(pval)
}  

### We can time the computation with the system.time() function (use the older assign operator <-)

st0 = system.time(junk1 <- fun.par(50))
st1 = system.time(junk1 <- fun.par(100))
st0
st1

### Time needed for nrep = 1600

st0[3]*1600/50

### Set up computation on 5 processors (your computer may have fewer processors, but it will still accept 5)

mc = 5
in.list = as.list(rep(320,mc))
cl = makeCluster(mc)
clusterSetRNGStream(cl,1234)
system.time(junk3 <- parLapply(cl,in.list,fun.par))
stopCluster(cl)

### consolidate simulation data into a single vector

pval = NULL
for (i in 1:5) {pval = c(pval,junk3[[i]])}
length(pval)


### Repeat summary

par(mfrow=c(1,2))
hist(pval,nclass=15)

# Examine cumulative distribution function of p-values, compare to the uniform distribution

nrep = length(pval)
plot(sort(pval),(1:nrep)/nrep,type='s')
abline(0,1,col='red',lwd=1)

mean(pval <= 0.05)

###
### Suppose initial code needs to be run on each processor, for example, a library needs to be loaded. 
### Use the  clusterEvalQ() function, for example:
###
###  cl = makeCluster(mc)
###  clusterSetRNGStream(cl,1234)
###  clusterEvalQ(cl,library(splines))
###  clusterEvalQ(cl,source("copLib.R"))
###  clusterCall(cl, fun, ...)
###  stopCluster(cl)
###

