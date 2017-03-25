import socket, ssl, platform
from core.worker import Worker
from core.database import Db
from core.status import Status
from core.syslog import Syslog
from core.config import Settings
from core.encrypt import SSLCertSetting
from core.utils import *

class Server():
    """docstring for Server."""
    def __init__(self):
        super(Server, self).__init__()
        self.log = Syslog()
        self.settings = Settings()
        self.ssl = SSLCertSetting()
        self.db = Db()
        # self.init_configure()
        # self.init_db()

    def init_check(self):
        system_python_version = platform.python_version()
        if float(system_python_version[:-2]) < 3.5:
            self.log.error(' Version of python on your system is less than 3.5, Cowry software not install here !!')
            exit()
        system_type = platform.system()
        if system_type == 'Linux':
            self.defaultConfigPath = '/etc/cowry/'
        elif system_type == 'Darwin':
            self.defaultConfigPath = '/etc/cowry/'
        elif system_type == 'Windows':
            self.defaultConfigPath = 'C:\\cowry'
        else:
            self.log.error("can't recognize type of your system, Cowry must be installed on Windows, Linux or Darwin system")
            exit()
        try:
            os.stat(self.defaultConfigPath)
        except FileNotFoundError:
            try:
                os.mkdir(self.defaultConfigPath)
            except Exception as e:
                self.log.error(str(e))


    def init_configure(self):
        self.log.info('start init configure file')
        if not os.path.isabs(self.settings.storage.datapath) or not os.path.isdir(self.settings.storage.datapath):
            setDefaultDataPath = os.path.join(getenv('COWRY_ROOT'), 'data')
            if not os.path.isdir(setDefaultDataPath):
                try:
                    os.mkdir(setDefaultDataPath)
                except Exception as e:
                    self.log.error(str(e))
            self.settings._set(('storage', 'datapath', setDefaultDataPath))


    def init_status(self):
        Status().start()

    # def init_db(self):
    #     self.log.info('start init server db')
    #     self.db.initDB()

    def init_ssl(self):
        # check if the certificate exists, if not, sysytem should be auto generate a new certificate
        if not checkFileExists(self.settings.certificates.privatekey) and not checkFileExists(self.settings.certificates.certificate):
            # write path of certificates and privatekey into settings
            setDefaultCertPath = os.path.join(getenv('COWRY_ROOT'), 'certs', 'server.crt')
            setDefaultKeyPath = os.path.join(getenv('COWRY_ROOT'), 'certs', 'server.key')
            self.settings._set(('certificates', 'certificate', setDefaultCertPath))
            self.settings._set(('certificates', 'privatekey', setDefaultKeyPath))
            # generate new certificate
            # check if settings have bind doamin
            if verifyDomain(self.settings.server.bind_domain):
                # a server domain is valid in configure file
                # the server will use this domain to generate a new certificate
                self.ssl.create_self_signed_cert(self.settings.server.bind_domain)
            elif self.settings.server.bind_address:
                self.ssl.create_self_signed_cert(self.settings.certificates.cn)
            else:
                self.log.error("can't read valid domain or IP adress from configure file, create a new certificate need it")
        # start load certificate
        # verify certificates
        if self.ssl.validate_ssl_cert():
            self.sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.log.info('start load certificates: {}'.format(self.settings.certificates.certificate))
            self.sslContext.load_cert_chain(certfile= self.settings.certificates.certificate, keyfile= self.settings.certificates.privatekey)
        else:
            exit()
    def init_socket(self):
        self.log.info('start init server socket')
        # create an INET, STREAMing socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        self.serverSocket.bind((self.settings.server.bind_address, int(self.settings.server.bind_port)))
        # become a server socket
        self.serverSocket.listen(5)

    def init_setenv(self):
        # set host name
        if verifyDomain(self.settings.server.bind_domain):
            setenv('COWRY_HOST', self.settings.server.bind_domain)
            self.log.info('system bind server name on : {}'.format(getenv('COWRY_HOST')))
        else:
            setenv('COWRY_HOST', self.settings.server.bind_address)
            self.log.info('system bind server name on : {}'.format(getenv('COWRY_HOST')))

    def new(self):
        self.log.info('Start congfigure a new cowry sysytem ...')
        self.init_configure()
        self.db.new()
        self.settings._set(('default', 'inited', '1'))
        self.log.info('Congfigure completed, watting for start up ...')

    def start(self):
        if self.settings.default.inited != '1':
            print('Please initialization system firstly !!!')
            exit()
        self.init_ssl()
        self.init_socket()
        self.init_setenv()
        self.init_status()
        self.log.info('start run server')
        while True:
            (clientSocket, clientAddress) = self.serverSocket.accept()
            self.log.info("{}<=====>{}".format(clientSocket, clientAddress))
            client = self.sslContext.wrap_socket(clientSocket, server_side=True)
            self.createWorker(client, clientAddress)

    def drop(self):
        self.log.info('Start drop cowry system !!! ')
        # delete uploaded files
        if os.path.isdir(self.settings.storage.datapath):
            delfolder(self.settings.storage.datapath)
        # delete server certificates
        if checkFileExists(self.settings.certificates.certificate) or checkFileExists(self.settings.certificates.privatekey):
            deleteFile(self.settings.certificates.certificate)
            deleteFile(self.settings.certificates.privatekey)
        # delete all database tables
        self.db.drop()
        self.log.info('Finished drop cowry system')
        exit()


    def createWorker(self, clientSocket, address):
        # workerId = hashlib.md5(str(address).encode('utf8')).hexdigest()
        worker = Worker(clientSocket, address, self.db.Session, sslContext = self.sslContext)
        worker.start()
