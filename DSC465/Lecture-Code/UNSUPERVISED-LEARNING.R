
### START

# recall iris data



my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)

par(mfrow=c(1,1))
prc<-prcomp(iris[,1:4], scale=T)

# can distinguish 2 groups without class knowledge

pairs(prc$x)
pairs(prc$x,col=my.pch)

par(mfrow=c(1,1))
biplot(prc,scale=F)
prc$rotation
plot(prc$x[,1],prc$x[,2])
lines(c(0,prc$rotation[2,1]),c(0,prc$rotation[2,2]),col='green',lty=1,type='l',lwd=3)


### gene expression data

GSE10245.data = read.table(file='GSE10245.csv',header=T,sep=',')
gem1 = GSE10245.data[,2:51]
gr = GSE10245.data[,1]

prc = prcomp(gem1)
plot(prc)

### loadings can give structure to the clustering 

par(mfrow=c(2,2))
biplot(prc,choices=c(1,2))
biplot(prc,choices=c(1,3))
biplot(prc,choices=c(1,4))
biplot(prc,choices=c(2,3))

pairs(prc$x[,1:4])

pairs(prc$x[,1:4],col=my.pch)

###
############ Hierarchical Clustering 

hfit = hclust(dist(iris[,1:4]))
plot(hfit)
plot(hfit,labels=my.pch)

### methods can give very different results

par(mfrow=c(3,1))
hfit = hclust(dist(iris[,1:4]), method="single")
plot(hfit,labels=my.pch,main='single')
hfit = hclust(dist(iris[,1:4]), method="complete")
plot(hfit,labels=my.pch,main='complete')
hfit = hclust(dist(iris[,1:4]), method="average")
plot(hfit,labels=my.pch,main='average')

### simulate data

set.seed(123)

my.pch = rep(c(1,2,3),each=50)


# case 1 - not very good at clustering

xm = matrix(NA, 150, 2)
xm[,2] = rnorm(150,sd=10)
xm[1:50,1] = rnorm(50,sd=0.1) + 1
xm[51:100,1] = rnorm(50,sd=0.1) + 2
xm[101:150,1] = rnorm(50,sd=0.1) + 3

plot(xm[,1],xm[,2],col=my.pch)

par(mfrow=c(3,1))
hfit = hclust(dist(xm), method="single")
plot(hfit,labels=my.pch,main='single',col=my.pch)
hfit = hclust(dist(xm), method="complete")
plot(hfit,labels=my.pch,main='complete')
hfit = hclust(dist(xm), method="average")
plot(hfit,labels=my.pch,main='average')


# case 2 - better, for single link clustering

xm = matrix(NA, 150, 2)
xm[,2] = rnorm(150,sd=1)
xm[1:50,1] = rnorm(50,sd=0.1) + 1
xm[51:100,1] = rnorm(50,sd=0.1) + 2
xm[101:150,1] = rnorm(50,sd=0.1) + 3

plot(xm[,1],xm[,2],col=my.pch)

par(mfrow=c(3,1))
hfit = hclust(dist(xm), method="single")
plot(hfit,labels=my.pch,main='single',col=my.pch)
hfit = hclust(dist(xm), method="complete")
plot(hfit,labels=my.pch,main='complete')
hfit = hclust(dist(xm), method="average")
plot(hfit,labels=my.pch,main='average')

# case 3 - standardized data from case 2

xm2 = xm
xm2[,1] = (xm[,1]-mean(xm[,1]))/sd(xm[,1])
xm2[,2] = (xm[,2]-mean(xm[,2]))/sd(xm[,2])

plot(xm2[,1],xm2[,2],col=my.pch)


par(mfrow=c(3,1))
hfit = hclust(dist(xm2), method="single")
plot(hfit,labels=my.pch,main='single')
hfit = hclust(dist(xm2), method="complete")
plot(hfit,labels=my.pch,main='complete')
hfit = hclust(dist(xm2), method="average")
plot(hfit,labels=my.pch,main='average')



####################

