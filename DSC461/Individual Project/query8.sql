SELECT COUNT(*) FROM (SELECT userID
					  FROM (SELECT userID, category 
					  	    FROM Item JOIN Category ON Item.ID = Category.itemID 
					  	    GROUP BY userID,category) AS A
					  GROUP BY userID
					  HAVING COUNT(userID) > 10) AS B;