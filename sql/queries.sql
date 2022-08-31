/*
-- TCSS445, Spring 2021
-- Riley Ruckman, 1721498
-- Final Project Submission - Queries

USE ruckmans
GO

-- Scenarios

-- NOTE:
-- My proposal contains 9 scenarios, but the last 2 include making reports. These reports
-- would have specific layouts and require multiple queries in order to grab the necessary information.
-- Therefore, I will only include the first 7 scenarios. If you want an example of a report, view an Order
-- Report from my frontend/UI implementation. Thank you for understanding.

-- 1) Make a new order/quote
-- This scenario requires multiple INSERT statements, as Orders and Quotes are subtypes of Jobs
-- and require at least 1 Door.
-- I have made many Orders in my backend.sql file, so I'll make a Quote.
*/
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
	VALUES(3, 4, '20200206', '20200220', 'Bathroom', NULL, 'Q', 'Custom Color', -20);

INSERT INTO JOBQUOTE VALUES(8, NULL);

INSERT INTO DOOR VALUES(8, 1, 'Maple', '13/16', '1100', 4, 20.5, 31.0625, '5', NULL, 'E-13', NULL, NULL);
INSERT INTO DOOR VALUES(8, 2, 'Maple', '1', '1000', 2, 20, 40, NULL, NULL, 'E-12', 'Make it 1-1/4"', NULL);

SELECT * FROM JOB;
SELECT * FROM JOBQUOTE;
SELECT * FROM DOOR;

/*
-- 2) Modify an existing order/quote
-- I'll modify the Quote I just made, but the process is the same for a Order.
-- This will have 3 different modifications: one for JOB, one for JOBQUOTE, and one for DOOR when DoorNumber = 1
*/
UPDATE JOB;
SET AppliedFinish = NULL;
WHERE JobNumber = 8;

UPDATE JOBQUOTE;
SET QuoteComments = 'Wants ASAP pricing';
WHERE JobNumber = 8;

UPDATE DOOR;
SET DoorWidth = 20.4375;
WHERE JobNumber = 8 AND DoorNumber = 1;

SELECT * FROM JOB WHERE JobNumber = 8;
SELECT * FROM JOBQUOTE WHERE JobNumber = 8;
SELECT * FROM DOOR WHERE JobNumber = 8;

/*
-- 3) Add/edit customers
*/
INSERT INTO CUSTOMER (CustomerName, DefaultModificationPerc, DefaultDeliveryMethod, isCompany)
	VALUES('RETAIIL SALE', 30, 'WILL CALL', 0);

SELECT * FROM CUSTOMER;

UPDATE CUSTOMER;
SET CustomerName = 'RETAIL SALE';
WHERE CustomerID = 4;

SELECT * FROM CUSTOMER;

/*
-- 4) Copy an order
-- This will include many queries as I need to copy information from JOB, JOBORDER, DOOR, and ORDERHARDWARE
*/
INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc) 
SELECT CustomerID, MainContact, '20210604', '20210618', JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc 
FROM JOB WHERE JobNumber = 1;

INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus)
SELECT 9, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, 'Processing'
FROM JOBORDER WHERE JobNumber = 1;

INSERT INTO DOOR (JobNumber, DoorNumber, MaterialName, Thickness, StyleCode, DoorQuantity, DoorWidth, DoorHeight, InsideProfile, PanelProfile, OutsideProfile, DoorComment, Bore)
SELECT 9, 1, MaterialName, Thickness, StyleCode, DoorQuantity, DoorWidth, DoorHeight, InsideProfile, PanelProfile, OutsideProfile, DoorComment, Bore
FROM DOOR WHERE JobNumber = 1 AND DoorNumber = 1;

INSERT INTO DOOR (JobNumber, DoorNumber, MaterialName, Thickness, StyleCode, DoorQuantity, DoorWidth, DoorHeight, InsideProfile, PanelProfile, OutsideProfile, DoorComment, Bore)
SELECT 9, 2, MaterialName, Thickness, StyleCode, DoorQuantity, DoorWidth, DoorHeight, InsideProfile, PanelProfile, OutsideProfile, DoorComment, Bore
FROM DOOR WHERE JobNumber = 1 AND DoorNumber = 2;

INSERT INTO ORDERHARDWARE (JobNumber, HardwareName, Quantity)
SELECT 9, HardwareName, Quantity
FROM ORDERHARDWARE WHERE JobNumber = 1;

