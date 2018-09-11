# CSC 482 HW#1 Problem 1.3

## Kefu Zhu, kzhu6

# Problem 1.3

**Objective**:

A shuffle of two strings $A,B$ is formed by interspersing the characters into a new string,
keeping the characters of $A$ and $B$ in the same order (for example, `several` is a shuffle of `seal` and `evr`). 

Given three strings $A = a_1, ..., a_n$, $B = b_1, ..., b_m$, and $C = c_1, ..., c_{m+n}$, we would like to verify whether $C$ is a shuffle of $A$ and $B$. Give a dynamic programming algorithm for the problem

**Define**:

- $A = a_1, a_2, ..., a_n$
- $B = b_1, b_2, ..., b_m$
- $C = c_1, c_2, ..., c_{m+n}$
- $T[i,j]$ = the True/False answer for whether $c_1, c_2, ..., c_{i+j}$ is a shuffle of $a_1, a_2, ..., a_i$ and $b_1, b_2, ..., b_j$

**Sudo code**

```
# Base case

T[1,0] = True # A contains one letter, B is empty -> Shuffle of one letter -> Must be TRUE
T[0,1] = True # B contains one letter, A is empty -> Shuffle of one letter -> Must be TRUE
T[1,1] = True # A contains one letter, B contains one letter -> Shuffle of two letters -> Must be TRUE

# Dynamic Programming
for i from 2 to n:
    for j from from 2 to m:
        # Three cases
        
        # Given T[i-1,j-1] is TRUE
        # Adding both the ithe letter from A, and the jth letter from B
        if T[i-1,j-1] == TRUE:
            # If the last two letter in current C (C[i+j-1] and C[i+j-2]), is the shuffle of 
            # ith letter in A (A[i]) and the jth letter in B (B[j])
            if (C[i+j-1] == A[i] AND C[i+j-2] = B[j])
               OR
               (C[i+j-1] == B[j] AND C[i+j-2] = A[i]):
               # Then the T[i,j] is also TRUE
               T[i,j] = TRUE
        
        # Given T[i-1,j] is TRUE
        # Adding the ith letter from A
        if T[i-1,j] == TRUE:
            
                

```
---

**Python code**:

```python
def maxSum(numlist):
    # Initialize an empty list to store the maximum sum of subarray numlist[0..i], such that no three elements are consecutive
    _sum = [None]*len(numlist)
    
    # Initialization of basic scenarios
    if len(numlist) >= 1:
        _sum[0] = numlist[0]
    if len(numlist) >= 2:
        _sum[1] = numlist[0] + numlist[1]
    # Base case: we have three consecutive elements at the first time
    if len(numlist) > 2:
        _sum[2] = max(numlist[0]+numlist[1], 
                      numlist[0]+numlist[2],
                      numlist[1]+numlist[2])
    # Dynamic programming for the rest of elements
    for i in range(3, len(numlist)):
        _sum[i] = max(_sum[i-1],
                      _sum[i-2] + numlist[i],
                      _sum[i-3] + numlist[i-1] + numlist[i]
                     )
        # Increment the index
        i += 1
    
    # Return the max sum given all elements in the input list
    return _sum[-1]
```

```python
# Test cases
num_list1 = [5,5,8,5,5]
num_list2 = [5,5,12,5,5]
num_list3 = [1,2,2,1,2,1,2,5,5]
```

```python
maxSum(num_list1) # Output: 20
maxSum(num_list2) # Output: 22
maxSum(num_list3) # Output: 17
```