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

**Recursion**:

$
T[i,j] =
\begin{cases}
T[i-1,j], \ if \ A[i-1] = C[i+j-1] \ and \ B[j-1] \ne C[i+j-1]\\
T[i,j-1], \ if \ B[j-1] = C[i+j-1] \ and \ A[i-1] \ne C[i+j-1]\\
T[i,j-1] \ or \ T[i-1,j], \ if \ A[i-1] = C[i+j-1] \ and \ B[j-1] = C[i+j-1]\\
\end{cases}
$


**Sudo code**

```
# Dynamic Programming
for i from 0 to m:
    for j from 0 to n:
        ## Base case
        
        # Both A and B are empty string, 
        # then the shuffle of empty string must be True for any C
        T[i,j] = True
        
        ## Six cases
        
        # (1) If A is empty, and the current letter in B (B[j-1]) is the same as 
        #     j-1 letter in C (C[j-1])
        
        if i == 0 and B[j-1] == C[j-1]:
            T[i,j] = T[i,j-1]
        
        # (2) If B is empty, and the current letter in A (A[j-1]) is the same as 
        #     i-1 letter in C (C[i-1])
        
        else if j == 0 and A[i-1] == C[i-1]:
            T[i,j] = T[i-1,j]
            
        # (3) Both A and B is not empty, letter in C matches only with the current letter in A
        else if (A[i-1] == C[i+j-1]) & (B[j-1] != C[i+j-1]):
            T[i,j] = T[i-1,j]
            
        # (3) Both A and B is not empty, letter in C matches only with the current letter in B 
        else if (B[j-1] == C[i+j-1]) & (A[i-1] != C[i+j-1]):
            T[i,j] = T[i,j-1]
        
        # Both A and B is not empty, 
        # letter in C matches with both the current letter in A and in B
        else if (A[i-1] == C[i+j-1]) & (B[j-1] == C[i+j-1]):
            T[i,j] = (T[i,j-1] | T[i-1,j])
        
        # None of the above condition is met
        else:
            T[i,j] = False
```

---

**Python code**:

```python
def isInterleaved(A,B,C):
    '''
    A = list of letters a1,a2, ..., an
    B = list of letters b1,b2, ..., bm
    C = list
    '''
    # Get the value of m and n
    m = len(A)
    n = len(B)
    # Initialize the matrix of T to all False
    T = np.matrix(np.reshape(np.array([False]*(m+1)*(n+1)),(m+1,n+1)))
    
    # Dynamic Porgramming
    for i in range(0,m+1):
        for j in range(0,n+1):
            # Both A and B are empty
            if (i == 0) & (j == 0):
                T[i,j] = True
            # A is empty, so we only need to match letters in B with letter in C one by one
            elif (i == 0) & (B[j-1] == C[j-1]):
                T[i,j] = T[i,j-1]
            # B is empty, so we only need to match letters in A with letter in C one by one
            elif (j == 0) & (A[i-1] == C[i-1]):
                T[i,j] = T[i-1,j]
            # Both A and B is not empty
            # letter in C matches only with the current letter in A
            elif (A[i-1] == C[i+j-1]) & (B[j-1] != C[i+j-1]):
                T[i,j] = T[i-1,j]
            # Both A and B is not empty
            # letter in C matches only with the current letter in B
            elif (B[j-1] == C[i+j-1]) & (A[i-1] != C[i+j-1]):
                T[i,j] = T[i,j-1]
            # Both A and B is not empty
            # letter in C matches with both the current letter in A and in B
            elif (A[i-1] == C[i+j-1]) & (B[j-1] == C[i+j-1]):
                T[i,j] = (T[i,j-1] | T[i-1,j])
            else:
                T[i,j] = False
            
    # Show the memory matrix
    print("The matrix of T: \n")
    print(T)
    # Return the result
    return T[m,n]
```

```python
# Test cases
A = ['s','e','a','l']
B = ['e','v','r']
C = ['s','e','v','e','r','a','l']
```

```python
isInterleaved(A,B,C) 
```

```
The matrix of T: 

[[ True False False False]
 [ True  True  True False]
 [ True False  True  True]
 [False False False  True]
 [False False False  True]]
 
True
```