# DSC 462 HW#2, Kefu Zhu

## Question 1

(a) $S_x = \{2,3,4,5,6,7\}$

(b)(c)

**Game Process**:

(1) The $1$st number ($6$ possible choices)

(2) The $2$nd number

- The $2$nd number is the same as the $1$st number ($1$ possible choices) $\rightarrow X=2, P(X=2) = \frac{6\cdot1}{6^2}$ 
- The $2$nd number is not the same as the $1$st number ($5$ possible choices)

(3) The $3$rd number

- The $3$rd number is the same as one of the first $2$ numbers ($2$ possible choices) $\rightarrow X=3, P(X=3) = \frac{(6\cdot5)\cdot2}{6^3}$
- The $3$rd number is not the same as any of the first $2$ numbers ($4$ possible choices)

...

Therefore, we have the following calculation

$P(X=2) = \frac{(6)\cdot1}{6^2} = \frac{1}{6}$

$P(X=3) = \frac{(6\cdot5)\cdot2}{6^3} = \frac{5}{18}$

$P(X=4) = \frac{(6\cdot5\cdot4)\cdot3}{6^4} = \frac{5}{18}$

$P(X=5) = \frac{(6\cdot5\cdot4\cdot3)\cdot4}{6^5} = \frac{5}{27}$

$P(X=6) = \frac{(6\cdot5\cdot4\cdot3\cdot2)\cdot5}{6^6} = \frac{25}{324}$

$P(X=7) = \frac{(6!)\cdot6}{6^7} = \frac{5}{324}$

**Sanity check**: $P(X=2) + P(X=3) + P(X=4) + P(X=5) + P (X=6) + P(X=7)$ 
$= \frac{1}{6} + \frac{5}{18} + \frac{5}{18} + \frac{5}{27} + \frac{25}{324} + \frac{5}{324} = 1$

Since we already have $P(X=i)$ for every $i \in S_x$, we can easily calculate every $P(X>i)$

$P(X>2) = 1 - P(X\le2) = 1 - P(X=2) = 1 - \frac{1}{6} \approx 0.83$

$P(X>3) = 1 - P(X=2) - P(X=3) = 1 - \frac{1}{6} - \frac{5}{18} \approx 0.56$

$P(X>4) = 1 - P(X=2) - P(X=3) - P(X=4) = 1 - \frac{1}{6} - \frac{5}{18} - \frac{5}{18} \approx 0.28$

$P(X>5) = P(X=6) + P(X=7) = \frac{25}{324} + \frac{5}{324} \approx 0.09$

$P(X>6) = P(X=7) \approx 0.02$

$P(X>7) = 0$

## Question 2

(a)

$f(x) = 
\begin{cases}
-c(x-2),\ x \in (0,2)\\
c(x-2),\ x \in [2,4)\\
0,\ otherwise\\
\end{cases}
$

$\sum p(x) = 1 = \int_0^2 -c(x-2) \mathrm{d}x + \int_2^4 c(x-2) \mathrm{d}x$

$=-c(\frac{x^2}{2}-2x\ |_0^2) + c(\frac{x^2}{2}-2x\ |_2^4)$

$=-c(2-4) + c[(8-8)-(2-4)]$

$=4c \Rightarrow c = \frac{1}{4}$

(b)

$\because f(x) = 
\begin{cases}
-\frac{1}{4}x + \frac{1}{2},\ x \in (0,2)\\
\frac{1}{4}x - \frac{1}{2},\ x \in [2,4)\\
0,\ otherwise\\
\end{cases}
$

$\therefore F(x) = 
\begin{cases}
0,\ x \in (-\infty,0]\\
\int_0^x -\frac{1}{4}x + \frac{1}{2} \mathrm{d}x = \frac{x}{2} - \frac{x^2}{8},\ x \in (0,2)\\
(\int_0^2 -\frac{1}{4}x + \frac{1}{2} \mathrm{d}x) + (\int_2^x \frac{1}{4}x - \frac{1}{2} \mathrm{d}x) = 1 + \frac{x^2}{8} - \frac{x}{2},\ x \in [2,4)\\
1,\ x \in [4,+\infty)\\
\end{cases}
$

```r
# F(x) for x in (0,2)
f1 = function(x) {x/2 - x^2/8}
# F(x) for x in (2,4)
f2 = function(x) {1 + x^2/8 - x/2}
# Plot F(x) in (0,2)
plot(f1, from = 0, to = 2, xlim = c(-6,6), ylim = c(0,1), xlab = 'X', ylab = 'F(X)')
# Plot F(x) in (2,4)
plot(f2, from = 2, to = 4, add = TRUE)
# Add F(x) = 0 from -infinity to 0
segments(-6,0,0,0)
# Add F(x) = 1 from 4 to +infinity
segments(4,1,6,1)
```

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC462/Homework/HW2/questions1.png)