/*
SELECT * FROM JOB
SELECT * FROM JOBORDER
SELECT * FROM DOOR
SELECT * FROM ORDERHARDWARE ORDER BY JobNumber
*/

/*
-- 5) Delete an order
-- I will delete the copy of the Order I just made in the previous scenario.
-- I will go in the opposite order that I did in the previous scenario.
*/

DELETE FROM ORDERHARDWARE WHERE JobNumber = 9;
DELETE FROM DOOR WHERE JobNumber = 9;
DELETE FROM JOBORDER WHERE JobNumber = 9;
DELETE FROM JOB WHERE JobNumber = 9;

/*
SELECT * FROM JOB
SELECT * FROM JOBORDER
SELECT * FROM DOOR
SELECT * FROM ORDERHARDWARE ORDER BY JobNumber
*/

/*
-- 6) Search by Customer
-- Included CustomerName as it reduces any confusion that may come from not including
-- CustomerName
*/

SELECT OrderNumber, CustomerName, JobName, PONumber, JobDate, EstimatedDueDate, OrderStatus
FROM JOB
INNER JOIN JOBORDER ON JOBORDER.JobNumber = JOB.JobNumber
INNER JOIN CUSTOMER ON CUSTOMER.CustomerID = JOB.CustomerID
WHERE Job.CustomerID = 1;

/*
-- 7) Search by Order Number
-- Included CustomerName as it reduces any confusion that may come from not including
-- CustomerName
*/
SELECT OrderNumber, CustomerName, JobName, PONumber, JobDate, EstimatedDueDate, OrderStatus
FROM JOB
INNER JOIN JOBORDER ON JOBORDER.JobNumber = JOB.JobNumber
INNER JOIN CUSTOMER ON CUSTOMER.CustomerID = JOB.CustomerID
WHERE OrderNumber = 3;

/*
-- Analytical Queries

-- NOTE:
-- Looking at my original list of analytical queries, #1 and #2 are extremely similar.
-- Therefore, I will alter #1 to search for a matching Job Name or PO, and will
-- have #2 search/filter by Material.

-- 1) Find all Orders with a specific Customer and Job Name/PO
*/
SELECT OrderNumber, JobName, PONumber 
FROM JOBORDER
INNER JOIN JOB ON JOBORDER.JobNumber = JOB.JobNumber
WHERE CustomerID = 1 AND (JobName like '%al%' or PONumber like '%al%');

/*
-- 2) Find all Customers who have Orders with a specific Material
*/
SELECT DISTINCT CustomerName, OrderNumber
FROM CUSTOMER
INNER JOIN JOB ON CUSTOMER.CustomerID = JOB.CustomerID
INNER JOIN JOBORDER ON JOBORDER.JobNumber = JOB.JobNumber
INNER JOIN DOOR ON DOOR.JobNumber = JOBORDER.JobNumber
WHERE MaterialName = 'Maple';

/*
-- 3) Find all Orders with am Estimated Due Date between two specified dates
*/
SELECT OrderNumber, EstimatedDueDate 
FROM JOBORDER
INNER JOIN JOB ON JOBORDER.JobNumber = JOB.JobNumber
WHERE EstimatedDueDate BETWEEN '20180101' AND '20201231';

/*
-- 4) Find all Orders with a specific Customer and has Hardware
*/
SELECT OrderNumber, HardwareName, Quantity 
FROM JOBORDER
INNER JOIN JOB ON JOBORDER.JobNumber = JOB.JobNumber
INNER JOIN ORDERHARDWARE ON JOB.JobNumber = ORDERHARDWARE.JobNumber
WHERE CustomerID = 2;

/*
-- 5) Find all Orders that will be delivered by Company truck, have the same City, and are completed.
*/
SELECT OrderNumber, CONCAT(StreetAddress, ' ', City, ', ', CityState, ' ', ZIPCODE) AS ShippingAddress, 
	ShippingInstructions 
FROM JOBORDER
INNER JOIN JOB ON JOBORDER.JobNumber = JOB.JobNumber
INNER JOIN CUSTOMER ON JOB.CustomerID = CUSTOMER.CustomerID
INNER JOIN ADDRESSES ON Customer.ShippingAddress = ADDRESSES.AddressID
WHERE (DeliveryMethod = 'OUR TRUCK' OR DefaultDeliveryMethod = 'OUR TRUCK') 
	AND City = 'Tacoma' AND OrderStatus = 'Completed';
