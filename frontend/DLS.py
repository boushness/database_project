import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from menus.MainMenuWindow import MainMenuWindow
from menus.SignIn import SignIn

# Launches GUI engine, asks for login credentials, and starts main menu
def main():

    # Creates base application for PyQT
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    signin = SignIn()
    signin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    if signin.exec() == QtWidgets.QDialog.Accepted:
        #print([signin.name, signin.password])

        # Open and show main menu
        mainWindow = MainMenuWindow(signin.connection)
        
        # Exits program and shuts down base application for PyQT
        sys.exit(app.exec_())
    else:
        sys.exit()


if __name__ == "__main__":
    #print(os.listdir())
    main()

