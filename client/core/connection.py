import socket, ssl
import json, random
from ast import literal_eval
from config import Settings
# from utils import *

class Client(object):
    """docstring for Client."""
    def __init__(self, **arg):
        super(Client, self).__init__()
        if arg:
            self.__dict__.update(arg)
        self.sslContext = ssl.create_default_context()
        self.sslContext.load_verify_locations('./pubkey/server.crt')

    msgCode = ('login','logout','refresh','list','get','put')
    userName = 'admin'
    passWord = 'admin888'
    host = '127.0.0.1'
    port = 2333

    sslContext = ''

    ctrlSock = ''
    ctrlSockPort = ''

    dataSock = ''
    dataSockPort = ''

    recvInfo = None
    lastCmdCode = ''
    certInfo = ''

    def createConnection(self):
        try:
            tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ctrlSock = self.sslContext.wrap_socket(tmpSock, server_hostname = self.host)
            self.ctrlSock.connect((self.host, self.port))
        except Exception as e:
            return (1,str(e))
        else:
            self.certInfo = str(self.ctrlSock.cipher())
            return (0,'connecting to remote host ...')


    def login(self):
        msg = { 'info' : 'login', 'code' : '1234', 'u' : self.userName, 'p' : self.passWord }
        return self.sendMsg(msg)


    def sendFile(self):
        pass

    def checkCmdCode(func):
        def wrapper(self, msg):
            self.lastCmdCode = '123'
            func(self, msg)
            print(self.recvInfo)
            if self.recvInfo['code'] == self.lastCmdCode:
            # if True:
                return (0,'login successd')
            else:
                return (1,'lastCmdCode is not same, login fails')
        return wrapper

    @checkCmdCode
    def sendMsg(self, msg):
        msg = str.encode(str(msg))
        try:
            self.ctrlSock.send(msg)
            self.recvInfo = literal_eval(self.ctrlSock.recv(1024).decode('utf8'))
            print(self.recvInfo)
        except Exception as e:
            return (0,str(e))

    def logout(self):
        try:
            self.ctrlSock.close()
        except Exception as e:
            return (1,str(e))
        else:
            return (0,'Logout Compeletly')

    def reconnect(self):
        self.logout()
        self.login()


    def close(self):
        self.ctrlSock.close()

    @staticmethod
    def test():
        print('host')




# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# clientSocket.connect(("127.0.0.1", 2333))
#
# f = open('./tmp/1.jpg','rb')
# print('start Sending...')
# l = f.read(1024)
# while (l):
#     print('Sending...')
#     clientSocket.send(l)
#     l = f.read(1024)
# f.close()
# clientSocket.close()
