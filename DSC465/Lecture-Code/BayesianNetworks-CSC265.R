

### code adapted from "Bayesian Networks in R", Nagarajan, Scutari and Lebre, 2013, Springer

library(bnlearn)
data(marks)
str(marks)

# Section 2.3.2 Creating and Manipulating Network Sturctures 

### 'bn' is an S3 class

help('bn class')
help(package='bnlearn')

### it represents a Bayesian network

ug = empty.graph(names(marks))
class(ug)
attributes(ug)

### it has 3 attributes. 'arcs' and 'nodes' define the DAG

ug$learning # correct in original code 
nodes(ug)
arcs(ug)

arcs(ug, check.cycles = TRUE) = matrix(
  c("MECH", "VECT", "MECH", "ALG", "VECT", "MECH",
    "VECT", "ALG", "ALG", "MECH", "ALG",   "VECT",
    "ALG", "ANL", "ALG", "STAT", "ANL",    "ALG",
    "ANL", "STAT", "STAT", "ALG", "STAT",  "ANL"),
  ncol = 2, byrow = TRUE,
  dimnames = list(c(), c("from", "to")))
ug
arcs(ug)

### graphs are easily to plot

plot(ug)


#-----------------------------------------------------------------------------#

### make a new BN

dag = empty.graph(names(marks))
arcs(dag) = matrix(
  c("VECT", "MECH", "ALG", "MECH", "ALG", "VECT",
    "ANL", "ALG", "STAT", "ALG", "STAT", "ANL"),
  ncol = 2, byrow = TRUE,
  dimnames = list(c(), c("from", "to")))
dag


mat = matrix(c(0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
      1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0), nrow = 5,
      dimnames = list(nodes(dag), nodes(dag)))
mat
dag2 = empty.graph(nodes(dag))
amat(dag2) = mat

amat(dag2)
arcs(dag2)
arcs(dag)

### dag and dag2 are the same DAG

all.equal(dag, dag2)

### remember, we can use an adjacency matrix to represent a directed graph

### edges can be added or deleted individually (see also 'drop.arc')

dag3 = empty.graph(nodes(dag))
dag3 = set.arc(dag3, "VECT", "MECH")
dag3 = set.arc(dag3, "ALG", "MECH")
dag3 = set.arc(dag3, "ALG", "VECT")
dag3 = set.arc(dag3, "ANL", "ALG")
dag3 = set.arc(dag3, "STAT", "ALG")
dag3 = set.arc(dag3, "STAT", "ANL")
all.equal(dag, dag3)
all.equal(ug, moral(dag))

#What kind of arc configuration is called a v-structure is not uniquely defined in literature. 
#The original definition from Pearl (2000), which is still followed by most texts and papers, 
#states that the two parents in the v-structure must not be connected by an arc.However, 
#Koller and Friedman (2009) call that an immoral v-structure and call a moral v-structure a 
#v-structure in which the parents are linked by an arc. 
#-----------------------------------------------------------------------------#

### a toplogical ordering is a ranking of the nodes in which parents 
#are always ranked higher than (or before) children. All DAGs have at 
#least one topological ordering (most have more). 

node.ordering(dag)

### Markov blanket for a given node = a nodes' parents, 
#children and childrens other parents. In a BN, a node is 
#independent of the remaining nodes conditional on the Markov 
#blanket (Pearl 1988)

### Neighborhood of a node consists of all connected nodes  


nbr(dag, "STAT")
mb(dag, "STAT")

nbr(dag, "ANL")
mb(dag, "ANL")

nbr(dag, "ALG")
mb(dag, "ALG")

nbr(dag, "VECT")
mb(dag, "VECT")

nbr(dag, "MECH")
mb(dag, "MECH")

### Markov blankets are symmetric, in the sense that if a node A is in mb(B) then node B is in mb(A).


"ANL" %in% mb(dag, "ALG")
"ALG" %in% mb(dag, "ANL")

### the neighborhood and the Markov blanket need not be the same

dag4 = dag
dag4 = set.arc(dag4, "STAT", "MECH")
plot(dag4)
nbr(dag4, "VECT")
mb(dag4, "VECT")

### we can also capture a nodes' children and parents, and extract children, parents, and childrens other parents. 

plot(dag)
chld = children(dag, "VECT")
par = parents(dag, "VECT")
o.par = sapply(chld, parents, x = dag)
unique(c(chld, par, o.par[o.par != "VECT"]))
mb(dag, "VECT")

#-----------------------------------------------------------------------------#

### we know introduce data to infer the probabilistic structure of the BN. 

