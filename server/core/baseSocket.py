import socket, ssl
from core.config import Settings
from core.syslog import Syslog
from core import utils

class BaseSocket(object):
    """docstring for Client."""
    def __init__(self, **arg):
        super(BaseSocket, self).__init__()
        # self.clientSocket = clientSocket
        # self.clientAddress = clientAddress
        self.log = Syslog()
        self.settings = Settings()

        self.SEND_CMD_BUFFER_SIZE = self.settings['DEFAULT'].getint('SEND_CMD_BUFFER_SIZE')
        self.SEND_FILE_BUFFER_SIZE = self.settings['DEFAULT'].getint('SEND_FILE_BUFFER_SIZE')
        self.RECV_CMD_BUFFER_SIZE = self.settings['DEFAULT'].getint('RECV_CMD_BUFFER_SIZE')

        self.__dict__.update(arg)

    msgCode = ('login','logout','refresh','list','get','put')


    def fillSnedMsg(func):
        def wrapper(self, msg):
            msg = str.encode(str(msg))
            msgLentgh = len(msg)
            if msgLentgh <= self.SEND_CMD_BUFFER_SIZE:
                fillSize = self.SEND_CMD_BUFFER_SIZE - msgLentgh
                msg = b''.join((msg, b' ' * fillSize))
                # print('resize send msg len is :{},type is {}, info is {}'.format(len(msg),type(msg),msg))
                self.log.info('perpare send recall info : {}'.format(msg))
                return func(self, msg)
            else:
                loops = msgLentgh // self.SEND_CMD_BUFFER_SIZE
                extendLentgh = msgLentgh % self.SEND_CMD_BUFFER_SIZE
                for i in range(loops):
                    self.log.info('perpare send recall info by {} loops: {}'.format(i, msg[i*self.SEND_CMD_BUFFER_SIZE:self.SEND_CMD_BUFFER_SIZE*(i + 1)]))
                    retInfo = func(self, msg[i*self.SEND_CMD_BUFFER_SIZE:self.SEND_CMD_BUFFER_SIZE*(i + 1)])
                    if retInfo[0] == 1:
                        return retInfo
                fillSize = self.SEND_CMD_BUFFER_SIZE - extendLentgh
                extendmsg = b''.join((msg[loops*self.SEND_CMD_BUFFER_SIZE:], b' ' * fillSize))
                self.log.info('perpare send recall extendmsg : {}'.format(extendmsg))
                return func(self, extendmsg)
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

    def sendFile(self):
        with open(self.downloadFilePath, 'rb') as f:
            try:
                sendSize = self.clientSocket.sendfile(f)
            except Exception as e:
                self.log.info('send file fails : {}'.format(str(e)))
            else:
                self.log.info('send file Successd')
            finally:
                self.log.info('total send size is :{:.2f} K'.format(sendSize / 1024))

    def recvMsg(self):
        try:
            info_tmp = self.clientSocket.recv(self.RECV_CMD_BUFFER_SIZE).strip()
        except Exception as e:
            return (1, str(e))
        else:
            if len(info_tmp) == 0:
                self.log.info('recv a null info, close client connecting')
                return (2, 'a null info')
            else:
                try:
                    self.recvInfo = utils.rebuildDictFromBytes(info_tmp)
                except Exception as e:
                    self.log.info('error info : {}'.format(info_tmp))
                    return (3, str(e))
                else:
                    return (0, "ok")

    def recvFile(self):
        self.log.info('######## start recv file ########')
        loop = self.fileSize // 1024
        extend = self.fileSize % 1024
        with open(self.uploadFilePath, 'wb') as f:
            recvedFileSize = 0
            for i in range(loop):
                recvfile = self.clientSocket.recv(self.RECV_CMD_BUFFER_SIZE)
                # self.log.info('receving data of file is : {:.2f}%'.format(recvedFileSize / filesize * 100))
                f.write(recvfile)
                self.log.info('start recv {} loop'.format(i))
                self.log.info('this task need to loop {}, the last info size of info is : {}'.format(loop, extend))

                recvedFileSize += len(recvfile)
                self.clientSocket.send(b'1') # receiving file
            recvfile = self.clientSocket.recv(extend)
            f.write(recvfile)

        calculateFileSize = utils.getSizeByPath(self.uploadFilePath)
        self.log.info('upload file size is : {}'.format(calculateFileSize))
        self.log.info('origin file size is : {}'.format(self.fileSize))
        if calculateFileSize == self.fileSize:
            self.clientSocket.send(b'0') # recv finished
            self.log.info('upload finished')
            return (0, 'ok')
        else:
            self.log.info('recved file size is :{}, upload file size is {}'.format(calculateFileSize, self.fileSize))
            self.clientSocket.send(b'2') # size not match
            return (1, 'size not match')

    def close(self):
        self.log.info("worker subprocess end")
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()


    def createSslSock(self):
        self.log.info('start perpare accept data connecting ......')
        self.clientSock, self.clientAddress = self.dataSock.accept()
        self.log.info('recv data connecting, client info is : {}'.format(self.clientAddress))
        self.clientSocket = self.sslContext.wrap_socket(self.clientSock, server_side=True)

    def createDataSock(self):
        self.log.info('start create data socket')
        # create an INET, STREAMing socket
        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        while True:
            randomPort = utils.generateRandomDigitFromRange(2333,2433)
            try:
                self.dataSocket.bind((utils.getenv('COWRY_HOST'), int(randomPort)))
            except Exception as e:
                self.log.info(str(e))
            else:
                dataSocketInfo = self.dataSocket.getsockname()
                self.log.info('data socket create successd on : {}'.format(dataSocketInfo))
                break
        # become a server socket
        self.dataSocket.listen(1)
        # return data port
        return (0, randomPort)


    def test(self):
        self.log.info('host')




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
