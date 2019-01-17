
### ANOVA with 4 treatments

Brand1 = c(99.34, 101.79, 103.52, 103.06, 101.45)
Brand2 = c(95.68,  94.57,  97.64, 102.93)
Brand3 = c(95.11, 88.60, 93.70, 87.62)
Brand4 = c(82.00, 87.59, 89.77, 85.70)

### Model form

y = c(Brand1, Brand2, Brand3, Brand4)
x = factor(c(rep(1,5),rep(2,4),rep(3,4),rep(4,4)))

### Test for equality of variances 

bartlett.test(y~x)
pval = bartlett.test(y~x)$p.value


boxplot(y~x, xlab='Brand',ylab='Some Measure of Quality')
title(paste("P = ",signif(pval,3)))

fit = aov(y~x)
summary(fit)
TukeyHSD(fit)

###
### We can conclude 1 > 3; 1 > 4; 2 > 4 at a significance level of 5%. 
### The best treatment is either 1 or 2. 
###
### Remember the P-value > 0.05 is not evidence that null hypothesis is true. 
###
