
### START


##################################################
### The Nadaraya–Watson kernel regression estimate
##################################################

f0 = function(x) {1 - exp(-0.75*x)}

x = seq(0,8,0.1)

plot(x,f0(x),type='l')


y = f0(x)+rnorm(length(x),sd=0.1)

band.list = c(0.125,0.25,0.5,1,2,4,8,16)

par(mfrow=c(2,4))
for (bnd in band.list) {
  plot(x,y,pch=20)
  lines(x,f0(x),col='blue',lwd=2)
  lines(ksmooth(x,y,band=bnd,kernel='box'),col='red',lwd=2)
  title(paste('Bandwidth =',bnd))
}

### note kernel quartiles are +/- 0.25*bandwidth

#################################################
#################################################
#################################################

### R script for ISLR 4.3

library(ISLR)

head(Default)

####################################
### Logistic Regression Section 4.3
####################################

### Model Default ~ Balance

# plot

plot(Default$balance, Default$default)

# default is categorical, but can still be plotted
# Plot doesn't say much

par(mfrow=c(2,2))
plot(Default$balance, Default$default, pch=3)
plot(Default$balance, Default$default, pch='+')
plot(Default$balance, Default$default, pch='W')
plot(Default$balance, Default$default, pch=17)

### ksmooth is a good way to see the shape of the response curve

par(mfrow=c(1,1))
plot(Default$balance, (Default$default=='Yes'), pch=3)
lines(ksmooth(Default$balance, (Default$default=='Yes'),band=200),col='red')

### to do logistic regression

fit = glm(default=='Yes' ~ balance,data = Default, family = binomial)
summary(fit)
points(Default$balance, fit$fitted.values, col='green',pch=20)

### be careful of smoother bias
### rule of thumb: a smoothed function should exhibit variation over most of the range

lines(ksmooth(Default$balance, (Default$default=='Yes'),band=500),col='black')
lines(ksmooth(Default$balance, (Default$default=='Yes'),band=750),col='black')
lines(ksmooth(Default$balance, (Default$default=='Yes'),band=1000),col='black')


### does Income improve the model?

# take a look at predictors (Review Chapter 21 of CSC262 lecture notes)

hist(Default$balance)
hist(Default$income)
plot(Default$balance,Default$income)
cor.test(Default$balance,Default$income,method='pearson')
cor.test(Default$balance,Default$income,method='spearman')
cor.test(Default$balance,Default$income,method='kendall')

### null model is in fit0, reduced model in fit1, full model in fit2

fit0 = glm(default=='Yes' ~ 1,data = Default, family = binomial)
fit1 = glm(default=='Yes' ~ balance,data = Default, family = binomial)
fit2 = glm(default=='Yes' ~ balance + income,data = Default, family = binomial)

summary(fit0)
summary(fit1)
summary(fit2)

### We can get the deviances from the fit, but also from anova()

anova(fit2)

###############################
#########  LDA/QDA Section 4.4
###############################

library(MASS)

boxplot(Sepal.Length ~ Species, data = iris)

lda.fit = lda(Species ~ Sepal.Length, data = iris)
plot(lda.fit)
pr = predict(lda.fit)
confusion.table = table(pr$class, iris$Species)
confusion.table
round(sum(diag(confusion.table))/sum(confusion.table),2)

### try QDA

qda.fit = qda(Species ~ Sepal.Length, data = iris)
pr = predict(qda.fit)
confusion.table = table(pr$class, iris$Species)
confusion.table
round(sum(diag(confusion.table))/sum(confusion.table),2)

### introduce two predictors

lda.fit = lda(Species ~ Sepal.Length + Sepal.Width, data = iris)
plot(lda.fit)
pr = predict(lda.fit)
confusion.table = table(pr$class, iris$Species)
confusion.table
round(sum(diag(confusion.table))/sum(confusion.table),2)

my.pch = rep(c(1,2,3),each=50)
plot(iris$Sepal.Length, iris$Sepal.Width, pch = my.pch, col=1+(pr$class!=iris$Species))
table(pr$class, iris$Species)


### introduce all parameters


lda.fit = lda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris)
pr = predict(lda.fit)
confusion.table = table(pr$class, iris$Species)
confusion.table
round(sum(diag(confusion.table))/sum(confusion.table),2)

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4], pch = my.pch, col=1+(pr$class!=iris$Species))
table(pr$class, iris$Species)

### QDA

qda.fit = qda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris)
pr = predict(qda.fit)
confusion.table = table(pr$class, iris$Species)
confusion.table
round(sum(diag(confusion.table))/sum(confusion.table),2)

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4], pch = my.pch, col=1+(pr$class!=iris$Species))
table(pr$class, iris$Species)

### we can also assess the level of certainty of the prediction

max.posterior = apply(pr$posterior,1,max)
boxplot(max.posterior)

### the less confident predictions are largely near the boundaries between classes

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4], pch = my.pch, col=1+(max.posterior < 0.95))
table(pr$class, iris$Species)

########################################
####### ROC and Precision/Recall Curves
########################################

# recall logistic regression model

fit2 = glm(default=='Yes' ~ balance + income,data = Default, family = binomial)

pr = fit2$fitted.values
boxplot(pr~Default$default)
title('Estimated probability of default')

# we might make a decision based on a threshold

pred.default = pr > 0.5
confusion.table = table(pred.default, Default$default)
confusion.table

sens1 = confusion.table[2,2]/sum(confusion.table[,2])
spec1 = confusion.table[1,1]/sum(confusion.table[,1])
ppv1 = confusion.table[2,2]/sum(confusion.table[2,])
npv1 = confusion.table[1,1]/sum(confusion.table[1,])
c(sens1,spec1,ppv1,npv1)

# or 

pred.default = pr > 0.25
confusion.table = table(pred.default, Default$default)
confusion.table

sens2 = confusion.table[2,2]/sum(confusion.table[,2])
spec2 = confusion.table[1,1]/sum(confusion.table[,1])
ppv2 = confusion.table[2,2]/sum(confusion.table[2,])
npv2 = confusion.table[1,1]/sum(confusion.table[1,])
c(sens2,spec2,ppv2,npv2)

#### ROC and PR graphs

# We have TP,FP,TN,FN

# SENSITIVITY = TPR = TP/(TP+FN)
# SPECIFICITY = TNR = TN/(FP+TN)

# RECALL = SENSITIVITY 
# PRECISION = PPV = TP/(TP+FP)

library(ROCR)

pred <- prediction( pr, Default$default )

par(mfrow=c(1,2))

### ROC curve

perf <- performance(pred,"tpr","fpr")
plot(perf)
points(1-spec1,sens1,col='red',pch=20)
points(1-spec2,sens2,col='red',pch=20)

### Precision/Recall curve

perf1 <- performance(pred, "prec", "rec")
plot(perf1)
points(sens1,ppv1,col='red',pch=20)     
points(sens2,ppv2,col='red',pch=20)     

### STOP


