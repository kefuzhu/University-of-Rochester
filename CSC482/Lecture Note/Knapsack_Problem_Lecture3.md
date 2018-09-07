# Lecture 3 ☀️ Thursday, September $6^{th}$, 2018
---
## Knapsack problem

**INPUT**: $v_1, v_2, ..., v_n$ and $w_1, w_2, ..., w_n$ are positive integers

- $v_i$ = the value of $ith$ item
- $w_i$ = weight of $ith$ item
- $L$ = weight limit

**OUTPUT**: the subset of the items that has maximize the total value and fits in the weight limit

- $\max \sum_{i \in S} v_i$
- $S \subseteq \{1,2,...,n\}$
- $\sum_{i \in S} w_i \le L$

Suppose we sort the items by $\frac{v_i}{w_i}$ in decreasing order and then greedily take the items $\Rightarrow$ Will this always yield optimal solution?

**Example A**

Assumptions: {\$10: 1lb, \$5: 3lb, \$7: 2lb, \$1: 5lb, \$6: 7lb}

- $L$ = 5lb
- $\frac {v_i}{w_i}$ = {10, 1.66, 3.5, 0.2, 0.8}

(1) Greedy approach: \$10 + \$7 = \$17, 1lb + 2lb = 3lb

(2) Optimal apprach: Same as the greedy approach

**Example B**

Assumptions: {\$5: 1lb, \$6: 3lb, \$7: 2lb, \$1: 5lb, \$6: 7lb}

- $L$ = 5lb
- $\frac {v_i}{w_i}$ = {5, 2, 3.5, 0.2, 0.8}

(1) Greedy approach: \$5 + \$7 = \$12, 1lb + 2lb = 3lb

(2) Optimal apprach: \$6 + \$7 = \$13, 3lb + 2lb = 5lb

*Greedy approach is not optimal in this case!*

### Solution

**Define**: $T[l,i]$ = the maximum value of a subset of the first $i$ items (items $1,2,...,i$) whose weight does not exceed $l$

$
T[l,i] = \max
\begin{cases}
T[l,i-1],\\
T[l-w_i,i-1] + v_i\\
\end{cases}
$

#### Sudo code: runtime = $O(n \cdot L)$

```
for l from 0 to L do:
	T[l,0] = 0 # Initialization
		for i from 1 to n do:
			for l from 0 to L do:
				T[l,i] <- T[l,i-1]
				if wi <= l, then T[l,i] <- max(T[l,i-1], T[l-wi,i-1]+vi)
```

Run sudo code on example

- $n = 3, L = 5$
- $v_1 = 5$, $w_1 = 1$
- $v_2 = 6$, $w_2 = 3$
- $v_3 = 7$, $w_3 = 2$

$i,l$| 0 | 1 | 2 | 3 | 4 | 5 
-----|---|---|---|---|---|---
  0  | 0 | 0 | 0 | 0 | 0 | 0 
  1  | 0 | 5 | 5 | 5 | 5 | 5 
  2  | 0 | 5 | 5 | 6 | 11| 11
  3  | 0 | 5 | 7 | 12| 12|==13==
  
**Answer**: $T[5,3] = 13$

#### Python code for example above
```python
# Item list
v = [5,6,7]
# Weight list
w = [1,3,2]
```
```python
def knapsack(L,v,w):
    '''
    This is a function to solve knapsack problem
    
    Input:
    This function takes in 4 parameters:
    1. L is the weight limit
    2. v is a list, containing all item value
    3. w is a list, containing all weights associated with corresponding item
    
    Output:
    A matrix:
    1. Columns indicate all possible weight limit (l) that is smaller or equal to L.
    2. Rows indicate all possible subset of first ith item where i is smaller or equal to the total number of items (n)
    3. Each cell indicate the maximum total value that can be achieved using the first ith item and does not exceed l
    '''
    # Number of items
    n = len(v)
    # Initialize the output matrix
    T = np.zeros([n+1, L+1]) # +1 is for the zero column and row
    
    for l in range(0, L+1): # +1 because range() exclude the last number
        # Initialize values when i is zero
        T[0,l] = 0 # Maximum value of a subset of the firt zero items is zero

    # Iterate through all possible combination of i and l where i <= n and l <= L
    for i in range(1, n+1):
        for l in range(0, L+1):
            # Fill the current slot with the result using i-1 item
            # Assuming we cannot use the ith item (Worst case)
            T[i,l] = T[i-1,l]
            # If it might be possible to use the ith item
            if w[i-1] <= l: # w[i-1] to accommodate list starting from 0 index
                # Find the larger value and substitue the original value in the slot
                T[i,l] = max(T[i-1,l],T[i-1,l-w[i-1]]+v[i-1]) # w[i-1],v[i-1] to accommodate list starting from 0 index
    
    return T
```
```python
optimal = knapsack(5,3,v,w)
optimal
```
**Output**

```
array([[ 0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  5.,  5.,  5.,  5.,  5.],
       [ 0.,  5.,  5.,  6., 11., 11.],
       [ 0.,  5.,  7., 12., 12., 13.]])
```
```python
# The maximum value of a subset of the first 3 items whose weight does not exceed 5
optimal[3,5] 
# Notice that optimal[3,5] = T[i,l] defined in code = T[l,i] defined in problem
```
**Output**: `13.0`

