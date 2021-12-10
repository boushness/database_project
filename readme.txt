WARNING: THIS README IS FROM THE FINALIZED SUBMISSION FOR A COLLEGE PROJECT. IT MAY NOT APPLY.

TCSS445 Database Systems, Spring 2021
Riley Ruckman, 1721498
Final Project Submission - README

=========================================================================================================================================================
| DISCLAIMER: The UI was made and designed with a 1440p monitor. It seems that the UI elements change, and the windows get larger, when using a monitor |
| resolution that is not 1440p. This can cause some buttons to clip into other UI elements, but this does not alter the program's functionality or ease | 
| of access.																		|
=========================================================================================================================================================

Contents (In Order as Seen):
- Instruction for Installation
- Order List Window
- New Order Form Window
- Order Report Window

=========================================================================================================================================================
																			|
Instructions for Installation:																|
																			|
1) Download "Final Project Submission - Riley Ruckman - TCSS445, Sp21.zip"										|
2) Unzip to desired directory																|
3) The necessary files are:																|
	- "Ruckman_Riley_backend.sql"															|
	- "Ruckman_Riley_frontend.exe"															|
																			|
4) Assuming you're using a recent version of SQL Server, open and run "Ruckman_Riley_backend.sql".							|
5) Run "Ruckman_Riley_frontend.exe"															|
																			|
If you don't want to run the .exe:															|
																			|
6) (At least) Python version 3.8.5 must be installed. You can use your preferred environment.								|
7) Assuming you know how to install Python libraries, download and install PyQt5.									|
8) Open and run "Ruckman_Riley_frontendSourceCode.py"													|
																			|
Assuming no errors occured, you're connected to the database and inside the program! The first window to show up is the Order List Window.		|
																			|
=========================================================================================================================================================
																		       	|
Order List Window:																       	|
																		       	|
- This window shows the Orders in the database. In the middle, a table is shown with all Orders with various information to know at a glance,	       	|
  like the Order Number, Customer Name, Job Name, PO, Estimated Due Date, and more.								       	|
																		       	|
- In the row above the table, a series of 3 dropdown boxes labeled Customer, Contact, and Order Number are used to filter the table contents.          	|
																		       	|
--- All of the boxes default to a *, and boxes with a * do not filter the table in any way.							       	|
																		       	|
--- When selecting by Customer, the table will be filtered to only show Orders by that Customer. The Contact options will be restricted to 	       	|
    Contacts that are associated with the selected Customer. Selecting a Contact while a Customer is selected will further filter the table to 	       	|
    only show Orders that have the selected Customer and Contact. 										       	|
																		       	|
--- When selecting only by Contact, the table is filtered to only show Orders with the selected Contact. Selecting a Customer while a Contact          	|
    is selected will reset the Contact selection to *. 												       	|
																		       	|
--- Selecting by Order Number will filter the table to show only one Order with the selected Order Number. Selecting by Order Number also 	       	|
    resets Customer and Contact to *. Also, selecting by Customer and/or Contact will reset Order Number to *.					       	|
																		       	|
- In the row below the table, there is a set of 3 buttons: "New Order", "View Order", and "Exit".						       	|
																		       	|
--- The "New Order" button will hide the Order List Window and open a New Order Form Window. We'll discuss the New Order Form Window in its own section.|
--- The "View Order" button will hide the Order List Window and open a Order Report Window. We'll discuss the New Order Form Window in its own section.	|
--- The "Exit" button will close the Order List Window, closing the program.										|
																			|
=========================================================================================================================================================
																			|				
New Order Form Window:																	|
																			|
- This window shows an Order form for the user to enter/select information for a new Order.								|
																			|
- It has 3 major sections: Order Info, Door Table, and Comments/Delivery.										|
																			|
- Order Info:																		|
																			|
