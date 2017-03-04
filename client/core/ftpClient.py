from core.socketClient import SocketClient
import logging

class FTPClient(SocketClient):
    """docstring for FTPClient."""
    def __init__(self, **arg):
        super(FTPClient, self).__init__(**arg)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def login(self):
        logging.warning('start login')
        loginCmdCode = {'info': 'login', 'code': '1234', 'u': self.username, 'p': self.password}
        try:
            self.sendMsg(loginCmdCode)
        except Exception as e:
            logging.warning(str(e))
            return (1, str(e))

        try:
            self.recvMsg()
        except Exception as e:
            logging.warning(str(e))
            return (1, str(e))


        if self.recvInfo['status'] == '0':
            return (0, 'Login Successd')
        else:
            return (1, self.recvInfo['reason'])

    def logout(self):
        logoutCmdCode = {'info': 'logout', 'code': ''}
        try:
            self.sendMsg(logoutCmdCode)
        except Exception as e:
            return (1,str(e))
        try:
            self.recvMsg()
        except Exception as e:
            logging.warning(str(e))
            return (1, str(e))

        if self.recvInfo['status'] == '0':
            return (0, 'Logout Successd')
        else:
            return (1, self.recvInfo['reason'])

    def reconnect(self, arg):
        self.logout()
        self.login()

    def upload(self, arg):
        pass

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
            logging.warning(str(e))
            return (1, str(e))
        else:
            return (0, self.recvInfo['list'])
