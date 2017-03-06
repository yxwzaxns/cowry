import sys, time
from PyQt5.QtWidgets import QMainWindow, QMessageBox,QFileDialog,QProgressBar,QWidget
from PyQt5 import QtWidgets
from core.ftpClient import FTPClient
from mainwindow import Ui_MainWindow
from upload import Ui_UploadFileDialog
from core.upload import Upload
from core.syslog import Syslog

class Action_MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for Action_MainWindow."""

    client = None
    loginStatus = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Setdefaultinfo.triggered.connect(self.setdefaultinfo)
        self.Setlist.triggered.connect(self.setlist)
        self.Download_2.triggered.connect(self.test)
        self.log = Syslog()
        # self.Infolist.scrollToBottom()

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
    def auth(func):
        def wrapper(self):
            if self.loginStatus != True:
                self.Infolist.addItem('please login system !!!')
            else:
                func(self)
            self.Infolist.scrollToBottom()
        return wrapper

    def quit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.loginStatus == True:
                self.logout()
            self.close()
        else:
            print("2333")

    def login(self):
        if self.loginStatus == True:
            self.logout()
        self.Filetree.clear()
        vhost = str(self.Host.text().strip())
        vport = int(str(self.Port.text().strip()) or '0')
        vusername = str(self.Username.text().strip())
        vpassword = str(self.Password.text().strip())
        if not vhost or not vport or not vusername or not vpassword:
            self.Infolist.addItem('please input connecting info')
        else:
            try:
                self.client = FTPClient(host = vhost, port = vport, username = vusername, password = vpassword)
            except Exception as e:
                raise
            loginInfo = self.client.login()
            if loginInfo[0] == 0:
                self.Infolist.addItem(str(loginInfo[1]))
                self.loginStatus = True
                listInfo = self.client.list()
                # start files list
                # fileList = self.client.list('/')
                if listInfo[0] == 0:
                    fileList = QtWidgets.QTreeWidgetItem([" /"])
                    if listInfo[1] and type(listInfo[1]) is list:
                        for file in listInfo[1]:
                            fileItem = QtWidgets.QTreeWidgetItem([file['name'], file['postfix'], file['size'], file['updatetime']])
                            fileList.addChild(fileItem)
                    self.Filetree.addTopLevelItem(fileList)
                else:
                    self.Infolist.addItem(str(listInfo[1]))


                # self.fileList.addItem(self.client.certInfo)
                # self.Filetree.topLevelItem(0).setText(0, QtCore.QCoreApplication.translate("MainWindow", "/"))
                # self.Filetree.topLevelItem(0).child(1).setText(0, QtCore.QCoreApplication.translate("MainWindow", "sw"))
                # self.Filetree.topLevelItem(0).child(1).setText(1, QtCore.QCoreApplication.translate("MainWindow", "a"))
                # self.Filetree.topLevelItem(0).child(1).setText(2, QtCore.QCoreApplication.translate("MainWindow", "a"))
                # self.Filetree.topLevelItem(0).child(1).setText(3, QtCore.QCoreApplication.translate("MainWindow", "a"))
            else:
                # print(type(loginInfo),type(loginInfo[1]), loginInfo)
                self.Infolist.addItem(loginInfo[1])
                # self.client.close()
        self.Infolist.scrollToBottom()

    @auth
    def logout(self):
        logoutInfo = self.client.logout()
        if logoutInfo[0] == 0:
            self.Infolist.addItem(logoutInfo[1])
            self.Filetree.clear()
            self.loginStatus = False
        else:
            self.Infolist.addItem(logoutInfo[1])

    def reconnect(self):
        self.log.info('start reconnect')
        self.Filetree.clear()
        if self.loginStatus == True:
            self.logout()
        self.login()
        self.Infolist.scrollToBottom()

    @auth
    def upload(self):

        try:
            retInfo = QFileDialog.getOpenFileName(self, 'Open upload file', '~')
        except Exception as e:
            raise

        if retInfo[0]:
            filename = retInfo[0]
            self.log.info('prepare  file :{}'.format(filename))

            uploadInfo = self.client.upload(filename)
            if uploadInfo[0] == 1:
                self.Infolist.addItem(uploadInfo[1])

            # uploadProcess = Upload(filename, authToken)
            # uploadProcess.start()
            #
            # upload_dialog = QtWidgets.QDialog()
            # upload_dialog.ui = Ui_UploadFileDialog()
            # upload_dialog.ui.setupUi(upload_dialog)
            # upload_dialog.exec_()
            # upload_dialog.show()
        # print(type(self.Filetree))
        # self.Filetree.topLevelItem(0).setText(0, QtCore.QCoreApplication.translate("MainWindow", "/"))

    @auth
    def download(self):
        print('ok')

    @auth
    def refresh(self):
        self.Filetree.clear()

        print('ok')

    def setdefaultinfo(self):
        self.Host.setText('127.0.0.1')
        self.Port.setText('2333')
        self.Username.setText('aong')
        self.Password.setText('1234')

    def setlist(self):
        fileList = QtWidgets.QTreeWidgetItem([" /"])
        # if listInfo[1] and type(listInfo[1]) is list:
        #     for file in fileList[1]:
        fileItem = QtWidgets.QTreeWidgetItem(['1','2','3','4'])
        fileList.addChild(fileItem)
        self.Filetree.addTopLevelItem(fileList)

    def test(self):
        upload_dialog = QtWidgets.QDialog()
        upload_dialog.ui = Ui_UploadFileDialog()
        upload_dialog.ui.setupUi(upload_dialog)
        upload_dialog.exec_()
        upload_dialog.show()

        # self.Infolist.addItem(str('abc'))
        # self.Infolist.addItem(str('123sdfadfadsdfadfadsfadfadfasdfadfadsfadfadfasfadfadfadsfadf'))
