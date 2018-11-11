# Create trigger before_insert_bid
DROP TRIGGER IF EXISTS before_insert_bid;
DELIMITER //
CREATE TRIGGER before_insert_bid BEFORE INSERT ON Bid
FOR EACH ROW
BEGIN
	IF NEW.userID = (SELECT userID FROM Item WHERE ID = NEW.itemID) THEN
		CALL `Error1: A user may not bid on an item he or she is also selling.`;
	ELSEIF NEW._time IN (SELECT _time FROM Bid) THEN
		CALL `Error2: No auction may have two bids at the exact same time.`;
	ELSEIF NEW._time NOT BETWEEN (SELECT started FROM Item WHERE ID = NEW.itemID) AND (SELECT ends FROM Item WHERE ID = NEW.itemID) THEN
		CALL `Error3: Cannot bid before an auction starts or after it ends.`;
	ELSEIF NEW.amount = (SELECT amount FROM Bid WHERE userID = NEW.userID AND itemID = NEW.itemID) THEN
		CALL `Error4: A user can only bid on a item with the same amount once.`;
	ELSEIF NEW.amount <= (SELECT MAX(amount) FROM Bid WHERE itemID = NEW.itemID) THEN
		CALL `Error5: New bid must be higher than any of the old bids.`;
	ELSEIF NEW._time != (SELECT timeNow FROM CurrentTime) THEN
		CALL `Error6: The time of bid must match current time of the system.`;
	END IF;
END;//
DELIMITER ;

# Create trigger after_insert_bid
DROP TRIGGER IF EXISTS after_insert_bid;
DELIMITER //
CREATE TRIGGER after_insert_bid AFTER INSERT ON Bid
FOR EACH ROW
BEGIN
	IF NEW.amount != (SELECT currently FROM Item WHERE ID = NEW.itemID) THEN
		UPDATE Item SET Item.currently = NEW.amount WHERE ID = NEW.itemID;
	END IF;
END;//
DELIMITER ;

# Create trigger before_update_time
DROP TRIGGER IF EXISTS before_update_time;
DELIMITER //
CREATE TRIGGER before_update_time BEFORE UPDATE ON CurrentTime
FOR EACH ROW
BEGIN
	IF NEW.timeNow < (SELECT timeNow FROM CurrentTime) THEN
		CALL `Error8: The current time of the system cannot move backward.`;
	END IF;
END;//
DELIMITER ;
