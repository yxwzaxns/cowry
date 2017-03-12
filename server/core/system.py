import socket, ssl
from core.worker import Worker
from core.database import Db
from core.status import Status
from core.syslog import Syslog
from core.config import Settings
from core.utils import *

class Server(Db):
    """docstring for Server."""
    def __init__(self, configurePath):
        super(Server, self).__init__()
        self.init_configure(configurePath)
        self.log = Syslog()
        self.init_db()
        self.init_status()
        self.init_ssl()
        self.init_socket()
        self.log.info('start init server')

    address = '127.0.0.1'
    port = '2333'

    sslContext = ''
    serverSocket = ''

    def init_configure(self, configurePath):
        self.settings = Settings(configPath= configurePath)

    def init_status(self):
        Status().start()

    def init_db(self):
        self.initDB()

    def init_ssl(self):
        self.sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.log.info('start load certificates: {}'.format(self.settings.certificates.certificate))
        self.sslContext.load_cert_chain(certfile= self.settings.certificates.certificate, keyfile= self.settings.certificates.privatekey)

    def init_socket(self):
        self.log.info('start init server socket')
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
            self.log.info("{}<=====>{}".format(clientSocket, clientAddress))
            client = self.sslContext.wrap_socket(clientSocket,server_side=True)
            self.createWorker(client, clientAddress)


    def createWorker(self, clientSocket, address):
        # workerId = hashlib.md5(str(address).encode('utf8')).hexdigest()
        worker = Worker(clientSocket, address, self.Session, sslContext = self.sslContext)
        worker.start()
