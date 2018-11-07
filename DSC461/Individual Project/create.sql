-- Drop the following tables if existed
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS User;

-- Create Table User if not existed
CREATE TABLE IF NOT EXISTS User(ID VARCHAR(40) PRIMARY KEY, # awk -F "<>" '{print $1}' user.dat | wc -L yields 34. So the longest userID has 34 characters. To be conservative, set the limit to 50 characters
								rating INT,
								location TEXT,
								country TEXT);

-- Create Table Item if not existed
CREATE TABLE IF NOT EXISTS Item(ID INT(10) PRIMARY KEY,
								name TEXT,
								currently DOUBLE, # NOT NULL
								buy_price DOUBLE,
								first_bid DOUBLE,
								started DATETIME, # NOT NULL
								ends DATETIME, # NOT NULL
								userID VARCHAR(40),
								FOREIGN KEY (userID) REFERENCES User(ID));

-- Create Table Category if not existed
CREATE TABLE IF NOT EXISTS Category(itemID INT(10),
									category VARCHAR(35), # wc -L yields 45. Because first 12 characters are itemID(10 digits) and delimiter <>(2 characters), so the longest category name has 33 characters (45-10-2)
									PRIMARY KEY(itemID, category),
									FOREIGN KEY(itemID) REFERENCES Item(ID) ON DELETE CASCADE ON UPDATE CASCADE);

-- Create Table Bid if not existed
CREATE TABLE IF NOT EXISTS Bid(itemID INT(10),
							   userID VARCHAR(40),
							   _time DATETIME,
							   amount DOUBLE,
							   PRIMARY KEY(itemID, userID),
							   FOREIGN KEY(itemID) REFERENCES Item(ID) ON DELETE CASCADE ON UPDATE CASCADE,
							   FOREIGN KEY(userID) REFERENCES User(ID) ON DELETE CASCADE ON UPDATE CASCADE);

