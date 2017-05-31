import threading
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets
from core.baseSocket import BaseSocket
from core import utils


class UploadSignal(QObject):
    # def __init__(self):
    #     super(UploadSignal, self).__init__()
    p = pyqtSignal(tuple)

class Upload(threading.Thread, BaseSocket):
    """docstring for Upload."""

    def __init__(self, remote, filepath, authtoken, file_info):
        BaseSocket.__init__(self, host=remote[0], port=remote[1])
        threading.Thread.__init__(self)
        # UploadSignal.__init__(self)
        self.signal = UploadSignal()
        self.filepath = filepath
        self.filename = utils.getBaseNameByPath(self.filepath)
        self.authtoken = authtoken
        self.file_info = file_info
        self.step = 0

    def run(self):
        self.createConnection()
        authCmdCode = {'info': 'uploadAuth', 'code': '', 'authtoken': self.authtoken, 'file_info': self.file_info}
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
            self.log.info('start upload file : {}'.format(self.filepath))

            utils.startNewThread(self.sendFile)

            # self.sendFile()
            self.drawProgress()

            retInfo = self.recvMsg()
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
            elif self.recvInfo['status'] == '0':
                self.log.info('upload completed')
                if self.filepath[0:4] == '/tmp':
                    # delete temp file
                    utils.deleteFile(self.filepath)
            else:
                self.log.info(self.recvInfo['reason'])
            exit()

    def drawProgress(self):
        filesize = utils.getSizeByPath(self.filepath)
        info = self.recvMark()
        count = 0
        while True:
            if info == b'0' or len(info) == 0:
                # start deal with upload progress bar
                self.log.info('recv mark end')
                self.callProgressGui((100, '100%'))
                # self.upload_dialog.ui.Percentage_label.setText('100%')
                break
            elif info == b'2':
                self.log.info('size of upload file is not same with local file ')
                # print(info)
            else:
                # self.log.info('recvMark : {}'.format(info))
                count += 1
                p = int(count * 1024 / filesize * 100)
                if p >= 99:
                    p = 100
                # self.upload_dialog.ui.UploadProgress.setValue(p)
                # self.upload_dialog.ui.Percentage_label.setText("{}%".format(p))
                self.callProgressGui((p, "{}%".format(p)))
            info = self.recvMark()

    def callProgressGui(self, progress):
        self.signal.p.emit(progress)
