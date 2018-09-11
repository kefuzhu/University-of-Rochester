# CSC 482 HW#1 Problem 1.2
## Kefu Zhu, kzhu6

**Objective**:

We are given an $n \times n$ array $A$ of zeros and ones. We want to find the size of the largest contiguous all-ones square. Give an $O(n2)$-time algorithm for the problem. 

*Hint*: let $B[i; j]$ be the side-length of the largest square whose bottom-right corner is at position $i, j$.

**Define**:

- $A$ = a matrix of $n \times n$ of zeroes and ones
- $B[i,j]$ = the side-length of the largest square whose bottom-right corner is at position $i, j$ in matrix A

**Sudo code**:

```
# Base case

# B[i,j] = A[i,j] for i,j in the first row and first column of matrix A
# First column
for i from 1 to n:
    B[i,1] = A[i,1]
# First row
for j from 1 to n:
    B[1,j] = A[1,j]

# Dynamic Programming

# For the rest of cells in matrix
for i from 2 to n:
    for j from 2 to n:
        # When A[i,j] = 1, if the top(B[i-1,j]), left(B[i,j-1]), top-left(B[i-1,j-1]) 
        # cells of A[i,j] are all 1, then a 2x2 square of ones is formed. 
        # Same logic for 3x3, 4x4, and etc.
        if A[i,j] = 1:
            B[i,j] = 1 + min(B[i,j-1],
                             B[i-1,j],
                             B[i-1,j-1])
        else: # A[i,j] = 0
            B[i,j] = 0

The size of the largest contiguous all-ones square for matrix A with n*n arrays is:

(max(B[i,j]))^2, for i from 1 to n, j from 1 to n
```
---

**Python code**:

```python
def maxOneSize(A):
    
    # Initialize the matrix B
    B = np.matrix(np.zeros((len(A),len(A))))
    # Copy the value from first row and first column from input matrix A
    for i in range(0, len(A)):
        B[i,0] = A[i,0] # First column
        B[0,i] = A[0,i] # First row
    
    # Dynamic programming for the rest of cells in matrix A
    for i in range(1, len(A)):
        for j in range(1, len(A)):
            if A[i,j] == 1:
                B[i,j] = 1 + min(B[i,j-1], B[i-1,j], B[i-1,j-1])
            else:
                B[i,j] = 0
    
    # Answer
    return (B.max())**2
```
```python
# Test case
A = np.matrix(np.random.randint(2, size = (10,10)))
A
```
```
matrix([[1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0]])
```
```python
maxOneSize(A) # Output: 4.0
```