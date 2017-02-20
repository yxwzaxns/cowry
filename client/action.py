import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets

class Action_MainWindow(QMainWindow):
    """docstring for Action_MainWindow."""
    def __init__(self):
        # super(Action_MainWindow, self).__init__()
        super().__init__()

    def getinfo(self):
        # QtWidgets.QMessageBox.information(self.pushButton,"标题","这是第一个PyQt5 GUI程序")
       msg = QtWidgets.QMessageBox()
       msg.setIcon(QtWidgets.QMessageBox.Information)

       msg.setText("This is a message box")
       msg.setInformativeText("This is additional information")
       msg.setWindowTitle("MessageBox demo")
       msg.setDetailedText("The details are as follows:")
       msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

       retval = msg.exec_()
    #    print("value of pressed message box button:", retval)

    def quit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # sys.exit()
            self.close()
        else:
            print("2333")

    def login(self):
        pass

    def logout(self):
        pass

    def reconnect(self):
        pass
