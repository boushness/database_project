# TCSS445, Spring 2021
# Riley Ruckman, 1721498
# Final Project Submission - frontend

#from _typeshed import NoneType
import configparser
from PyQt5 import QtGui
import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QTableWidgetItem,
)
import mysql.connector

# Order Report window Class for viewing Order information from the database.
# Will include CUSTOMER, CONTACT, JOB, JOBORDER, HARDWARE, FINISH, DOOR, etc.
# information from the database for a specific OrderNumber
class ViewOrder(QtWidgets.QMainWindow):
    def __init__(self, parent, orderNumber):

        # Uses QtWidgets.QMainWindow's __init__()
        super().__init__(parent)

        # Set to be deleted by garbage collection
        # when closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Creates widget that all subwidgets will attach to
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        ###############################################################################

        # Initializes self.info for Customer, Contact, and Job information
        self.info = QtWidgets.QWidget()
        #############

        # Initializes all subwidgets of self.info.
        # Most values are grabbed from respective queries where
        # the OrderNumber can be specified with the passed value
        # All text lines/boxes are made read-only
        self.OrderNumber = QtWidgets.QLineEdit(str(orderNumber))
        self.OrderNumber.setReadOnly(True)
        #############
        query = mydb.cursor()
        query.execute('SELECT DISTINCT CustomerName FROM CUSTOMER'
                        + ' INNER JOIN JOB ON JOB.CustomerID = CUSTOMER.CustomerID'
                        + ' INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber'
                        + ' WHERE OrderNumber = {}'.format(orderNumber))

        self.CustomerName = QtWidgets.QLineEdit(query.fetchone()[0])
        self.CustomerName.setReadOnly(True)
        #############
        
        query.execute("SELECT DISTINCT CONCAT(FirstName, ' ', LastName) FROM CONTACT"
                        + " INNER JOIN JOB ON JOB.MainContact = CONTACT.ContactID"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        self.Contact = QtWidgets.QLineEdit(query.fetchone()[0])
        self.Contact.setReadOnly(True)
        #############
        
        query.execute("SELECT JobName FROM JOB"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        self.JobName = QtWidgets.QLineEdit(query.fetchone()[0])
        self.JobName.setReadOnly(True)
        #############
         
        query.execute("SELECT PONumber FROM JOB"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        self.PO = QtWidgets.QLineEdit(query.fetchone()[0])
        self.PO.setReadOnly(True)
        #############
         
        query.execute("SELECT JobDate FROM JOB"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        # Formatting for date type variable
        self.JobDate = QtWidgets.QLineEdit(query.fetchone()[0].strftime("%m/%d/%Y"))
        '''.toString("MM/dd/yy")'''
        self.JobDate.setReadOnly(True)
        #############
         
        query.execute("SELECT EstimatedDueDate FROM JOB"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        # Formatting for date type variable
        self.EstimatedDueDate = QtWidgets.QLineEdit(query.fetchone()[0].strftime("%m/%d/%Y"))
        self.EstimatedDueDate.setReadOnly(True)
        #############
         
        query.execute("SELECT AppliedFinish FROM JOB"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        self.Finish = QtWidgets.QLineEdit(query.fetchone()[0]) 
        # If there is no selected Finish value, 'None' is inserted
        if self.Finish.text() == '':
            self.Finish.insert('None')
        self.Finish.setReadOnly(True)
        #############
         
        query.execute("SELECT CONCAT(Quantity, 'x ', HardwareName) FROM ORDERHARDWARE"
                        + " INNER JOIN JOBORDER ON ORDERHARDWARE.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))

        self.Hardware = QtWidgets.QLineEdit('None')
        # If there is no selected Hardware value, 'None' is inserted
        hardwareText = query.fetchone()
        if query.rowcount != 0 and type(hardwareText) == type(None):
            self.Hardware.insert(hardwareText[0])
        self.Hardware.setReadOnly(True)
        ############# 

        # Labels for self.info subwidgets
        self.OrderNumberLabel = QtWidgets.QLabel('Order Number:')
        self.CustomerNameLabel = QtWidgets.QLabel('Customer:')
        self.ContactLabel = QtWidgets.QLabel('Contact:')
        self.JobNameLabel = QtWidgets.QLabel('Job Name:')
        self.POLabel = QtWidgets.QLabel('PO:')
        self.JobDateLabel = QtWidgets.QLabel('Job Date:')
        self.EstimatedDueDateLabel = QtWidgets.QLabel('Estimated Due Date:')
        self.FinishLabel = QtWidgets.QLabel('Finish:')
        self.HardwareLabel = QtWidgets.QLabel('Hardware:')

        # self.info subwidgets are placed into self.info layout
        lay = QtWidgets.QGridLayout(self.info)

        lay.addWidget(self.OrderNumberLabel, 0, 0, 1, 1)
        lay.addWidget(self.OrderNumber, 1, 0, 1, 1)

        lay.addWidget(self.CustomerNameLabel, 2, 0, 1, 1)
        lay.addWidget(self.CustomerName, 3, 0, 1, 1)
        lay.addWidget(self.ContactLabel, 4, 0, 1, 1)
        lay.addWidget(self.Contact, 5, 0, 1, 1)
        lay.addWidget(self.JobNameLabel, 6, 0, 1, 1)
        lay.addWidget(self.JobName, 7, 0, 1, 1)
        lay.addWidget(self.POLabel, 8, 0, 1, 1)
        lay.addWidget(self.PO, 9, 0, 1, 1)

        lay.addWidget(self.JobDateLabel, 2, 1, 1, 1)
        lay.addWidget(self.JobDate, 3, 1, 1, 1)
        lay.addWidget(self.EstimatedDueDateLabel, 4, 1, 1, 1)
        lay.addWidget(self.EstimatedDueDate, 5, 1, 1, 1)
        lay.addWidget(self.FinishLabel, 6, 1, 1, 1)
        lay.addWidget(self.Finish, 7, 1, 1, 1)
        lay.addWidget(self.HardwareLabel, 8, 1, 1, 1)
        lay.addWidget(self.Hardware, 9, 1, 1, 1)
        ###############################################################################
        
        # self.table is initialized, and a query and for loop grabs the desired information using
        # the passed value
        self.table = QtWidgets.QTableWidget()

         
        query.execute("SELECT DoorQuantity, DoorWidth, DoorHeight, MaterialName,"
                        + " Thickness, StyleCode, InsideProfile, PanelProfile, OutsideProfile, Bore, DoorComment"
                        + " FROM DOOR"
                        + " INNER JOIN JOBORDER ON DOOR.JobNumber = JOBORDER.JobNumber"
                        + " WHERE JOBORDER.OrderNumber = {}".format(orderNumber))

        # self.table has its rows removed, gains columns equal to the number of columns in the query,
        # and gets custom column labels
        self.table.setRowCount(0)
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(['Quantity', 'Door Width', 'Door Height', 'Material', 'Thickness', 'StyleCode',
                                                            'Inside Profile', 'Panel Profile', 'Outside Profile', 'Bore', 'Comment'])
        # Values from the query are added to the table
        for row in query:
            rows = self.table.rowCount()
            self.table.setRowCount(rows + 1)
            for i in range(len(row)):
                self.table.setItem(rows, i, QTableWidgetItem(str(row[i])))

        # Sets resizing behavior for all columns in the table
        header = self.table.horizontalHeader()
        for i in range(10):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.Stretch)

        ###############################################################################

        # Widget for storing the Delivery Method, Shipping Instructions, and Production Comments
        self.shippingAndComments = QtWidgets.QWidget()

        # Subwidgets for self.shippingAndComments. They are read-only.

        # Query to grab DeliveryMethod from the Order
         
        query.execute("SELECT DeliveryMethod FROM JOBORDER"
                        + " WHERE OrderNumber = {}".format(orderNumber))
        self.deliveryMethod = QtWidgets.QLineEdit(query.fetchone()[0])

        # If the Order has no specified DeliveryMethod, the DefaultDeliveryMethod is grabbed
        # from the Customer
        if self.deliveryMethod.text() == '':
             
            query.execute("SELECT DefaultDeliveryMethod FROM CUSTOMER"
                        + " INNER JOIN JOB ON JOB.CustomerID = CUSTOMER.CustomerID"
                        + " INNER JOIN JOBORDER ON JOB.JobNumber = JOBORDER.JobNumber"
                        + " WHERE OrderNumber = {}".format(orderNumber))
            self.deliveryMethod = QtWidgets.QLineEdit(query.fetchone()[0])
        self.deliveryMethod.setReadOnly(True)
        #############
        # Query to grab ShippingInstructions from the Order
         
        query.execute("SELECT ShippingInstructions FROM JOBORDER"
                        + " WHERE OrderNumber = {}".format(orderNumber))
        self.shippingInstructions = QtWidgets.QTextEdit(query.fetchone()[0])
        self.shippingInstructions.setReadOnly(True)
        #############
        # Query to grab ProductionComments from the Order
         
        query.execute("SELECT ProductionComments FROM JOBORDER"
                        + " WHERE OrderNumber = {};".format(orderNumber))
        self.productionComments = QtWidgets.QTextEdit(query.fetchone()[0])
        self.productionComments.setReadOnly(True)
        #############
        
        # Labels for subwidgets
        self.deliveryMethodLabel = QtWidgets.QLabel('Delivery Method: ')
        self.shippingInstructionsLabel = QtWidgets.QLabel('Shipping Instructions:')
        self.productionCommentsLabel = QtWidgets.QLabel('Production Comments:')

        # Subwidgets and labels are added to self.shippingAndComments layout
        lay = QtWidgets.QGridLayout(self.shippingAndComments)

        lay.addWidget(self.deliveryMethodLabel, 0, 0, 1, 1)
        lay.addWidget(self.deliveryMethod, 0, 1, 1, 1)
        lay.addWidget(self.shippingInstructionsLabel, 1, 0, 1, 2)
        lay.addWidget(self.shippingInstructions, 2, 0, 1, 2)
        lay.addWidget(self.productionCommentsLabel, 3, 0, 1, 2)
        lay.addWidget(self.productionComments, 4, 0, 1, 2)

        ###############################################################################

        # Button subwidget
        self.buttons = QtWidgets.QWidget()

        # Button for closing Order Report
        self.exitButton = QtWidgets.QPushButton(self.buttons)
        self.exitButton.setText('Close')
        self.exitButton.move(0, 0)
        self.exitButton.clicked.connect(self.exitOrder)

        ###############################################################################

        # Subwidgets are added to central_widget layout
        lay = QtWidgets.QGridLayout(central_widget)
        self.empty = QtWidgets.QWidget()

        lay.addWidget(self.info, 0, 0, 1, 1)
        lay.addWidget(self.shippingAndComments, 0, 1, 1, 1)
        lay.addWidget(self.table, 1, 0, 1, 2)
        lay.addWidget(self.buttons, 3, 0, 1, 2)

        # Only the table can stretch
        lay.setRowStretch(0, 0)
        lay.setRowStretch(1, 1)
        lay.setRowStretch(2, 0)
        lay.setRowStretch(3, 0)

        # self.info cannot stretch
        lay.setColumnStretch(0, 0)
        lay.setColumnStretch(1, 1)

        # Set minimum row heights for desired look
        lay.setRowMinimumHeight(3, 30)
        lay.setRowMinimumHeight(1, 600)

        # Sets title of window and minimum size of window to allow
        # all information to be comfortably shown 
        self.setWindowTitle("Order Report")
        self.setMinimumSize(1200, 800)

        query.close()

    # Closed Order Report window and shows Order list window
    def exitOrder(self):
        self.close()
        self.parent().show()

###############################################################################

# New Order Form window Class for creating new JOBORDER entries.
# Allows selection of Customer, Contact, Finish, Hardware, etc.
# Allows modular DOOR entries
# Option for cancelling Order Form or inserting Order Form to database
class NewOrderWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):

        # Uses QtWidgets.QMainWindow's __init__()
        super(NewOrderWindow, self).__init__(parent)

        # Set to be deleted by garbage collection
        # when closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Arrays for storing CustomerID and ContactID values.
        # Customer in index 0 of the Customer dropbox menu
        # will have its CustomerID stored in index 0 of the CustomerID array.
        # This is true for ContactID as well.
        self.CustomerID = []
        self.ContactID = []

        # Creates widget that all subwidgets will attach to
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Creates self.info widgets for Order information
        self.info = QtWidgets.QWidget()

        # Initialization of all self.info widgets
        self.OrderNumber = QtWidgets.QLineEdit()
        self.CustomerName = QtWidgets.QComboBox()
        self.Contact = QtWidgets.QComboBox()
        self.JobName = QtWidgets.QLineEdit()
        self.PO = QtWidgets.QLineEdit()

        # Current date is retrieved and put into JobDate.
        # If the current date is on the weekend (Saturday or Sunday),
        # the date is advanced to Monday
        # Monday = 1, Tuesday = 2, ... , Sunday = 7
        date = QtCore.QDate().currentDate()
        while date.dayOfWeek == 6 or date.dayOfWeek == 7:
            date = date.addDays(1)
        self.JobDate = QtWidgets.QDateEdit(date)

        # EstimatedDueDate is 14 days after JobDate by default
        date = date.addDays(14)
        self.EstimatedDueDate = QtWidgets.QDateEdit(date)

        self.Finish = QtWidgets.QComboBox()
        self.Hardware = QtWidgets.QComboBox()
        self.PriceModCheck = QtWidgets.QCheckBox('Custom Price Modification')
        self.PriceMod = QtWidgets.QLineEdit()

        self.OrderNumberLabel = QtWidgets.QLabel('Order Number:')
        self.CustomerNameLabel = QtWidgets.QLabel('Customer Name:')
        self.ContactLabel = QtWidgets.QLabel('Contact:')
        self.JobNameLabel = QtWidgets.QLabel('Job Name:')
        self.POLabel = QtWidgets.QLabel('PO:')
        self.JobDateLabel = QtWidgets.QLabel('Job Date:')
        self.EstimatedDueDateLabel = QtWidgets.QLabel('Estimated Due Date:')
        self.FinishLabel = QtWidgets.QLabel('Finish')
        self.HardwareLabel = QtWidgets.QLabel('Hardware')
        self.PriceModLabel = QtWidgets.QLabel('Price Modification')

        # Opens layout for self.info
        lay = QtWidgets.QGridLayout(self.info)

        # Adds all entry widgets to self.info
        lay.addWidget(self.OrderNumber, 0, 1)
        lay.addWidget(self.CustomerName, 1, 1)
        lay.addWidget(self.Contact, 2, 1)
        lay.addWidget(self.JobName, 3, 1)
        lay.addWidget(self.PO, 4, 1)
        lay.addWidget(self.JobDate, 5, 1)
        lay.addWidget(self.EstimatedDueDate, 6, 1)
        lay.addWidget(self.Finish, 7, 1)
        lay.addWidget(self.Hardware, 8, 1)
        lay.addWidget(self.PriceModCheck, 9, 1)
        lay.addWidget(self.PriceMod, 10, 1)

        # Adds all self.info label widgets to the left
        # of their respective entry widgets
        lay.addWidget(self.OrderNumberLabel, 0, 0)
        lay.addWidget(self.CustomerNameLabel, 1, 0)
        lay.addWidget(self.ContactLabel, 2, 0)
        lay.addWidget(self.JobNameLabel, 3, 0)
        lay.addWidget(self.POLabel, 4, 0)
        lay.addWidget(self.JobDateLabel, 5, 0)
        lay.addWidget(self.EstimatedDueDateLabel, 6, 0)
        lay.addWidget(self.FinishLabel, 7, 0)
        lay.addWidget(self.HardwareLabel, 8, 0)
        lay.addWidget(self.PriceModLabel, 9, 0)

        # The next available OrderNumber for JOBORDER from the database is calculated
        # using the latest JOBORDER entry. The text line cannot be edited, but can be highlighted
        # for copy/paste purposes
        query = mydb.cursor()
        query.execute("SELECT OrderNumber FROM JOBORDER ORDER BY OrderNumber DESC LIMIT 1")
        self.OrderNumber.setText(str(query.fetchone()[0] + 1))
        self.OrderNumber.setReadOnly(True)
        
        # Customer menu and CustomerID array is loaded with CustomerName and CustomerID from the database, respectively
         
        query.execute("SELECT CustomerName, CustomerID FROM CUSTOMER")
        for row in query:
            self.CustomerName.addItem("{}".format(row[0]))
            self.CustomerID.append(row[1])

        # Sets CustomerName to update the Contact menu whenever the current selection changes
        self.CustomerName.activated[str].connect(self.updateContact)

        # Sets maximum character length of JobName and PO to 20 characters
        self.JobName.setMaxLength(20)
        self.PO.setMaxLength(20)

        # Finish dropdown menu is loaded with FinishName from the database
        # with a "None" option
         
        query.execute("SELECT FinishName FROM FINISH;")
        self.Finish.addItem("None")
        for row in query:
            self.Finish.addItem("{}".format(row[0]))

        # Hardware dropdown menu is loaded with HardwareName from the database
        # with a "None" option
         
        query.execute("SELECT HardwareName FROM HARDWARE;")
        self.Hardware.addItem("None")
        for row in query:
            self.Hardware.addItem("{}".format(row[0]))

        # Sets behavior for PriceModCheck checkbox
        # Initially, PriceModCheck is False.unchecked
        # When PriceModCheck changes, a signal connect updates the PriceMod text line
        # PriceMod is validated to only contain int types between -100 and 250
        self.PriceModCheck.setChecked(False)
        self.PriceModCheck.stateChanged.connect(self.updatePriceMod)
        self.PriceMod.setValidator(QtGui.QIntValidator(-100, 250))

        ###############################################################################

        # Creates QTableWidget widget with one row, and formats the row
        self.table = QtWidgets.QTableWidget(1, 11)
        self.formatNewestRow()

        # Sets column labels for the table
        self.table.setHorizontalHeaderLabels(
            ['Quantity', 'Door Width', 'Door Height', 'Material', 'Thickness', 'StyleCode',
            'Inside Profile', 'Panel Profile', 'Outside Profile', 'Bore', 'Comment']
        )
        
        # Sets resizing behavior for all columns in the table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.Stretch)
        
    ##############################################################################

        # Widget for buttons
        self.buttons = QtWidgets.QWidget()

        # Button for exiting the New Order Form without
        # inserting data into the database
        self.exitButton = QtWidgets.QPushButton(self.buttons)
        self.exitButton.setText('Cancel')
        self.exitButton.move(20, 80)
        self.exitButton.clicked.connect(self.exitOrder)

        # Button for exiting the New Order Form and inserting data
        # into the database
        self.doneButton = QtWidgets.QPushButton(self.buttons)
        self.doneButton.setText('Done')
        self.doneButton.move(217, 80)
        self.doneButton.clicked.connect(self.insertOrder)

        # Button for inserting a new row into the table
        self.addRowbutton = QtWidgets.QPushButton(self.buttons)
        self.addRowbutton.setText('Add Row')
        self.addRowbutton.move(20, 0)
        self.addRowbutton.setFixedWidth(290)
        self.addRowbutton.clicked.connect(self.insertNewRow)

        # Button for deleting a selected row from the table
        self.addRowbutton = QtWidgets.QPushButton(self.buttons)
        self.addRowbutton.setText('Delete Selected Row')
        self.addRowbutton.move(20, 40)
        self.addRowbutton.setFixedWidth(290)
        self.addRowbutton.clicked.connect(self.deleteSelectedRow)

        ###############################################################################

        # Widget to store production and invoice comments
        self.comments = QtWidgets.QWidget()

        # Production and invoice comments are stored in QTextEdit widgets
        # Labels are made for both comments using QLabel
        self.productionComments = QtWidgets.QTextEdit()
        self.invoiceComments = QtWidgets.QTextEdit()
        self.productionCommentsLabel = QtWidgets.QLabel('Production Comments:')
        self.invoiceCommentsLabel = QtWidgets.QLabel('Invoice Comments:')

        # The comment widgets are added to the self.comments layout
        lay = QtWidgets.QGridLayout(self.comments)

        lay.addWidget(self.productionComments, 1, 0)
        lay.addWidget(self.productionCommentsLabel, 0, 0)
        lay.addWidget(self.invoiceComments, 1, 1)
        lay.addWidget(self.invoiceCommentsLabel, 0, 1)

        ###############################################################################

        # Widget for shipping-related information and entry
        self.shipping = QtWidgets.QWidget()

        # Dropdown menu that includes all options for product delivery, and label
        self.deliveryMethod = QtWidgets.QComboBox()
        self.deliveryMethodLabel= QtWidgets.QLabel('Delivery Method:')

        # Query grabs all delivery methods that are not 'WILL CALL', and the appends the results
        # to the menu with 'WILL CALL' added first.
        # This is to allow WILL CALL to be the first and default selection in the menu
         
        query.execute("SELECT DeliveryMethodName FROM PRODUCTDELIVERYMETHOD WHERE DeliveryMethodName <> 'WILL CALL'")
        self.deliveryMethod.addItem('WILL CALL')
        for row in query:
            self.deliveryMethod.addItem(row[0])

        # Shipping instruction label and text box
        self.shippingInstructionsLabel = QtWidgets.QLabel('Shipping Instruction:')
        self.shippingInstructions = QtWidgets.QTextEdit()
        
        # Shipping widgets are applied to the self.shipping layout
        lay = QtWidgets.QGridLayout(self.shipping)

        lay.addWidget(self.deliveryMethodLabel, 0, 0, 1, 1)
        lay.addWidget(self.deliveryMethod, 1, 0, 1, 1)
        lay.addWidget(self.shippingInstructionsLabel, 2, 0, 1, 1)
        lay.addWidget(self.shippingInstructions, 3, 0, 1, 1)

        # Only the text box is allowed to stretch
        lay.setColumnStretch(0, 0)
        lay.setColumnStretch(1, 0)
        lay.setColumnStretch(2, 0)
        lay.setColumnStretch(3, 1)
        ###############################################################################

        # Adds all sub-widgets into central widget
        lay = QtWidgets.QGridLayout(central_widget)

        lay.addWidget(self.info, 0, 0, 1, 1)
        lay.addWidget(self.buttons, 1, 0, 1, 1)
        lay.addWidget(self.shipping, 2, 0, 1, 1)
        lay.addWidget(self.table, 0, 1, 2, 2)
        lay.addWidget(self.comments, 2, 1, 1, 2)

        # Sets column and row stretch to allow the table to grow while all of the other
        # widgets minimally stretch
        lay.setColumnStretch(0, 0)
        lay.setColumnStretch(1, 1)
        lay.setColumnStretch(2, 1)

        lay.setRowStretch(0, 0)
        lay.setRowStretch(1, 1)
        lay.setRowStretch(2, 0)

        # Sets minimum height for row 1 so the buttons are displayed correctly
        lay.setRowMinimumHeight(1, 200)

        # Initalizes Contact menu, Price Modification option, Thickness menu, and StyleCode menu
        self.updateContact()
        self.updatePriceMod()
        self.updateThicknessStyleCode()
        self.updateStyleCode()

        # Sets New Order title and minimum window size to comfortably show all content
        self.setWindowTitle("New Order Form")
        self.setMinimumSize(1800, 1000)

    # Verifies QLineEdit text for Door Width and Door Height columns
    def verifyDimensionInput(self):
        # Grabs QLineEdit cell that called for validation
        send = self.sender()
        
        # If the input is not valid, the last character to be added is removed
        if not send.hasAcceptableInput():
            send.end(False)
            send.backspace()

    # Formats the cells of a new row in self.table
    def formatNewestRow(self):

        # Targets the newest row
        latestRow = self.table.rowCount() - 1

        # QLineEdit object for Quantity column
        # Set object's validator to only allow an int input with specified range
        quantityCell = QtWidgets.QLineEdit(parent=self.table)
        quantityCell.setValidator(QtGui.QIntValidator(0, 100))

        # Validator for Door Width and Door Height columns
        doubleValidator = QtGui.QDoubleValidator(0, 200.0, 4)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)

        # QLineEdit widget for Door Width with validator and signal connections to validate input
        doorWidthCell = QtWidgets.QLineEdit(parent=self.table)
        doorWidthCell.setValidator(doubleValidator)
        doorWidthCell.textChanged.connect(self.verifyDimensionInput)
        doorWidthCell.returnPressed.connect(self.verifyDimensionInput)
        doorWidthCell.editingFinished.connect(self.verifyDimensionInput)

        # QLineEdit widget for Door Height with double validator and signal connections to validate input
        doorHeightCell = QtWidgets.QLineEdit(parent=self.table)
        doorHeightCell.setValidator(doubleValidator)
        doorHeightCell.textChanged.connect(self.verifyDimensionInput)
        doorHeightCell.returnPressed.connect(self.verifyDimensionInput)
        doorHeightCell.editingFinished.connect(self.verifyDimensionInput)

        # Sets Quantity, Door Width, and Door Height cells of self.table to customized widgets
        self.table.setCellWidget(latestRow, 0, quantityCell)
        self.table.setCellWidget(latestRow, 1, doorWidthCell)
        self.table.setCellWidget(latestRow, 2, doorHeightCell)

        # An array of queries in the same order as the cells in table's rows
        queries = []

        queries.append("SELECT DISTINCT MaterialName FROM MATERIAL")
        queries.append("SELECT DISTINCT Thickness FROM MATERIAL")
        queries.append("SELECT StyleCode FROM DOORSTYLE")
        queries.append("SELECT ProfileName FROM DOORPROFILE WHERE ProfileType = 'I'")
        queries.append("SELECT ProfileName FROM DOORPROFILE WHERE ProfileType = 'P'")
        queries.append("SELECT ProfileName FROM DOORPROFILE WHERE ProfileType = 'O'")
        queries.append("SELECT HingeBoringName FROM HINGEBORING")

        query = mydb.cursor()
        # Cells that use and/or require pre-existing values from the database are loaded with a dropdown menu
        for j in range(3, 10):
            # A new dropdown menu object is made with self.table as the parent.
            # The object is also set as editable so the user can input the values they want EDIT: Not anymore, caused input issues
            ch = QtWidgets.QComboBox(parent=self.table)
            #ch.setEditable(True)
            # Certain values can be NULL, so those cells have a "None" option
            # This value is the first option in the affected menus
            if j >= 6:
                ch.addItem("None")
            # The dropdown menu is loaded with the values from the respective query.
            
            query.execute(queries[j-3])
            for row in query:
                ch.addItem(row[0])
            # The Material cell has a signal connection to update the Thickness and StyleCode menus
            if j == 3:
                ch.currentIndexChanged.connect(self.updateThicknessStyleCode)
            # The Thickness cell has a signal connection to update the StyleCode menus
            if j == 4:
                ch.currentIndexChanged.connect(self.updateStyleCode)
            # Sets specific self.table cell as the customized widget
            self.table.setCellWidget(latestRow, j, ch)

        # Comment column is a QLineEdit widget with a 20-character limit
        comment = QtWidgets.QLineEdit(parent=self.table)
        comment.setMaxLength(30)
        self.table.setCellWidget(latestRow, 10, comment)

        # Changes Material cell's current selection from 1 to 0 to manually trigger updateThicknessStyleCode
        self.table.cellWidget(latestRow, 3).setCurrentIndex(1)
        self.table.cellWidget(latestRow, 3).setCurrentIndex(0)

        query.close()

    # Inserts and formats a new row to the bottom of self.table
    def insertNewRow(self):
        rowCount = self.table.rowCount()
        self.table.insertRow(rowCount)
        self.formatNewestRow()
    
    # Deletes user-selected row from self.table
    def deleteSelectedRow(self):
        if len(self.table.selectionModel().selectedRows()) > 0: # Checks if any rows are selected
            selectedRow = self.table.selectionModel().selectedRows()[0].row() # Deletes first selected row only
            self.table.removeRow(selectedRow) # Removes row

    # Updates available Thickness and StyleCode selections based on new Material selection
    def updateThicknessStyleCode(self):

        # Grabs row of Material dropdown menu that triggered the signal
        row = self.table.indexAt(self.sender().pos()).row()

        # Creates new object to replace Thickness menu with
        chNew = QtWidgets.QComboBox(parent=self.table)
        #chNew.setEditable(True)
        
        # Query for getting Thickness values based on Material
        query = mydb.cursor()
        query.execute("SELECT DISTINCT Thickness FROM MATERIAL WHERE MaterialName = '{}'"
            .format(self.table.cellWidget(row, 3).currentText()))
        
        # Adds query values to new Thickness menu object
        for queryRow in query:
            chNew.addItem(queryRow[0])
        
        query.close()

        # Sets signal connection for when the user interacts with the Thickness dropdown menu
        chNew.currentIndexChanged.connect(self.updateStyleCode)

        # Replaces current Thickness menu object with new object
        self.table.setCellWidget(row, 4, chNew)

        ######################################################################################################

        # Creates new object to replace StyleCode menu with
        chNew = QtWidgets.QComboBox(parent=self.table)
        #chNew.setEditable(True)

        # Query for getting StyleCode values based on Material and Thickness
        query = mydb.cursor()
        query.execute("SELECT DISTINCT StyleCode FROM STYLEPRICING WHERE MaterialName = '{}'"
            .format(self.table.cellWidget(row, 3).currentText()))
        
        # Adds query values to new StyleCode menu object
        for queryRow in query:
            chNew.addItem(queryRow[0])
        
        query.close()

        # Replaces current StyleCode menu object with new object
        self.table.setCellWidget(row, 5, chNew)
    
    # Updates available StyleCode selection based on current Material selection and new Thickness selection
    def updateStyleCode(self):
        # Grabs row of Thickness dropdown menu that triggered the signal
        row = self.table.indexAt(self.sender().pos()).row()

        # Creates new object to replace StyleCode menu with
        chNew = QtWidgets.QComboBox(parent=self.table)
        #chNew.setEditable(True)

        # Query for getting StyleCode values based on Material and Thickness
        query = mydb.cursor()
        query.execute("SELECT StyleCode FROM STYLEPRICING WHERE MaterialName = '{}' AND Thickness = '{}'"
            .format(self.table.cellWidget(row, 3).currentText(), self.table.cellWidget(row, 4).currentText()))
        
        # Adds query values to new StyleCode menu object
        for queryRow in query:
            chNew.addItem(queryRow[0])
        
        query.close()
        
        # Replaces current StyleCode menu object with new object
        self.table.setCellWidget(row, 5, chNew)

    # Closes New Order window, updates the Order List parent window, and show the Order List window
    def exitOrder(self):
        self.close()

        # Updates Order List's Customer, Contact, and Order Number dropdown menus and table 
        # with current database data
        self.parent().updateCustomer()
        self.parent().updateContact()
        self.parent().updateOrderNumber()
        self.parent().updateTable()

        self.parent().show()
    
    # Will transform New Order entries into a series of INSERT statements to enter the 
    # order into the database
    def insertOrder(self):
        # Hides Order Form so user can alter any data
        self.hide()

        # Checks if any of the rows have complete entries for the Quantity, Door Width, and Door Height
        # If so, then the order, doors, and hardware can be added to the database
        isEmpty = True
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).text() != '' and self.table.cellWidget(i, 1).text() != '' and self.table.cellWidget(i, 2).text() != '':
                isEmpty = False

        if not isEmpty:
            
            # Converts any empty string or 'None' to NULL, or surrounds string with '' for
            # the INSERT statement
            # For text from QComboBox/dropdown menu objects, a seperate variable is used
            # to contain the verified value
            if self.JobName.text() == '':
                self.JobName.setText('NULL')
            else:
                self.JobName.setText("'{}'".format(self.JobName.text()))
            
            if self.PO.text() == '':
                self.PO.setText('NULL')
            else:
                self.PO.setText("'{}'".format(self.PO.text()))
            
            finish = self.Finish.currentText()
            if self.Finish.currentText() == 'None':
                finish = 'NULL'
            else:
                finish = "'{}'".format(self.Finish.currentText())
            
            if self.PriceMod.text() == '':
                self.PriceMod.setText('NULL')
            else:
                self.PriceMod.setText("'{}'".format(self.PriceMod.text()))

            # Inserts JOB into database after validating all variables
            insertQueryStatement = ("INSERT INTO JOB (CustomerID, MainContact, JobDate, EstimatedDueDate, JobName, PONumber, JobType, AppliedFinish, PriceModificationPerc)"
                            + " VALUES({}, {}, '{}', '{}', {}, {}, 'O', {}, {})"
                            .format(
                                    self.CustomerID[self.CustomerName.currentIndex()], 
                                    self.ContactID[self.Contact.currentIndex()], 
                                    self.JobDate.date().toString('yyyyMMdd'),   # Dates are converted to a format that is accepted
                                    self.EstimatedDueDate.date().toString('yyyyMMdd'), # by the database
                                    self.JobName.text(),
                                    self.PO.text(),
                                    finish,
                                    self.PriceMod.text()
                                    )
            )

            query = mydb.cursor()
            query.execute(insertQueryStatement)
            #print(insertQueryStatement)
            
            # Query to grab the latest job that was created, which will be the job created with the last query
            jobQuery = mydb.cursor()
            jobQuery.execute("SELECT JobNumber FROM JOB ORDER BY JobNumber DESC LIMIT 1")
            jobNumber = str(jobQuery.fetchone()[0])

            # Converts any empty string or 'None' to NULL, or surrounds string with '' for
            # the INSERT statement
            # For text from QComboBox/dropdown menu objects, a seperate variable is used
            # to contain the verified value
            if self.productionComments.toPlainText() == '':
                self.productionComments.setText('NULL')
            else:
                self.productionComments.setText("'{}'".format(self.productionComments.toPlainText()))

            if self.invoiceComments.toPlainText() == '':
                self.invoiceComments.setText('NULL')
            else:
                self.invoiceComments.setText("'{}'".format(self.invoiceComments.toPlainText()))

            if self.shippingInstructions.toPlainText() == '':
                self.shippingInstructions.setText('NULL')
            else:
                self.shippingInstructions.setText("'{}'".format(self.shippingInstructions.toPlainText()))

            # Inserts JOBORDER into database after validating all variables
            insertQueryStatement = ("INSERT INTO JOBORDER (JobNumber, ProductionComments, InvoiceComments, ShippingInstructions, DeliveryMethod, OrderStatus)"
                            + " VALUES({}, {}, {}, {}, '{}', 'Processing')"
                            .format(jobNumber,
                                    self.productionComments.toPlainText(),
                                    self.invoiceComments.toPlainText(),
                                    self.shippingInstructions.toPlainText(),
                                    self.deliveryMethod.currentText()
                                )
                             )
             
            query.execute(insertQueryStatement)
            #print(insertQueryStatement)

            # Summing variable to determine Hardware Quantity
            hardwareNum = 0

            # Goes through each row of the table
            for i in range(self.table.rowCount()):
                
                # Any rows with incomplete entries of Quantity, Door Width, and Door Height are not processed to avoid issues
                if (self.table.cellWidget(i, 0).text() == '' or self.table.cellWidget(i, 1).text() == '' or self.table.cellWidget(i, 2).text() == '' or
                        self.table.cellWidget(i, 0).text() == '0' or self.table.cellWidget(i, 1).text() == '0' or self.table.cellWidget(i, 2).text() == '0'):

                    continue # Continues through the rest of the table
                else:

                    # Converts any empty string or 'None' to NULL, or surrounds string with '' for
                    # the INSERT statement
                    # For text from QComboBox/dropdown menu objects, a seperate variable is used
                    # to contain the verified value
                    insideProfile = self.table.cellWidget(i, 6).currentText()
                    if insideProfile == 'None':
                        insideProfile = 'NULL'
                    else:
                        insideProfile = "'{}'".format(self.table.cellWidget(i, 6).currentText())
                    
                    panelProfile = self.table.cellWidget(i, 7).currentText()
                    if panelProfile == 'None':
                        panelProfile = 'NULL'
                    else:
                        panelProfile = "'{}'".format(self.table.cellWidget(i, 7).currentText())
                    
                    outsideProfile = self.table.cellWidget(i, 8).currentText()
                    if outsideProfile == 'None':
                        outsideProfile = 'NULL'
                    else:
                        outsideProfile = "'{}'".format(self.table.cellWidget(i, 8).currentText())
                    
                    if self.table.cellWidget(i, 10).text() == '':
                        self.table.cellWidget(i, 10).setText('NULL')
                    else:
                        self.table.cellWidget(i, 10).setText("'{}'".format(self.table.cellWidget(i, 10).text()))
                    
                    bore = self.table.cellWidget(i, 9).currentText()
                    if bore == 'None':
                        bore = 'NULL'
                    else:
                        bore = "'{}'".format(self.table.cellWidget(i, 9).currentText())

                    # Inserts DOOR into database after validating all variables
                    insertQueryStatement = ("INSERT INTO DOOR VALUES({}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {})"
                            .format(
                                    jobNumber,
                                    i + 1,
                                    self.table.cellWidget(i, 3).currentText(),
                                    self.table.cellWidget(i, 4).currentText(),
                                    self.table.cellWidget(i, 5).currentText(),
                                    self.table.cellWidget(i, 0).text(),
                                    self.table.cellWidget(i, 1).text(),
                                    self.table.cellWidget(i, 2).text(),
                                    insideProfile,
                                    panelProfile,
                                    outsideProfile,
                                    self.table.cellWidget(i, 10).text(),
                                    bore,

                                    )
                                )
                     
                    query.execute(insertQueryStatement)
                    #print(insertQueryStatement)

                    # Door Quantity is summed into hardwareNum
                    hardwareNum += int(self.table.cellWidget(i, 0).text())

            # If Hardware was chosen, an INSERT is called with the selected Hardware and hardwareNum
            if self.Hardware.currentText() != 'None':
                insertQueryStatement = ("INSERT INTO ORDERHARDWARE VALUES({}, '{}', {})".format(jobNumber, self.Hardware.currentText(), hardwareNum))
                 
                query.execute(insertQueryStatement)
                #print(insertQueryStatement)
            
            # Commit data to database
            mydb.commit()
            query.close()
        # Exits out of the Order Form
        self.exitOrder()

    # Updates Contact options based on the selected Customer
    def updateContact(self):
        # Grabs CustomerID of the current Customer selection using self.CustomerID
        customerID = self.CustomerID[self.CustomerName.currentIndex()]

        # Query to grab Contact name from database
        query = mydb.cursor()
        query.execute("SELECT CONCAT(FirstName, ' ', LastName) AS Name, CONTACT.ContactID" 
            + " FROM CONTACT INNER JOIN CUSTOMERCONTACTS ON CONTACT.ContactID = CUSTOMERCONTACTS.ContactID"
            + " WHERE CustomerID = {}".format(customerID))

        # Clears Contact menu
        self.Contact.clear()
        self.ContactID.clear()

        # Fills Contact menu and Contact ID with query results
        for row in query:
            self.Contact.addItem(row[0])
            self.ContactID.append(row[1])
    
    # Updates the Prime Modification box to allow user input or not.
    # If set to off, the current input is cleared
    def updatePriceMod(self):    
        if self.PriceModCheck.isChecked():
            self.PriceMod.setReadOnly(False)
        else:
            self.PriceMod.setReadOnly(True)
            self.PriceMod.clear()

#############################################################################################################

# Order List window Class for viewing JOBORDER entries in the database.
# Allows searching of JOBORDER by Customer, Contact, and/or Order Number
# Allows entry of new JOBORDERs and report views of JOBORDER entries
class OrderListWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

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
        query = mydb.cursor()
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
        
        query = mydb.cursor()
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
        
        query = mydb.cursor()
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
            query = mydb.cursor()
            query.execute("SELECT JobNumber FROM JOBORDER WHERE OrderNumber={}".format(selectedOrder))
            jobNumber = query.fetchone()[0]
            
            # Deletes all entries associated with the JobNumber/OrderNumber
            query.execute("DELETE FROM JOB WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM JOBORDER WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM ORDERHARDWARE WHERE JobNumber={}".format(jobNumber))
            query.execute("DELETE FROM DOOR WHERE JobNumber={}".format(jobNumber))

            # Commit changes to database, close cursor, and update table and dropdowns
            mydb.commit()
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
        query = mydb.cursor()
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

#############################################################################################################

# Creates and verifies connection with database
def createConnection():

    # Uses PyQt SQL database connection library
    """
    # Adds database connection protocol to available options
    con = QSqlDatabase.addDatabase("QMYSQL")

    # Sets parameters for connecting to the database.
    # Includes the driver, server name, database name, and the type of connection
    
    # Sets hostname for the current location.
    # Since the database is hosted locally, I used localhost
    con.setHostName('localhost')
    con.setDatabaseName("ruckmans")
    con.setUserName('root')
    con.setPassword('mysqlPassword_123')

    # Verifies that the connection is valid. 
    # If it is not valid, an error will appear and the function will return False.
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    
    """

    # Uses MySQL Python connector
    config = configparser.ConfigParser()
    config.read("dbcon.cfg")

    global mydb

    mydb = mysql.connector.connect(
        host = config["DEFAULT"]["host"],
        user = "riley",
        password = "password",
        database = config["DEFAULT"]["database"]
    )

    """
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    print(len(mycursor.fetchone()))
    """

    return True

###############################################################################

# Makes connection to database and open an Order List window
def main():

    # Creates base application for PyQT
    app = QApplication(sys.argv)

    # The program is exited out of if the database connection is invalid
    if not createConnection():
        sys.exit(1)

    # Open and show OrderListWindow()
    mainWindow = OrderListWindow()
    mainWindow.show()

    # Exits program and shuts down base application for PyQT
    sys.exit(app.exec_())

###############################################################################

if __name__ == "__main__":
    main()

