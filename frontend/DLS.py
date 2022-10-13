# TCSS445, Spring 2021
# Riley Ruckman, 1721498
# Final Project Submission - frontend

#from _typeshed import NoneType
import configparser
import sys
from PyQt5.QtWidgets import QApplication
import mysql.connector

from MainMenuWindow import MainMenuWindow

# Creates and verifies connection with database
def createConnection():

    # Uses MySQL Python connector
    config = configparser.ConfigParser()
    config.read("dbcon.cfg")

    try: 
        mydb = mysql.connector.connect(
            host = config["DEFAULT"]["host"],
            user = "riley",
            password = "MYsql123!",
            database = config["DEFAULT"]["database"]
        )
    except:
        sys.exit("Database Connection Failed")
    
    return mydb

# Makes connection to database and open an Order List window
def main():

    # The program is exited out of if the database connection is invalid

    # Creates base application for PyQT
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Open and show main menu
    mainWindow = MainMenuWindow(createConnection())
    #QObject.connect(mainWindow)

    # Exits program and shuts down base application for PyQT
    sys.exit(app.exec())

###############################################################################

if __name__ == "__main__":
    main()

