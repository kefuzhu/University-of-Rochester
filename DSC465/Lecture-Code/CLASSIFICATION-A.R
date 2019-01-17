

##################
# Bayes classifier
##################

mu1 = 10
var1 = 1.2
pi1 = 0.5
mu2 = 15
var2 = 3.7
pi2 = 0.5


xgrid = seq(0,25,0.1)

par(mfrow=c(2,1))
plot(xgrid,dnorm(xgrid,mean=mu1,sd=sqrt(var1)),col='green',type='l')
lines(xgrid,dnorm(xgrid,mean=mu2,sd=sqrt(var2)),col='red')


f0 = function(x,mu1,var1,mu2,var2,pi1,pi2) {
  (pi2/pi1)*dnorm(x,mean=mu2,sd=sqrt(var2))/dnorm(x,mean=mu1,sd=sqrt(var1))
}

plot(xgrid,log(f0(xgrid,mu1,var1,mu2,var2,pi1,pi2)),type='l')
abline(h=0)

sort.list(log(f0(xgrid,mu1,var1,mu2,var2,pi1,pi2))^2)[1:10]

# boundaries at indices 121, 33

par(mfrow=c(1,1))
plot(xgrid,dnorm(xgrid,mean=mu1,sd=sqrt(var1)),col='green',type='l')
lines(xgrid,dnorm(xgrid,mean=mu2,sd=sqrt(var2)),col='red')
abline(v=xgrid[33],lty=2)
abline(v=xgrid[121],lty=2)


###############################
# KNN, with Fisher's iris data
###############################

library(class)

iris.col <- c(rep(2,50), rep(3,50), rep(4,50))
pairs(iris[,1:4],col=iris.col,pch=20)

par(mfrow=c(1,1))

errv0 = rep(0,40) 
klist = c(1:40)
errv = rep(NA, 40)
for (iii in 1:500) {
  for (i in 1:40) {
    train <- rbind(iris3[1:25,,1], iris3[1:25,,2], iris3[1:25,,3])
    test <- rbind(iris3[26:50,,1], iris3[26:50,,2], iris3[26:50,,3])
    cl <- factor(c(rep("s",25), rep("c",25), rep("v",25)))
    pr = knn(train, test, cl, k = klist[i], prob=F)
    errv[i] = mean(cl!=pr)
  }
  errv0 = errv0 + errv
}
errv0 = errv0 / 500

plot(klist,errv0,type='b', ylab='Classification Error',xlab='K')


