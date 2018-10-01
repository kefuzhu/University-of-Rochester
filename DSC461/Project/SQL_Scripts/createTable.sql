-- Office_Location
CREATE TABLE IF NOT EXISTS Office_Location (OfficeID INT(5) PRIMARY KEY,
											StreetAddress VARCHAR(50) UNIQUE,
							  				City VARCHAR(25),
							  				State VARCHAR(25),
							  				ZipCode INT(5));
-- Department
CREATE TABLE IF NOT EXISTS Department (Name VARCHAR(50),
									   Dnumber INT(5),
									   OfficeID INT(5),
									   ManagerID INT(5),
									   PRIMARY KEY(Name,Dnumber),
									   FOREIGN KEY(OfficeID) REFERENCES Office_Location(OfficeID));
-- Employee
CREATE TABLE IF NOT EXISTS Employee (EmployeeID INT(5) PRIMARY KEY,
									 FirstName VARCHAR(30),
									 LastName VARCHAR(30),
									 Position VARCHAR(50),
									 Department VARCHAR(50));
-- Add additional foreign keys
ALTER TABLE Department ADD FOREIGN KEY Department(ManagerID) REFERENCES Employee(EmployeeID);
ALTER TABLE Employee ADD FOREIGN KEY Employee(Department) REFERENCES Department(Name);

-- Open_Positions
CREATE TABLE IF NOT EXISTS Open_Positions (JobID INT(5) PRIMARY KEY,
										   OfficeID INT(5),
										   Type CHAR(8), -- Define an user-defined domain type
										   PostDate DATE,
										   Position VARCHAR(50),
										   Department VARCHAR(50),
										   Salary INT,
										   Duration FLOAT,
										   VISASponsor Bool,
										   AdsPlatform1 VARCHAR(50),
										   AdsPlatform2 VARCHAR(50),
										   AdsPlatform3 VARCHAR(50),
										   FOREIGN KEY (OfficeID) REFERENCES Office_Location(OfficeID),
										   FOREIGN KEY (Department) REFERENCES Department(Name));

-- Application_Received
CREATE TABLE IF NOT EXISTS Application_Received (ApplicationID CHAR(5) PRIMARY KEY,
												 FirstName VARCHAR(30),
												 LastName VARCHAR(30),
												 Email VARCHAR(50), -- Define an user-defined domain type
												 School VARCHAR(80),
												 Degree VARCHAR(50), -- Define an user-defined domain type
												 JobID INT(5),
												 Platform VARCHAR(50),
												 RecruiterID INT(5),
												 FOREIGN KEY (JobID) REFERENCES Open_Positions(JobID),
												 FOREIGN KEY (RecruiterID) REFERENCES Employee(EmployeeID));