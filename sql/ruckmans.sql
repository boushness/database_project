--  TCSS445, Spring 2021
--  Riley Ruckman, 1721498
--  Final Project Submission - backend

USE mysql;
DROP DATABASE ruckmans;

CREATE DATABASE ruckmans;

USE ruckmans;
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -
--  Run each function individually after creating and using TCSS445_Project database

DELIMITER |
CREATE FUNCTION IsCompanyCheck ( ID int )
RETURNS int DETERMINISTIC
BEGIN
	return (SELECT isCompany FROM CUSTOMER WHERE CustomerID = ID);
END |

CREATE FUNCTION ProfileTypeCheck ( profile VARCHAR(5) )
RETURNS CHAR(1) DETERMINISTIC
BEGIN
	return (SELECT ProfileType FROM DOORPROFILE WHERE ProfileName = profile);
END |

DELIMITER ;

/*
INSERT INTO CONTACT(FirstName, LastName, PhoneNumber, EmailAddress) VALUES ('Riley', 'Ruckman', '253-414-1456', 'abcd@gmail.com');

SELECT * FROM CONTACT;
*/

/*
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -

-- DROP TABLE MATERIAL
-- GO

*/

CREATE TABLE MATERIAL
(
	MaterialName VARCHAR(20) NOT NULL,
	Thickness VARCHAR(6) NOT NULL
		CHECK (Thickness IN ('3/4', '13/16', '15/16','1')),
	PRIMARY KEY(MaterialName, Thickness)
);
/*
-- DROP TABLE ADDRESSES;
-- GO
*/

CREATE TABLE ADDRESSES
(
	AddressID int NOT NULL AUTO_INCREMENT,
	StreetAddress VARCHAR(20) NOT NULL,
	City VARCHAR(10) NOT NULL,
	CityState CHAR(2) NOT NULL 
		CHECK (CityState IN ('WA','OR','ID','HI','AK','CA')),
	ZIPCODE CHAR(5) NOT NULL,
	PRIMARY KEY(AddressID)/*,

	CONSTRAINT Valid_ZIPCode
		CHECK (ZIPCode LIKE '5*[0-9]')*/
);

/*
-- DROP TABLE CONTACT;
-- GO
*/

CREATE TABLE CONTACT
(
	ContactID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	FirstName VARCHAR(15) NOT NULL,
	LastName VARCHAR(15),
	PhoneNumber CHAR(12),
	EmailAddress VARCHAR(30) NULL/*,
	
	CONSTRAINT Check_Phone CHECK (PhoneNumber LIKE '[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]')*/,
	CONSTRAINT Has_Contact_Info CHECK (PhoneNumber <> NULL AND EmailAddress <> NULL)
);

/*
ALTER TABLE CONTACT
DROP CHECK Check_Phone;

ALTER TABLE CONTACT
ADD CONSTRAINT Check_Phone CHECK (PhoneNumber LIKE '[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]');

*/
/*
-- DROP TABLE PRODUCTDELIVERYMETHOD
-- GO
*/

CREATE TABLE PRODUCTDELIVERYMETHOD 
(
	DeliveryMethodName VARCHAR(10) PRIMARY KEY,
	DeliveryMethodPrice float NOT NULL
);

/*
-- DROP TABLE CUSTOMER
-- GO
*/

