import threading
from core.baseSocket import BaseSocket

class Upload(threading.Thread, BaseSocket):
    """docstring for Upload."""
    def __init__(self, remote, filepath, authtoken):
        BaseSocket.__init__(self, host = remote[0], port = remote[1])
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.authtoken = authtoken

    def run(self):
        authCmdCode = {'info': 'uploadAuth', 'code': '', 'authtoken': self.authtoken}
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
            self.sendFile()

            retInfo = self.recvMsg()
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
                self.close()
            elif self.recvInfo['status'] == '0':
                self.log.info('upload completed')
            else:
                self.log.info(self.recvInfo['reason'])
