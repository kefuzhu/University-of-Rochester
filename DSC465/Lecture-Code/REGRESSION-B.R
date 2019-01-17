
### START

setwd("/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE")

### Read .csv file (comma delimited)

tab = read.csv("Advertising.csv")

#Create new variables

TV = tab$TV
Sales = tab$Sales
Radio = tab$Radio
Newspaper = tab$Newspaper

#######################################
### Calculating regression coefficients
#######################################

############################
### Simple linear regression
############################

fit = lm(Sales ~ TV)

# do this directly:

y = Sales
x = TV 
n = length(y)

ssx = sum((x-mean(x))^2)
ssy = sum((y-mean(y))^2)
ssxy = sum((x-mean(x))*(y - mean(y)))

beta1 = ssxy/ssx
beta0 = mean(y) - beta1*mean(x)
mse = sum(fit$residuals^2)/(n-2)
se.beta1 = sqrt(mse/ssx)
t.beta1 = beta1/se.beta1
p.beta1 = 2*pt(-abs(t.beta1),df=n-2)

# We get the same values calculated by lm() 

summary(fit)
c(beta0,beta1,se.beta1,t.beta1,p.beta1)

# can get also get beta1 this way

cor(x,y)*sqrt(ssy/ssx)

##############################
### multiple linear regression
##############################

fit = lm(Sales ~ TV+Radio+Newspaper)

y = Sales
n = length(y)
x = cbind(rep(1,n),TV,Radio,Newspaper)

### We get directly the coefficient and covariance matrices 

beta.matrix = solve(t(x)%*%x)%*%(t(x)%*%y)
mse = sum(fit$residuals^2)/(n-4)
v.matrix = mse*solve(t(x)%*%x)

# We get the same values calculated by lm() 

summary(fit)
cbind(beta.matrix, sqrt(diag(v.matrix)))

# We can extract the T statistic for Newspaper, and do a t-test 
# against Ho : beta4 = 0   

t.beta4 = beta.matrix[4]/sqrt(v.matrix[4,4])
2*pt(-abs(t.beta4),df=n-4)

###################################
### Goodness of fit measures
###################################


### We want RSS, TSS, Rsq, adjRsq, Fstat

# we can get this from the fitted values

fit = lm(Sales ~ TV)

# what can we extract from 'fit'?

names(fit)
names(summary(fit))

cf = fit$coefficients
cf

fv = fit$fitted.values
res = fit$residuals

# the following three columns each contain the fitted values

cbind(fv, cf[1] + TV*cf[2], Sales - res)
cor(cbind(fv, cf[1] + TV*cf[2], Sales - res))

# sums of squares

n = length(TV)
dft = n-1
dfq = 1
dfr = dft - dfq

rss = sum(res^2)
tss = sum((Sales-mean(Sales))^2)
qss = tss - rss

rms = rss/dfr
tms = tss/dft
qms = qss/dfq

# Rsq

Rsq = 1 - rss/tss

# adjRsq

adjRsq = 1 - rms/tms 

# Fstat and p-value

Fstat = qms/rms
pv = 1 - pf(Fstat,dfq,dfr)

# gather all quantities

sumdf = data.frame(qss,rss,tss,dfq,dfr,dft,qms,rms,tms,Rsq,adjRsq,Fstat,pv)
sumv = c(qss,rss,tss,dfq,dfr,dft,qms,rms,tms,Rsq,adjRsq,Fstat,pv)
sumdf
sumv
class(sumdf)
class(sumv)
names(sumv) = names(sumdf)
sumv
class(sumv)
rm(sumdf)

# compare numbers

anova(fit)
sumv

summary(fit)$r.squared
summary(fit)$adj.r.squared
summary(fit)$fstatistic
sumv

### Create a function that accepts a lm object and outputs the summary vector

compact.lm.summary = function(fit) {

  # sums of squares (We can get these quatities from various summary objects

  dfq = summary(fit)$f[2]
  dfr = summary(fit)$f[3]
  dft = dfq+dfr
 
  qss = sum((fit$fitted.values - mean(fit$fitted.values))^2)
  rss = sum(fit$residuals^2)
  tss = qss + rss
  
  qms = qss/dfq
  rms = rss/dfr
  tms = tss/dft
  
  Rsq = summary(fit)$r.squared
  adjRsq = summary(fit)$adj.r.squared
  Fstat = summary(fit)$fstatistic[1]
  pv = 1 - pf(Fstat,dfq,dfr)
  
  sumdf = data.frame(qss,rss,tss,dfq,dfr,dft,qms,rms,tms,Rsq,adjRsq,Fstat,pv)
  sumv = c(qss,rss,tss,dfq,dfr,dft,qms,rms,tms,Rsq,adjRsq,Fstat,pv)
  names(sumv) = names(sumdf)
 
  return(sumv)
  
}  

sumv2 = compact.lm.summary(fit)

### There are ways of testing equality of more complex objects

# nearly equal (within tolerance)
all.equal(sumv, sumv2)
# exactly equal 
identical(sumv,sumv2)
# The issue is numerical precision
identical(round(sumv,7),round(sumv2,7))
# Let's have a look
cbind(sumv, sumv2)
  
### We can now systematically compare all models

lm(Sales ~ TV+Radio+Newspaper)

formula.list = list(
  Sales ~ TV,
  Sales ~ Radio,
  Sales ~ Newspaper,
  Sales ~ TV+Radio,
  Sales ~ TV+Newspaper,
  Sales ~ Radio+Newspaper,
  Sales ~ TV+Radio+Newspaper
)

class(formula.list[[1]])
lm(formula.list[[1]])
lm(Sales ~ TV)

# note that there is some flexibility

string1 = 'Sales ~ TV'
formula1 = Sales ~ TV
class(string1)
class(formula1)
lm(string1)
lm(formula1)

# construct model fit table

fit.table = NULL
for (i in 1:7)  fit.table = rbind(fit.table, compact.lm.summary(lm(formula.list[[i]]))) 
row.names(fit.table) = formula.list  

fit = lm(formula.list[[7]])
summary(fit)

### do F-test to compare model 4 to model 7 (ie. does adding Newspaper help?)

F74 = (fit.table[4,2]-fit.table[7,2])/(fit.table[7,2]/196)  
1 - pf(F74,1,196)

### STOP