import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QTableWidgetItem,
)

from menus.ViewOrder import ViewOrder
from menus.OrderWindow import OrderWindow

# Order List Window Class for viewing JOBORDER entries in the database.
# Allows searching of JOBORDER by Customer, Contact, and/or Order Number
# Allows entry of new JOBORDERs and report views of JOBORDER entries
class OrderListWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        
        # Uses QtWidgets.QMainWindow's __init__()
        super().__init__(parent)

        self.mydb = parent.mydb

        # Set to be deleted by garbage collection
        # when closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Creates central widget that all other widgets will attach to.
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Arrays for storing CustomerID and ContactID values.
        # Customer in index x of the Customer dropbox menu
        # will have its CustomerID stored in index x of the CustomerID array.
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
        self.JobNumber = QtWidgets.QComboBox()

        # Label widgets for Customer, Contact, and Order Number
        self.CustomerNamelabel = QtWidgets.QLabel('Customer')
        self.ContactLabel = QtWidgets.QLabel('Contact')
        self.OrderNumberLabel = QtWidgets.QLabel('Order Number')

        # Adds widgets to self.selection grid layout
        lay.addWidget(self.CustomerName, 1, 0)
        lay.addWidget(self.Contact, 1, 1)
        lay.addWidget(self.JobNumber, 1, 2)
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
        self.JobNumber.setEditable(True)

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

        # A JobNumber selection will reset Customer, update Contacts, and update the table
        self.JobNumber.activated[str].connect(self.updateCustomer)
        self.JobNumber.activated[str].connect(self.updateContact)
        self.JobNumber.activated[str].connect(self.updateTable)

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
        self.JobNumber.setCurrentIndex(0)
    """

    # Updates all elements of OrderListWindow
    def update(self):
        self.updateContact()
        self.updateCustomer()
        self.updateOrderNumber()
        self.updateTable()


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
        query.execute("SELECT JobNumber FROM JOBORDER")

        # Order Number menu is cleared
        self.JobNumber.clear()

        # Adds '*' selection first, and then adds query results to Customer
        self.JobNumber.addItem("*")
        for row in query:
            self.JobNumber.addItem(str(row[0]))
        
        self.JobNumber.setCurrentIndex(0)

        query.close()

    # Creates a New Order window with the Order List window being the parent and hiding
    def newOrder(self):
        self.hide()
        self.order = OrderWindow(self)
        self.order.show()

    # Processes selected row in the Order List window and open a report window for the row
    def viewReport(self):
        # Checks if there is a valid selection
        if len(self.table.selectionModel().selectedRows()) > 0:
            self.hide() # Hides Order list window
            selectedRow = self.table.selectionModel().selectedRows()[0].row() # Processes report for first selection only
            selectedOrder = self.table.item(selectedRow, 0).text() # Grabs JobNumber from selected row
            report = ViewOrder(self, selectedOrder) # Creates child window for the report
            report.show() # Shows the child report window

    def deleteOrder(self):
        # Checks if there is a valid selection
        if len(self.table.selectionModel().selectedRows()) > 0:
            selectedRow = self.table.selectionModel().selectedRows()[0].row() # Processes report for first selection only
            selectedOrder = self.table.item(selectedRow, 0).text() # Grabs JobNumber from selected row

            warningBox = QtWidgets.QMessageBox()

            warningBox.setWindowTitle("Are you sure?")
            warningBox.setText("You are about to delete Order {}.".format(selectedOrder)
                + "\nDo you want to proceed?")
            warningBox.setIcon(QtWidgets.QMessageBox.Warning)
            warningBox.setStandardButtons(QtWidgets.QMessageBox.Yes |
                QtWidgets.QMessageBox.No)

            choice = warningBox.exec()
            
            if choice == QtWidgets.QMessageBox.Yes:
                # Grabs JobNumber that the selected JobNumber is connected to
                query = self.mydb.cursor()
                query.execute("SELECT JobNumber FROM JOBORDER WHERE JobNumber={}".format(selectedOrder))
                jobNumber = query.fetchone()[0]
                
                # Deletes all entries associated with the JobNumber/JobNumber
                query.execute("DELETE FROM JOB WHERE JobNumber={}".format(jobNumber))
                query.execute("DELETE FROM JOBORDER WHERE JobNumber={}".format(jobNumber))
                query.execute("DELETE FROM ORDERHARDWARE WHERE JobNumber={}".format(jobNumber))
                query.execute("DELETE FROM DOOR WHERE JobNumber={}".format(jobNumber))

                # Commit changes to database, close cursor, and update table and dropdowns
                self.mydb.commit()
                query.close()

                self.update()

    # Redudant function for closing the Order List window using the Exit button
    def exitWindow(self):
        self.close()
        self.parent().show()
    
    # Function called whenever a change to the table in the Order List window has occurred.
    # This is called whenever the current values for the Customer, Contact, and/or JobNumber dropdown menus change.
    def updateTable(self):
        
        # Grabs new values for customerID, ContactID, and JobNumber from 
        # self.CustomerID, self.ContactID, and the JobNumber dropdown box
        # customerID and contactID must be adjusted by -1 to account for "*"
        # being in index 0
        customerID, contactID, JobNumber = 0, 0, 0
        if len(self.CustomerID) > 1: 
            customerID = self.CustomerID[self.CustomerName.currentIndex() - 1]
        if len(self.ContactID) > 1: 
            contactID = self.ContactID[self.Contact.currentIndex() - 1]
        if len(self.JobNumber) > 1: 
            JobNumber = self.JobNumber.currentText()
        #print([customerID, contactID, JobNumber])

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
        
        if self.JobNumber.currentIndex() == 0:
            orderNumberQuery = 'JOBORDER.JobNumber IS NOT NULL'
        else:
            orderNumberQuery = 'JOBORDER.JobNumber = {}'.format(JobNumber)

        # Query to grab the desired information from the database
        query = self.mydb.cursor()
        query.execute("SELECT JOBORDER.JobNumber, CustomerName, CONCAT(FirstName, ' ', LastName) AS ContactName, JobName, PONumber, JobDate, EstimatedDueDate, OrderStatus" + 
                                " FROM JOBORDER" + 
                                " INNER JOIN JOB ON JOBORDER.JobNumber = JOB.JobNumber" +
                                " INNER JOIN CUSTOMERCONTACTS ON JOB.MainContact = CUSTOMERCONTACTS.ContactID AND JOB.CustomerID = CUSTOMERCONTACTS.CustomerID" + 
                                " INNER JOIN CUSTOMER ON CUSTOMER.CustomerID = CUSTOMERCONTACTS.CustomerID" + 
                                " INNER JOIN CONTACT ON CONTACT.ContactID = CUSTOMERCONTACTS.ContactID" + 
                                " WHERE {} AND {} AND {} AND JOB.JobType = 'O'".format(customerIDQuery, contactIDQuery, orderNumberQuery) +
                                " ORDER BY JOBORDER.JobNumber DESC"
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
