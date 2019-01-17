
### START

### R script for ISLR 3.1-3.2

setwd("/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE")

### Read .csv file (comma delimited)

tab = read.csv("Advertising.csv")

#Create new variables

TV = tab$TV
Sales = tab$Sales
Radio = tab$Radio
Newspaper = tab$Newspaper

### This gives Figure 2.1 of ISLR

par(mfrow=c(1,3))

plot(TV,Sales,col='red')
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)

plot(Radio,Sales,col='red')
cf = lm(Sales ~ Radio)$coef
abline(cf,col='blue',lwd=2)

plot(Newspaper,Sales,col='red')
cf = lm(Sales ~ Newspaper)$coef
abline(cf,col='blue',lwd=2)

### This gives Figure 2.1 of ISLR with the slope added as text

par(mfrow=c(1,3))

plot(TV,Sales,col='red')
cf = lm(Sales ~ TV)$coef
abline(cf,col='blue',lwd=2)
legend('bottomright',paste('Slope =',signif(cf[2],4)),bty ='n')

plot(Radio,Sales,col='red')
cf = lm(Sales ~ Radio)$coef
abline(cf,col='blue',lwd=2)
legend('bottomright',paste('Slope =',signif(cf[2],4)),bty ='n')

plot(Newspaper,Sales,col='red')
cf = lm(Sales ~ Newspaper)$coef
abline(cf,col='blue',lwd=2)
legend('bottomright',paste('Slope =',signif(cf[2],4)),bty ='n')

### Look at the numerical fits

summary(lm(Sales ~ TV))$coef
summary(lm(Sales ~ Radio))$coef
summary(lm(Sales ~ Newspaper))$coef

### Multiple fit using all 3 predictors

summary(lm(Sales ~ TV+Radio+Newspaper))$coef

### Look at correlation of the predictors (ie. look for collinearity)

cor(cbind(TV, Radio, Newspaper))

### Why is Newspaper alone a significant predictor, but not when included 
### in the multiple regression fit?

par(mfrow=c(1,1))
plot(Radio,Newspaper,col=1+(Sales > median(Sales)))
abline(h=quantile(Newspaper,0.75),lty=2)
abline(v=quantile(Radio,0.75),lty=2)

### Large newspaper budgets imply large radio budgets, which imply high sales.

### STOP

