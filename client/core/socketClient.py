import socket, ssl
import json, random, logging
from ast import literal_eval
from config import Settings
# from utils import *

class SocketClient(object):
    """docstring for Client."""
    def __init__(self, **arg):
        super(SocketClient, self).__init__()
        if arg:
            self.__dict__.update(arg)
        self.createSslConttext()
        self.createConnection()


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
    lastCmd = ''
    lastCmdCode = ''
    certInfo = ''

    def createConnection(self):
        logging.warning('start createConnection')
        try:
            tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ctrlSock = self.sslContext.wrap_socket(tmpSock, server_hostname = '127.0.0.1')
            self.ctrlSock.connect((self.host, self.port))
        except Exception as e:
            logging.warning(str(e))
        else:
            self.certInfo = str(self.ctrlSock.cipher())
            logging.warning('connecting to remote host ...')

    def createSslConttext(self):
        self.sslContext = ssl.create_default_context()
        self.sslContext.load_verify_locations('./pubkey/server.crt')

    def login(self):
        pass


    def sendFile(self):
        pass

    def checkCmdCode(func):
        def wrapper(self):
            func(self)
            if self.recvInfo['code'] != self.lastCmdCode:
                print('lastCmdCode is not same, login fails')
        return wrapper

    def setupCmdCode(func):
        def wrapper(self, msg):
            self.lastCmdCode = str(random.randrange(10000,99999))
            msg['code'] = self.lastCmdCode
            print('setup cmd code')
            func(self, msg)
        return wrapper

    @setupCmdCode
    def sendMsg(self, msg):
        self.lastCmd = msg
        msg = str.encode(str(msg))
        self.ctrlSock.send(msg)
        print('send info : ', msg)

    @checkCmdCode
    def recvMsg(self):
        recvInfo = self.ctrlSock.recv(1024).strip()
        self.recvInfo = literal_eval(recvInfo.decode('utf8'))
        print('recv info ', recvInfo)

    def logout(self):
        pass

    def reconnect(self):
        pass

    def _close(self):
        self.ctrlSock.shutdown(socket.SHUT_RDWR)
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
