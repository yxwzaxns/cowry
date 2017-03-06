import threading, os, socket, hashlib
from core.syslog import Syslog
from config import Settings
from ast import literal_eval

class Upload(threading.Thread):
    """docstring for Upload."""
    def __init__(self, sslContext, dataSock, fileHashCode, authtoken):
        super(Upload, self).__init__()
        self.log = Syslog()
        self.fileHashCode = fileHashCode
        self.authtoken = authtoken
        self.sslContext = sslContext
        self.dataSock = dataSock
        self.settings = Settings()

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
                retInfo = self.recvFile()
                if retInfo[0] == 0:
                    self.checkFileIfUpload()
                else:
                    self.log.info(retInfo[1])

    def checkFileIfUpload(self):
        filepath = os.path.join(self.settings.datapath, self.fileHashCode)
        try:
            with open(filepath, 'rb') as f:
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

    def recvFile(self):
        self.log.info('######## start recv file ########')
        with open(os.path.join(self.settings.datapath, self.fileHashCode), 'wb') as f:
            try:
                fileData = self.sslDataSock.recv(1024)
                while fileData:
                    f.write(fileData)
                    fileData = self.sslDataSock.recv(1024)
            except Exception as e:
                self.log.info("can't write data to file : {}".format(str(e)))
                ret =  (1, str(e))
            else:
                self.log.info('recv file end')
                ret = (0, 'ok')
        return ret

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
