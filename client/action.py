import sys, time
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from core.connection import Client as FTPClient
from mainwindow import Ui_MainWindow

class Action_MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for Action_MainWindow."""

    client = None
    loginStatus = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

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
        self.client = FTPClient(host = str(self.Host.text()), port = int(str(self.Port.text()) or '0'), userName = str(self.Username.text()), passWord = str(self.Password.text()))
        connectInfo = self.client.createConnection()
        if connectInfo[0] == 0:
            self.infoList.addItem(str(connectInfo[1]))
            loginInfo = self.client.login()
            self.infoList.addItem(str(loginInfo[1]))
            self.loginStatus = True
            self.fileList.addItem(self.client.certInfo)
        else:
            print(type(connectInfo),type(connectInfo[1]),connectInfo)
            self.infoList.addItem(connectInfo[1])
            # self.client.close()
        self.infoList.scrollToBottom()

    def logout(self, arg):
        if self.loginStatus == True:
            logoutInfo = self.client.logout()
            if logoutInfo[0] == 0:
                self.infoList.addItem(logoutInfo[1])
            else:
                self.infoList.addItem(logoutInfo[1])
        else:
            self.infoList.addItem('Not Login')
        self.infoList.scrollToBottom()

    def reconnect(self, arg):
        self.login()
        self.infoList.scrollToBottom()

    def test(self):
        self.infoList.addItem(str('abc'))
        self.infoList.addItem(str('123sdfadfadsdfadfadsfadfadfasdfadfadsfadfadfasfadfadfadsfadf'))