### score types
#the multivariate Gaussian log-likelihood (loglik-g) score. 
#the corresponding Akaike Information Criterion score (aic-g). 
#the corresponding Bayesian Information Criterion score (bic-g). 
#a score equivalent Gaussian posterior density (bge).

bnlearn::score(dag, data = marks, type = "loglik-g")
dag.eq = reverse.arc(dag, "STAT", "ANL")
bnlearn::score(dag.eq, data = marks, type = "loglik-g")
dag.eq1 = reverse.arc(dag, "VECT", "ALG")
dag.eq2 = reverse.arc(dag.eq1, "MECH", "ALG")
bnlearn::score(dag.eq2, data = marks, type = "loglik-g")


par(mfrow=c(2,2))
plot(dag,main=paste('dag',bnlearn::score(dag, data = marks, type = "loglik-g")))
plot(dag.eq,main=paste('dag.eq', bnlearn::score(dag.eq, data = marks, type = "loglik-g")))
plot(dag.eq2,main=paste('dag.eq2',bnlearn::score(dag.eq2, data = marks, type = "loglik-g")))

### cpdag gives a representation of an equivalence class

par(mfrow=c(1,3))
plot(dag,main='dag')
plot(dag.eq,main='dag.eq')
plot(cpdag(dag), main='equivalence class containing dag')

###########

par(mfrow=c(3,2),oma=c(2,2,2,2))

ug2 = empty.graph(as.character(1:5))

ug2.arcs = matrix(c("1", "2", "3", "2","3","1"),
  ncol = 2, byrow = TRUE,
  dimnames = list(c(), c("from", "to")))

ug2.arcs
arcs(ug2, check.cycles = TRUE) = ug2.arcs
plot(ug2)

vstructs(ug2)
vstructs(ug2, moral = TRUE)
vstructs(ug2, moral = FALSE)
plot(moral(ug2))
plot(cpdag(ug2))

set.seed(02232016)
x = data.frame(matrix(rnorm(5*100),ncol=5))
names(x) = nodes(ug2)

elist = list(
  c("1", "2", "3", "2","3","1"),
  c("2", "1", "3", "2","3","1"),
  c("1", "2", "2", "3","3","1"),
  c("2", "1", "2", "3","3","1"),
  c("1", "2", "3", "2","1","3"),
  c("2", "1", "3", "2","1","3"),
  c("1", "2", "2", "3","1","3"),
  c("2", "1", "2", "3","1","3"),
  c("1", "2", "3", "2","5","4"),
  c("2", "1", "3", "2","4","5"),
  c("2", "1", "3", "2","5","4"),
  c("1", "2", "2", "3","4","5")
  )

par(mfrow=c(3,4),mar=c(2,2,2,2))
for (i in 1:12) {
 
  ug2.arcs = matrix(elist[[i]],
                  ncol = 2, byrow = TRUE,
                  dimnames = list(c(), c("from", "to")))
  arcs(ug2, check.cycles = FALSE) = ug2.arcs
  plot(ug2)
  sc = bnlearn::score(ug2, data = x, type = "loglik-g")
  title(sc)
}
  


# Section 2.3.3 Plotting Network Strucutres omitted. See also Chapter 12 in "Bioconductor Case Studies" 

# Section 2.3.4 Structure Learning

### model x1 -> x2 -> x3

par(mfrow=c(2,2), oma=c(1,1,1,1))
  
n=200
x2 = rnorm(n)
x1 = (x2 + rnorm(n))/sqrt(2)
x3 = (x2 + rnorm(n))/sqrt(2)
data1 = data.frame(x1,x2,x3)
bn1 = hc(data1)
plot(bn1,main='x1 <- x2 -> x3')
round(cor(data1),2)

### model x1 -> x2 <- x3

x1 = rnorm(n)
x3 = rnorm(n)
x2 = (x1 + x3)/sqrt(2)
data2 = data.frame(x1,x2,x3)
bn2 = iamb(data2)
plot(bn2,main='x1 -> x2 <- x3')
round(cor(data2),2)

###

library(ISLR)

# Wage data.frame

help(Wage)


#### Does marital status influence wage, or does age influence wage, and married people tend to be older? 

par(mfrow=c(1,2),mar=c(6,4,2,1),las=2)
boxplot(wage ~ maritl, data=Wage,ylab='wage')
boxplot(age ~ maritl, data=Wage,ylab='age')


# need to convert integer type to numeric 

head(Wage)

Wage[[1]] = as.numeric(Wage[[1]])
Wage[[2]] = as.numeric(Wage[[2]])

var.list = c(2:10)
names(Wage[,var.list])

par(mfrow=c(1,2))
plot(hc(Wage[,var.list]),main='DAG')
plot(cpdag(hc(Wage[,var.list])),main='Equivalence Class')