CREATE TABLE CUSTOMER
(
	CustomerID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	CustomerName VARCHAR(20) NOT NULL,
	ShippingAddress int references 
		ADDRESSES(AddressID),
	BillingAddress int references 
		ADDRESSES(AddressID),
	PrimaryPhone CHAR(12),
	SecondaryPhone CHAR(12),
	EmailAddress VARCHAR(30),
	DefaultContact int references CONTACT(ContactID),
	DefaultModificationPerc float NOT NULL,
	DefaultDeliveryMethod VARCHAR(10) NOT NULL references PRODUCTDELIVERYMETHOD(DeliveryMethodName),
	TaxRate float NOT NULL DEFAULT (9.3),
	isCompany int NOT NULL CHECK (isCompany IN (0,1))/*,

	CONSTRAINT Check_Primary_Phone 
		CHECK (PrimaryPhone <> NULL AND PrimaryPhone LIKE '[0-9][0-9][0-9][-][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9]'),
	CONSTRAINT Check_Secondary_Phone 
		CHECK (SecondaryPhone <> NULL AND SecondaryPhone LIKE '[0-9][0-9][0-9][-][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9]'),
	CONSTRAINT Has_Company_Contact_Info 
		CHECK (isCompany = 0 OR (PrimaryPhone = NULL AND EmailAddress = NULL))*/
);

/*
-- DROP TABLE COMPANY
-- GO
*/

CREATE TABLE COMPANY
(
	CustomerID int NOT NULL references CUSTOMER(CustomerID),
	CompanyAddress int NOT NULL
		references ADDRESSES(AddressID),
	FaxNumber CHAR(12),
	ResellerPermit VARCHAR(20) UNIQUE,
	PRIMARY KEY(CustomerID)/*,
	
	CONSTRAINT CheckCustomerCompany
		CHECK (IsCompanyCheck(CustomerID) = 1),

	CONSTRAINT CheckCustomerCompany
		CHECK ((SELECT isCompany FROM CUSTOMER WHERE CUSTOMER.CustomerID = COMPANY.CustomerID) = 1),

	CONSTRAINT Check_Fax_Number 
		CHECK (FaxNumber LIKE '[0-9][0-9][0-9][-][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9]')*/
);

/*
-- DROP TABLE CUSTOMERCONTACTS
-- GO
*/

CREATE TABLE CUSTOMERCONTACTS
(
	CustomerID int NOT NULL references CUSTOMER(CustomerID),
	ContactID int NOT NULL references CONTACT(ContactID),
	Affiliation VARCHAR(12),
	PRIMARY KEY(CustomerID, ContactID)
);

/*
-- DROP TABLE FINISH
-- GO
*/

CREATE TABLE FINISH
(
	FinishName VARCHAR(20) PRIMARY KEY,
	FinishPrice float NOT NULL,
	FinishDescription VARCHAR(30)
);

/*
-- DROP TABLE HARDWARE
-- GO
*/

CREATE TABLE HARDWARE
(
	HardwareName VARCHAR(50) PRIMARY KEY,
	HardwarePrice float NOT NULL,
	HardwareDescription VARCHAR(50)
);

/*
-- DROP TABLE JOB
-- GO
*/

CREATE TABLE JOB
(
	JobNumber int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	JobDate date NOT NULL,
	EstimatedDueDate date NOT NULL,
	CustomerID int NOT NULL,
	MainContact int NOT NULL,
	JobName VARCHAR(20),
	PONumber VARCHAR(20),
	JobType CHAR(1) NOT NULL CHECK (JobType IN ('O','Q')),
	AppliedFinish VARCHAR(20) references FINISH(FinishName),
	PriceModificationPerc float,

	CONSTRAINT Customer_Contact 
        FOREIGN KEY (CustomerID, MainContact) 
        REFERENCES CUSTOMERCONTACTS (CustomerID, ContactID)
);

/*
-- DROP TABLE JOBORDER
-- GO
*/

CREATE TABLE JOBORDER
(
	OrderNumber int NOT NULL AUTO_INCREMENT,
	JobNumber int NOT NULL references Job(JobNumber),
	ProductionComments VARCHAR(100),
	InvoiceComments VARCHAR(100),
	ShippingInstructions VARCHAR(100),
	DeliveryMethod VARCHAR(10) references PRODUCTDELIVERYMETHOD(DeliveryMethodName),
	OrderStatus VARCHAR(50) NOT NULL
		CHECK (OrderStatus in ('Processing', 'In Production','Completed')),
	PRIMARY KEY(OrderNumber),
	UNIQUE (JobNumber)
);