## Question 3

$var(S_N) = \sum_{i=1}^n \sigma_i^2 + 2\sum_{i<y} \sigma_{ij}$

$\because \sigma_i^2 = E[X_i^2] - E[X_i]^2 = \frac{1}{N} - (\frac{1}{N})^2 = \frac{1}{N} \cdot (1-\frac{1}{N})$

$\because \sigma_{ij} = E[X_iX_j] - E[X_i]E[X_j] = 1 \cdot \frac{1}{N}\frac{1}{N-1} - \frac{1}{N}\frac{1}{N} = \frac{1}{N^2(N-1)}$

$\therefore var(S_N) = \sum_{i=1}^n \frac{1}{N} \cdot (1-\frac{1}{N}) + 2\sum_{i,j=1,\ i<y}^n \frac{1}{N^2(N-1)} = 1 + 2 \cdot (\frac{N(N-1)}{2}) \cdot \frac{1}{N^2(N-1)} = 1$

## Question 4

(a)

**Define**:

1. $X =$ the test score of an individual
2. $N =$ the number of candidates who passed the test

$P(X \ge 625) = P(Z \ge \frac{625-500}{75}) \approx 0.04779035$

```r
# Calculate the P(Z >= (625-500)/75)
1 - pnorm(625, mean = 500, sd = 75) # 0.04779035
```

**Define**:

1. $p$ = the probability that an individual passes the test = 0.04779035
2. $q$ = the probability that an individual does not pass the test = $1 - p$ = 0.9522097

$P(N \ge 3) = 1 - P(N=0) - P(N=1) - P(N=2)$

$= 1 - {35 \choose 0} \cdot q^{35} - {35 \choose 1} \cdot p \cdot q^{34} - {35 \choose 2} \cdot p^2 \cdot q^{33}$

$= 1 - 1 \cdot (0.9522097)^{35} - 35 \cdot 0.04779035 \cdot (0.9522097)^{34} - 595 \cdot (0.04779035)^2 \cdot (0.9522097)^{33}$

$\approx 0.2333842$

(b)

$P(N \ge 3) = 0.8 = 1 - {35 \choose 0} \cdot q^{35} - {35 \choose 1} \cdot p \cdot q^{34} - {35 \choose 2} \cdot p^2 \cdot q^{33}$

$\Rightarrow {35 \choose 0} \cdot q^{35} + {35 \choose 1} \cdot p \cdot q^{34} + {35 \choose 2} \cdot p^2 \cdot q^{33} - 0.2 = 0$

```r
# Define function
f = function(x) {
choose(35,0)*(1-x)^35 + 
choose(35,1)*x*(1-x)^34 + 
choose(35,2)*(x^2)*(1-x)^33 - 0.2}
# Calculate the value of x
uniroot(f,c(0,1))
```

```
# Result
$root
[1] 0.1183283

$f.root
[1] -2.792853e-05

$iter
[1] 9

$init.it
[1] NA

$estim.prec
[1] 6.103516e-05
```

Therefore, $p \approx 0.1183283$. Based on the $Z$-score table, $Z \approx 1.18$

```r
# Check the Z-score in R
qnorm(0.1183283, 0, 1, lower.tail = FALSE) # 1.183385
```
$\therefore Z \approx 1.18 = \frac{X-500}{75} \rightarrow X \approx 589$

## Question 5

$F(M) = P(X_1 \le M, X_2 \le M, ..., X_n \le M)$

$\because X_1, ..., X_n$ are i.i.d

$\therefore F_x(M) = P(X_1 \le M)P(X_2 \le M) \cdot\cdot\cdot P(X_n \le M) = F(M)^k = (\frac{M-0}{c-0})^n = (\frac{M}{c})^n$

$\Rightarrow f(x) = \frac{\mathrm{d}}{\mathrm{d}M} F_x(M) = \frac{nM^{n-1}}{c^n}$

Then, $E(M) = \int_0^c M \cdot f(M) \mathrm{d}M$

$= \int_0^c M \cdot \frac{n}{c^n} \cdot M^{n-1} \mathrm{d}M$

$= \frac{n}{c^n \cdot (n+1)} \cdot M^{n+1}\ |_0^c$

$=\frac{n}{n+1} \cdot c$