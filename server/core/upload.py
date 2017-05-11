import threading
from core.baseSocket import BaseSocket
from core.utils import *

class Upload(threading.Thread, BaseSocket):
    """docstring for Upload."""
    def __init__(self, sslContext, dataSock, fileHashCode, filesize, authtoken):
        BaseSocket.__init__(self, sslContext = sslContext, dataSock = dataSock)
        threading.Thread.__init__(self)
        self.fileHashCode = fileHashCode
        self.fileSize = filesize
        self.authtoken = authtoken

        self.uploadFilePath = joinFilePath(self.settings['STORAGE']['Datapath'], self.fileHashCode)

        self.createSslSock()

    def run(self):
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                self.log.info("can't upload info : {}".format(recvInfo[1]))
                self.close()
            elif recvInfo[0] == 2:
                self.log.info('client was disconnected')
                self.close()
            elif recvInfo[0] == 3:
                self.log.info('can\'t analyze client command.')
                self.close()

            if self.recvInfo:
                self.log.info('Received cmd code : {}'.format(self.recvInfo))
                cmd = self.recvInfo['info']
                try:
                    func = getattr(self, cmd)
                    func()
                except AttributeError as err:
                    self.log.info(str(err))
            else:
                self.close()

    def uploadAuth(self):
        if self.recvInfo['authtoken'] == self.authtoken:
            authCmdCode = {'info': 'uploadAuth', 'code': self.recvInfo['code'], "status": '0'}
            retInfo = self.sendMsg(authCmdCode)
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
                self.close()
            else:
                retInfo = self.recvFile()
                if retInfo[0] == 0:
                    self.checkFileIfUpload()
                else:
                    self.log.info(retInfo[1])

    def checkFileIfUpload(self):
        try:
            fileHashCode = calculateHashCodeForFile(self.uploadFilePath)
        except Exception as e:
            self.log.info("checkFileIfUpload : {}".format(str(e)))
        else:
            self.log.info('upload file  md5 code is : {}'.format(fileHashCode))
            if fileHashCode == self.fileHashCode:
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '0'}
            else:
                # deleteFile(self.uploadFilePath)
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '1', 'reason': "md5 code not same as upload file"}
            self.sendMsg(remsg)
        self.close()
        exit()