----
### Suppose that values are small integers and weights are large integers. Can we get a better algorithm in this scenario?

Transform the original question:

- The maximum value ($T[L,i]$) of a subset of the first $i$ items whose weight does not exceed $L$

$\Rightarrow$

- The minimum weight ($S[i,v]$) of a subset of the first $i$ items whose total value is at least $v$

Where, $L = S[i,v]$ and $v = T[L,i]$

**In this case, we only need to construct the matrix based on $i$ (number of items) and $v$ (total value). The $w$ (weight) will be the value inside each cell. Therefore, we can bypass the curse of dimensionality of large weights by not constructing super large matrix in memory.**

**Define**: 

- $S[i,v]$ = minimum weight of a subset of the first $i$ items whose total value is at least $v$
- Let $S[i,v] = \infty$, if total value of first $i$ items is less than $v$
- $\hat{V} = \sum v_i$

$
S[i,v] = \min
\begin{cases}
S[i-1,v],\\
S[i-1,v-v_i] + w_i\\
\end{cases}
$

#### Sudo code

```
# Initialization
S[0,0] = 0

for v from 1 to V_hat do:
	S[0,v] <- positive infinity

for i from 1 to n do:
	for v from 0 to V_hat do:
		S[i,v] <- S[i-1,v]
		if v_i >= v, then S[i,v] <- min(S[i,v], w_i)
		else S[i,v] <- min(S[i,v]. S[i-1,v-v_i] + w_i)
```

**Example**:

- $w_1 = 1$, $v_1 = 2$
- $w_2 = 3$, $v_2 = 3$
- $w_3 = 2$, $v_3 = 4$

$i,v$| 0 |   1    |   2    |   3    |   4    |   5    |   6    | ==7==  |   8    |   9
-----|---|--------|--------|--------|--------|--------|--------|--------|--------|--------
  0  | 0 |$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$
  1  | 0 |   1    |   1    |$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$|$\infty$ 
  2  | 0 |   1    |   1    |   3    |   4    |   4    |$\infty$|$\infty$|$\infty$|$\infty$     
  3  | 0 |   1    |   1    |   2    |   2    |   3    |   3    | ==5==  |   6    |   6 

If $L=5$, then find $S[i,v]=5 \rightarrow S[3,7] = 5 \rightarrow v = 5 = T[l,i]$

$\Rightarrow$ The maximum value of a subset of the first 3 items whose weight does not exceed 5 is 7

#### Python code
```python
# Value list
V = [2,3,4]
# Weight list
w = [1,3,2]
```
```python
def knapsack_v2(V,w):
    '''
    This is a function to solve knapsack problem. Especially when we have 
    * Small values
    * Large weights
    
    Input:
    This function takes in 2 parameters:
    2. V is a list, containing all item value
    3. w is a list, containing all weights associated with corresponding item
    
    Output:
    A matrix:
    1. Columns indicate all possible total value (v) for a given value list, V
    2. Rows indicate all possible subset of first ith item where i is smaller or equal to the total number of items (n)
    3. Each cell indicate the minimum weights that can be achieved using the first ith item and has total value at least v
    '''
    # Number of items
    n = len(V)
    # All possible total value
    V_hat = sum(V)
    # Initialize the output matrix
    S = np.zeros([n+1, V_hat+1]) # +1 is for the zero column and row
    
    for v in range(1, V_hat+1): # +1 because range() exclude the last number
        # Initialize weight when we have zero items
        S[0,v] = np.inf # Set the weight to positive infinity because that indicate impossible 
                        # and will always be greater than any real solution
    
    for i in range(1, n+1):
        for v in range(0, V_hat+1):
            # Fill the current slot with the result using i-1 item
            # Assuming we cannot use the ith item (Worst case)
            S[i,v] = S[i-1,v]
            # If we might be able to use the ith item alone to fulfill the requirement
            if V[i-1] >= v: # v[i-1] to accommodate list starting from 0 index
                S[i,v] = min(S[i,v], w[i-1]) # w[i-1] to accommodate list starting from 0 index
            # Otherwise
            else:
                S[i,v] = min(S[i,v], S[i-1, v-V[i-1]] + w[i-1]) # v[i-1], w[i-1] to accommodate list starting from 0 index
    
    return S
```
```python
optimal_v2 = knapsack_v2(V,w)
optimal_v2
```
**Output**

```
array([[ 0., inf, inf, inf, inf, inf, inf, inf, inf, inf],
       [ 0.,  1.,  1., inf, inf, inf, inf, inf, inf, inf],
       [ 0.,  1.,  1.,  3.,  4.,  4., inf, inf, inf, inf],
       [ 0.,  1.,  1.,  2.,  2.,  3.,  3.,  5.,  6.,  6.]])
```
```python
# If the weight limit is 5, what is the maximum total value that can be reached using the given item list
np.where(optimal_v2==5)[1]
# Notice that the answer will only exist in the last row. Because you have all the items to choose only in last row
```

**Output**: `array([7])`