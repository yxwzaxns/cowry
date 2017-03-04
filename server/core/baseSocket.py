import socket, ssl
import json, random
from ast import literal_eval
from config import Settings
# from utils import *

class BaseSocket(object):
    """docstring for Client."""
    def __init__(self, clientSocket, clientAddress):
        super(BaseSocket, self).__init__()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

        self.dataSocket = ''


    msgCode = ('login','logout','refresh','list','get','put')

    def sendMsg(self, msg):
        msg = str.encode(str(msg))
        print('prepare send msg size : ', len(msg))
        try:
            self.clientSocket.send(msg)
            # self.recvInfo = literal_eval(self.ctrlSock.recv(1024).decode('utf8'))
            # print(self.recvInfo)
        except Exception as e:
            print(e)
        print(msg)

    def recvMsg(self):
        try:
            info_tmp = self.clientSocket.recv(1024).rstrip()
        except Exception as e:
            return (1, str(e))
        else:
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
