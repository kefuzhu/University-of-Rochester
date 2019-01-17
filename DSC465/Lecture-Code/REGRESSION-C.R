
### START


setwd("/home/anthony/USERA/CSC 265 SPRING 2018/SOFTWARE")

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

# log tranform of response

par(mfrow=c(2,1))

plot(TV, log(Sales))
fit = lm(log(Sales) ~ TV)
plot(TV, fit$residuals)
abline(h=0)

# polynomial regression


par(mfrow=c(3,2))

fit1 = lm(log(Sales) ~ TV)
plot(TV, log(Sales))
points(TV,predict(fit1),col='green',pch=20)
plot(TV, fit1$residuals)
abline(h=0)

fit2 = lm(log(Sales) ~ poly(TV,2))
plot(TV, log(Sales))
points(TV,predict(fit2),col='green',pch=20)
plot(TV, fit2$residuals)
abline(h=0)

fit3 = lm(log(Sales) ~ poly(TV,3))
plot(TV, log(Sales))
points(TV,predict(fit3),col='green',pch=20)
plot(TV, fit3$residuals)
abline(h=0)

summary(fit1)$coef
summary(fit2)$coef
summary(fit3)$coef





