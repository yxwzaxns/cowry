import socket
import ssl
import sys
import hashlib
from core.worker import Worker
from core.database import Db
import logging
from core.status import Status

class Server(Db):
    """docstring for Server."""
    def __init__(self, **arg):
        print('start init server')
        super(Server, self).__init__()
        if arg:
            self.__dict__.update(arg)
        self.init_db()
        self.init_status()
        self.init_ssl()
        self.init_socket()


    address = '127.0.0.1'
    port = '2333'

    sslContext = ''
    serverSocket = ''

    workers = []

    def init_status(self):
        Status().start()

    def init_db(self):
        self.initDB()

    def init_ssl(self):
        self.sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.sslContext.load_cert_chain(certfile="./certs/server.crt", keyfile="./certs/server.key")

    def init_socket(self):
        print('start init server socket')
        # create an INET, STREAMing socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        self.serverSocket.bind((self.address, int(self.port)))
        # become a server socket
        self.serverSocket.listen(5)

    def start(self):
        while True:
            (clientSocket, clientAddress) = self.serverSocket.accept()
            print(clientSocket,'===', clientAddress)
            client = self.sslContext.wrap_socket(clientSocket,server_side=True)
            self.createWorker(client, clientAddress)


    def createWorker(self, clientSocket, address):
        # workerId = hashlib.md5(str(address).encode('utf8')).hexdigest()
        worker = Worker(clientSocket, address, self.Session, sslContext = self.sslContext)
        worker.start()
        self.workers.append(worker)
