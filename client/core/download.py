from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets
import threading
from core.baseSocket import BaseSocket
from core.utils import *

class DownloadSignal(QObject):
    # def __init__(self):
    #     super(UploadSignal, self).__init__()
    p = pyqtSignal(tuple)
    recv = pyqtSignal(int)

class Download(threading.Thread, BaseSocket):
    """docstring for Upload."""
    def __init__(self, remote, downloadfileinfo, savefilepath, authtoken, filehashcode, filesize):
        BaseSocket.__init__(self, host = remote[0], port = remote[1])
        threading.Thread.__init__(self)
        # UploadSignal.__init__(self)
        self.createDataSock()
        self.signal = DownloadSignal()
        self.saveFilePath = savefilepath
        self.downloadFileInfo = downloadfileinfo
        self.authtoken = authtoken
        self.fileHashCode = filehashcode
        self.fileSize = filesize
        self.step = 0

        # signal connect
        self.signal.recv.connect(self.drawProgress)

    def run(self):
        authCmdCode = {'info': 'downloadAuth', 'code': '', 'authtoken': self.authtoken}
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
            self.log.info('start download file : {}'.format(self.downloadFileInfo['filename']))

            retInfo = self.recvFile()
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
            else:
                self.log.info(retInfo[1])
            exit()

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
