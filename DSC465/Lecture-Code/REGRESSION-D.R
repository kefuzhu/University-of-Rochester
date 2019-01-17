
### START

###########################
### Collinearity and VIF
###########################


setwd("/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE")

### Read .csv file (comma delimediited)

tab = read.csv("Credit.csv")

Income = tab$Income
Limit = tab$Limit
Rating = tab$Rating
Cards = tab$Cards
Age = tab$Age
Education = tab$Education
Balance = tab$Balance

### Create Fig 3.6

pairs(cbind(Balance,Age,Cards,Education,Income,Limit,Rating),pch=20,cex=0.5,col='navyblue')

### Model Balance = Age + Rating + Limit

fit = lm(Balance ~ Age + Rating + Limit)
summary(fit)

cor(cbind(Age,Rating,Limit))

vif.age = (1-summary(lm(Age ~ Rating + Limit))$r.squared)^-1
vif.rating = (1-summary(lm(Rating ~ Age + Limit))$r.squared)^-1
vif.limit = (1-summary(lm(Limit ~ Age + Rating))$r.squared)^-1

vif.age
vif.rating
vif.limit

### Drop limit

fit = lm(Balance ~ Age + Rating)
summary(fit)

vif.age = (1-summary(lm(Age ~ Rating))$r.squared)^-1
vif.rating = (1-summary(lm(Rating ~ Age))$r.squared)^-1

vif.age
vif.rating

### Compare coefficient and SE for Rating between the two models.

#############################
### Leverage
#############################


setwd("/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE")

### Read .csv file (comma delimited)

tab = read.csv("Advertising.csv")

#Create new variables

Sales = log10(tab$Sales)
TV = tab$TV
Radio = tab$Radio
Newspaper = tab$Newspaper

### plot data

par(mfrow=c(2,2))

plot(TV,Sales,col='red')
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)

plot(Radio,Sales,col='red')
cf = lm(Sales ~ Radio)$coef
abline(cf,col='blue',lwd=2)

plot(Newspaper,Sales,col='red')
cf = lm(Sales ~ Newspaper)$coef
abline(cf,col='blue',lwd=2)

### calculate leverage statistics 

fit = lm(Sales~TV + Radio + Newspaper)

hii = hatvalues(fit)
sum(hii)

### Show high leverage points

par(mfrow=c(2,2))

plot(TV,Sales,col=3-(hii>0.04))
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)

plot(Radio,Sales,col=3-(hii>0.04))
cf = lm(Sales ~ Radio)$coef
abline(cf,col='blue',lwd=2)

plot(Newspaper,Sales,col=3-(hii>0.04))
cf = lm(Sales ~ Newspaper)$coef
abline(cf,col='blue',lwd=2)

### High leverage points are better seen in predictor x predictor scatter plots.

pairs(cbind(TV,Radio,Newspaper),col=3-(hii>0.04),pch=20)

## or use Cooks's distance

cookd = cooks.distance(fit) 

pairs(cbind(TV,Radio,Newspaper),col=3-(cookd>4/200),pch=20)

par(mfrow=c(1,1))
plot(TV,Sales,col=3-(cookd>4/200))
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)

### STOP
