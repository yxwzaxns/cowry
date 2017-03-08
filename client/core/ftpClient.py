from core.baseSocket import BaseSocket
from core.syslog import Syslog
from core.upload import Upload
import hashlib, os

class FTPClient(BaseSocket):
    """docstring for FTPClient."""
    def __init__(self, **arg):
        super(FTPClient, self).__init__(**arg)
        self.log = Syslog()

    def login(self):
        self.log.info('start login')
        loginCmdCode = {'info': 'login', 'code': '1234', 'u': self.username, 'p': self.password}
        loginInfo = self.sendMsg(loginCmdCode)
        if loginInfo[0] == 1:
            self.log.info(loginInfo[1])
            return (1, loginInfo[1])

        recvInfo = self.recvMsg()
        if recvInfo[0] == 1:
            self.log.info(recvInfo[1])
            return (1, recvInfo[1])

        if self.recvInfo['status'] == '0':
            return (0, 'Login Successd')
        else:
            return (1, self.recvInfo['reason'])

    def logout(self):
        self.log.info('start logout')
        logoutCmdCode = {'info': 'logout', 'code': ''}
        logoutInfo = self.sendMsg(logoutCmdCode)
        if logoutInfo[0] == 1:
            return (1,logoutInfo[1])

        recvInfo = self.recvMsg()
        if recvInfo[0] == 1:
            return (1, recvInfo[1])

        if self.recvInfo['status'] == '0':
            return (0, 'Logout Successd')
        else:
            return (1, self.recvInfo['reason'])

    def reconnect(self):
        self.logout()

    def upload(self, filepath, pbar):
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        try:
            with open(filepath, 'rb') as f:
                fileHashCode = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return (1, str(e))

        self.log.info('upload file md5 is :{}'.format(fileHashCode))
        uploadCmdCode = {'info': "upload", "code": "", "filename": filename, "filesize": filesize, "hash": fileHashCode }
        uploadInfo = self.sendMsg(uploadCmdCode)
        if uploadInfo[0] == 1:
            sys.log.info(uploadInfo[1])
        else:
            retInfo = self.recvMsg()
            if retInfo[0] == 1:
                return (1, recvInfo[1])
            elif self.recvInfo['status'] == '0':
                uploadAuthCode = self.recvInfo['token']
                remoteDataInfo = self.recvInfo['dataAddress']
                self.log.info('recv upload auth token is : {}'.format(uploadAuthCode))
                self.log.info('remote open data info : {}:{}'.format(remoteDataInfo[0],remoteDataInfo[1]))

                uploadProcess = Upload(remoteDataInfo, filepath, uploadAuthCode, pbar)
                uploadProcess.start()
                
                return (0, 'ok')
            else:
                return (1, self.recvInfo['reason'])
        # uploadProcess = Upload()

    def uploadComfirm(self):
        uploadComfirmCmdCode = {'info': 'uploadComfirm', 'code': '', 'status': '0'}
        self.sendMsg(uploadComfirmCmdCode)

    def download(self, filename):
        downloadCmdCode = {'info': 'download', 'code': '', 'filename': filename}
        return self.sendMsg(downloadCmdCode)

    def refresh(self, folder):
        return self.list(folder)

    def list(self, folder= '/'):
        listCmdCode = {'info': 'list', 'code': '', 'dir': folder}
        try:
            self.sendMsg(listCmdCode)
        except Exception as e:
            return (1, str(e))

        try:
            self.recvMsg()
        except Exception as e:
            self.log.info(str(e))
            return (1, str(e))
        else:
            return (0, self.recvInfo['list'])
