import socket, ssl
import json, random, logging
from ast import literal_eval
from config import settings
from core.syslog import Syslog


# from utils import *

class BaseSocket(object):
    """docstring for Client."""
    def __init__(self, **arg):
        super(BaseSocket, self).__init__()
        if arg:
            self.__dict__.update(arg)
        self.log = Syslog()
        self.settings = settings()
        self.createSslConttext()
        self.createConnection()


    msgCode = ('login','logout','refresh','list','get','put')
    userName = 'admin'
    passWord = 'admin888'
    host = '127.0.0.1'
    port = 2333

    sslContext = ''

    SEND_BUFFER_SIZE = 1024

    ctrlSock = ''
    ctrlSockPort = ''

    dataSock = ''
    dataSockPort = ''

    recvInfo = None
    lastCmd = ''
    lastCmdCode = ''
    certInfo = ''

    def createConnection(self):
        self.log.info('start createConnection')
        try:
            tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ctrlSock = self.sslContext.wrap_socket(tmpSock, server_hostname = '127.0.0.1')
            self.ctrlSock.connect((self.host, int(self.port)))
        except Exception as e:
            self.log.info(str(e))
            # raise
        else:
            self.certInfo = str(self.ctrlSock.cipher())
            self.log.info('connecting to remote host ...')

    def createSslConttext(self):
        self.sslContext = ssl.create_default_context()
        self.sslContext.load_verify_locations(self.settings['certificates']['PublicKey'])

    def createDataSock(self):
        pass


    def sendFile(self):
        with open(self.filepath, 'rb') as f:
            try:
                self.ctrlSock.sendfile(f)
            except Exception as e:
                self.log.info('send file fails : {}'.format(str(e)))
            else:
                self.log.info('send file Successd')
            # finally:
            #     self.close()

    def checkCmdCode(func):
        def wrapper(self):
            res = func(self)
            if self.recvInfo['code'] != self.lastCmdCode:
                self.log.info('lastCmdCode is not same, login fails')
            return res
        return wrapper

    def setupCmdCode(func):
        def wrapper(self, msg):
            self.lastCmdCode = str(random.randrange(10000,99999))
            # print('*********** send msg len is :{},type is {}, info is {}'.format(len(msg),type(msg),msg))
            msg['code'] = self.lastCmdCode
            return func(self, msg)
        return wrapper

    def fillSnedMsg(func):
        def wrapper(self, msg):
            msg = str.encode(str(msg))
            fillSize = self.SEND_BUFFER_SIZE - len(msg)
            msg = b''.join((msg, b' ' * fillSize))
            # print('resize send msg len is :{},type is {}, info is {}'.format(len(msg),type(msg),msg))
            return func(self, msg)
        return wrapper

    @setupCmdCode
    @fillSnedMsg
    def sendMsg(self, msg):
        self.lastCmd = msg
        try:
            self.ctrlSock.send(msg)
        except Exception as e:
            return (1, str(e))
        else:
            self.log.info('send info : {}'.format(msg.strip()))
            # self.log.info('###########{}##########'.format(msg))
            return (0, "ok")

    @checkCmdCode
    def recvMsg(self):
        try:
            recvInfo = self.ctrlSock.recv(1024).strip()
        except Exception as e:
            return (1, str(e))
        else:
            self.recvInfo = literal_eval(recvInfo.decode('utf8'))
            self.log.info('recv info {}'.format(recvInfo.strip()))
            return (0, "ok")

    def logout(self):
        pass

    def reconnect(self):
        pass

    def close(self):
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
