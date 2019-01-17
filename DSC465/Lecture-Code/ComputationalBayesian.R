
#############
############# Archaeology example
#############

pg = function(u) {0.01 + (0.81-0.01)*(u-11)/(16-11)}
pd = function(u) {0.5 - (0.5-0.05)*(u-11)/(16-11)}

#sample take  u = 13.5 add 20 sample at a time

set.seed(123)

par(mfrow=c(3,3))

ng = 0
nd = 0
n = 0
nstep = 20
for (i in c(1:9)) {
  ng0 = rbinom(1,size=nstep, prob=pg(13.5))
  nd0 = rbinom(1,size=nstep, prob=pd(13.5))

  n = n + nstep
  ng = ng + ng0
  nd = nd + nd0
  
  ugrid = seq(11,16,by = 0.1)
  pg.grid = pg(ugrid)
  pd.grid = pd(ugrid)

  post.density = (pg.grid^ng)*((1-pg.grid)^(n-ng))*(pd.grid^nd)*((1-pd.grid)^(n-nd))
  post.density = post.density/(sum(post.density)*0.1)
  plot(ugrid,post.density,type='l',col='green',xlab="Century")
  title(paste('N = ',n))
  abline(v=13.5)
}
  
######## MCMC

# do ntrace transitions

ntrace = 10000
x = numeric(ntrace)
nstate = length(ugrid)

### simulate sample of size n
n = 100
ng = rbinom(1,size=n, prob=pg(13.5))
nd = rbinom(1,size=n, prob=pd(13.5))

#starting state
x0 = 1
set.seed(234)
for (i in 1:ntrace) {
  
  # simulate transition from Q
  
  if (x0 == 1) {
    x1 = 2
  } else {
    if (x0 == nstate) {
      x1 = nstate-1
    } else {
      x1 = x0 + sample(c(-1,1),1)
    }
  }
  
  # determine Q[j,i]/Q[i,j]
  
  if (x0 ==1 | x0 == nstate) {
    q.ratio = 1/2
  } else {
    if ((x0==2 & x1==1) | (x0==nstate-1 & x1==nstate)) {
      q.ratio = 2
    } else {q.ratio=1}
  }
  
  # determine acceptance probability 
  
  a1 = pg(ugrid[x1])/pg(ugrid[x0]) 
  a2 = (1-pg(ugrid[x1]))/(1-pg(ugrid[x0]))
  a3 = pd(ugrid[x1])/pd(ugrid[x0]) 
  a4 = (1-pd(ugrid[x1]))/(1-pd(ugrid[x0]))
  alpha = min((a1^ng * a2^(n-ng) * a3^nd * a4^(n-nd))*q.ratio,1)
  if (runif(1) <= alpha) {x[i] = x1} else {x[i] = x0}
  
  x0 = x[i]
  
}

#### "burn-in" refers to the initial transitions which bring the process to the vicinity
#### of the steady state distribution

plot(ugrid[x],pch=20)

#### usual practice is to remove 'burn-in'

x = x[1000:ntrace]


# exact density 

post.density = (pg.grid^ng)*((1-pg.grid)^(n-ng))*(pd.grid^nd)*((1-pd.grid)^(n-nd))
post.density = post.density/(sum(post.density)*0.1)

# sample from density

par(mfrow=c(1,1))
hist(ugrid[x],breaks=c(ugrid[1]-0.05,ugrid+0.05),prob=T)
lines(ugrid,post.density,col='red',lwd=2)
