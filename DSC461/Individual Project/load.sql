-- Load data from user.dat into Table User
LOAD DATA LOCAL INFILE "user.dat"
INTO TABLE User
FIELDS TERMINATED BY "<>";
-- Load data from item.dat into Table Item
-- Note: The operation yields a lot of warnings because in the original file, buy_price field contains a lot of NULL values, which will be truncated to 0 in the Item.buy_price attribute
LOAD DATA LOCAL INFILE "item.dat"
INTO TABLE Item
FIELDS TERMINATED BY "<>";
-- Load data from category.dat into Table Category
LOAD DATA LOCAL INFILE "category.dat"
INTO TABLE Category
FIELDS TERMINATED BY "<>";
-- Load data from bid.dat into Table Bid
LOAD DATA LOCAL INFILE "bid.dat"
INTO TABLE Bid
FIELDS TERMINATED BY "<>";