# DSC 461 HW#2 Kefu Zhu

## Problem 1

**(a) No manufacturer (maker) of PC’s may also make laptops**

```sql
CREATE ASSERTION manufacturer_1
CHECK (NOT EXISTS (SELECT * FROM
				  			(SELECT DISTINCT maker 
				  			 FROM Product,PC 
						     WHERE Product.model = PC.model) AS P
							JOIN 
							(SELECT DISTINCT maker 
							 FROM Product,Laptop 
							 WHERE Product.model = Laptop.model) AS L 
						    ON P.maker = L.maker
				  ));
```

**(b) A PC maker must also be a Laptop maker and the laptop has to have speed at least the speed of the PC from the same maker**

Since the question itself may be interpreted in multiple ways, here I will claim my understanding of the question

Assumption:

- A PC maker must also make at least one laptop
- A maker can make multiple PCs and laptops
- The processor speed attribute may have NULL values
- Any laptops produced by a same maker must have processor speed at least as great as any of the PCs produced by that maker $\rightarrow$ For any maker, MIN(laptop\_speed) > MAX(PC\_speed)

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
					  WHERE (min_laptop_speed < max_PC_speed) OR 
					        (min_laptop_speed IS NULL)
			      ));
			      
// I put 'min_laptop_speed IS NULL' as one of the condition in WHERE
// clause because the result of 'NULL < Any Number' will always be FALSE.
// However, if I do encounter a NULL value in the laptop processor speed,
// since I can not infer what actual value it indicates, I should consider
// it as worst case scenario, which should be consider as negative infinity.

// Therefore, if a laptop has NULL value for its processor speed. It should also
// be considered as a violation of the constraint
```					                   

**(c) If a laptop has a larger main memory than a PC, then the laptop must also have a higher price than the PC**


```sql
CREATE ASSERTION Laptop_1
CHECK (NOT EXISTS (SELECT * FROM Laptop as l,PC as p
				   			WHERE l.ram > p.ram & l.price <= p.price))
```

**(d) If the relation Product mentions a model and its type, then this model must appear in the relation appropriate to that type**

```sql
CREATE ASSERTION Product_1
CHECK (NOT EXISTS(
		SELECT * FROM Product 
		WHERE (type = 'PC' AND model NOT IN (SELECT model FROM PC)) OR
	   		  (type = 'laptop' AND model NOT IN (SELECT model FROM Laptop)) OR
	   		  (type = 'printer' AND model NOT IN (SELECT model FROM Printer))
	  )); 
```

## Problem 2

**(a) List the strong entity types in the ER diagram**

- BANK
- ACCOUNT
- CUSTOMER
- LOAN


**(b) Is there a weak entity type? If so, give its name, partial key, and identifying relationship.**

**BANK_BRANCH** is a weak entity type. Its partial key is **Branch\_no** and it is identified by relationship **BRANCHES**

**(c) What constraints do the partial key and the identifying relationship of the weak entity type specify in this diagram?**

A specific **BANK_BRANCH** must belongs to and only belongs to one **BANK** (total participation). While a **BANK** can have multiple **BANK_BRACH**. The **BANK_BRANCH** has **Branch_no** as partial key but **BANK_BRANCH** from different **BANK** may have the same **Branch_no**

**(d) List concisely the user requirements that led to this ER schema design**

The user requires a database to keep track of the data in a mini-world, which contains banks along with their own branches which can provide both bank account and loan services to individual customer.

Below are some specific requirements

1. Each bank has name and address as well as a unique code for each bank an have multiple branches. A bank must has one or more bank branches but one bank branch must belongs to one and only one bank.
2. Each bank branch has address and branch number. 
3. A bank branch can create zero or more accounts and/or provide zero or more loans.
4. Each account has balance and type as well as unique account number.
5. Each loan has amount and type as well as unique loan number.
6. Each account or loan must belongs to one and only one bank branch.
7. Each customer has name, phone number, address as well as unique SSN number.
8. A customer can have zero or multiple accounts or loans.

## Problem 3

![](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Homework/HW2/ER_Diagram.png)
