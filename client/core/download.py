import threading
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets
from core.baseSocket import BaseSocket
from core.cryptogram import Cryptogram
from core.config import Settings
from core import utils

class DownloadSignal(QObject):
    """DownloadSignal."""

    # def __init__(self):
    #     super(UploadSignal, self).__init__()
    p = pyqtSignal(tuple)
    recv = pyqtSignal(int)

class Download(threading.Thread, BaseSocket):
    """docstring for Upload."""

    def __init__(self, remote, savefilepath, authtoken, fileinfo, decrypt_info):
        BaseSocket.__init__(self, host=remote[0], port=remote[1])
        threading.Thread.__init__(self)
        # UploadSignal.__init__(self)
        self.createDataSock()
        self.signal = DownloadSignal()
        self.saveFilePath_E = utils.joinFilePath('/tmp/', fileinfo['name'] + '.enc')
        self.saveFilePath_D = savefilepath
        self.authtoken = authtoken
        self.fileinfo = fileinfo
        self.decrypt_info = decrypt_info
        self.fileHashCode = fileinfo['hashcode']

        if fileinfo['encryption'] == 1:
            self.fileSize = fileinfo['encsize']
        else:
            self.fileSize = fileinfo['size']

        self.crypt = Cryptogram()
        self.settings = Settings()
        self.step = 0

        # signal connect
        self.signal.recv.connect(self.drawProgress)

    def run(self):
        ret = self.createConnection()
        self.log.info(ret)
        authCmdCode = {'info': 'downloadAuth',
                       'code': '',
                       'authtoken': self.authtoken,
                       'hash': self.fileinfo['hashcode']}
        retInfo = self.sendMsg(authCmdCode)
        if retInfo[0] == 1:
            self.log.info(retInfo[1])
            self.close()

        retInfo = self.recvMsg()
        if retInfo[0] == 1:
            self.log.info(retInfo[1])
            self.close()
        elif self.recvInfo['status'] == '0':
            self.lastCmdCode = '23333'
            # self.log.info('start download file : {}'.format(self.downloadFileInfo['filename']))

            retInfo = self.recvFile()
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
            else:
                if self.fileinfo['encryption'] != 1:
                    # move file to download path
                    utils.moveFile(self.saveFilePath_E, self.saveFilePath_D)
                else:
                    self.decryptFile()

    def decryptFile(self):
        if self.fileinfo['is_transfer'] != 1:
            self.log.info('start decrypt file.....')
            retInfo = self.crypt.decrypt(self.decrypt_info['cipher'],
                                         self.saveFilePath_E,
                                         savefilepath=self.saveFilePath_D,
                                         mode=self.fileinfo['encryption_type'])
            if retInfo[0] == 0:
                utils.deleteFile(self.saveFilePath_E)
        else:
            self.log.info('start decrypt file from private_key')
            # get user private key
            private_key = self.settings.default.private_key
            if private_key:
                self.log.info('get private_key : {}'.format(private_key))
            else:
                with open(utils.convertPathFromHome('~/.ssh/id_rsa'), 'rb') as f:
                    private_key = f.read()

            dec_cipher = self.crypt.decrypt_text(self.fileinfo['c_enc'], private_key)
            self.log.info('decrypt c_enc is :{}'.format(dec_cipher))
            self.log.info('start decrypt file.....')
            retInfo = self.crypt.decrypt(dec_cipher[1],
                                         self.saveFilePath_E,
                                         savefilepath=self.saveFilePath_D,
                                         nck=1,
                                         mode=self.fileinfo['encryption_type'])
            if retInfo[0] == 0:
                utils.deleteFile(self.saveFilePath_E)
    def drawProgress(self, p):
        if p == 0:
            # start deal with upload progress bar
            self.callProgressGui((100, '100%'))
        elif p == 1:
            # self.log.info('recvMark : {}'.format(info))
            self.step += 1
            k = int(self.step * 1024 / int(self.fileSize) * 100)
            self.callProgressGui((k, "{}%".format(k)))

    def callProgressGui(self, progress):
        self.signal.p.emit(progress)