/*
-- DROP TABLE JOBQUOTE
-- GO
*/

CREATE TABLE JOBQUOTE
(
	QuoteNumber int NOT NULL AUTO_INCREMENT,
	JobNumber int NOT NULL references Job(JobNumber),
	QuoteComments VARCHAR(100),
	PRIMARY KEY(QuoteNumber),
	UNIQUE(JobNumber)
);

/*
-- DROP TABLE ORDERHARDWARE
-- GO
*/

CREATE TABLE ORDERHARDWARE
(
	JobNumber int NOT NULL references Job(JobNumber),
	HardwareName VARCHAR(50) NOT NULL references HARDWARE(HardwareName),
	Quantity int NOT NULL DEFAULT (1),

	PRIMARY KEY (HardwareName, JobNumber)
);

/*
-- DROP TABLE HINGEBORING
-- GO
*/

CREATE TABLE HINGEBORING
(
	HingeBoringName VARCHAR(50) PRIMARY KEY,
	HingeBoringPrice float NOT NULL
);

/*
-- DROP TABLE DOORPROFILE
GO
*/

CREATE TABLE DOORPROFILE
(
	ProfileName VARCHAR(5) PRIMARY KEY,
	ProfileType CHAR(1) NOT NULL
		CHECK (ProfileType in ('I','O','P')),
	ProfilePrice float NOT NULL,
	ProfileDescription VARCHAR(20)
);

/*
-- DROP TABLE INSIDEPROFILETYPE
GO
*/

CREATE TABLE INSIDEPROFILETYPE
(
	InsideProfileName VARCHAR(5) NOT NULL references DOORPROFILE(ProfileName),
	RailLengthAdjustment float DEFAULT (0),
	PRIMARY KEY(InsideProfilename)
/*
	CONSTRAINT HasToBeInsideProfile
		CHECK (dbo.ProfileTypeCheck(InsideProfileName) = 'I')
*/
);

/*
-- DROP TABLE DOORSTYLE
-- GO
*/

CREATE TABLE DOORSTYLE
(
	StyleCode VARCHAR(10) PRIMARY KEY,
	TopStileWidth float NOT NULL,
	BottomStileWidth float NOT NULL,
	LeftRailWidth float NOT NULL,
	RightRailWidth float NOT NULL,
	PanelType VARCHAR(10) NOT NULL
		CHECK (PanelType IN ('Recessed', 'Raised', 'No Panel')),
	DoorStyleDescription VARCHAR(20)
);

/*
-- DROP TABLE STYLEPRICING
-- GO
*/

CREATE TABLE STYLEPRICING
(
	MaterialName VARCHAR(20) NOT NULL,
	Thickness VARCHAR(6) NOT NULL,
	StyleCode VARCHAR(10) NOT NULL references DOORSTYLE(StyleCode),
	StylePrice float NOT NULL,

	CONSTRAINT Pricing_Materials_Keys
		FOREIGN KEY (MaterialName, Thickness)
		references MATERIAL (MaterialName, Thickness),

	PRIMARY KEY(MaterialName, Thickness, StyleCode)
);

/*
-- DROP TABLE DOOR
-- GO
*/