--- The Order Info is the upper-left to mid-left section of the window. This section contains information regarding the Order Number, Customer, Contact,|
    Job Name, and more. The user is allowed to select and/or enter for all of the different options, except for the Order Number.			|
																			|
--- The Contact options will update based on the selected Customer just like the Order List Window.							|
																			|
--- For the Job Date and Estimated Due Date, there are arrows to change the displayed date. In order to effectively change the desired section of the 	|
    date (Month, Day, Year), you must click on the desired part and verify that the mouse cursor is in the desired section. Now, when an arrow is	|
    clicked, the correct section will be altered.													|
																			|
--- The Price Modification has a checkbox to enable a custom value. When the checkbox is checked, you can enter a value between -100 and 250, which	|
    corresponds to discount percentages applied to the Order. When the checkbox is unchecked, the line to enter a custom value becomes read-only, and	|
    any existing values will be cleared.														|
																			|
--- The "Cancel" button will exit out of the New Order Form window without inserting the Order into the database.					|
--- The "Done" button will exit out of the New Order Form window and insert the Order into the database.						|
--- For the "Cancel" and "Done" buttons, they will return you to the Order List Window.									|
--- The other buttons will be discussed in the Door Table section.											|
																			|
- Door Table:																		|
																			|	
--- The Door Table covers a majority of the window, and contains a table for entering new Door items into the form.					|
																			|
--- Quantity, Door Width, and Door Height must all be specified in order for the Door to be entered into the database.					|
																			|
--- Quantity is limited to a max of 100, and Door Width and Door Height is limited to a max of 200 and can have up to 4 decimal digits.			|
																			|
--- Each row must have a Material, Thickness, and StyleCode in order to be inserted into the database.							|
																			|
--- When a Material is selected, the options for Thickness and StyleCode will be updated with valid options from the database. When a Thickness		|
    is selected when a Material is already selected, the options for StyleCode is updated.								|
																			|
--- The "Add Row" button will add another row to the bottom of the table.										|
																			|
--- The "Delete Selected Row" button will delete a selected row in the table.										|
																			|
--- These are the steps for deleting a selected row in the table:											|
																			|
1) Select the desired Door row by clicking the row tab on the far left of the table that corresponds to the desired Door row.				|
2) While the desired Door row is selected/highlighted, click on "Delete Selected Row".									|
																			|
- Comments/Delivery:																	|
																			|
--- The Comments/Delivery section contains the Deliver Method dropdown and the Shipping Instructions, Production Comments, and Invoice Comments		|
    text boxes.																		|
																			|
--- The default value for Delivery Method is "WILL CALL", but can be changed. The text boxes can be filled with any appropriate information.		|
																			|
=========================================================================================================================================================
																			|
Order Report Window:																	|
																			|
- This window shows a summary/report of a specified Order from the Order List Window.									|
																			|
- These are the steps for opening an Order Report Window:												|
																			|
1) Select the desired Order by clicking the row tab on the far left of the table that corresponds to the desired Order.					|
2) While the desired Order row is selected/highlighted, click on "View Order".										|
																			|
- The window will show Customer, Contact, and Order information. This information includes:								|
--- Order Number																	|
--- Customer																		|
--- Contact																		|
--- Job Name																		|
--- PO																			|
--- Job Date -> Date the Order was entered into the system.												|
--- [Estimated] Due Date																|
--- Finish -> Finish applied to Doors.															|
--- Hardware -> Supplied hardware for the Order. 													|
--- Delivery Method -> The method for getting the Order to its Customer.										|
--- Shipping Instructions																|
--- Production Comments -> Comments to be used when producing the Order.										|
--- Door Table -> Table of Doors in the Order. Each row will have a quantity, dimensions, and other information of the row's door.			|
																			|
- All entries in the Order Report Window are read-only/cannot be edited.										|
																			|
- To close the Order Report Window, click the "Close" button in the lower-left corner of the window. This will return you to the Order List Window.	|
																			|
=========================================================================================================================================================
