SELECT COUNT(*) FROM Category WHERE itemID IN (SELECT DISTINCT itemID FROM Bid WHERE amount > 1000);