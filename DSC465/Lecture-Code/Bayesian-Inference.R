

####### 
####### Binomial parameters with beta priors  
#######

pgrid = seq(0,1,by = 0.01)

### uniform prior

alpha = 1
beta = 1
plot(pgrid,dbeta(pgrid,alpha,beta),type='l')

### gradually more informative

par(mfrow=c(1,2))

alpha = 1
beta = 1
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',ylim=c(0,10))
abline(v=0.5,col='green')
for (n in seq(5,50,by=5)) {lines(pgrid,dbeta(pgrid,n*alpha,n*beta),type='l')}


alpha = 1
beta = 3
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',ylim=c(0,20))
abline(v=0.25,col='green')
for (n in seq(5,50,by=5)) {lines(pgrid,dbeta(pgrid,n*alpha,n*beta),type='l')}

#### a variety of shapes

par(mfrow=c(2,2))

alpha = 0.2
beta = 10
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',xlab=expression(italic(x)),ylab='density')
title(bquote(alpha == .(alpha) ~ ', ' ~ beta == .(beta)))

alpha = 0.5
beta = 0.5
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',xlab=expression(italic(x)),ylab='density')
title(bquote(alpha == .(alpha) ~ ', ' ~ beta == .(beta)))

alpha = 0.5
beta = 0.25
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',xlab=expression(italic(x)),ylab='density')
title(bquote(alpha == .(alpha) ~ ', ' ~ beta == .(beta)))

alpha = 10
beta = 80
plot(pgrid,dbeta(pgrid,alpha,beta),type='l',xlab=expression(italic(x)),ylab='density')
title(bquote(alpha == .(alpha) ~ ', ' ~ beta == .(beta)))
