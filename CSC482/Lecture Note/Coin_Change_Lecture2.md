# Lecture 2 ☀️ Thuesday, September $4^{th}$, 2018
---
## Coin change problem

### 1. Unlimited supply

**INPUT**: $C_1, ..., C_k$ positive integers. $A$ positive integer to pay

- Minimize $\sum_{} X_j$
- $\sum_{} X_jC_i = A$
- $\forall X_j \ge 0$, integer

#### Scenario 1

**INPUT**: $C_i \in \{1, 3, 10\}$, $A = 12 \rightarrow 2, 0, 1$ (2 of $\$1$, 0 of $\$3$, 1 of $\$10$)

#### Scenario 2

**INPUT**: $C_i \in \{1, 5, 11\}$, $A = 15 \rightarrow 0, 3, 0$ (Idea is the same as above)

**Objective**: Find optimal solution for every amount in $\{0, 1, 2, ..., A\}$

$S[a] = $ minimal number of coins to pay for amount $a$, $\exists a \in S[0, 1, 2, ..., A]$

   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 ...
---|---|---|---|---|---|---|---|---|---|---|----|----|----|
$S$| 0 | 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 | 5 | 2  | 1  | ...

* Suppose we already know $S[0], S[1], ..., S[a-1]$, we can then compute $S[a]$ as following:

$S[a] = 1 + \min S[a - C_i]$ where $i = \{1, 2, ..., k\}$ and $C_i \le a$ 

(1) $S[a] \le 1 + S[a-C_i], \forall i \in \{1,2,...,k\}$ AND $C_i \le a$

- Interpretation: If you can pay $a-C_i$ amount using $S[a-C_i]$ coins, then you can pay $a$ amount using **at least** $1 + S[a-C_i]$ coins

(2) Suppose the optimal solution to pay amount $a$ uses coin of value $C_i$, then:

$S[a] = 1 + S[a-C_i]$

##### Sudo code, runtime = $O(A \cdot k)$:
```
for a from 1 to A do:
	for i from 1 to k:
		S[a] = 1 + min(S[a-Ci])
```

##### Python code:
```python
# Choices of coins
coinList = [1, 5, 11]
```
```python
def coinChange_unlimited(A, coins):
    '''
    Input:
    This function takes in two parameters A and coins
    1. A is the amount of money need to change
    2. coins is a list of numbers contains possible value of coins that can be used for 
       the coin change problem
    
    Output: A list contains the least number of coins needed to change any integer amount of value
            that is smaller than A
    '''
    # Initialize the solution list
    S = [None]*(A+1)
    # Initialize the zero index (0 coin is needed for the change of $0)
    S[0] = 0
    
    # Iterate through all possible value <= A
    for a in range(1,A+1):
        # Iterate through choices of coins for change
        for i in range(len(coins)):
            # If the current choice of coin is smaller than the amount need to be paid
            if a-coins[i] >= 0:
                # If the current amount coin change problem does not have any solution
                if S[a] is None:
                    # Add the current solution (# of coins used for change) to the solution list
                    S[a] = 1 + S[a-coins[i]]
                # If the current amount coin change problem already have a solution
                else:
                    # If the original solution is better than the current one. Make no changes
                    if S[a] <= 1 + S[a-coins[i]]:
                        pass
                    # If the original solution is worse than the current one. Substitue it with the current one.
                    else:
                        S[a] = 1 + S[a-coins[i]]
    # Return the solution list
    return S
```
```python
solution = coinChange_unlimited(15,coinList)
solution # [0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 2, 1, 2, 3, 4, 3]
```
```python
solution[15] # The least number of coins needed to change for $15
```

Now that we computed the values of optimal solution for $a \in \{0, 1, ..., A\}$. The solution for unlimited coin change on amount $A$ will be the following:

```
# Define P[a] = min(S[a-Ci])

def PrintSolution(a):
	if a = 0, then return 0
	else print("use coins of value ", C[P[a]]) # This might not be correct. Don't take it too serious
		PrintSolution(a-C[P[a]])
```
### 2. Limited supply

#### Scenario 1

**INPUT**: $C_1, ..., C_k$ positive integers. $A$ positive integer to pay

**OBJECTIVE**: Can you pay the exact amount $A$?

**Define**:

- $a = \{0, 1, ..., A\}$
- $l = \{0, 1, ..., k\}$
- $T[a,l]$ = 
  - **True**, if we can pay amount of $a$ using a subset of coins from $C_1, ..., C_l$
  - **False**, otherwise

##### Example:

**INPUT**: $1,1,5,10,10,25,25$ ($k = 5$)

(1) $T[7,2]$ = **False**, $1+1 < 7$

(2) $T[7,4]$ = **True**, $1+1+5=7$ 

(3) $T[37,5]$ = **False**, $1+1+5+10+10 < 37$

(4) $T[37,6]$ = **True**, $1+1+10+25 = 37$

##### Summary

1. If $T[a, l-1]$ is true $\Rightarrow T[a,l]$ is true

  - **Interpretation**: If you can pay $a$ with the first $l-1$ coins, then you can definitely pay $a$ with the first $l$ coins.

2. If $T[a-C_l, l-1]$ is true $\Rightarrow T[a,l]$ is true

  - **Interpretation**: If you can pay $a-C_l$ with the first $l-1$ coins, then you can definitely pay $a$ with the first $l$ coins. Because the only difference can be filled with the $l$th coin.
 
3. Therefore, $T[a, l]$ is equal to either of the following:

  - If uses the last coin ($C_l$) to pay $a$, then $T[a,l] = T[a-C_l, l-1]$
  - If does NOT use the last coin to pay $a$, then $T[a,l] = T[a, l-1]$

##### Sudo code
```
for l from 1 to k:
	for a from 0 to A:
		T[a,l] = T[a, l-1] OR T[a-Cl, l-1]
```

#### Scenario 2

**Define**: Can you pay the exact amount $A \Rightarrow T[A,k]$ 

  - $T[a,l]$ = minimum number of coins to pay $a$ with a subset of coins from $C_1,...,C_l$

**OBJECTIVE**: minimum number of coins needed to pay amount $A$

##### Summary

$T[a,l] = \min (T[a,l-1], T[a-C_l,l-1]+1)$

- If optimial solution does NOT use $C_l$, then $T[a,l] = T[a,l-1]$
- If optimal solution does use $C_l$, then $T[a,l] = 1+T[a-C_l,l-1]$ 

#### Sudo code
```
for l from 1 to k:
	for a from 0 to A:
		T[a,l] = min (T[a,l-1], 1+T[a-Cl,l-1])
```

- **Initialization** of $T[a,0]$:
  - 0, if $a=0$
  - $\infty$, otherwise

#### Scenario 3

$T[a,l]$ = maximum number of coins to pay $a$ with a subset of coins from $C_1,...,C_l$

#### Sudo code
```
for l from 1 to k:
	for a from 0 to A:
		T[a,l] = max (T[a,l-1], 1+T[a-Cl,l-1])
```

- **Initialization** of $T[a,0]$:
  - 0, if $a=0$
  - $-\infty$, otherwise
