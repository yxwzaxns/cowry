import threading, os, socket, hashlib
from core.syslog import Syslog
from config import Settings
from ast import literal_eval

class Upload(threading.Thread):
    """docstring for Upload."""
    def __init__(self, sslContext, dataSock, fileHashCode, filesize, authtoken):
        super(Upload, self).__init__()
        self.log = Syslog()
        self.fileHashCode = fileHashCode
        self.filesize = filesize
        self.authtoken = authtoken
        self.sslContext = sslContext
        self.dataSock = dataSock
        self.settings = Settings()
        self.uploadFilePath = os.path.join(self.settings.datapath, self.fileHashCode)

    def run(self):
        self.clientSocket, self.clientAddress = self.dataSock.accept()
        self.sslDataSock = self.sslContext.wrap_socket(self.clientSocket, server_side=True)
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                self.log.info("can't upload info : {}".format(recvInfo[1]))
                self.close()
            elif self.recvInfo:
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
                retInfo = self.recvFile(self.filesize)
                if retInfo[0] == 0:
                    self.checkFileIfUpload()
                else:
                    self.log.info(retInfo[1])

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

    def sendMsg(self, msg):
        msg = str.encode(str(msg))
        print('prepare send msg size : ', len(msg))
        try:
            self.sslDataSock.send(msg)
            # self.recvInfo = literal_eval(self.ctrlSock.recv(1024).decode('utf8'))
            # print(self.recvInfo)
        except Exception as e:
            self.log.info(str(e))
            return (1, str(e))
        else:
            return (0, 'ok')

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

    def recvMsg(self):
        try:
            info_tmp = self.sslDataSock.recv(1024).strip()
        except Exception as e:
            return (1, str(e))
        else:
            print("##########{}############".format(len(info_tmp)))
            info_tmp = info_tmp.strip()
            print("***********{}****************".format(info_tmp))
            try:
                self.recvInfo = literal_eval(info_tmp.decode('utf8'))
            except Exception as e:
                return (1, str(e))
            else:
                return (0, "ok")

    def close(self):
        print("worker subprocess end")
        self.sslDataSock.shutdown(socket.SHUT_RDWR)
        self.sslDataSock.close()
        exit()
