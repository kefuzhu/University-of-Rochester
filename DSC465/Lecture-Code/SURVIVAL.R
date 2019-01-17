library(MASS)
library(survival)
library(muhaz)

#### Melanoma

help(Melanoma)

Melanoma2 = subset(Melanoma, status!=3)

# we need to know whether observations are censored or not

par(mfrow=c(1,2))
plot(Melanoma2$thickness,Melanoma2$time,col=1+Melanoma2$status)
legend('topright',legend=c("Alive","Dead from melanoma"),col=c(3,2),pch=1,cex=0.75)
lines(smooth.spline(Melanoma2$thickness,Melanoma2$time,df=4),col='blue')
boxplot(time ~ thickness > 10,data=Melanoma2)
 
# We will discuss splies in future lectures

####
#### survival times and events
####

# Simple KM curve

## estimated KM curve

z = c(1.5,2,2,4)
ev = c(1,1,0,1)
par(mfrow=c(1,2))
plot(survfit(Surv(z,ev)~1))

zz = c(0,1.5,2,4)
sv = c(1,0.75,1/2,0)

points(zz,sv,col='red')

#################
################# Cox PH model
#################

# exponential distribution has constant hazard function

par(mfrow=c(1,2))
z1 = rexp(1000)
ev1 = rep(1,1000)
junk = plot(survfit(Surv(z1,ev1)~1),fun="cumhaz")
abline(0,1,col='green')

z2 = rexp(1000,rate=2)
ev2 = rep(1,1000)
junk = plot(survfit(Surv(z2,ev2)~1),fun="cumhaz")
abline(0,2,col='green')

z = c(z1,z2)
ev = c(ev1,ev2)
gr = as.factor(rep(c(1,2),each=1000))

### the hazards ratio is 2 in this example

fit = coxph(Surv(z,ev) ~ gr)
summary(fit)$coef
               
#########################
######################### Set up Melanoma 
#########################

head(Melanoma2)
Melanoma3 = data.frame(Melanoma2, ev = 1*(Melanoma2$status==1))
head(Melanoma3)

#### Use KM to investigate difference by sex

### sex 1 = male, 0 = female

par(mfrow=c(2,2),oma=c(1,1,1,1),mar=c(4,4,2,2))
fit = survfit(Surv(time,ev)~as.factor(sex),data=Melanoma3)
plot(fit,col=c('red','green'),xlab='days',ylab='Survival')
legend('bottomleft',legend = c("Female","Male"),col=c('red','green'),lty=1,cex=0.5)

### check which sex has longer survival times

boxplot(time~sex,data=Melanoma3)

plot(fit,col=c('red','green'),xlab='days',ylab='Survival',conf.int = T)
legend('bottomleft',legend = c("Female","Male"),col=c('red','green'),lty=1,cex=0.5)

### Chi Sq test for difference in KM curves 

chisq = survdiff(Surv(time,ev)~as.factor(sex),data=Melanoma3)$chisq
pv = 1-pchisq(chisq,1)
title(paste('P = ',signif(pv,3)),cex.main=0.75)

###
### Use Cox PH to build multiple regression models
###

### sex alone

fit = coxph(Surv(time,ev) ~ sex, data=Melanoma3)
summary(fit)$coef

### sex and thickness

fit = coxph(Surv(time,ev) ~ sex+thickness, data=Melanoma3)
summary(fit)$coef

### all main effects and 2nd order interactios

fit = coxph(Surv(time,ev) ~ (sex+thickness+age+ulcer)^2, data=Melanoma3)
summary(fit)$coef

### AIC model selection keeps main effects but not interactions (we will discuss AIC in future lectures)

fitaic = step(fit,k = log(dim(Melanoma3)[1]))
summary(fitaic)$coef