CREATE TABLE DOOR
(
	JobNumber int NOT NULL references Job(JobNumber),
	DoorNumber int,
	MaterialName VARCHAR(20) NOT NULL,
	Thickness VARCHAR(6) NOT NULL,
	StyleCode VARCHAR(10) NOT NULL references DOORSTYLE(StyleCode),
	DoorQuantity int NOT NULL,
	DoorWidth float NOT NULL,
	DoorHeight float NOT NULL,
	InsideProfile VARCHAR(5) references DOORPROFILE(ProfileName),
	OutsideProfile VARCHAR(5) references DOORPROFILE(ProfileName),
	PanelProfile VARCHAR(5) references DOORPROFILE(ProfileName),
	DoorComment VARCHAR(400),
	Bore VARCHAR(50) references HINGEBORING(HingeBoringName),

	CONSTRAINT Door_Materials_Keys
		FOREIGN KEY (MaterialName, Thickness)
		references MATERIAL (MaterialName, Thickness),

	PRIMARY KEY (JobNumber, DoorNumber)
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -

--  Addresses:
INSERT INTO ADDRESSES(StreetAddress, City, CityState, ZIPCODE) VALUES('1231 65Th Ave W', 'Tacoma', 'WA', '98468');
INSERT INTO ADDRESSES(StreetAddress, City, CityState, ZIPCODE) VALUES('92 34Th Ave Ct E', 'Honolulu', 'HI', '96701');

--  1 - Tom's Cabinets
--  2 - Rick's Woodworking

--  Contact:
INSERT INTO CONTACT(FirstName, LastName, PhoneNumber, EmailAddress) VALUES ('Tom', 'Hardey', '253-897-2013', 'tomh@timscab.com');
INSERT INTO CONTACT(FirstName, LastName, PhoneNumber, EmailAddress) VALUES ('Charles', 'Hardey', '253-658-1852', 'rickh@timscab.com');
INSERT INTO CONTACT(FirstName, LastName, PhoneNumber, EmailAddress) VALUES ('Rick', 'Thin', '808-322-2853', 'rickthin@gmail.com');
INSERT INTO CONTACT(FirstName, LastName, PhoneNumber, EmailAddress) VALUES ('Thomas', 'Picle', '253-242-1513', 'thopic12@yahoo.com');

-- 1 - Tom Hardey
-- 2 - Charles Hardney
-- 3 - Rick Thin
-- 4 - Thomas Picle

-- ProductDeliveryMethod:
INSERT INTO PRODUCTDELIVERYMETHOD VALUES('WILL CALL', 0);
INSERT INTO PRODUCTDELIVERYMETHOD VALUES('OUR TRUCK', 25.10);
INSERT INTO PRODUCTDELIVERYMETHOD VALUES('CRATE', 250.0);

-- Customer:
INSERT INTO CUSTOMER (Customername, ShippingAddress, BillingAddress, PrimaryPhone, SecondaryPhone, EmailAddress, DefaultContact, DefaultModificationPerc, DefaultDeliveryMethod, TaxRate, isCompany) VALUES('Tom''s Cabinets', 1, 1, '253-653-1249', NULL, 'office@timscab.com', 1, 0.0, 'OUR TRUCK', 0.0, 1);

INSERT INTO CUSTOMER (Customername, ShippingAddress, BillingAddress, PrimaryPhone, SecondaryPhone, EmailAddress, DefaultContact, DefaultModificationPerc, DefaultDeliveryMethod, TaxRate, isCompany) VALUES('Rick''s Woodworking', 2, 2, '808-322-2634', NULL, 'rickthin@gmail.com', 3, 0.0, 'CRATE', 0.0, 1);

INSERT INTO CUSTOMER (CustomerName, DefaultModificationPerc, DefaultDeliveryMethod, isCompany)
	VALUES('CASH SALE', 10, 'WILL CALL', 0);

-- 1 - Tom's Cabinets
-- 2 - Rick's Woodworking
-- 3 - CASH SALE

-- Company:
INSERT INTO COMPANY VALUES(1, 1, '253-124-1451', 'AG3241AFDW'); 
INSERT INTO COMPANY VALUES(2, 2, '808-214-2151', NULL);

-- CustomerContacts:
INSERT INTO CUSTOMERCONTACTS VALUES(1, 1, 'Owner');
INSERT INTO CUSTOMERCONTACTS VALUES(1, 2, 'Associate');
INSERT INTO CUSTOMERCONTACTS VALUES(2, 3, 'Owner');
INSERT INTO CUSTOMERCONTACTS VALUES(3, 4, 'Homeowner');

-- Material:
INSERT INTO MATERIAL VALUES('Maple', '13/16');
INSERT INTO MATERIAL VALUES('Maple', '1');
INSERT INTO MATERIAL VALUES('Alder', '13/16');
INSERT INTO MATERIAL VALUES('Walnut', '1');

-- DoorProfile:
INSERT INTO DOORPROFILE VALUES('5','I',0.53,'Shaker-Style');
INSERT INTO DOORPROFILE VALUES('3','I',0.53, NULL);
INSERT INTO DOORPROFILE VALUES('E-12','O',0.53,'1/16" Radius');
INSERT INTO DOORPROFILE VALUES('E-13','O',0.53,'1/8" Radius');
INSERT INTO DOORPROFILE VALUES('B','P',0.53,'');
INSERT INTO DOORPROFILE VALUES('F','P',0.53,'');

-- InsideProfileType:
INSERT INTO INSIDEPROFILETYPE (InsideProfileName) VALUES ('5');
INSERT INTO INSIDEPROFILETYPE VALUES ('3', 0.23);

-- DoorStyle:
INSERT INTO DOORSTYLE VALUES('1100', 2.25, 2.25, 2.25, 2.25, 'Raised', '2-1/4", Raised');
INSERT INTO DOORSTYLE VALUES('2100', 2.25, 2.25, 2.25, 2.25, 'Recessed', '2-1/4", Recessed');
INSERT INTO DOORSTYLE VALUES('1120', 2.5, 2.5, 2.5, 2.5, 'Raised', '2-1/2", Raised');
INSERT INTO DOORSTYLE VALUES('1000', 0, 0, 0, 0, 'No Panel', 'Slab');

-- StylePricing:
INSERT INTO STYLEPRICING VALUES('Maple', '13/16', '1100', 5.25);
INSERT INTO STYLEPRICING VALUES('Maple', '13/16', '1120', 5.75);
INSERT INTO STYLEPRICING VALUES('Alder', '13/16', '2100', 4.15);
INSERT INTO STYLEPRICING VALUES('Walnut', '1', '1000', 20.0);
INSERT INTO STYLEPRICING VALUES('Maple', '1', '1000', 10.0);

-- HingeBoring:
INSERT INTO HINGEBORING VALUES('BLUM35/2mm, 3mm offset', 1.00);
INSERT INTO HINGEBORING VALUES('BLUM35/8mm, 5mm offset', 1.00);

-- Hardware:
INSERT INTO HARDWARE VALUES('B71B-355/600', 3.80, 'B71B-355 Long Arm Hinges w/ 600 Plates');
INSERT INTO HARDWARE VALUES('B73B-355/600', 3.80, 'B71B-355 Long Arm Hinges w/ 600 Plates');
INSERT INTO HARDWARE VALUES('1/2"" COMPACT S/C', 2.50, '1/2" Blum Compact Hinges');

-- Finish:
INSERT INTO FINISH VALUES('Clear Lacquer', 10.80, 'Clear Lacquer on Both Sides');
INSERT INTO FINISH VALUES('Custom Color', 12.33, 'Custom Color on Both Sides');

-- Job:
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(1, 1, '20160815', '20160823', 'Alet Downstairs', '323-1', 'O', 'Clear Lacquer', NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(1, 2, '20180314', '20180328', 'Alet Upstairs', '323-2', 'O', 'Clear Lacquer', NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(2, 3, '20190502', '20190516', NULL, NULL, 'O', NULL, NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(3, 4, '20200106', '20200120', 'Kitchen', NULL, 'Q', 'Custom Color', NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(2, 3, '20210914', '20210928', 'Living Room', NULL, 'O', NULL, NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(1, 1, '20160815', '20160823', 'Town Downstairs', '334-1', 'O', 'Clear Lacquer', NULL);
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(1, 2, '20180314', '20180328', 'Town Upstairs', '334-2', 'O', 'Clear Lacquer', NULL);

-- 1 - Tom's Cabinets, Alet Downstairs
-- 2 - Tom's Cabinets, Alet Upstairs
-- 3 - Rick's Woodworking, NULL
-- 4 - CASH SALE, Kitchen

-- JobOrder:
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(1, 'Perfect Sizing', 'Call Customer for Payment', NULL, NULL, 'In Production');
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(2, NULL, 'Call Customer for Payment', NULL, NULL, 'Processing');
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(3, NULL, NULL, 'Package Carefully!', NULL, 'Completed');
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(5, 'Rustic Maple', 'A check will be mailed in.', NULL, 'WILL CALL', 'In Production');
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(6, 'Perfect Sizing', 'Call Customer for Payment', NULL, NULL, 'Completed');
INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus) VALUES(7, NULL, 'Call Customer for Payment', NULL, NULL, 'Completed');

-- JobQuote:
INSERT INTO JOBQUOTE (JobNumber, QuoteComments) VALUES(4, NULL);

-- OrderHardware:
INSERT INTO ORDERHARDWARE VALUES(1, 'B71B-355/600', 20);
INSERT INTO ORDERHARDWARE VALUES(2, 'B73B-355/600', 14);
INSERT INTO ORDERHARDWARE VALUES(3, '1/2"" COMPACT S/C', 11);
INSERT INTO ORDERHARDWARE VALUES(4, '1/2"" COMPACT S/C', 4);

-- Door:
INSERT INTO DOOR VALUES(1, 1, 'Maple', '13/16', '1100', 5, 12.5, 24, '5', 'F', 'E-13', NULL, 'BLUM35/8mm, 5mm offset');
INSERT INTO DOOR VALUES(1, 2, 'Maple', '13/16', '1100', 4, 18.75, 12.3125, '5', 'F', 'E-13', NULL, NULL);
INSERT INTO DOOR VALUES(1, 3, 'Maple', '13/16', '1100', 8, 21.4375, 40, '5', 'F', 'E-13', NULL, 'BLUM35/8mm, 5mm offset');

INSERT INTO DOOR VALUES(2, 1, 'Alder', '13/16', '2100', 3, 12.75, 12, '3', NULL, 'E-12', NULL, NULL);
INSERT INTO DOOR VALUES(2, 2, 'Alder', '13/16', '2100', 5, 24.4375, 34.9375, '3', NULL, 'E-12', NULL, 'BLUM35/8mm, 5mm offset');

INSERT INTO DOOR VALUES(3, 1, 'Walnut', '1', '1000', 1, 48, 102.5, NULL, NULL, NULL, NULL, NULL);

INSERT INTO DOOR VALUES(4, 1, 'Maple', '13/16', '1100', 2, 11, 25.6875, '3', 'B', NULL, NULL, 'BLUM35/2mm, 3mm offset');

INSERT INTO DOOR VALUES(5, 1, 'Maple', '13/16', '1100', 2, 13, 24.6875, '5', NULL, 'E-12', 'Want 2" frame', 'BLUM35/2mm, 3mm offset');
INSERT INTO DOOR VALUES(5, 2, 'Maple', '13/16', '1100', 2, 20, 15.0, '5', NULL, 'E-12', 'Want 2" frame', 'BLUM35/2mm, 3mm offset');

/*
SELECT * FROM ADDRESSES
SELECT * FROM CONTACT
SELECT * FROM PRODUCTDELIVERYMETHOD
SELECT * FROM CUSTOMER
SELECT * FROM COMPANY
SELECT * FROM CUSTOMERCONTACTS
SELECT * FROM MATERIAL
SELECT * FROM DOORPROFILE
SELECT * FROM INSIDEPROFILETYPE
SELECT * FROM DOORSTYLE
SELECT * FROM STYLEPRICING
SELECT * FROM HINGEBORING
SELECT * FROM HARDWARE
SELECT * FROM FINISH
SELECT * FROM JOB
SELECT * FROM JOBORDER
SELECT * FROM DOOR
SELECT * FROM JOBQUOTE
SELECT * FROM ORDERHARDWARE
SELECT * FROM DOOR
*/

