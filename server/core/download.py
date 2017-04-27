import threading
from core.baseSocket import BaseSocket
from core import utils

class Download(threading.Thread, BaseSocket):
    """docstring for Upload."""

    def __init__(self, sslContext, dataSock, downloadfilepath, authtoken):
        # super(Upload, self).__init__()
        BaseSocket.__init__(self, sslContext=sslContext, dataSock=dataSock)
        threading.Thread.__init__(self)
        self.authtoken = authtoken
        self.downloadFilePath = downloadfilepath

        self.createSslSock()

    def run(self):
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                self.log.info("can't recv download action info : {}".format(recvInfo[1]))
                self.close()
            elif recvInfo[0] == 2:
                self.log.info('client was disconnected')
                self.close()
            elif recvInfo[0] == 3:
                self.log.info('can\'t analyze client command.')
                self.close()

            if self.recvInfo:
                self.log.info('Received  download request cmd code : {}'.format(self.recvInfo))
                cmd = self.recvInfo['info']
                try:
                    func = getattr(self, cmd)
                    func()
                except AttributeError as err:
                    self.log.info(str(err))
            else:
                self.close()

    def downloadAuth(self):
        if self.recvInfo['authtoken'] == self.authtoken:
            authCmdCode = {'info': 'downloadAuth', 'code': self.recvInfo['code'], "status": '0'}
            retInfo = self.sendMsg(authCmdCode)
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
                self.close()
            else:
                # start send file
                self.sendFile()
                exit()
