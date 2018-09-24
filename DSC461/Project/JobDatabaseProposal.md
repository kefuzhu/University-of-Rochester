# Project details

# Problem Statement

This database will solve the problem that a large company have too many recruiting going on around the world which often creates conflicts in both job advertisements and interviews.

Two recruiters are assigned for the recruiting of the same position where only one recruiter is needed. 

- Waste of human resource.

The HR has already given the offer to a candidate for a specific position and the candidate also has accepted the offer. But the advertisement for this opening position is still alive online. 

- Waste of money on advertisement
- Possible waste of human resource for incoming calls and applications for a position that is already closed

Better than excel spreadsheet

- **Date integrity**: you can't store different types of data in the same attribute (Prevent unintentional wront data input on some level)
- **Consistency**: Anyone with access permissions and can write changes will be able to make some changes that become visible for everyone else who have access permission. No need to copy and past excel or send someone a new excel through email
- **Recovery**: Data in a database is more easier and stable in terms of recovery than data in an excel spreadsheet
- balbalblablabla

# Target user

Users of this database

- Employee of the company (Mainly HR and Middle Managers)
- Visitor of the web interface (Company Career Website) which displays current opening positions

Administrator

- Database Engineer or Data Engineer inside the company

# List of Relations

- **Office**: OfficeID, StreetAddress, City, State, Country
- **OpenPosition**: JobID, OfficeID, Type, PostDate, Position, Department, Salary, Duration, VISASponsor
- **JobAds**: JobID, AdsPlatform1, AdsPlatform2, AdsPlatform3
- **Recruiter**: FirstName, LastName, Position, Department, JobID

# Web-interface

- Straightforward and Intuitive (Many users, especiall HR people, do not have complex computer knowledge)
- Clean and tidy
- Provide examples or tutorials

# Data

Make things up bro! 🦄

---

**Requirement for a complete database system**

1. Users can create their own databases
2. Users modify/retrieve data
3. Store large amounts of data over a long time
4. Recovery in case of failures
5. Control concurrent access