xm3 = matrix(NA,150,2)
xm3[,1] = rnorm(150)+rep(c(5,10,15),each=50)
xm3[,2] = (xm3[,1]+rnorm(150,sd=0.25))/sqrt(1+0.25^2)

plot(xm3[,1],xm3[,2],col=my.pch)

par(mfrow=c(3,1),las=0)
hfit = hclust(dist(xm3), method="single")
plot(hfit,labels=my.pch,main='single')
hfit = hclust(dist(xm3), method="complete")
plot(hfit,labels=my.pch,main='complete')
hfit = hclust(dist(xm3), method="average")
plot(hfit,labels=my.pch,main='average')
abline(h=9,col='red')
abline(h=5,col='green')

### can extract clusters

pr = cutree(hfit,k=3)
table(my.pch,pr)

pr = cutree(hfit,k=6)
table(my.pch,pr)


pr = cutree(hfit,h=5)
table(my.pch,pr)

pr = cutree(hfit,h=9)
table(my.pch,pr)

### example

xy = cbind(c(2,3,2,4,3),c(3,2,4,5,5))
dist(xy)
hfit = hclust(dist(xy))
plot(hfit)
cphz = cophenetic(hfit)
cphz
hfit$height


########## K-means


my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)
fit = kmeans(iris[,1:4],centers=3,nstart=100)

table(fit$cluster,my.pch)

# exchange 1,2  

my.pch = rep(c(2,3,1),each=50)

table(fit$cluster,my.pch)

pairs(iris[,1:4],col=1+(fit$cluster!=my.pch))

# can examine centers

fit$centers

x = rbind(iris[,1:4],fit$centers)
colv=c(rep(1,150),rep(2,3))
pchv=c(rep(3,150),rep(19,3))
pairs(x,col=colv,pch=pchv)

### try with 2-5 means

nc = 2

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)
fit = kmeans(iris[,1:4],centers=nc,nstart=100)
x = rbind(iris[,1:4],fit$centers)
colv=c(rep(1,150),rep(2,nc))
pchv=c(rep(3,150),rep(19,nc))
pairs(x,col=colv,pch=pchv)

fit$totss
fit$betweenss
fit$tot.withinss
fit$withinss

sum(fit$withinss)+fit$betweenss
fit$totss

nc = 3

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)
fit = kmeans(iris[,1:4],centers=nc,nstart=100)
x = rbind(iris[,1:4],fit$centers)
colv=c(rep(1,150),rep(2,nc))
pchv=c(rep(3,150),rep(19,nc))
pairs(x,col=colv,pch=pchv)

fit$totss
fit$betweenss
fit$tot.withinss
fit$withinss

sum(fit$withinss)+fit$betweenss
fit$totss


nc = 4

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)
fit = kmeans(iris[,1:4],centers=nc,nstart=100)
x = rbind(iris[,1:4],fit$centers)
colv=c(rep(1,150),rep(2,nc))
pchv=c(rep(3,150),rep(19,nc))
pairs(x,col=colv,pch=pchv)

fit$totss
fit$betweenss
fit$tot.withinss
fit$withinss

sum(fit$withinss)+fit$betweenss
fit$totss


nc = 5

my.pch = rep(c(1,2,3),each=50)
pairs(iris[,1:4],col=my.pch)
fit = kmeans(iris[,1:4],centers=nc,nstart=100)
x = rbind(iris[,1:4],fit$centers)
colv=c(rep(1,150),rep(2,nc))
pchv=c(rep(3,150),rep(19,nc))
pairs(x,col=colv,pch=pchv)

fit$totss
fit$betweenss
fit$tot.withinss
fit$withinss

sum(fit$withinss)+fit$betweenss
fit$totss

sse = rep(0,10)
for (i in 1:10) {
  fit = kmeans(iris[,1:4],centers=i)
  sse[i] = fit$totss-fit$betweenss
}
plot(sse,type='b')


r2 = rep(0,10)
for (i in 1:10) {
  fit = kmeans(iris[,1:4],centers=i)
  r2[i] = fit$betweenss/fit$totss
}
plot(r2,type='b')


### STOP



