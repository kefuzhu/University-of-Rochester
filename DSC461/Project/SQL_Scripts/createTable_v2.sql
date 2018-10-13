-- Office
CREATE TABLE IF NOT EXISTS OFFICE (ID INT NOT NULL PRIMARY KEY,
								   StreetAddress VARCHAR(50) NOT NULL UNIQUE,
				  				   City VARCHAR(25) NOT NULL,
				  				   State CHAR(2) NOT NULL,
				  				   ZipCode INT(5) NOT NULL);
-- Department
CREATE TABLE IF NOT EXISTS DEPARTMENT (ID INT,
									   OfficeID INT,
									   Name VARCHAR(50) NOT NULL,
									   PRIMARY KEY(ID),
									   FOREIGN KEY(OfficeID) REFERENCES Office(ID) ON DELETE SET NULL ON UPDATE CASCADE);
-- Recruiter
CREATE TABLE IF NOT EXISTS RECRUITER(ID INT	NOT NULL,
									 FirstName VARCHAR(30)	NOT NULL,
									 LastName VARCHAR(30)	NOT NULL,
									 Position VARCHAR(50)	NOT NULL,
									 DepartmentID INT,
								     PRIMARY KEY (ID),
 									 FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(ID) ON DELETE SET NULL ON UPDATE CASCADE);
-- Position_
CREATE TABLE IF NOT EXISTS POSITION_ (ID INT NOT NULL PRIMARY KEY,
								     Type CHAR(8) DEFAULT 'FullTime',
								     Title VARCHAR(50) NOT NULL,
							         DepartmentID INT,
 								     RecruiterID INT,
 								     PostDate DATE,
 								     Salary INT,
 								     VisaSponsorship VARCHAR(15) DEFAULT 'Yes',
 								     FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(ID) ON DELETE SET NULL ON UPDATE CASCADE,
 								     FOREIGN KEY (RecruiterID) REFERENCES RECRUITER(ID) ON DELETE SET NULL ON UPDATE CASCADE);
-- Applicant
CREATE TABLE IF NOT EXISTS APPLICANT(ID INT NOT NULL,
 									 Email VARCHAR(50)		NOT NULL,
 									 FirstName VARCHAR(30)	NOT NULL,
 									 LastName VARCHAR(30)	NOT NULL,
 									 School VARCHAR(50),
 									 Degree VARCHAR(30),
 									 Major VARCHAR(30),
 									 PRIMARY KEY (ID));
-- Apply_to
CREATE TABLE IF NOT EXISTS APPLY_TO(ApplicantID INT,
 									PositionID INT,
 									AdsPlatform VARCHAR(50) NOT NULL,
 									PRIMARY KEY(ApplicantID, PositionID),
 									FOREIGN KEY(ApplicantID) REFERENCES APPLICANT(ID) ON DELETE CASCADE ON UPDATE CASCADE,
 									FOREIGN KEY(PositionID) REFERENCES POSITION_(ID) ON DELETE CASCADE ON UPDATE CASCADE);
-- AdsPlatform
CREATE TABLE IF NOT EXISTS ADSPLATFORM(PositionID INT,
 									   AdsPlatform VARCHAR(50) NOT NULL,
 									   PRIMARY KEY(PositionID, AdsPlatform),
 									   FOREIGN KEY(PositionID) REFERENCES POSITION_(ID) ON DELETE CASCADE ON UPDATE CASCADE);