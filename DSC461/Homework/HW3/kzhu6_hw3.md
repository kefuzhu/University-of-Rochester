# DSC 461, HW#3, Kefu Zhu

## Problem 1

(1) **Initialize Matrix S**

|  | A | B | C | D | E |
|:---:|:---:|:----:|------|------|------|
| $R_1$ | $a_1$ | $a_2$ | $a_3$ | $b_{14}$ | $b_{15}$ |
| $R_2$ | $a_1$ | $b_{12}$ | $b_{13}$ | $a_4$ | $a_5$ |

(2) **Apply FD**

|  | A | B | C | D | E |
|:---:|:---:|:----:|------|------|------|
| $R_1$ | $a_1$ | $a_2$ | $a_3$ | $a_4$ | $a_5$ |
| $R_2$ | $a_1$ | $a_2$ | $a_3$ | $a_4$ | $a_5$ |

Because both rows are made up entirely of $a$ symbols, the decomposition is a lossless-join

## Problem 2

### Write an SQL query to test whether the functional dependency $b \rightarrow c$ holds on relation r

```sql
SELECT IF((SELECT COUNT(*) 
		   FROM r AS r1, r AS r2 
    	   WHERE r1.b = r2.b AND r1.c != r2.c) 
    	   = 0),
	       'Functional dependency of b to c holds.',
	       'Functional dependency of b to c DOES NOT hold.');
```

### Write an SQL assertion that enforces the functional dependency. Assume that no null values are present

```sql
CREATE ASSERTION FD_b_to_c
CHECK (NOT EXISTS (SELECT * 
		   		   FROM r AS r1, r AS r2 
    	           WHERE r1.b = r2.b AND r1.c != r2.c
    	          ));
```

## Problem 3

### What are all the keys for Courses?

(1) **Initialize K**

$K = \{C, T, H, R, S, G\}$

(2) **For each attribute in K, determine whether it can be determined by the rest of attributes**

- $C$ can be determined by $HR$, remove $C$ from $K$. Reset $K = \{T, H, R, S, G\}$
- $T$ can be determined by $HR$ because $\{HR \rightarrow C, C \rightarrow T\} \Rightarrow \{HR \rightarrow T\}$. Reset $K = \{H, R, S, G\}$
- $H$ cannot be determined by any attributes in $K$
- $R$ can be determined by $HS$. Reset $K = \{H, S, G\}$
- $S$ cannot be determined by any attributes in $K$
- $G$ can be determined by $HS$ because $CS \rightarrow G$ and $C$ can be determined by $HR$, where $R$ can be determined by $HS$. Reset $K = \{H, S\}$

**Answer**: Key for Courses is $\{H, S\}$

### Is the given set F of FD’s a minimal cover for F itself? Explain.

(1) **Reduce all FDs in canonical form**

Since every FDs has only one attribute on the right hand side, all FDs are in canonical form.

(2) **For each FD, X$\rightarrow$A, reduce it to (X-{B})$\rightarrow$A if possible**

- $C \rightarrow T$, cannot be reduced
- $HR \rightarrow C$, cannot be reduced to $H \rightarrow C$ or $R \rightarrow C$
- $HT \rightarrow R$, annot be reduced to $H \rightarrow R$ or $T \rightarrow R$
- $HS \rightarrow R$, annot be reduced to $H \rightarrow R$ or $S \rightarrow R$
- $CS \rightarrow G$, annot be reduced to $C \rightarrow G$ or $S \rightarrow G$

(3) **Remove any redundant FD**

None of the FDs is redundant

**Answer**: The given set F of FD is a minimal cover for F itself


### Use the 3NF algorithm discussed in lecture to find a lossless-join, dependencypreserving decomposition of R into 3NF relations.

(1) **Find minimal cover G for F**

$G = \{C \rightarrow T, HR \rightarrow C, HT \rightarrow R, HS \rightarrow R, CS \rightarrow G\}$

(2) **Create relation**

- $R_1 = \{C, T\}$
- $R_2 = \{H, R, C\}$
- $R_3 = \{H, T, R\}$
- $R_4 = \{H, S, R\}$
- $R_5 = \{C, S, G\}$

Where we have $R_4$ that contains the keys $\{H, S\}$

(3) **Remove redundant relation**

None of the relations is redundant.
 
**Answer** the decomposition of R into 3NF relations are 

- $R_1 = \{C, T\}$
- $R_2 = \{H, R, C\}$
- $R_3 = \{H, T, R\}$
- $R_4 = \{H, S, R\}$
- $R_5 = \{C, S, G\}$

