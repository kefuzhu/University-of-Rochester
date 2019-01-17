

### START

#### Cross Validation 

library(ISLR)
library(ROCR)
library(splines)

#### Complex formula intended to predict S&P 500 stock index

myFormula = Direction == 'Up'~Lag1 + Lag2 + Lag3 + Lag4 + Lag5

fit = glm(myFormula,data=Weekly, family='binomial')
pr = predict(fit)

par(mfrow=c(2,2))

### draw AUC

boxplot(pr ~ Weekly$Direction)
title(paste('P = ', signif(wilcox.test(pr ~ Weekly$Direction)$p.value,3)))
pred <- prediction(pr,  Weekly$Direction  == "Up")
perf <- performance(pred,"tpr","fpr")
plot(perf)
perf <- performance(pred,"auc")
title(paste('AUC = ', signif(as.numeric(perf@y.values),3)))
abline(a=0,b=1,col='green')

### looks pretty good

### remove one observation

fit = glm(myFormula,data=Weekly[-1,], family='binomial')
fit$coef
fit = glm(myFormula,data=Weekly[-2,], family='binomial')
fit$coef

### make prediction for test observation

new.pred = predict(fit, newdata = Weekly)[1]
new.pred

### do this for each observation

n = dim(Weekly)[1]
new.pred = numeric(n)
for (i in 1:n) {
  fit = glm(myFormula, data=Weekly[-i,],family='binomial')
  new.pred[i] = predict(fit, newdata = Weekly)[i]
}

### Redo ROC analysis

pr = new.pred
boxplot(pr ~ Weekly$Direction)
title(paste('P = ', signif(wilcox.test(pr ~ Weekly$Direction)$p.value,3)))
pred <- prediction( new.pred,  Weekly$Direction == "Up")
perf <- performance(pred,"tpr","fpr")
plot(perf)
perf <- performance(pred,"auc")
title(paste('AUC = ', signif(as.numeric(perf@y.values),3)))
abline(a=0,b=1,col='green')

### predictive ability of model not supported by cross-validation


####
#### CV and model selection
####

#### variable selection 

library(boot)

  ### Read .csv file (comma delimited)

  tab = read.csv("Advertising.csv")
  
  f1 = Sales ~ TV + Radio
  f2 = Sales ~ TV + Radio + Newspaper
  
  fit1 = glm(f1,data = tab)
  fit2 = glm(f2,data = tab)
  
  aov(fit1)
  aov(fit2)
  cv.glm(tab,fit1)$delta
  cv.glm(tab,fit2)$delta
  sqrt(cv.glm(tab,fit1)$delta)
  sqrt(cv.glm(tab,fit2)$delta)
  
# both fitted MSE and CV error give similar conclusions.    
  
#### determine degree of polynomal regression fit 
  
  par(mfrow=c(1,2))
  
  set.seed(1)

  # simulate 3rd order polynomial model
    
  f0 = function(x) {1 + 2*x + 0.1*x^2 - 0.05*x^3}
  x = sort(rep(seq(1,25,1),1))
  y = f0(x) + rnorm(length(x),sd=25.75)
  
  plot(x,f0(x),ylim=range(y),type='l')
  points(x,y)
  
  yx = data.frame(y,x)
  
  # calculate both MSE and CV error
  
  msev = numeric(20)
  msecv = numeric(20)
  for (i in 1:20) {
    fit = glm(y~poly(x,i), data = yx)
    msev[i] = summary(aov(fit))[[1]][2,3]
    msecv[i] = cv.glm(yx,fit)$delta[1]
  }
  
  summary(fit)
  msev
  msecv
  
  matplot(cbind(msev,msecv),log='y',type='b')
  legend('topright',c('Fit','CV'),pch=c('1','2'),bg='transparent')
  
  # CV error does not suffer from 'over-fitting
  
  
#### CV is sometimes an option  
  
  library(MASS)
  
  lda.fit = lda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris)
  pr = predict(lda.fit)
  confusion.table = table(pr$class, iris$Species)
  confusion.table
  round(sum(diag(confusion.table))/sum(confusion.table),2)
  
  lda.fit = lda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris, CV=T)
  confusion.table = table(lda.fit$class, iris$Species)
  confusion.table
  round(sum(diag(confusion.table))/sum(confusion.table),2)
  
  qda.fit = qda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris)
  pr = predict(qda.fit)
  confusion.table = table(pr$class, iris$Species)
  confusion.table
  round(sum(diag(confusion.table))/sum(confusion.table),2)
  
  qda.fit = qda(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,  data = iris, CV=T)
  confusion.table = table(qda.fit$class, iris$Species)
  confusion.table
  round(sum(diag(confusion.table))/sum(confusion.table),2)

#####  
##### Bootstrap  
#####
  
  library(boot)
  
  set.seed(1) 
  
  x = rnorm(100)
  y = (x + rnorm(100))/sqrt(2)
  
  xy = data.frame(x,y)
  
  corf <- function(d,ind) {cor(d$x[ind],d$y[ind])}
  boot.obj = boot(xy, statistic = corf, R = 999, stype='i')
  boot.obj
  
  cor.test.obj = cor.test(x,y)
  cor.test.obj
  cor.test.obj$conf.int
  
  ### Standard error
  
  diff(cor.test.obj$conf.int)/4
  
  ### Bootstrap standard error/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE/UPLOAD/Auto.csv

  sd(boot.obj$t)
  
  
### STOP
