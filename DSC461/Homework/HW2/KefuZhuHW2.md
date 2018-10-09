# DSC 461 HW#2 Kefu Zhu

## Problem 1

**(a)**

```sql
// Solution 1
CREATE ASSERTION manufacturer_1
CHECK (NOT EXISTS (SELECT * FROM
				  			(SELECT DISTINCT maker FROM Product,PC 
						                           WHERE Product.model = PC.model) AS P
							JOIN 
							(SELECT DISTINCT maker FROM Product,Laptop 
												   WHERE Product.model = Laptop.model) AS L 
						    ON P.maker = L.maker
				  ));
```

**(b)**

```sql
// P: Makers of PC and their max processor speed
// L: Makers of laptop and their min processor speed

CREATE ASSERTION Laptop_1
CHECK (NOT EXISTS (SELECT * FROM
						((SELECT maker, MAX(speed) AS max_PC_speed 
						  FROM Product,PC 
						  WHERE Product.model = PC.model GROUP BY maker) AS P
						  JOIN
						 (SELECT maker, MIN(speed) AS min_laptop_speed 
						  FROM Product,Laptop 
						  WHERE Product.model = Laptop.model GROUP BY maker) AS L
						  ON P.maker = L.maker) 
						  WHERE (min_laptop_speed > max_PC_speed) OR 
						        (min_laptop_speed IS NULL)
			      ));
```					                   

**(c)**


```sql
CREATE ASSERTION Laptop_1
CHECK (NOT EXISTS (SELECT * FROM Laptop as l,PC as p
				   			WHERE l.ram > p.ram & l.price <= p.price))
```

**(d)**

```sql
CREATE ASSERTION Product_1
CHECK (NOT EXISTS(SELECT * FROM Product 
				  WHERE (type = 'PC' AND maker NOT IN (SELECT maker FROM PC)) OR
	   					(type = 'laptop' AND maker NOT IN (SELECT maker FROM Laptop)) OR
	   					(type = 'printer' AND maker NOT IN (SELECT maker FROM Printer))
	   			 ));
```

## Problem 2

**(a) List the strong entity types in the ER diagram**

- BANK
- ACCOUNT
- CUSTOMER
- LOAN


**(b) Is there a weak entity type? If so, give its name, partial key, and identifying relationship.**

**BANK_BRANCH** is a weak entity type. Its partial key is **Branch\_no** and it involves in 3 relationships:

- BRANCHES
- LOANS
- ACCTS


**(c) What constraints do the partial key and the identifying relationship of the weak entity type specify in this diagram?**

A specific **BANK_BRANCH** must belongs to and only belongs to one **BANK** (total participation). It can create multiple **ACCOUNT** and provide multiple **LOAN** (partial participation)

**(d) List concisely the user requirements that led to this ER schema design**

The user requires a database to keep track of the data in a mini-world, which contains banks along with their own branches which can provide both bank account and loan services to individual customer.

Below are some specific requirements

1. A bank can have multiple branches. A bank branch must belongs to one and only one bank



2. A bank branch can create multiple accounts and/or provide multiple loans
3. Every account or loan can only belongs to one bank branch


4. A customer can have zero or multiple accounts or loans


????? What does A\_C and L\_C means? Why one BANK\_BRANCH can only have one ACCOUNT?

