
############################# EXAMPLE 1

library(MASS)

#### step functions

head(Boston)
help(Boston)

plot(Boston$nox, Boston$medv)

### identify range 

range(Boston$nox)

### create cutpoints 

br = seq(0.3,0.9,by=0.1)
br
nox.steps = cut(Boston$nox,br)

new.frame = data.frame(nox.steps,medv = Boston$medv)
fit = lm(medv~nox.steps, data=new.frame)

#### construct predictor data.frame

nox.rng = seq(0.3,0.9,by = 0.001)
predict.frame = data.frame(nox.rng, nox.steps=cut(nox.rng,br))
pr = predict(fit,newdata=predict.frame)

#### various ways to represent fitted curve, some better than others

par(mfrow=c(2,2))
plot(Boston$nox, Boston$medv)
points(Boston$nox, fit$fitted.value,col='green')
plot(Boston$nox, Boston$medv)
lines(Boston$nox, fit$fitted.value,col='green')
plot(Boston$nox, Boston$medv)
lines(nox.rng, pr,col='green',lwd=3,pty='s')

############################# EXAMPLE 2

#### splines as basis functions

library(splines)

x = seq(1,100,by=1)

x.cubic.spline = ((x - 50)^3)*(x > 50)
x.1 = (x-25)*(x>25)
x.2 = (x-75)*(x>75)

### examine basis functions

par(mfrow=c(2,2))
plot(x, x.cubic.spline)
plot(x, x.1)
plot(x, x.2)

### simulate test model 

y = rnorm(100)+(x-50)^2/500
plot(x,y)

#### PW linear spline

bs1 = bs(x,knots = c(25,75),degree=1)
matplot(x,bs1)

#### fit models

fit1 = lm(y ~ x+x.1+x.2)
fit2 = lm(y ~ bs1)
summary(fit1)
summary(fit2)

par(mfrow=c(1,2))

plot(x,y)
lines(x,predict(fit1),col='red',lwd=5)
lines(x,predict(fit2),col='green',lwd=2)
plot(predict(fit1),predict(fit2))
abline(0,1,col='red')

#### Cubic spline


par(mfrow=c(1,1))
bs2 = bs(x,knots = c(50))
matplot(x,bs2)

fit1 = lm(y ~ poly(x,3)+x.cubic.spline)
fit2 = lm(y ~ bs2)
summary(fit1)
summary(fit2)

par(mfrow=c(1,2))
plot(x,y)
lines(x,predict(fit1),col='red',lwd=5)
lines(x,predict(fit2),col='green',lwd=2)
plot(predict(fit1),predict(fit2))
abline(0,1,col='red')

############################# EXAMPLE 3

library(ISLR)

### Weekly S&P Stock Market Data

help(Weekly)

year = Weekly$Year
volume = Weekly$Volume

par(mfrow=c(2,1))
plot(year, volume)
logVolume = log10(volume)
plot(year,logVolume)

# We need the range 

rng = range(year)

br = seq(1985,2015,by=2.5)
br
year.steps = cut(year,br)
new.frame = data.frame(year,year.steps,logVolume)

# fit model with step function

fit = lm(logVolume~year.steps, data=new.frame)
year.rng = seq(1989,2010,by = 0.01)
predict.frame = data.frame(year.rng, year.steps=cut(year.rng,br))
pr = predict(fit,newdata=predict.frame)
par(mfrow=c(1,1))
plot(year, logVolume)
lines(year.rng, pr,col='green',lwd=3,pty='s')

# now fit a linear spline

kn = c(1994, 2002,2004,2008)
xb = bs(year,knot=kn, degree=1)
fit = lm(logVolume ~ xb)
plot(year, logVolume)
lines(year,fit$fitted.values,col='green',lwd=3)


### smoothing splines

par(mfrow=c(1,1))
fit = smooth.spline(year,logVolume)
plot(year,logVolume)
lines(predict(fit),col='green',lwd=3)
fit$lambda
fit$df

# use 10 degrees of freedom (df)

fit2 = smooth.spline(year,logVolume,df=10)
lines(predict(fit2),col='red',lwd=3)


############################# EXAMPLE 4

### return to advertising data, fit a B-spline

tab = read.csv("Advertising.csv")

TV = tab$TV
Sales = tab$Sales

TV.grid = seq(min(TV),max(TV),by=1)
plot(TV, log(Sales))
fit = lm(log(Sales) ~ bs(TV,knots=c(25),degree=3))
lines(TV.grid, predict(fit,newdata=list(TV=TV.grid)),col='green',lwd=3)

############################# EXAMPLE 5

### LOESS Boston Housing 

par(mfrow=c(1,1))

head(Boston)
help(Boston)

plot(Boston$nox, Boston$medv,pch=20)
fit1 = loess(medv ~ nox, data=Boston,span=0.75,degree=2)
fit2 = loess(medv ~ nox, data=Boston,span=0.25,degree=2)
fit3 = loess(medv ~ nox, data=Boston,span=0.5,degree=1)
fit4 = loess(medv ~ nox, data=Boston,span=0.25,degree=1)

nox.rng = seq(0.3,0.9,by = 0.001)

lines(nox.rng,predict(fit1,nox.rng),col='green',lwd=3)
lines(nox.rng,predict(fit2,nox.rng),col='red',lwd=3)
lines(nox.rng,predict(fit3,nox.rng),col='blue',lwd=3)
lines(nox.rng,predict(fit4,nox.rng),col='orange',lwd=3)
legend('topright',legend=c("sp = 0.75, deg = 2", "sp = 0.25, deg = 2","sp = 0.75, deg = 1","sp = 0.25, deg = 1"),
       lty=1,col=c('green','red','blue','orange'))


############################# EXAMPLE 6

### LOESS Advertising Data 

TV.grid = seq(min(TV),max(TV),by=1)
plot(TV, log(Sales))
fit = loess(log(Sales) ~ TV,span=0.25)
lines(TV.grid,predict(fit,TV.grid),col='green',lwd=3)
fit = loess(log(Sales) ~ TV,span=0.5)
lines(TV.grid,predict(fit,TV.grid),col='red',lwd=3)
fit = loess(log(Sales) ~ TV,span=0.75)
lines(TV.grid,predict(fit,TV.grid),col='orange',lwd=3)
legend('bottomright',legend=c("sp = 0.25", "sp = 0.5","sp = 0.75"),
       lty=1,col=c('green','red','orange'))


############################# EXAMPLE 7

### Generalized Additive Models GAM - Advertising Data
### Splines with standard errors

library(gamm4)
library(ISLR)
library(MASS)
library(splines)


tab = read.csv("Advertising.csv")

# Create new variables

TV = tab$TV
Sales = tab$Sales


plot(TV, log(Sales),pch=20)
fit.gam = gam(log(Sales) ~ s(TV), data=tab)

TV.grid = seq(min(TV),max(TV),by=1)
pr = predict(fit.gam,list(TV=TV.grid))
lines(TV.grid,pr,col='green',lwd=3)

### We can construct confidence bands

pr = predict(fit.gam,list(TV=TV.grid),se=T)
names(pr)

plot(TV, log(Sales),pch=20)
lines(TV.grid,pr$fit,col='green',lwd=3)
lines(TV.grid,pr$fit-2*pr$se.fit,col='green',lwd=3,lty=3)
lines(TV.grid,pr$fit+2*pr$se.fit,col='green',lwd=3,lty=3)

### STOP









