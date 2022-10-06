# TCSS445, Spring 2021
# Riley Ruckman, 1721498
# Final Project Submission - frontend

#from _typeshed import NoneType
import configparser
import sys
from PyQt5.QtWidgets import QApplication
import mysql.connector

from OrderListWindow import OrderListWindow

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
        password = "MYsql123!",
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

    # The program is exited out of if the database connection is invalid
    if not createConnection():
        sys.exit(1)

    # Creates base application for PyQT
    app = QApplication(sys.argv)

    # Open and show OrderListWindow()
    mainWindow = OrderListWindow(mydb)
    mainWindow.show()

    # Exits program and shuts down base application for PyQT
    sys.exit(app.exec_())

###############################################################################

if __name__ == "__main__":
    main()

