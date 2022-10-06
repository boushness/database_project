from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QTableWidgetItem
)

# Order Report window Class for viewing Order information from the database.
# Will include CUSTOMER, CONTACT, JOB, JOBORDER, HARDWARE, FINISH, DOOR, etc.
# information from the database for a specific OrderNumber
class ViewOrder(QtWidgets.QMainWindow):
    def __init__(self, parent, orderNumber):

        self.mydb = parent.mydb

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
        query = self.mydb.cursor()
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
