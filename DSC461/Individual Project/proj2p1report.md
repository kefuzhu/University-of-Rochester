# DSC 461, Project 2 (Individual Project)
# Part 1 Report, Kefu Zhu

## ER Diagram

<center>
![](https://github.com/datamasterkfz/University-of-Rochester/raw/master/DSC461/Individual%20Project/ER_diagram.png)
</center>



## User

1. **Attributes**
	- ID: TEXT
	- rating: INT
	- location: TEXT
	- country: TEXT
2. **Primary Key**: ID
3. **Foreign Key**: None

## Item

1. **Attributes**
	- ID: INT
	- name: TEXT
	- currently: DOUBLE
	- buy_price: DOUBLE
	- first_bid: DOUBLE
	- started: DATETIME
	- ends: DATETIME
	- userID: TEXT
2. **Primary Key**: ID
3. **Foreign Key**: userID $\rightarrow$ User.ID

## Bid

1. **Attributes**
	- itemID: INT
	- userID: TEXT
	- time: DATETIME
	- amount: DOUBLE
2. **Primary Key**: (itemID,userID,amount)
3. **Foreign Key**: 
	- itemID $\rightarrow$ Item.ID
	- userID $\rightarrow$ User.ID

## Category

1. **Attributes**
	- itemID: INT
	- category: TEXT
2. **Primary Key**: (itemID, category)
3. **Foreign Key**: itemID $\rightarrow$ Item.ID