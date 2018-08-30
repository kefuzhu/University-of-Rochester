# Lecture 1 ☁️ 💨 Thursday, August $30^{th}$, 2018
---
## Asymptotic notation

$f(n) = O(g(n)) \Longleftrightarrow (\exists C)(\forall n) f(n) \le C \cdot g(n) $

1. $n = O(n^2)$, **TURE**

	*Proof* : take $C = 1, (\forall n): n^2 \le C \cdot n$  
	
2. $n^2 = O(n)$, **FALSE**
	
	*Proof* : suppose for some $C \gt 0$, we have $(\forall n)\cdot n^2 \le C \cdot n$. If we take $n \ge 2C$, then $(2C)^2 not \le 2C^2$

3. $log(n) = O(n)$, **TRUE**

	*Proof* : take $C = 1$, claim $(\forall n) log(n) \le n$ 
	
	- $log(n)^{100} = O(n)$, **TRUE**
	
		*WANT* : $log(n)^{100} \le C \cdot n$
			
		*Proof* : $100 \cdot log(log(n)) \le log(C) + log (n)$, set $t = log(n)$ 
		
		$\to 100 \cdot log(t) \le log(C) + t \to 100 \cdot log(t) -t \le log(C)$
		
		Because as t increases, $100 \cdot log(t) - t$ will increase to reach a peak (maximum value) and drops down to $-\infty$, so I claim that there must exist a $C$ such that the $log(C)$ has the same value as the peak.
	
4. $f(n) = O(f(n-1))$ for $\forall n \gt 2$

- $f(n) = n$, **TRUE**, *Proof* : take $C = 2$
- $f(n) = n^2$, **TRUE**, *Proof* : take $C = 2$
- $f(n) = 2^n$, **TRUE**, *Proof* : take $C \gt 2$
- $f(n) = n!$, **FALSE**, *Proof* : $n! \le C \cdot (n-1)! \to n \le C$ for $\forall C$

## Coin Change Problem
Fixed coin denominations

**INPUT**: amount $A$ to be paid

**OBJECTIVE**: minimize the number of coins used for the change

---

### Scenario A: denominations are $1, 5 ,10, 20$

**Solutions**:

$C_1 < C_2 ... < C_k$, here $k = 4, C_1 = 1, C_2 = 5, C_3 = 10, C_4 = 20$

Sudo code:

```
for l from k to 1:
	print( A mod Cl)
	A <- A - Cl * (A mod Cl)
```

Prove optimal solution is the greedy algorithm:

- Optimal solution: Suppose $X_1, X_2, X_3, X_4$ is an optimal way of paying $A$

	$A = X_1 \cdot 1 + X_2 \cdot 5 + X_3 \cdot 10 + X_4 \cdot 20$
	
	(1) $0 \le X_3 \le 1$
	
	(2) $0 \le X_2 \le 1$
	
	(3) $0 \le X_1 \le 4$
	
	Therefore, $X_1 + 5X_2 + 10X_3 \le 19 \Rightarrow X_4 = A \bmod 20 = g_4 $
	 
	- Similar process recursivley for the remaining amount

**Conclusion**: Since the optimal solution acts the same as the greedy solution, so the greedy solution is the optimal one

### Scenario B: denominations are $1, 5 ,11$

The greedy solution is not optimal in this case. Real solution will be discussed in the future.

**Counter example**: 

Suppose $A$ is 20, the optimal solution will be

$20 = 5 + 5 + 5 + 5$, which uses 4 coins

but the greedy solution is

$20 = 11 + 5 + 1 + 1 + 1 + 1$, which uses 6 coins


### Scenario C: denominations are $1, 3, 7$

The greedy solution is optimal

*Proof* : $A = X_1 + 3X_2 + 7X_3$

The optimal solution will be uses the most 7's

(1) $0 \le X_2 \le 2$

(2) $0 \le X_1 \le 2$

Therefore, $X_1 + 3X_2 \le 8$. But since we can use 7 whenever we are paying 8, so the $X_1 + 3X_2$ is actually $\le 6$