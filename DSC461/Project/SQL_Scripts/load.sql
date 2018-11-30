# Empty the OFFICE relation
DELETE FROM OFFICE;
# Load data into OFFICE relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Office.csv"
INTO TABLE OFFICE
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the DEPARTMENT relation
DELETE FROM DEPARTMENT;
# Load data into DEPARTMENT relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Department.csv"
INTO TABLE DEPARTMENT
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the RECRUITER relation
DELETE FROM RECRUITER;
# Load data into RECRUITER relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Recruiter.csv"
INTO TABLE RECRUITER
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the POSITION_ relation
DELETE FROM POSITION_;
# Load data into POSITINO_ relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Position.csv"
INTO TABLE POSITION_
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the APPLICANT relation
DELETE FROM APPLICANT;
# Load data into APPLICANT relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Applicant.csv"
INTO TABLE APPLICANT
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the APPLY_TO relation
DELETE FROM APPLY_TO;
# Load data into APPLY_TO relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Apply_to.csv"
INTO TABLE APPLY_TO
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

# Empty the ADSPLATFORM relation
DELETE FROM ADSPLATFORM;
# Load data into ADSPLATFORM relation
LOAD DATA LOCAL INFILE "/home/kzhu6/group_proj/data/Adsplatform.csv"
INTO TABLE ADSPLATFORM
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\r\n";

