# Lecture 10, Wednesday, 02/20

### Topics: 
- Message Passing

**Definition**

For each variable vertex $n$ and its neighboring factor vertex $\ f_m$, the information propagated from $n$ to $\ f_m$ is

<center>
$q_{n \rightarrow m} (X_n) = \prod_{m' \in M(n) \backslash \{m\}} r_{m' \rightarrow n} (X_n)$ 
</center>

where $M(n) =$ factors connecting to variable $n$

For each factor vertex $\ f_m$ and its neighboring variable $n$, the information propagated from $\ f_m$ to $n$ is 

<center>
$r_{m \rightarrow n} (X_n) = \sum_{\vec{X_m}\ \backslash X_n} [f_m(\vec{X_m}) \prod_{n' \in N(m) \backslash \{n\}} q_{n' \rightarrow m}(X_{n'})]$
</center> 

where $N(m) = $ variables connecting to factor $\ f_m$. 

$\sum_{\vec{X_m}\ \backslash X_n}$ is the sum over all variables connected to $\ f_m$ except $X_n$

The procedure of message passing or belief propagation is first to propagate the information from leaf vertices to the center by filling in the tables for each message. Once all the messages variables $x_n$ have been computed, the marginal probability of $x_n$ is computed by combing all incoming messages

<center>
$P(X_n) = \frac{1}{Z} \prod_{m \in M(n)} r_{m \rightarrow n}(X_n)$
</center>