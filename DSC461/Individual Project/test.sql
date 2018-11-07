SELECT COUNT(*) FROM Item; -- 19532 
SELECT COUNT(*) FROM Item WHERE ID NOT IN(SELECT itemID FROM Bid); -- 15656: Majority of items were not bid by any users
SELECT COUNT(*) FROM Item WHERE ID NOT IN(SELECT itemID FROM Category); -- 0: Every exisiting item is categorized

SELECT COUNT(*) FROM User; -- 13422
SELECT COUNT(*) FROM User WHERE ID NOT IN(SELECT userID FROM Bid); -- 6412: Nearly half of users have not participated in any bidding

SELECT Bid.userID, COUNT(Bid.userID) as NumOfBid FROM User,Bid
WHERE User.ID = Bid.userID
GROUP BY Bid.userID
HAVING NumOfBid > 1
ORDER BY NumOfBid DESC
LIMIT 5; -- yields 2177 users who have bid on more than one item

SELECT DISTINCT COUNT(itemID) FROM Bid WHERE userID = 'Antonios'; -- Antonios is the user who has bid on the most number of item