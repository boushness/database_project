from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from menus.OrderListWindow import OrderListWindow
#from OrderListWindow import OrderListWindow

# Main Menu for application
class MainMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, mydb, parent=None):
        super().__init__(parent)

        # Database connection
        self.mydb = mydb

        # Central widget for window
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Creates widget for buttons and sets functions and positions of buttons
        buttons = QtWidgets.QWidget()

        orderListButton = QtWidgets.QPushButton(buttons)
        orderListButton.setText("View/Edit Orders")
        orderListButton.move(0, 0)
        orderListButton.clicked.connect(self.DisplayOrderList)

        exitButton = QtWidgets.QPushButton(buttons)
        exitButton.setText("Exit")
        exitButton.move(0, 30)
        exitButton.clicked.connect(self.ExitMenu)

        # Company logo widget
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap('logo.png').scaledToWidth(200))

        # Adds logo and button widgets to central widget
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(label, 0, 0)
        lay.addWidget(buttons, 1, 0)

        lay.setRowStretch(0, 0)
        lay.setRowStretch(1, 1)

        lay.setRowMinimumHeight(1, 60)

        self.show()

    # Hides main menu and displays list of orders
    def DisplayOrderList(self):
        self.hide()
        orderList = OrderListWindow(self)
        orderList.show()

    # Closes menu
    def ExitMenu(self):
        
        warningBox = QtWidgets.QMessageBox()

        warningBox.setWindowTitle("Are you sure?")
        warningBox.setText("Do you want to exit?")
        warningBox.setIcon(QtWidgets.QMessageBox.Warning)
        warningBox.setStandardButtons(QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No)

        choice = warningBox.exec()

        if choice == QtWidgets.QMessageBox.Yes:
            self.mydb.close()
            QCoreApplication.exit()
    

