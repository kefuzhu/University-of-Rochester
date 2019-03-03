# Lecture 9, Monday, 02/18

### Topics: 
- Hidden Markov Model (HMM) 
	- Viterbi Algorithm

### YouTube Resources

**mathmaticalmonk**

- [Viterbi Algorithm - part 1](https://www.youtube.com/watch?v=RwwfUICZLsA&index=105&list=PLD0F06AA0D2E8FFBA)
- [Viterbi Algorithm - part 2](https://www.youtube.com/watch?v=t3JIk3Jgifs&list=PLD0F06AA0D2E8FFBA&index=106)

**Recall: Known Parameters**

1. **Initial Distribution**: $\pi(i) = P(Z_1 = i), i \in \{1,2,...,m\}$
2. **Transition Probability (Matrix)**: $T(i,j) = P(Z_t = j\ |Z_{t-1} = i), i,j \in \{1,2,...,m\}$
3. **Emission Probability**: $\epsilon_i(x) = P(x|Z_t = i), i \in \{1,2,...,m\}$

**Goal**: 

Compute 

<center>
$Z^* = arg\max_{Z_{1:T}}\ P({Z_{1:T}}|X_{1:T})$
</center>

which is equivalent to saying what is the sequence of hidden states $Z^* = \{Z_1^*,Z_2^*,...,Z_T^*\}$ that maximizes the probability of seeing the observed values $X_{1:T} = \{X_1,X_2,...,X_T\}$

**Note**: $arg\max_{Z_{1:T}}\ P(Z|X) \propto arg\max_{Z_{1:T}}\ P(Z, X)$

First we consider computing the maximum probability, $\max_{Z_{1:T}} P({Z_{1:T}}, X_{1:T})$. 

Define 

<center>
$\delta(t,i) = \max_{Z_{1:t-1}} P(Z_t = i, Z_{1:t-1}, X_{1:t})$
</center>

which is saying what is the sequence of hidden states $\{Z_1,Z_2,...,Z_{t-1}\}$ that maximizes the probability of seeing the observed values $\{X_1,X_2,...,X_t\}$ when the hidden state at time $t$ is at state $i$, $Z_t = i$

We can marginalize $\delta(t,i)$ like this

$\delta(t,i) = \max_{Z_{1:t-1}} P(Z_t = i|Z_{t-1} = j)P(X_t|Z_t = i)P(Z_{t-1} = j, Z_{1:t-2}, X_{1:t-1})$, $j \in \{1,2,...,m\}$

**Base case:** $t = 1$

$\delta(1,i) = P(Z_1 = i, X_1) = P(Z_1 = i) \cdot P(X_1|Z_1 = i)$

where

- $P(Z_1 = i)$ is known from the **initial distribution**
- $P(X_1 | Z_1 = i)$ is known from the **emission probability**

**Dynamic Programming (Recursion)::** $t = 2,3,...,T$

**Remark**: If we have $f(a), g(a,b)$ that have the same sign $\forall a,b$, then

<center>
$\max_{a,b} f(a)g(a,b) = max_a[f(a)max_b(g(a,b))]$
</center>

So we can separate the $\max$ into two parts

$\delta(t,i) = \max_{Z_{1:t-1}} P(Z_t = i, Z_{1:t-1}, X_{1:t})$

$= \max_{Z_{1:t-1}} P(Z_t = i|Z_{t-1} = j)P(X_t|Z_t = i)P(Z_{t-1} = j,Z_{1:t-1}, X_{1:t-1})$

$= \max_{Z_{t-1}} [P(Z_t = i|Z_{t-1} = j)P(X_t|Z_t = i) \max_{Z_{1:t-2}} P(Z_{t-1} = j,Z_{1:t-2}, X_{1:t-1})]$

$= \max_j [P(Z_t = i|Z_{t-1} = j) \cdot P(X_t|Z_t = i) \cdot \delta(t-1,j)]$

where

- $P(X_t | Z_t = i)$ is known from the **emission probability**
- $P(Z_t = i|Z_{t-1} = j)$ is known from the **transition matrix**

In order to find the sequence of hidden states that maximizes the probability, we only need to keep track the value of states, namely the value of $j$ in $Z_{t-1} = j$, that gives max value for each time step

<center>
$\psi(t,i) = arg\max_j [P(Z_t = i|Z_{t-1} = j) \cdot P(X_t|Z_t = i) \cdot \delta(t-1,j)]$
</center>

Hence the best value of state at time $t$ is $Z_{VIT,t} = \psi(t+1, Z_{VIT,t+1})$

**Sudo-code**

```
# Base case
δ(1,i) = P(Z1=i)⋅P(X1|Z1=i)

# Recursion
For t from 2 to T
	for i from 1 to m
		δ(t,i) = max_j P(Zt = i|Zt-1 = j)⋅P(Xt|Zt = i)⋅δ(t-1,i)
		ψ(t,i) = argmax_j [P(Zt=i|Zt−1=j)⋅P(Xt|Zt=i)⋅δ(t−1,j)]
```