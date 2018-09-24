# DSC 462 HW#1 Kefu Zhu

## Q1

### (a)

$P(\bigcup\limits_{i=1}^{3} A_i) = P(A_1) + P (A_2) + P(A_3) - P(A_1A_2) - P(A_1A_3) - P (A_2A_3)$

### (b)

**Define**:

- $A_1$ = The chosen integer from $1$ to $105$ inclusively is divisible by $2$
- $A_2$ = The chosen integer from $1$ to $105$ inclusively is divisible by $9$
- $A_3$ = The chosen integer from $1$ to $105$ inclusively is divisible by $13$

$\because$

$P(A_1) = \frac{105 \ // \ 2}{105} = \frac{52}{105}$, 
$P(A_2) = \frac{105 \ // \ 9}{105} = \frac{11}{105}$, 
$P(A_3) = \frac{105 \ // \ 13}{105} = \frac{8}{105}$

$P(A_1A_2) = \frac{105 \ // \ 18}{105} = \frac{5}{105}$, 
$P(A_1A_3) = \frac{105 \ // \ 26}{105} = \frac{4}{105}$, 
$P(A_2A_3) = \frac{105 \ // \ 117}{105} = \frac{0}{105}$

$\therefore P(\bigcup\limits_{i=1}^{3} A_i) =  P(A_1) + P (A_2) + P(A_3) - P(A_1A_2) - P(A_1A_3) - P (A_2A_3)$ 

$ = \frac{52}{105} + \frac{11}{105} + \frac{8}{105} - \frac{5}{105} - \frac{4}{105} - \frac{0}{105} = \frac{62}{105}$

## Q2
### (a)

**Answer**:

Consider four adjacent red birds as a whole, then the total number of possible arrangements equals to the value of $A$, where $A = $ number of blue birds sitting on the left side of red birds

$A = {7 \choose 1} = 7$ 

$\because$
$B = $ Number of total possible arrangements $=\frac{10!}{6! \cdot 4!} = 210$

$\therefore P \ (Four \ red \ birds \ are \ all \ adjacent ) = \frac{A}{B} = \frac{1}{30}$

### (b)

In order to make sure no two red birds are adjacent, a subset of this line of birds must looks like: **red, blue, red, blue, red, blue, red**

Therefore, the scenario becomes similar to the previous question. Consider the formation above as a whole, then the total number of possible arrangements equals to the value of $A$, where $A = $ number of possible arrangements for the rest 3 blue birds

The rest $3$ blue birds can be placed at any of the following $5$ position

- Left side of the formation
- Right side of the formation
- Anywhere between two closest red birds
  - Between $1st$ red bird and the $2nd$ red bird
  - Between $2nd$ red bird and the $3rd$ red bird
  - Between $3rd$ red bird and the $4th$ red bird	

$A = {3 + 5 - 1 \choose 5 - 1} = 35$

$\because$
$B = $ Number of total possible arrangements $=\frac{10!}{6! \cdot 4!} = 210$

$\therefore P \ (no \ two \ red \ birds \ are \ adjacent ) = \frac{A}{B} = \frac{35}{210} = \frac{1}{6}$

## Q3

### (a)

$P(All \ cards \ are \ face \ cards \ of \ a \ single \ color) = 
2 \cdot (\frac{6}{52} \cdot \frac{5}{51} \cdot \frac{4}{50} \cdot \frac{3}{49} \cdot \frac{2}{48}) \approx 0.0000047
$

### (b)

- Pick one suit that appears twice: ${4 \choose 1} = 4$ 
- Pick two cards from that suit: ${13 \choose 2} = 78$
- Pick the rest 3 cards from the rest 3 suits: ${{13 \choose 1}^3} = 2197$

$P(All \ suits \ are \ represented \ at \ least \ once) = \frac{4 \cdot 78 \cdot 2197}{52 \choose 5} \approx 0.2637$


### (c)

- Pick five ranks: ${13 \choose 5} = 1287$
- Pick a color: ${2 \choose 1} = 2$
- Pick the suit of the card for every card in the five cards: $2^5$

$P(All \ ranks \ are \ distinct, \ and \ of \ a \ single \ color) = \frac{1287 \cdot 2 \cdot 2^5}{52 \choose 5} \approx 0.03$

## Q4

### (a)
 
$P(R_1|R_m) = \frac{1}{2} \cdot 2(1-q)q + q^2 = q$

### (b)

$P(R_2)$ has four cases

- The mother is **rr** and father is **rR**: $\frac{1}{2} \cdot q^2 \cdot 2(1-q)q$
- The father is **rr** and mother is **rR**: $\frac{1}{2} \cdot q^2 \cdot 2(1-q)q$
- The mother is **rr** and father is **rr**: $1 \cdot q^2 \cdot q^2$
- The mother is **rR** and father is **rR**: $\frac{1}{2} \cdot \frac{1}{2} \cdot 2(1-q)q \cdot 2(1-q)q$

$P(R_2) = 2 \cdot [\frac{1}{2} \cdot q^2 \cdot 2(1-q)q] + [q^2 \cdot q^2] + [\frac{1}{2} \cdot \frac{1}{2} \cdot 2(1-q)q \cdot 2(1-q)q] = q^2 $

$P(R_1R_2)$ also has four cases

- The mother is **rr** and father is **rR**: $\frac{1}{2} \cdot \frac{1}{2} \cdot q^2 \cdot 2(1-q)q$
- The father is **rr** and mother is **rR**: $\frac{1}{2} \cdot \frac{1}{2} \cdot q^2 \cdot 2(1-q)q$
- The mother is **rr** and father is **rr**: $q^2 \cdot q^2$
- The mother is **rR** and father is **rR**: $\frac{1}{4} \cdot \frac{1}{4} \cdot 2(1-q)q \cdot 2(1-q)q$

$P(R_1R_2) = 2 \cdot [\frac{1}{2} \cdot \frac{1}{2} \cdot q^2 \cdot 2(1-q)q] + [q^2 \cdot q^2] + [\frac{1}{4} \cdot \frac{1}{4} \cdot 2(1-q)q \cdot 2(1-q)q]$
$ = q^3 + \frac{1}{4} (1-q^2)q^2$

$P(R_1|R_2) = \frac{P(R_1R_2)}{P(R_2)} = \frac{q^3 + \frac{1}{4} (1-q^2)q^2}{q^2} = q + \frac{1}{4} (1-q^2)$

### (c)

- $lim_{q \to 0} P(R_1|R_m) = 0$
- $lim_{q \to 0} P(R_1|R_2) = \frac{1}{4}$

## Q5

### (a)

**(i) Proof of $P(\emptyset) = 0$**

$\because P(S) = P(S \cup \{\cup_{i=1}^{\infty} \emptyset \})$, By Axiom 2, $P(S) = 1$, and the set $\emptyset$ is disjoint with all other sets, including $\emptyset$ itself

$\therefore$ By Axiom 3, $P(S) = P(S) + \sum_{i=1}^{\infty} \emptyset$

$\therefore 1 = 1 + \sum_{i=1}^{\infty} \emptyset$

$\therefore \sum_{i=1}^{\infty} \emptyset = 0 \rightarrow P(\emptyset) = 0$ 

**(ii) Proof of $A \cap B = \emptyset$ implies $P(A \cap B) = P(A) + P(B)$**

$\because A \cap B = \emptyset$

$\therefore A \ and \ B \ are \ mutually \ exclusive$

$\because$ the set $\emptyset$ is disjoint with all other sets, including $\emptyset$ itself

$\because P(\emptyset) = 0$ 

By Axiom 3, $P(A \cup B) = P(A \cup B \cup  \{\cup_{i=1}^{\infty} \emptyset) = P(A) + P(B) +  \sum_{i=1}^{\infty} \emptyset = P(A) + P(B)$

**(iii) Proof of $P(A^c) = 1 - P(A)$**

$\because P(S) = P(A) + P(A^c)$

By Axiom 2, $P(S) = 1$

$\therefore 1 = P(A) + P(A^c) \rightarrow P(A^c) = 1 - P(A)$

**(iv) Proof of $A \subset B$ implies $P(A) \le P(B)$**

$P(B) = P(A \cup (A^c \cap B)) = P(A) + P(A^c \cap B)$

$\because By \ Axiom \ 1, \ P(A^c \cap B) \ge 0$

$\therefore P(A) \le P(B)$

### (b)

**(i)** 

$\because \overline{E_i} = E_i \cap E_{i-1}^c \cap E_{i-2}^c \cap ... \cap E_1^c$

$\therefore \forall A \in \overline{E_i}, A \in E_i \Rightarrow \overline{E_i} \subset E_i$

**(ii)**

$\forall m,n$ where $m < n$

We have 
$\overline{E_m} = E_m \cap E_{m-1}^c \cap ... E_1^c$
and
$\overline{E_n} = E_n \cap E_{n-1}^c \cap ... E_1^c$

$\overline{E_n}$ can also be written as  $\overline{E_n} = E_n \cap ... E_m^c \cap ... E_1^c$

$\forall A \in \overline{E_m}, A \in E_m$ and $\forall B \in \overline{E_n}, B \in E_m^c$

$\because E_m$ and $E_m^c$ are mutually exclusive

$\therefore$ There is no pair of $A$ and $B$ such that $A = B$

$\therefore \forall m,n$ where $m < n$, $\overline{E_m}$ and $\overline{E_n}$ are mutually exclusive

$\Rightarrow$ The sets $\overline{E_1}, \overline{E_2}, ...$ are mutually exclusive

**(iii)**

$n = 1$

- $\cup_{i=1}^{n} E_i = E_1$
- $\cup_{i=1}^{n} \overline{E_i} = E_1$

$n = 2$

- $\cup_{i=1}^{n} E_i = E_1 \cup E_2$
- $\cup_{i=1}^{n} \overline{E_i} = (E_2 \cap E_1^c) \cup (\cup_{i=1}^{1} \overline{E_i}) = (E_2 \cap E_1^c) \cup E_1 = E_2 \cup E_1$

$n = 3$

- $\cup_{i=1}^{n} E_i = E_1 \cup E_2 \cup E_3$
- $\cup_{i=1}^{n} \overline{E_i} = (E_3 \cap E_2^c \cap E_1^c) \cup (\cup_{i=1}^{2} \overline{E_i}) = (E_3 \cap E_2^c \cap E_1^c) \cup (E_2 \cup E_1) = E_3 \cup E_2 \cup E_1$

...

$n = m$

- $\cup_{i=1}^{m} E_i = E_1 \cup E_2 \cup ... \cup E_m$
- $\cup_{i=1}^{m} \overline{E_i} = (E_m \cap E_{m-1}^c \cap E_{m-2}^c \cap ... \cap E_1^c) \cup (\cup_{i=1}^{m-1} \overline{E_i}) = (E_m \cap E_{m-1}^c \cap E_{m-2}^c \cap ... \cap E_1^c) \cup (E_{m-1} \cup E_{m-2} \cup ... \cup E_1) = E_m \cup E_{m-1} \cup ... \cup E_1$

$\therefore \forall m$, where $m \ge 1$, we have $\cup_{i=1}^{m} E_i = \cup_{i=1}^{m} \overline{E_i}$

As $m \rightarrow \infty$, $\cup_{i=1}^{\infty} E_i = \cup_{i=1}^{\infty} \overline{E_i}$


### (c)

Proved in question (b)(iii), $\cup_{i=1}^{\infty} E_i = \cup_{i=1}^{\infty} \overline{E_i}$, therefore, $P (\cup_{i=1}^{\infty} E_i) = P(\cup_{i=1}^{\infty} \overline{E_i})$. 

Since $\overline{E_1}, \overline{E_2}, ..., \overline{E_i}$ are mutually exclusive (Proved in question (b)(ii)), by Axiom 3, $P(\cup_{i=1}^{\infty} \overline{E_i}) = \sum_{i = 1}^{\infty} P(\overline{E_i})$

Proved in questions (b)(i), $\overline{E_i} \subset E_i, \forall i \ge 1$. Therefore, $P(\overline{E_i}) \le P(E_i), \forall i \ge 1 \Rightarrow \sum_{i = 1}^{\infty} P(\overline{E_i}) \le \sum_{i = 1}^{\infty} P(E_i)$

In conclusion, $P(\cup_{i=1}^{\infty} E_i) = P(\cup_{i=1}^{\infty} \overline{E_i}) = \sum_{i = 1}^{\infty} P(\overline{E_i}) \le \sum_{i = 1}^{\infty} P(E_i)$

Simplify as $P(\cup_{i=1}^{\infty} E_i) \le \sum_{i = 1}^{\infty} P(E_i)$

### (d)

(1)

Based on the definition of $Q_i \rightarrow Q_i = P(\cap_{n=i}^\infty E_n^c)$

$\because P(\cap_{n=i}^\infty E_n^c) = 1 - P(\cup_{n=i}^\infty E_n)$

$\because P(\cup_{n=i}^{\infty} E_n) \le \sum_{n = i}^{\infty} P(E_n)$ (Boole's Inequality proved in part c)

$\therefore Q_i = 1 - P(\cup_{n=i}^\infty E_n) \ge 1 - \sum_{n = i}^{\infty} P(E_n) \ge 1 - (\sum_{n = 1}^{\infty} P(E_n) - \sum_{n = 1}^{i} P(E_n))$

$\because \sum_{n = 1}^{\infty} P(E_n) < \infty$

$\therefore \lim_{i \rightarrow \infty} Q_i = 1$

(2)

If $P(E_i) \le \frac{c}{i^k}, c > 0, k > 1$, then

$\sum_{i = 1}^{\infty} P(E_i) = c(1+ \frac{1}{2^k} + \frac{1}{3^k} + ....)$

$ = c (1 + \int_1^\infty \frac{1}{x^k} \mathrm{d}x)$

$ = c (1 + \frac{x^{-k+1}}{-k+1}) |_{i}^\infty$

$ = c + \frac{c}{1-k} = c \cdot \frac{k}{k-1} < \infty$

$\therefore \sum_{n = 1}^{\infty} P(E_n) < \infty \rightarrow \lim_{i \rightarrow \infty} Q_i = 1$ (Proved in part 1)