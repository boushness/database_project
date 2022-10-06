import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QTableWidgetItem,
)

from ViewOrder import ViewOrder
from NewOrderWindow import NewOrderWindow

# Order List Window Class for viewing JOBORDER entries in the database.
# Allows searching of JOBORDER by Customer, Contact, and/or Order Number
# Allows entry of new JOBORDERs and report views of JOBORDER entries
class OrderListWindow(QtWidgets.QMainWindow):
    def __init__(self, mydb, parent=None):
        
        self.mydb = mydb
        # Uses QtWidgets.QMainWindow's __init__()
        super(OrderListWindow, self).__init__(parent)

        # Creates central widget that all other widgets will attach to.
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Arrays for storing CustomerID and ContactID values.
        # Customer in index 0 of the Customer dropbox menu
        # will have its CustomerID stored in index 0 of the CustomerID array.
        # This is true for ContactID as well.
        self.CustomerID = []
        self.ContactID = []

        #############################################################################################################

        # Widget that holds dropdown menus for Customer, Contact, and Order Number
        self.selection = QtWidgets.QWidget()

        # Grid layout for the selection widget
        lay = QtWidgets.QGridLayout(self.selection)

        # Dropdown menu widgets for Customer, Contact, and Order Number
        self.CustomerName = QtWidgets.QComboBox()
        self.Contact = QtWidgets.QComboBox()
        self.OrderNumber = QtWidgets.QComboBox()

        # Label widgets for Customer, Contact, and Order Number
        self.CustomerNamelabel = QtWidgets.QLabel('Customer')
        self.ContactLabel = QtWidgets.QLabel('Contact')
        self.OrderNumberLabel = QtWidgets.QLabel('Order Number')

        # Adds widgets to self.selection grid layout
        lay.addWidget(self.CustomerName, 1, 0)
        lay.addWidget(self.Contact, 1, 1)
        lay.addWidget(self.OrderNumber, 1, 2)
        lay.addWidget(self.CustomerNamelabel, 0, 0)
        lay.addWidget(self.ContactLabel, 0, 1)
        lay.addWidget(self.OrderNumberLabel, 0, 2)

        ####################################################################################

        # Create table widget
        self.table = QtWidgets.QTableWidget()

        ####################################################################################

        # Create button widget
        self.buttons = QtWidgets.QWidget()

        # Button for entering a new order
        self.newOrderButton = QtWidgets.QPushButton(self.buttons)
        self.newOrderButton.setText('New Order')
        self.newOrderButton.move(10, 0)
        self.newOrderButton.clicked.connect(self.newOrder)

        # Button for viewing an existing order
        self.printReportButton = QtWidgets.QPushButton(self.buttons)
        self.printReportButton.setText('View Order')
        self.printReportButton.move(138, 0)
        self.printReportButton.clicked.connect(self.viewReport)

        # Button for viewing an existing order
        self.printReportButton = QtWidgets.QPushButton(self.buttons)
        self.printReportButton.setText('Delete Order')
        self.printReportButton.move(266, 0)
        self.printReportButton.clicked.connect(self.deleteOrder)

        # Button for exiting Order List window
        self.exitButton = QtWidgets.QPushButton(self.buttons)
        self.exitButton.setText('Exit')
        self.exitButton.move(394, 0)
        self.exitButton.clicked.connect(self.exitWindow)

        ####################################################################################

        # Central widget that self.selection, self.table. and self.buttons
        # attach to
        lay = QtWidgets.QGridLayout(central_widget)

        # Set position of sub-widgets inside central_widget
        lay.addWidget(self.selection, 0, 0, 1, 1)
        lay.addWidget(self.table, 1, 0, 1, 3)
        lay.addWidget(self.buttons, 2, 0, 1, 3)

        # Sets stretch of specific columns and rows to allow the table
        # to grow bigger while keeping the selection and button widgets
        # from changing
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 0)
        lay.setColumnStretch(2, 1)
        
        lay.setRowStretch(0, 0)
        lay.setRowStretch(1, 1)
        lay.setRowStretch(2, 0)

        # Sets minimum height for row 2 to allow the button widget to show in the window
        lay.setRowMinimumHeight(2, 50)

        # Initializes Contact dropdown menu and table
        self.updateCustomer()
        self.updateContact()
        self.updateOrderNumber()
        self.updateTable()

        # Allows dropdown menus to have line fields that the user can enter text into
        self.CustomerName.setEditable(True)
        self.Contact.setEditable(True)
        self.OrderNumber.setEditable(True)

        # Sets signal connections for when the user interacts with the 
        # dropdown menus.

        # A Customer selection will update Contact, reset the Order Number selection
        # and update the table
        self.CustomerName.activated[str].connect(self.updateContact)
        self.CustomerName.activated[str].connect(self.updateOrderNumber)
        self.CustomerName.activated[str].connect(self.updateTable)

        # A Contact selection with reset the Order Number and update the table
        self.Contact.activated[str].connect(self.updateOrderNumber)
        self.Contact.activated[str].connect(self.updateTable)

        # A OrderNumber selection will reset Customer, update Contacts, and update the table
        self.OrderNumber.activated[str].connect(self.updateCustomer)
        self.OrderNumber.activated[str].connect(self.updateContact)
        self.OrderNumber.activated[str].connect(self.updateTable)

        # Sets title of window and minimum size of window to allow
        # all information to be comfortably shown 
        self.setWindowTitle("Order List")
        self.setMinimumSize(1100, 520)
    
    """
    # Resets Customer dropdown menu selection to '*'
    def resetCustomer(self):
        self.CustomerName.setCurrentIndex(0)
    
    # Resets Contact dropdown menu selection to '*'
    def resetContact(self):
        self.Contact.setCurrentIndex(0)

    # Resets Order Number dropdown menu selection to '*'
    def resetOrderNumber(self):
        self.OrderNumber.setCurrentIndex(0)
    """

    # Updates the Contact dropdown menu options based on a selection of Customer
    # When a specific Customer is selected, only Contacts associated with that Customer
    # are available in the menu
    def updateContact(self):
        # Grabs current index/value of Customer menu
        customerID = self.CustomerName.currentIndex()

        # If the current Customer selection is '*', then all Contacts are grabbed from the database
        # If a different index is chosen, then the CustomerID of the same value as the current index is
        # specified in the query
        query = self.mydb.cursor()
        if customerID == 0:
            query.execute("SELECT DISTINCT CONCAT(FirstName, ' ', LastName) AS Name, CONTACT.ContactID" 
                + " FROM CONTACT INNER JOIN CUSTOMERCONTACTS ON CONTACT.ContactID = CUSTOMERCONTACTS.ContactID"
                + " INNER JOIN JOB ON JOB.MainContact = CONTACT.ContactID"
                + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                )
        else:
            query.execute("SELECT DISTINCT CONCAT(FirstName, ' ', LastName) AS Name, CONTACT.ContactID" 
                + " FROM CONTACT INNER JOIN CUSTOMERCONTACTS ON CONTACT.ContactID = CUSTOMERCONTACTS.ContactID"
                + " INNER JOIN JOB ON JOB.MainContact = CONTACT.ContactID"
                + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                + " WHERE JOB.CustomerID = {}".format(customerID)
                )

        # Contact menu and ContactID array are cleared
        self.Contact.clear()
        self.ContactID.clear()

        # '*' option is added first
        self.Contact.addItem("*")

        # The query results are then added to the Contact menu and ContactID array
        for row in query:
            self.Contact.addItem(row[0])
            self.ContactID.append(row[1])
        
        self.Contact.setCurrentIndex(0)

        query.close()

    # Updates Customer dropdown menu with database data
    def updateCustomer(self):
        # Query for grabbing CustomerName from the database
        # Only grabs Customers who have an existing JOBORDER entry in the
        # database.
        
        query = self.mydb.cursor()
        query.execute("SELECT DISTINCT CustomerName, CUSTOMER.CustomerID FROM CUSTOMER"
                        + " INNER JOIN CUSTOMERCONTACTS ON CUSTOMER.CustomerID = CUSTOMERCONTACTS.CustomerID"
                        + " INNER JOIN JOB ON JOB.CustomerID = CUSTOMERCONTACTS.CustomerID" 
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber ORDER BY CUSTOMER.CustomerID")

        # Customer menu and CustomerID array are cleared
        self.CustomerName.clear()
        self.CustomerID.clear()

        # Adds '*' selection first, and then adds query results to Customer
        self.CustomerName.addItem("*")
        for row in query:
            self.CustomerName.addItem(row[0])
            self.CustomerID.append(row[1])
        
        self.CustomerName.setCurrentIndex(0)

        query.close()

    # Updates Order Number dropdown menu with database data
    def updateOrderNumber(self):
        # Grabs all Order Numbers from the database
        
        query = self.mydb.cursor()
        query.execute("SELECT OrderNumber FROM JOBORDER")

        # Order Number menu is cleared
        self.OrderNumber.clear()

        # Adds '*' selection first, and then adds query results to Customer
        self.OrderNumber.addItem("*")
        for row in query:
            self.OrderNumber.addItem(str(row[0]))
        
        self.OrderNumber.setCurrentIndex(0)

        query.close()

    # Creates a New Order window with the Order List window being the parent and hiding
    def newOrder(self):
        self.hide()
        self.order = NewOrderWindow(self)
        self.order.show()

    # Processes selected row in the Order List window and open a report window for the row
    def viewReport(self):
        # Checks if there is a valid selection
        if len(self.table.selectionModel().selectedRows()) > 0:
            self.hide() # Hides Order list window
            selectedRow = self.table.selectionModel().selectedRows()[0].row() # Processes report for first selection only
            selectedOrder = self.table.item(selectedRow, 0).text() # Grabs OrderNumber from selected row
            self.report = ViewOrder(self, selectedOrder) # Creates child window for the report
            self.report.show() # Shows the child report window

    def deleteOrder(self):
        # Checks if there is a valid selection
        if len(self.table.selectionModel().selectedRows()) > 0:
            selectedRow = self.table.selectionModel().selectedRows()[0].row() # Processes report for first selection only
            selectedOrder = self.table.item(selectedRow, 0).text() # Grabs OrderNumber from selected row

            self.warningBox = Warning(self, "Are you sure?", "You are about to delete Order {}. Do you want to proceed?".format(selectedOrder))

            # Grabs JobNumber that the selected OrderNumber is connected to
            query = self.mydb.cursor()
            query.execute("SELECT JobNumber FROM JOBORDER WHERE OrderNumber={}".format(selectedOrder))
            jobNumber = query.fetchone()[0]
            
            # Deletes all entries associated with the JobNumber/OrderNumber
            query.execute("DELETE FROM JOB WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM JOBORDER WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM ORDERHARDWARE WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM DOOR WHERE JobNumber={}".format(jobNumber))

            # Commit changes to database, close cursor, and update table and dropdowns
            self.mydb.commit()
            query.close()

            self.updateContact()
            self.updateCustomer()
            self.updateOrderNumber()
            self.updateTable()

            #self.report = ViewOrder(self, selectedOrder) # Creates child window for the report

    # Redudant function for closing the Order List window using the Exit button
    def exitWindow(self):
        self.close()
    
    # Function called whenever a change to the table in the Order List window has occurred.
    # This is called whenever the current values for the Customer, Contact, and/or OrderNumber dropdown menus change.
    def updateTable(self):
        
        # Grabs new values for customerID, ContactID, and OrderNumber from 
        # self.CustomerID, self.ContactID, and the OrderNumber dropdown box
        # customerID and contactID must be adjusted by -1 to account for "*"
        # being in index 0
        customerID, contactID, orderNumber = 0, 0, 0
        if len(self.CustomerID) > 1: 
            customerID = self.CustomerID[self.CustomerName.currentIndex() - 1]
        if len(self.ContactID) > 1: 
            contactID = self.ContactID[self.Contact.currentIndex() - 1]
        if len(self.OrderNumber) > 1: 
            orderNumber = self.OrderNumber.currentText()
        #print([customerID, contactID, orderNumber])

        # Formats values to a boolean check for a query, or to a check that grabs everything.
        # Index 0 is '*', which is designed to grab all non-null values.
        # To incorporate this functionality, if-else statements are used.
        if self.CustomerName.currentIndex() == 0:
            customerIDQuery = 'CUSTOMERCONTACTS.CustomerID IS NOT NULL'
        else:
            customerIDQuery = 'CUSTOMERCONTACTS.CustomerID = {}'.format(customerID)

        if self.Contact.currentIndex() == 0:
            contactIDQuery = 'CUSTOMERCONTACTS.ContactID IS NOT NULL'
        else:
            contactIDQuery = 'CUSTOMERCONTACTS.ContactID = {}'.format(contactID)
        
        if self.OrderNumber.currentIndex() == 0:
            orderNumberQuery = 'OrderNumber IS NOT NULL'
        else:
            orderNumberQuery = 'OrderNumber = {}'.format(orderNumber)

        # Query to grab the desired information from the database
        query = self.mydb.cursor()
        query.execute("SELECT OrderNumber, CustomerName, CONCAT(FirstName, ' ', LastName) AS ContactName, JobName, PONumber, JobDate, EstimatedDueDate, OrderStatus" + 
                                " FROM JOB" + 
                                " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber" +
                                " INNER JOIN CUSTOMERCONTACTS ON JOB.MainContact = CUSTOMERCONTACTS.ContactID AND JOB.CustomerID = CUSTOMERCONTACTS.CustomerID" + 
                                " INNER JOIN CUSTOMER ON CUSTOMER.CustomerID = CUSTOMERCONTACTS.CustomerID" + 
                                " INNER JOIN CONTACT ON CONTACT.ContactID = CUSTOMERCONTACTS.ContactID" + 
                                " WHERE {} AND {} AND {}".format(customerIDQuery, contactIDQuery, orderNumberQuery) +
                                " ORDER BY OrderNumber DESC"
                                )
        
        self.table.setRowCount(0) # Resets the Order List window's table by setting its rowCount to 0
        self.table.setColumnCount(8) # Sets number of columns in the table to the number of columns in the query result
        # Sets the column labels
        self.table.setHorizontalHeaderLabels(["Order Number", "Customer Name", "Contact", "Job Name", "PO", "Entered Date", "Due Date", "Job Status"])

        # While the query results has readable rows, the query results are entered in the table
        for row in query:
            # Rows are added by grabbing the current number of rows and adding another row to the table
            rows = self.table.rowCount()
            self.table.setRowCount(rows + 1)
            # For each column in each row, the appropriate value from the query result is entered into a table cell
            for i in range(len(row)):
                if type(row[i]) == type(PyQt5.QtCore.QDate()): # There is a Date type in the database, so that variable needs to be transformed using a .toString() function with a specified format
                    self.table.setItem(rows, i, QTableWidgetItem(query.value(i).toString("MM/dd/yy")))
                else:
                    self.table.setItem(rows, i, QTableWidgetItem(str(row[i])))

        # Makes the columns resize automatically to the available space in the window.
        header = self.table.horizontalHeader()    
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        query.close()
