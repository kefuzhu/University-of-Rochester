# Midterm Review

## Chapter 1, Definition

(1) **Database**: a collection of related data

(2) **Data**: known facts that can be recorded and have implicit meaning

(3) **Database Management System (DBMS)**: a computerized system that enables users to create and maintain a database

(4) **Functionality**

- **Define** a particular database: data types, structures, constraints
- **Construct** or **Load** the initial database contents on a secondary storage medium
- **Manipulating** the database
	- Retrieval: Querying, generating reports
	- Modification: Insertions, deletions and updates to its content
	- Accessing the database through Web applications
- **Processing** and **Sharing** by a set of concurrent users and application programs, while keeping all data valid and consistent

(5) **Data Model**: A set of concepts to describe the **structure** of a database, the **operations** for manipulating these structures, and certain **constraints** that the database should obey

(6) **Data Model Operations**: Used for specifying database **retrievals** and **updates** by referring to the constructs of the data model

- Basic model operations: generic insert, delete, update, ...
- User-defined operations: compute\_student\_gpa, update\_inventory, ...

(7) **Data Model Categories**

- **Conceptual (high-level, semantic)**: Provide concepts that are close to the way many users perceive data
- **Physical (low-level, internal)**: Provide concepts that describe details of how data is stored in the computer
- **Implementation (representational)**: Provide concepts that fall between the above two, used by many commercial DBMS implementations
- **Self-Describing**: Combine the description of data with the data values. Examples include XML, key-value stores and some NOSQL systems

(8) **Database Schema**: The description of a database, including structure, data types, and constrains

(9) **Schema Diagram**: An illustrative display of (most aspects of) a database schema

(10) **Schema Construct**: A component of the schema or an object within the schema (e.g. STUDENT, COURSE)

(11) **Database State/Instance**: The actual data stored in a database at a **particular moment in time**

- **Valid State**: A state that satisfies the structure and constraints of the database

(12) Schema is also called **intension**. State is also called **extension**

(13) **Relation**: Looks like a table of values

(14) **Attribute**: column header is called attribute

(15) **Tuple**: rows are called tuples (an ordered set of values)

(16) **Schema**: Denoted by $R(A_1,A_2, ..., A_n)$, where $R$ is the name of relation and $A_i$ is attribute

(17) **Domain of Attribute**: a set of valid values for an attribute

(18) **Relation State**: a subset of the Cartesian product of the domains of its attributes (or NULL)

(19) **NULL Values**: represent attributes whose values are unkonwn or do not exist

## Chapter 3, ER

(1) **Entity type**: a collection of entities that have the same attributes (each relation is a collection of a lot of similar entity)

(2) **Entity set**: The collection of all entities of a particular entity type in the database at any point in time

![entity](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/Entity_EntityType.png)

(3) **Attribute type**: 

- Composite vs. Simple (Atomic)
- Single-Valued vs. Multivalues
- Stored vs. Detrived: Birth_date is stored attribute, Age is derived attribute
- Complex: (Address_phone((Phone (Area code, number)), Address((Street\_address, State))))

(4) **Cardinality ratio**: For a binary relationship: 1:1, 1:N, N:1, N:M

(5) **Participation constraint**: Total/partial participation


## Chapter 5, Relational Model and SQL

### 1. Operations

(1) **Set operation**: UNION, UNION ALL, INTERSECT, MINUS

### 2. Keys

(1) **Superkey**: A set of attributes $S \subset R$ with the property that no two tuples $t_1$ and $t_2$ will have $t_1[S] = t_2[S]$.

- Any set of attributes that includes a key are all superkeys
	
(2) **Key**: Removal of any attribute from a key will cause it not to be a superkey anymore

(3) **Candidate key**: If a relation schema has more than one key, each is called a candidate key

(4) **Primary key**: One is the candidate key is designated to be the primary key. All others are then called **secondary key**

### 3. Constraints

#### A. Inherent model-based/Implicit: 

Characteristics of relations

- No order among tuples in a relation
- Values within a tuple is ordered
- Tuple only contain atomic values and NULLs

#### B. Schema-based/Explicit

(1) **Domain Constraint**: Values must be certain data type

(2) **Key Constraint**: Values within a key must be unique

(3) **Constraint on NULL Value**: Whether NULL value is permitted or not

(4) **Entity Integrity Constraint**: No primary key value can be NULL

(5) **Referential Integrity Constraint**: Tuple in foreign key cannot has values that do not exist in primary key, to which the foreign key refers

#### C. Application-based/Semantic


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

**Note**: Ssn $\rightarrow$ Dmgr\_ssn is a transitive FD. Because both Ssn $\rightarrow$ Dnumber and Dnumber $\rightarrow$ Dmgr\_ssn hold.

### 5. Trivial/Non-trivial FDs

(1) **Trivial FD**: $X \rightarrow Y$ holds, where $Y$ is a subset of $X$. Trivial FD always holds

(2) **Non-trivial FD**: $X \rightarrow Y$ holds, where $Y$ is NOT a subset of $X$

### 6. 1NF, 2NF, 3NF, BCNF

**Definition**: The normal form of a relation refers to the highest normal form condition that it meets, and hence indicates the degree to which it hs been normalized

(1) **First Normal Form (1NF)**

(2) **Second Normal Form (2NF)**

**Definition**: A relation schema $R$ is in second normal form if every non-prime attribute $A$ in $R$ is fully functionally dependent on the primary key

![2NF](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/2NF.png)

- **Ename** can be functionally determined by only **Ssn**
- **Pname** and **Plocation** can be functionally determined by only **Pnumber**

(3) **Third Normal Form**

**Definition**: Whenever a nontrivial FD $X \rightarrow A$ holds in $R$, 

either **X is a superkey**, or **A is a prime attribute**


![3NF](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/3NF.png)

- **Dmgr_ssn** depend on **Dnumber**, which is neither a key itself nor a subset of the key of relation **EMP_DEPT**

(4) **Boyece-Codd Normal Form (BCNF)**

**Definition**: If there is $X \rightarrow A$, no matter $A$ is prime or non-prime attribute, $X$ must be a superkey

<center>
![BCNF](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Midterm/BCNF.png)
</center>


### 7. Properties of Decomposition.

(1) **Attribute Preservation**: Each attribute in $R$ will appear in at least one relatin schema $R_i$ in the decomposition so that no attributes are lost

(2) **Nonadditive (Lossless) Join**: Ensures that no spurious tuples are generated when a NATURAL JOIN operation is applied to hte relations resulting from the decomposition


**Side note**: Goal is to have each individual relation in the decomposition be in BCNF or 3NF