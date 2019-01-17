
############################# EXAMPLE 1

auto = read.table("Auto.csv",sep=',',header=T, quote="", stringsAsFactors = F)
auto = na.omit(auto)
auto = auto[sort.list(auto$displacement),]

### variable order polynomial function

my.lm = function(x,y,pd=1,xl="X",yl="Y") {
  
  if (pd ==1) {
    fit = lm(y~x)
  } else
  {
    fit = lm(y~poly(x,pd))
  }
  plot(x,y,xlab=xl,ylab=yl)
  ind = sort.list(x)
  lines(x[ind],fit$fitted.values[ind],col='green',lwd=2)
  plot(fit$fitted.values,fit$residuals,xlab="Fitted Values",ylab="Residuals")
  abline(h=0,col='green',lwd=2)
  return(fit)
}

### examine log transformation

par(mfrow=c(2,2))
my.lm(auto$horsepower, auto$mpg)
auto2 = data.frame(auto,log10(auto$mpg))
names(auto2) = c(names(auto),'logmpg')
my.lm(auto2$horsepower, auto2$logmpg)


###### polynomial regression

par(mfrow=c(2,2))

my.lm(auto$horsepower, auto$mpg,2,"HP","MPG")
my.lm(auto2$horsepower, auto2$logmpg,2,"HP","MPG")

# Seems to work well

############################# EXAMPLE 2

### Encephalization quotient
### Snells equation W = K (BW)^r

library(MASS)

head(mammals)

par(mfrow=c(1,2))
boxplot(log10(mammals$body))

### data is approximately linear on a double logarithmic scale

plot(mammals,log='xy')

### what is r?

lm(log(brain) ~ log(body), data = mammals)
lm(log(brain) ~ log(body), data = mammals, subset = (log10(body) > 2))
lm(log(brain) ~ log(body), data = mammals, subset = (log10(body) < -1))

############################# EXAMPLE 3

#### Forbes' Data on Boiling Points in the Alps

head(forbes)

par(mfrow=c(1,2))
fit1 = my.lm(forbes$pres,forbes$bp)

forbes2 = forbes[-which(fit1$residual < -1),]

par(mfrow=c(3,2))
fit1 = my.lm(forbes2$pres,forbes2$bp)
fit1 = my.lm(forbes2$pres,forbes2$bp,1)
fit1 = my.lm(log(forbes2$pres),forbes2$bp,2)

############################# EXAMPLE 4

###
### advertising data
###

### Read .csv file (comma delimited)

tab = read.csv("Advertising.csv")

#Create new variables

TV = tab$TV
Sales = tab$Sales
Radio = tab$Radio
Newspaper = tab$Newspaper

plot(TV,Sales,col='red',xlim=c(0,310))
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)

### residual plot

fit = lm(Sales ~ TV)
plot(TV, fit$residuals)
abline(h=0)

# polynomial regression with log transform of response

par(mfrow=c(3,2))
my.lm(TV,log(Sales))
my.lm(TV,log(Sales),2)
my.lm(TV,log(Sales),3)

# polynomial regression with log transform of response and predictor

par(mfrow=c(3,2))
my.lm(log(TV),log(Sales))
my.lm(log(TV),log(Sales),2)
my.lm(log(TV),log(Sales),3)

### STOP





