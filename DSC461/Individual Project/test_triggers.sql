-- 1. A user may not bid on an item he or she is also selling.
INSERT INTO Bid VALUES(1673481277, '!peanut', '2001-12-20 00:00:01', 10);
-- 2. No auction may have two bids at the exact same time.
INSERT INTO Item VALUES(1673481202, 'MacBook Pro 2018', 0, NULL, 10, '2001-12-19 00:00:01', '2001-12-22 00:00:01', 'rulabula');
INSERT INTO Bid VALUES(1673481202, '$glenn$', '2001-12-20 00:00:01', 10);
INSERT INTO Bid VALUES(1673481202, '$rollin$', '2001-12-20 00:00:01', 15);
-- 3. No auction may have a bid before its start time or after its end time.
INSERT INTO Bid VALUES(1673481202, '!peanut', '2001-12-20 00:00:01', 10);
-- 4. No user can make a bid of the same amount to the same item more than once.
INSERT INTO Bid VALUES(1673481202, '$glenn$', '2001-12-20 00:01:01', 10);
-- 5. Any new bid for a particular item must have a higher amount than any of the previous bids for that item.
INSERT INTO Bid VALUES(1673481202, '$rollin$', '2001-12-20 00:01:01', 5);
-- 6. All new bids must be placed at the time which matches the current time of your AuctionBase system. item.
UPDATE CurrentTime SET timeNow = '2001-12-20 00:01:01';
INSERT INTO Bid VALUES(1673481202, '$rollin$', '2001-12-20 00:02:01', 15);
-- 7. The Current Price of an item must always match the Amount of the most recent bid for that item. 
SELECT currently FROM Item WHERE ID = 1673481202; -- Result should be 10 because the most recent bid is from INSERT INTO Bid VALUES(1673481202, '$glenn$', '2001-12-20 00:00:01', 10);
-- 8. The current time of your AuctionBase system can only advance forward in time, not backward in time.
UPDATE CurrentTime SET timeNow = '2000-12-20 00:01:01';