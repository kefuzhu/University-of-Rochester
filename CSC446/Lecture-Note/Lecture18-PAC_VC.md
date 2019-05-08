# Lecture 18, Wednesday, 04/10

### Topics

- PAC (Partially ($1-\delta$) Approximately ($\epsilon$) Correct) Learning
- VC Dimension


## PAC Learning

**Goal**: Understand how large a data set needs to be in order to give good generalization.

We want 

<center>
$P(error) < \epsilon$ over test set holds with probability $> 1- \delta$
</center>

```
k = 0
for i in range(N):
	train_x = Train Data Sample (Generated from distribution D)
	test = Test Data
	h = train(train_x)
	error_rate = error(h, test)
	
	if error_rate ≤ ϵ:
		k = k + 1

If (k/N) < δ:
	This is PAC learning
 
```

- **Error ($\epsilon$)**

	Given a trained hypothesis $h$, what is the error rate I make on test examples
	
	$\forall x \in D$, $Pr(h(x) \ne c(x))$

- **Failure ($\delta$)**

	If error rate of $h$ is greater than $\epsilon$, then it is a failure

### Version Space

<center>
$VS_{H,D} = \{h \in H | \forall <x, c(x)> \in D; h(x) = c(x)\}$
</center>

- Set of hypothesis with zero training error
- **Observation**: If the version space ($VS$) contains all acceptable hypothesis (less than $\epsilon$ error rate), then we will definitely laern an acceptable hypothesis
- To get a bound on number of training examples needed by a consistent learner
	- Need bound on the number of training examples to ensure $VS_{H,D}$ contains no *unacceptable hypothesis*

**$\epsilon$-Exhausted Version Space**

- $VS_{H,D}$ is $\epsilon$-exhausted with respect to $c$ and $D$ if
	- $\forall h \in VS_{H,D},\ error_D(h) < \epsilon$

**Theorem**:
> If $H$ is finite and $D$ is a sequence of $m$ training examples (randomly sampled from $D$), probability that version space $VS_{H,D}$ is **not $\epsilon$-exhausted** with respect to $c$ is less than or equal to:
> <center>$|H|e^{-\epsilon \cdot m}$</center>

**Proof**:

- $h_1, h_2, ..., h_k$ are **unacceptable hypothesis** in $H$

	$\Rightarrow \forall h_i,\ i = 1,2,...,k,\ error\_rate(h_i) > \epsilon$
	
- To have $h_i,\ i = 1,2,...,k$ in vision space, training error of $h_i = 0$

Let $p_i$ be the probability that $h_i$ is consistent with $m$ examples (training error $=0$)

<center>
$p_i \le (1-\epsilon)^m$
</center>

Then probability that any of the $h_1,h_2,...,h_k$ will be in vision space $\le \sum_{i=1}^k p_i\ \Leftrightarrow\ \le k(1-\epsilon)^m$

$\because k \le |H|$ and $\forall\ 0 \le a \le 1, (1-a) \le e^{-a}$

$\therefore$ Then probability that $h_1,h_2,...,h_k$ will be in vision space

<center>
$\le |H|(1-\epsilon)^m \Leftrightarrow |H|e^{-\epsilon \cdot m}$
</center>

---

Recall that we want $Pr(VS\ \mathrm{is\ not}\ \epsilon-\mathrm{exhausted}) \le \delta$

$\Rightarrow$

<center>
$|H|e^{-\epsilon \cdot m} \le \delta$

$ln|H| - \epsilon \cdot m \le ln(\delta)$

$ln|H| + ln(\frac{1}{\delta}) \le \epsilon \cdot m$

$m \ge \frac{1}{\epsilon} [ln|H| + ln(\frac{1}{\delta})]$

$\Leftrightarrow m \ge \frac{1}{\epsilon} \cdot ln(\frac{|H|}{\delta})$
</center>


## VC Dimension

- $C$: concept class (classifier type)
- $c$ is a concept where $c \subset X$ (data point) that are positive
- $S$: samples of $m$ data points, $S \in X^m$
- $c \cap S$: **behavior** of $c$ on $S$

$\pi_C(S)$ = all behaviors of concepts $c$ in $C$ = $\{c_1: c_1 = c \cap S, c \in C\}$

Suppose we have a $C$ that is a linear classifier, and we have a sample $S$ that has 4 data points, then

$\pi_C(S) = \{\{\},\{1\}, \{2\}, ...,\{1,2,3,4\}\}$

$\Rightarrow |\pi_C(S)| = 16-2 = 14 \le 16 = 2^m$

**Definition**

1. $\pi_C(m) = \max_{S:|S| = m} |\pi_C(S)|$ = highest # of behaviors of $C$ on $m$ data points $\le 2^m$

	e.g. $\pi_{linear}(4) = 14 \le 2^4 = 16$
	
2. $VCD(C) = \max \{m: \pi_C(m) = 2^m\}$

	$=$ largest # of data points, under some arrangements (Don't have to be every possible arrangement), that can be classified all possible ways ("**shattered**")
	
	**Note**: shatter = classify all $2^m$ ways
	
	e.g. $VCD(linear) = 3$
