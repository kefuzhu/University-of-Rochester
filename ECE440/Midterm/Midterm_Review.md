# ECE 440, Midterm Review

## Probability

**(1) Axioms of Probability**
	
- **Non-negativity**: $P(E) \ge 0$
- **Probability of universe**: $P(S) = 1$
- **Additivity**: Given sequence of **disjoint** events $E_1, E_2, ...$

<center>
$P(\cup_{i=1}^{\infty} E_i) = \sum_{i=1}^{\infty} P(E_i)$
</center>	

**(2) Law of Large Numbers**: Sequence of i.i.d. RVs $X_1, X_2, ..., X_n, ...$ with mean $\mu$. Define sample average $\bar{X_N} := (1/N)\sum_{n=1}^N X_n$
	
- Weak version: Sample average $\bar{X_N}$ of i.i.d sequence **converges in prob** to $\mu = E[X_n]$
	
	$\lim_{N \rightarrow \infty} P(|\bar{X_N} - \mu| < \epsilon) = 1$, for all $\epsilon > 0$
	 
- Strong version: Sample average $\bar{X_N}$ of i.i.d sequence **converges a.s.(almost surely)** to $\mu = E[X_n]$

	$\lim_{N \rightarrow \infty} P(|\bar{X_N}| = \mu) = 1$
	
**(3) Bayes's Rule**

<center>
$P(E|F) = \frac{P(F|E)P(E)}{P(F)} = \frac{P(F|E)P(E)}{\sum_i P(F|E_i)P(E_i)}$
</center>

**(4) Mutually Independent**: 

$P(\cap_i E_i) = \prod_i P(E_i)$ for **every finite** subset of $i$ at least two integers (Every two pairs, three subset, four subset, and etc...)

**(5) Pairwise Independent**: $P(E_i \cap E_j) = P(E_i)P(E_j)$ for all $(i,j)$

**(6) Bernoulli RV**: $X$ with parameter $p$ indicate a random event $E$ can succeed with $P(E) = p$

- $p(x) = p^x(1-p)^{1-x},\ E[X] = p,\ var[X] = p(1-p)$

**(7) Geometric RV**: $X$ with parameter $p$ counts the number of Bernoulli trials needed to register first success

- $p(x) = p(1-p)^{x-1},\ F(x) = 1-(1-p)^x,\ E[X] = \frac{1}{p}, var[X] = \frac{1-p}{p^2}$

**(8) Binomial RV**: $X$ with parameters $n$ and $p$ counts the number of successes in $n$ Bernoulli trials.

- $p(x) = {n \choose x}p^x(1-p)^{n-x},\ E[X] = np,\ var[X] = np(1-p)$
- For $B_1, B_2, ..., B_n$ i.i.d Bernoulli RVs with parameter $p$. Can write binomial X with parameters $(n,p)$ as $X = \sum_{i=1}^n B_i$
- For binomials $Y$ and $Z$ with parameters $(n_Y,p)$ and $(n_Z,p)$, then $X = Y + Z$ ~ binomial$(n_Y+n_Z,p)$

**(9) Poisson RV**: $X$ with parameter $\lambda$ counts of rare events or "arrivals"

- $p(x) = e^{-\lambda}\frac{\lambda^x}{x!},\ E[X] = \lambda,\ var[X] = \lambda$
- For $X_1$ ~ $Poisson(\lambda_1)$ and $X_2$ ~ $Poisson(\lambda_2)$, then $Y = X_1 + X_2$ ~ $Poisson(\lambda_1+\lambda_2)$
- The law of rare events asserts that the distribution of $X$ ~ Binomial$(n,p)$ converges to a Poisson$(\lambda)$ as $n \rightarrow \infty$, provided $np=\lambda$

**(10) Uniform RV**: $X$ with parameters $a$ and $b$ models problems with equal probability of landing on an interval $[a,b]$

- $f(x) = \frac{1}{b-a},\ F(x) = \frac{x-a}{b-a}$
- $E[X] = \frac{a+b}{2}$

**(11) Exponential RV**: $X$ with parameter $\lambda$ models duration of phone calls, lifetime of electronic components

- $f(x) = \lambda e^{-\lambda x}, x \ge 0$
- $F(x) = 1-e^{-\lambda x}$
- $E[X] = \frac{1}{\lambda}$

**(12) Gaussian/Normal RV**: $X$ with parameter $\mu$ and $\sigma^2$ models randomness arising from large number of random effects

- $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/2\sigma^3}$
- $E[X] = \mu,\ var[X] = \sigma^2$

**(13) Markov's Inequality**: $P(|X| \ge a) \le \frac{E(|X|)}{a}$

**(14) Chebyshev's Inequality**: $P(|X-\mu| \ge k) \le \frac{\sigma^2}{k^2}$

**(15) Iterated Expectations**: $E[X] = E_Y[E_X[X|Y]] = \sum_y E_X[X|Y=y] \cdot p_Y(y)$

- $var[X] = E_Y[var_X(X|Y)] + var_Y[E_X(X|Y)]$, using iterated expectation to compute the variance

## Discrete Markov Chain

**(1) Chapman-Kolmogorov Equation**: $P_{ij}^{m+n} = \sum_{k=0}^{\infty} P_{kj}^nP_{ik}^m \rightarrow P^{(m+n)} = P^{(m)}P^{(n)}$

**(2) n-step Transition Probabilities**: $P^{(n)} = P^n$

**(3) Communication**: States $i$ and $j$ are said to **communicate ($i \leftrightarrow j$)** if $P_{ij}^n > 0$ and $P_{ji}^m > 0$ for some $n$ and $m$

- **Reflexivity**: $i \leftrightarrow i$ (Because $P_{ii}^0 = 1$ always holds)
- **Symmetry**: If $i \leftrightarrow j$ then $j \leftrightarrow i$
- **Transitivity**: If $i \leftrightarrow j$ and $j \leftrightarrow k$, then $i \leftrightarrow k$
- **Partitions set of states into disjoint classes**

**(4) Irreducible MC**

- All states communicate with each other
- If MC has finite number of states, the single class is recurrent
- If MC has infinite number of states, the single class is transient

**(5) Recurrent**

Define the return time to state $i$ as $T_i = \min \{n > 0: X_n = i\ |\ X_0 = i\}$

- **recurrent**: Probability of not returning is $0$. $P(T_i = \infty \ |\ X_0 = i) = 0$
	- **positive recurrent**: Expected value of $T_i$ is finite. $E[T_i\ |\ X_0 = i] = \sum_{n=1}^{\infty} nP(T_i = n\ |\ X_0 = i) < \infty$
	- **null recurrent**: Expected value of $T_i$ is infinite. $E[T_i\ |\ X_0 = i] = \sum_{n=1}^{\infty} nP(T_i = n\ |\ X_0 = i) = \infty$

**(6) Ergodic MC**

- **irreducible**
- **positive recurrent**
- **aperiodic**

**(7) Ensemble Average**: across different realizations of the MC

<center>
$E[f(X_n)] = \sum_{i=1}^{\infty} f(i)P(X_n = i) \rightarrow \sum_{i=1}^{\infty} f(i)\pi_i$
</center>

**(8) Ergodic Average**: across time for a single realization of the MC

<center>
$\bar{f_n} = \frac{1}{n} \sum_{m=1}^{n} f(X_m)$
</center>

**Note**: Ensemble average equals to ergodic average almost surely, asymptotically in $n$
<center>
$\lim_{n \rightarrow \infty} \frac{1}{n} \sum_{m=1}^{n} f(X_m) = \sum_{i=1}^{\infty} f(i)\pi_i$
</center>

