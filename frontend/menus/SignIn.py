from PyQt5 import QtWidgets
import mysql.connector
import configparser

# Dialog window for signing in into application
# Validates with user information stored on database
class SignIn(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.createForm()

    # Creates form for user to interact with, including fields for login credentials and buttons
    def createForm(self):
        form = QtWidgets.QFormLayout()
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.passwordLineEdit = QtWidgets.QLineEdit()

        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        submitButton = QtWidgets.QPushButton("Submit")
        cancelButton = QtWidgets.QPushButton("Cancel")
        submitButton.setDefault(True)

        submitButton.clicked.connect(self.LogIn)
        cancelButton.clicked.connect(self.close)

        form.addRow("Name:", self.nameLineEdit)
        form.addRow("Password:", self.passwordLineEdit)
        form.addRow(cancelButton, submitButton)

        self.setLayout(form)

    # Creates valid connection to database and closes sign-in box
    # if login credentials are valid
    def LogIn(self):
        if self.createConnection():
            self.accept()

    # Creates connection to local MySQL server
    # Uses MySQL Python connector
    def createConnection(self):

        # Reads config file with server IP address and database name
        config = configparser.ConfigParser()
        config.read("config/dbcon.cfg")

        # Attempts to create connection with database with given name and password.
        try: 
            self.connection = mysql.connector.connect(
                host = config["DEFAULT"]["host"],
                user = self.nameLineEdit.text(),
                password = self.passwordLineEdit.text(),
                database = config["DEFAULT"]["database"]
            )
        except:
            # Creates warning message about incorrect login
            warning = QtWidgets.QMessageBox()

            warning.setWindowTitle("Please Try Again")
            warning.setText("Your login credentials are incorrect.\nPlease try again.")

            warning.exec()

            # Wipes name and password text fields
            self.nameLineEdit.setText('')
            self.passwordLineEdit.setText('')

            return 0

        return 1
