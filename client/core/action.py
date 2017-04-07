from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QProgressBar, QWidget
from PyQt5 import QtWidgets
from resources.mainwindow import Ui_MainWindow
from resources.upload import Ui_UploadFileDialog
from resources.download import Ui_DownloadFileDialog
from core.ftpClient import FTPClient
from core.config import Settings
from core.syslog import Syslog
from core import utils

class Action_MainWindow(QMainWindow, Ui_MainWindow):
    """docstring for Action_MainWindow."""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.Setlist.triggered.connect(self.setlist)
        # self.Download_2.triggered.connect(self.test)

        self.client = None
        self.loginStatus = False
        self.upload_dialog = None
        self.download_dialog = None
        # self.Infolist.scrollToBottom()

    def start(self):
        self.init_configure()
        self.init_folder()
        self.init_log()
        self.init_signal()
        self.init_ui_setting()
        self.show()

    def init_configure(self):
        """Pass."""
        # self.log.info('start init configure file')
        if not utils.checkFileExists(utils.getenv('COWRY_CONFIG')):
            src = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'cowry.conf.default')
            dst = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'cowry.conf')
            utils.copyfile(src, dst)
            print('Not find default configure file, copy default configure to use')

        self.settings = Settings()

        # set default certificates folders values
        if not self.settings.certificates.certdirs:
            setDefaultCertDirs = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'certs')
            self.settings._set(('certificates', 'certdirs', setDefaultCertDirs))

    def init_folder(self):
        # create upload folders
        if not utils.checkFolderExists(self.settings.certificates.certdirs):
            try:
                utils.makeDirs(self.settings.certificates.certdirs)
            except Exception as e:
                self.log.error('certs folder create error : {}'.format(str(e)))

    def init_log(self):
        self.log = Syslog()

    def init_signal(self):
        self.actionloadLoginInfo.triggered.connect(self.setdefaultinfo)
        self.actiondeleteCertificate.triggered.connect(self.deleteCerts)

        self.Encrypts.currentIndexChanged.connect(self.setEncryptStatus)
        self.Usepassword.clicked.connect(self.setCiphercode)

    def init_ui_setting(self):
        if self.Encrypts.currentText() == 'None':
            self.Ciphercode.hide()
            self.Label_cipher.hide()
            self.Usepassword.hide()
            self.Button_encrypt.hide()
        self.Ciphercode.setEnabled(False)
        self.Ciphercode.setText(self.Password.text())
        self.Usepassword.setChecked(True)

    def auth(func):
        def wrapper(self):
            if self.loginStatus != True:
                self.Infolist.addItem('please login system !!!')
            else:
                func(self)
            self.Infolist.scrollToBottom()
        return wrapper

    @auth
    def setEncryptStatus(self):
        if self.Encrypts.currentText() == 'None':
            self.Ciphercode.hide()
            self.Label_cipher.hide()
            self.Usepassword.hide()
            self.Button_encrypt.hide()

            self.client.encrypt = False
            self.Infolist.addItem("Close Local Files Model Of Encryption")
        else:
            self.Ciphercode.show()
            self.Label_cipher.show()
            self.Usepassword.show()
            self.Button_encrypt.show()
        self.setCiphercode()

    @auth
    def setCiphercode(self):
        if self.Usepassword.isChecked():
            self.Ciphercode.setEnabled(False)
            self.Ciphercode.setText(self.Password.text())
        else:
            self.Ciphercode.setText('')
            self.Ciphercode.setEnabled(True)

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
        self.log.info("value of pressed message box button: {}".format(retval))

    def quit(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.loginStatus is True:
                self.logout()
            self.close()
        else:
            print("2333")

    def login(self):
        if self.loginStatus is True:
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
                self.client = FTPClient(host=vhost, port=vport,
                                        username=vusername, password=vpassword)
            except Exception as e:
                self.log.error(e)
            self.client.signal.refresh.connect(self.refresh)
            loginInfo = self.client.login()
            if loginInfo[0] == 0:
                self.Infolist.addItem(str(loginInfo[1]))
                self.Infolist.addItem(str().join(('Encryption with : ', loginInfo[2][2:29])))
                self.loginStatus = True
                self.refresh()
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
        if self.loginStatus is True:
            self.logout()
        self.login()
        self.Infolist.scrollToBottom()

    @auth
    def upload(self):

        try:
            retInfo = QFileDialog.getOpenFileName(self, 'Open upload file', utils.getUserHome())
        except Exception as e:
            self.log.info(e)

        if retInfo[0]:
            filepath = retInfo[0]
            filename = utils.getBaseNameByPath(filepath)
            self.log.info('prepare  file :{}'.format(filepath))

            self.upload_dialog = QtWidgets.QDialog()
            self.upload_dialog.ui = Ui_UploadFileDialog()
            self.upload_dialog.comfirm = self.client.uploadComfirm
            self.upload_dialog.ui.setupUi(self.upload_dialog)
            self.upload_dialog.ui.Filename.setText(filename)
            self.upload_dialog.ui.Progress.setValue(0)
            self.upload_dialog.show()

            self.client.upbar = self.upload_dialog
            retInfo = self.client.upload(filepath)
            if retInfo[0] == 0:
                self.Infolist.addItem('file upload successd')
            else:
                self.Infolist.addItem(retInfo[1])

    @auth
    def download(self):
        selectFiles = self.Filetree.selectedItems()
        if not selectFiles:
            self.Infolist.addItem('Please select file')
        else:
            # self.log.info('selected file is : {}'.format(selectFiles)
            # self.log.info('index : {}'.format(self.Filetree.selectedIndexes()))
            downloadFileInfo = {}
            downloadFileInfo['filename'] = selectFiles[0].text(0)
            downloadFileInfo['postfix'] = selectFiles[0].text(1)
            downloadFileInfo['encryption_type'] = selectFiles[0].text(3)

            downloadFileName = str().join((downloadFileInfo['filename'],
                                           '.',
                                           downloadFileInfo['postfix']))
            # check the download file whether need to decrypt
            # if not, alert info of open encryption option
            if downloadFileInfo['encryption_type'] != 'None' and not self.client.encryption:
                self.Infolist.addItem('The file to be downloaded has been encrypted, you must open encrypt option!')
            else:
                try:
                    retInfo = QFileDialog.getSaveFileName(self, 'Save download file', downloadFileName)
                except Exception as e:
                    raise
                if retInfo[0]:
                    downloadFilePath = retInfo[0]
                #     # filename = os.path.basename(filepath)
                    self.log.info('start draw download progress GUI')
                    self.download_dialog = QtWidgets.QDialog()
                    self.download_dialog.ui = Ui_DownloadFileDialog()
                    self.download_dialog.comfirm = self.client.downloadComfirm
                    self.download_dialog.ui.setupUi(self.download_dialog)
                    self.download_dialog.ui.Filename.setText(downloadFileName)
                    self.download_dialog.ui.Progress.setValue(0)
                    self.download_dialog.show()

                    self.client.dpbar = self.download_dialog
                    retInfo = self.client.download(downloadFileName,
                                                   downloadFilePath,
                                                   decryption_type= downloadFileInfo['encryption_type'])
                    if retInfo[0] == 0:
                        self.Infolist.addItem('file download successd')
                    else:
                        self.Infolist.addItem(retInfo[1])

    @auth
    def refresh(self):
        self.Filetree.clear()
        listInfo = self.client.list()
        # start files list
        # fileList = self.client.list('/')
        if listInfo[0] == 0:
            fileList = QtWidgets.QTreeWidgetItem([" /"])
            if listInfo[1] and isinstance(listInfo[1], list):
                for file in listInfo[1]:
                    if file['encryption'] == '1':
                        encryption = file['encryption_type']
                    else:
                        encryption = 'None'
                    fileItem = QtWidgets.QTreeWidgetItem([file['name'], file['postfix'][1:],
                                                          utils.prettySize(file['size']),
                                                          encryption,
                                                          file['updatetime']])
                    fileList.addChild(fileItem)
            self.Filetree.addTopLevelItem(fileList)
            self.Filetree.expandToDepth(0)
            self.Infolist.addItem("Refresh Completed")
        else:
            self.Infolist.addItem(str(listInfo[1]))

    @auth
    def encrypt(self):
        # if self.Usepassword.clicked():
        #     self.log.info('current select item is : {}'.format(self.Encrypts.currentText()))
        self.client.encryption = True
        self.client.encryption_type = str(self.Encrypts.currentText().strip())
        self.client.encryption_cipher = str(self.Ciphercode.text().strip())
        self.Infolist.addItem("Open Local Files Model Of Encryption")

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.quit()

    def setdefaultinfo(self):
        self.Host.setText('127.0.0.1')
        self.Port.setText('2333')
        self.Username.setText('aong')
        self.Password.setText('1234')

    def deleteCerts(self):
        if utils.delFilesFromFolder(self.settings.certificates.certdirs):
            self.Infolist.addItem("Delete All Certificates In System Successd.")

    def setlist(self):
        self.step += 1
        # fileList = QtWidgets.QTreeWidgetItem([" /"])
        # # if listInfo[1] and type(listInfo[1]) is list:
        # #     for file in fileList[1]:
        # fileItem = QtWidgets.QTreeWidgetItem(['1','2','3','4'])
        # fileList.addChild(fileItem)
        # self.Filetree.addTopLevelItem(fileList)
        # self.upload_dialog.UploadProgress.setValue(50)
        self.upload_dialog.ui.UploadProgress.setValue(self.step)

    def test(self):
        # a=self.Filetree.headerItem()
        # print(a.text(0))
        pass

        # self.Infolist.addItem(str('abc'))
        # self.Infolist.addItem(str('123sdfadfadsdfadfadsfadfadfasdfadfadsfadfadfasfadfadfadsfadf'))
