# Midterm Review

## Chapter 3, SQL

### 1. Keys

(1) **Superkey**: A set of attributes $S \subset R$ with the property that no two tuples $t_1$ and $t_2$ will have $t_1[S] = t_2[S]$.

- Any set of attributes that includes a key are all superkeys
	
(2) **Key**: Removal of any attribute from a key will cause it not to be a superkey anymore

(3) **Candidate key**: If a relation schema has more than one key, each is called a candidate key

(4) **Primary key**: One is the candidate key is designated to be the primary key. All others are then called **secondary key**



## Chapter 14, Normalization

### 1. Functional Dependencies (FD)

**Definition**: Denoted by $X \rightarrow Y$, between two sets of attrivutes $X$ and $Y$ that are subsets of $R$, where for any two tuples $t_1$ and $t_2$ in $R$ that have $t_1[X] = t_2[X]$, they must also have $t_1[Y] = t_2[Y]$

- If $X$ is a candidate key (all values of $X$ are unique), this implies that $X \rightarrow Y$ for any subset of attribute $Y$ of $R$
- If $X \rightarrow Y$ in $R$, this does not imply whether or not $Y \rightarrow X$ in $R$

### 2. Prime/Non-prime Attributes

(1) **Prime attribute**: It is a member of some candidate key

(2) **Nonprime attribute**: Attribute that is not a prime attribute

### 3. Full/Partial FDs

(1) **Full FD**: a FD $Y \rightarrow Z$ where removal of any attribute from $Y$ causes FD to not hold anymore

(2) **Partial FD**: a FD $X \rightarrow Y$ where removal of some attributes from $X$ can still makes FD hold

### 4. Transitive FDs 

**Definition**: A FD $X \rightarrow Y$ is a transitive FD, if there exists a set of attributes $Z$ 

- That is neither a candidate key nor a subset of any key
- Both $X \rightarrow Z$ and $Z \rightarrow Y$ hold

![transitive_FD](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/transitive_FD.png)

### 5. Trivial/Non FDs

### 6. 1NF, 2NF, 3NF, BCNF

**Definition**: The normal form of a relation refers to the highest normal form condition that it meets, and hence indicates the degree to which it hs been normalized

(1) **First Normal Form (1NF)**

(2) **Second Normal Form (2NF)**

**Definition**: A relation schema $R$ is in second normal form if every non-prime attribute $A$ in $R$ is fully functionally dependent on the primary key

![2NF](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/2NF.png)

- **Ename** can be functionally determined by only **Ssn**
- **Pname** and **Plocation** can be functionally determined by only **Pnumber**

(3) **Third Normal Form**

**Definition**: If there is $X \rightarrow A$, for some $A$ that are non-prime attribute, $X$ must be a superkey

![3NF](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/3NF.png)

- **Dmgr_ssn** depend on **Dnumber**, which is neither a key itself nor a subset of the key of relation **EMP_DEPT**

(4) **Boyece-Codd Normal Form (BCNF)**

**Definition**: If there is $X \rightarrow A$, no matter $A$ is prime or non-prime attribute, $X$ must be a superkey

### 7. Properties of Decomposition.