import socket, ssl
import json, random
from ast import literal_eval
from config import Settings
from core.syslog import Syslog
# from utils import *

class BaseSocket(object):
    """docstring for Client."""
    def __init__(self, clientSocket, clientAddress):
        super(BaseSocket, self).__init__()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.log = Syslog()

        self.SEND_BUFFER_SIZE = 1024


    msgCode = ('login','logout','refresh','list','get','put')


    def fillSnedMsg(func):
        def wrapper(self, msg):
            msg = str.encode(str(msg))
            fillSize = self.SEND_BUFFER_SIZE - len(msg)
            msg = b''.join((msg, b' ' * fillSize))
            # print('resize send msg len is :{},type is {}, info is {}'.format(len(msg),type(msg),msg))
            return func(self, msg)
        return wrapper

    @fillSnedMsg
    def sendMsg(self, msg):
        self.log.info('prepare send msg size : {} '.format(len(msg)))
        try:
            self.clientSocket.send(msg)
        except Exception as e:
            return (1, str(e))
        else:
            return (0, "ok")

    def recvMsg(self):
        try:
            info_tmp = self.clientSocket.recv(1024)
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
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()

    def createDataSock(self):
        self.log.info('start create data  socket')
        # create an INET, STREAMing socket
        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        while True:
            randomPort = random.randrange(2333,2433)
            try:
                self.dataSocket.bind(('127.0.0.1', int(randomPort)))
            except Exception as e:
                self.log.info(str(e))
            else:
                dataSocketInfo = self.dataSocket.getsockname()
                break
        # become a server socket
        self.dataSocket.listen(1)
        return (0, dataSocketInfo)


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
