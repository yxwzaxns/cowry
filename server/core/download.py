import threading, os, socket, hashlib
from core.baseSocket import BaseSocket
from config import Settings
from ast import literal_eval

class Download(threading.Thread, BaseSocket):
    """docstring for Upload."""
    def __init__(self, sslContext, dataSock, fileinfo, authtoken):
        # super(Upload, self).__init__()
        BaseSocket.__init__(self, sslContext = sslContext, dataSock = dataSock)
        threading.Thread.__init__(self)
        self.settings = Settings()

        self.fileInfo = fileinfo
        self.authtoken = authtoken
        self.sslContext = sslContext
        self.dataSock = dataSock
        self.downloadFilePath = os.path.join(self.settings.datapath, self.fileInfo.hashcode)

        self.createSslSock()

    def run(self):
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                self.log.info("can't recv download action info : {}".format(recvInfo[1]))
                self.close()
            elif self.recvInfo:
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

    def checkFileIfUpload(self):
        try:
            with open(self.uploadFilePath, 'rb') as f:
                fileHashCode = hashlib.md5(f.read()).hexdigest()
                self.log.info('upload file md5 is :{}'.format(fileHashCode))
        except Exception as e:
            self.log.info("checkFileIfUpload : {}".format(str(e)))
        else:
            if fileHashCode == self.fileHashCode:
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '0'}
            else:
                os.remove(filepath)
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '1', 'reason': "md5 code not same as upload file"}
            self.sendMsg(remsg)
        self.close()


    def recvFile(self, filesize):
        self.log.info('######## start recv file ########')
        loop = filesize // 1024
        extend = filesize % 1024
        with open(self.uploadFilePath, 'wb') as f:
            recvedFileSize = 0
            for i in range(loop):
                recvfile = self.sslDataSock.recv(1024)
                # self.log.info('receving data of file is : {:.2f}%'.format(recvedFileSize / filesize * 100))
                f.write(recvfile)
                self.log.info('start recv {} loop'.format(i))
                self.log.info('this task need to loop {}, the last info size of info is : {}'.format(loop, extend))

                recvedFileSize += len(recvfile)
                self.sslDataSock.send(b'1') # receiving file
            recvfile = self.sslDataSock.recv(extend)
            f.write(recvfile)
        if os.path.getsize(self.uploadFilePath) == filesize:
            self.sslDataSock.send(b'0') # recv finished
            self.log.info('upload finished')
            return (0, 'ok')
        else:
            self.sslDataSock.send(b'2') # size not match
            return (1, 'size not match')
