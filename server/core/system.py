"""Cowry system core module."""
import socket
import ssl
import time
import platform
import redis
import stat, os
from core.worker import Worker
from core.database import Db
from core.status import Status
from core.syslog import Syslog
from core.config import Settings
from core.console import WebConsole
from core.encrypt import SSLCertSetting
from core import utils

class Server():
    """docstring for Server."""

    def __init__(self):
        """Default model is start, Add some necessary for it."""
        super(Server, self).__init__()
        self.log = None
        self.settings = None
        self.ssl = None
        self.db = None
        self.systemStatus = None
        self.serverSocket = None
        self.defaultConfigPath = None

        self.init_configure()
        self.init_log()

    def init_check(self):
        """Init check."""
        system_python_version = platform.python_version()
        if float(system_python_version[:-2]) < 3.5:
            self.log.error(' Version of python on your system is less than 3.5, \
                            Cowry software not install here !!')
            exit()
        system_type = platform.system()
        if system_type == 'Linux':
            self.defaultConfigPath = '/etc/cowry/'
        elif system_type == 'Darwin':
            self.defaultConfigPath = '/etc/cowry/'
        elif system_type == 'Windows':
            self.defaultConfigPath = 'C:\\cowry'
        else:
            self.log.error("can't recognize type of your system, \
                            Cowry must be installed on Windows, Linux or Darwin system")
            exit()
        try:
            # os.stat(self.defaultConfigPath)
            pass
        except FileNotFoundError:
            try:
                pass
                # os.mkdir(self.defaultConfigPath)
            except Exception as e:
                self.log.error(str(e))

    def init_db(self):
        """Pass."""
        self.db = Db()

    def init_configure(self):
        """Pass."""
        # self.log.info('start init configure file')
        if not utils.checkFileExists(utils.getenv('COWRY_CONFIG')):
            src = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'cowry.conf.default')
            dst = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'cowry.conf')
            utils.copyfile(src, dst)
            print('Not find default configure file, copy default configure to use')

        self.settings = Settings()

        # set default uploaded files path
        if not utils.checkAbsPath(self.settings.storage.datapath) or not utils.checkFolderExists(self.settings.storage.datapath):
            setDefaultDataPath = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'data')
            self.settings._set(('storage', 'datapath', setDefaultDataPath))
        # set default certificates values
        if not utils.checkAbsPath(self.settings.certificates.privatekey) and not utils.checkAbsPath(self.settings.certificates.certificate):
            setDefaultPrivateKey = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'certs', 'server.key')
            setDefaultCert = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'certs', 'server.crt')
            self.settings._set(('certificates', 'privatekey', setDefaultPrivateKey))
            self.settings._set(('certificates', 'certificate', setDefaultCert))
        # set db default path if sqlite be used
        if self.settings.database.type == 'sqlite' and not self.settings.database.df:
            setDefaultSqliteDbPath = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'db', 'data', 'default.sqlite')
            self.settings._set(('database', 'df', setDefaultSqliteDbPath))

    def init_folder(self):
        """Pass."""
        # create upload folders
        if not utils.checkFolderExists(self.settings.storage.datapath):
            try:
                utils.makeDirs(self.settings.storage.datapath)
            except Exception as e:
                self.log.error('upload folder create : {}'.format(str(e)))
        # create certs folders
        cert_dir_name = utils.getDirNameByPath(self.settings.certificates.privatekey)
        if not utils.checkFolderExists(cert_dir_name):
            try:
                utils.makeDirs(cert_dir_name)
            except Exception as e:
                self.log.error('cert folder create : {}'.format(str(e)))
        # create database folders if system use sqlite
        if self.settings.database.type == 'sqlite':
            db_dir_name = utils.getDirNameByPath(self.settings.database.df)
            if not utils.checkFolderExists(db_dir_name):
                utils.makeDirs(db_dir_name)
            if not utils.checkFolderExists(db_dir_name):
                try:
                    utils.makeDirs(db_dir_name)
                except Exception as e:
                    self.log.error('db folder create : {}'.format(str(e)))

    def init_log(self):
        """Pass."""
        self.log = Syslog()

    def init_status(self):
        """Pass."""
        if utils.getenv('COWRY_STATUS') != 'NO':
            self.systemStatus = Status()
            self.systemStatus.start()
        else:
            self.log.info('Start system without echo status of system.')

    def init_web_console(self):
        # up redis
        # set app root path into redis
        # if utils.getenv('COWRY_WEB_CONSOLE') == 'YES':
        self.log.info('start init server web console')
        WebConsole.start()


    def init_ssl(self):
        self.ssl = SSLCertSetting()
        # check if the certificate exists, if not, sysytem should be auto generate a new certificate
        if not utils.checkFileExists(self.settings.certificates.privatekey) and not utils.checkFileExists(self.settings.certificates.certificate):
            # generate new certificate
            # check if settings have bind doamin
            if utils.verifyDomain(self.settings.server.bind_domain):
                # a server domain is valid in configure file
                # the server will use this domain to generate a new certificate
                self.ssl.create_self_signed_cert(self.settings.server.bind_domain)
            elif self.settings.server.bind_address:
                self.ssl.create_self_signed_cert(self.settings.certificates.cn)
            else:
                self.log.error("can't read valid domain or IP adress from configure file, create a new certificate need it")
            # set key own
            os.chmod(path=self.settings.certificates.privatekey, mode=stat.S_IRUSR)
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

    def init_redis(self):
        if self.settings.default.cluster == '0':
            # redis_host = '127.0.0.1'
            return 0
        else:
            redis_host = self.settings.redis.host
        self.r = redis.Redis(host=redis_host,
                        port=int(self.settings.redis.port),
                        db=int(self.settings.redis.db))
        for i in range(3):
            if self.r.ping() == True:
                continue
            else:
                time.sleep(1)
                if i == 3:
                    self.log.error('can\'t connect redis server')
                    exit()
        self.r.set('master_status','1')

    def init_setenv(self):
        # set host name
        if utils.verifyDomain(self.settings.server.bind_domain):
            utils.setenv('COWRY_HOST', self.settings.server.bind_domain)
            self.log.info('system bind server name on : {}'.format(utils.getenv('COWRY_HOST')))
        else:
            utils.setenv('COWRY_HOST', self.settings.server.bind_address)
            self.log.info('system bind server name on : {}'.format(utils.getenv('COWRY_HOST')))

    def new(self):
        if self.settings.default.inited != '0':
            print('System has been inited !!')
            exit()

        self.log.info('Start congfigure a new cowry sysytem ...')
        self.init_folder()
        self.init_db()
        self.db.new()
        self.settings._set(('default', 'inited', '1'))
        self.log.info('Congfigure completed, watting for start up ...')

    def start(self):
        if self.settings.default.inited != '1':
            print('Please initialization system firstly !!!')
            exit()
        self.init_db()
        self.init_ssl()
        self.init_redis()
        self.init_socket()
        self.init_setenv()
        self.init_web_console()
        self.init_status()
        self.log.info('start run server')
        while True:
            (clientSocket, clientAddress) = self.serverSocket.accept()
            self.log.info("{}<=====>{}".format(clientSocket, clientAddress))
            try:
                client = self.sslContext.wrap_socket(clientSocket, server_side=True)
            except Exception as e:
                self.log.info(str(e))
            else:
                self.createWorker(client, clientAddress)

    def drop(self):
        """Clear system info and delete all info of cowry."""
        # check if system been droped
        # Check that the system has been deleted
        if self.settings.default.inited == '0':
            self.log.info('the system has been deleted'.title())
            utils.deleteFile(utils.getenv('COWRY_CONFIG'))
            exit()
        self.log.info('Start drop cowry system !!! ')
        # delete uploaded files
        if utils.checkFolderExists(self.settings.storage.datapath):
            utils.delfolder(self.settings.storage.datapath)
        # delete server certificates
        if utils.checkFileExists(self.settings.certificates.certificate) or utils.checkFileExists(self.settings.certificates.privatekey):
            utils.deleteFile(self.settings.certificates.certificate)
            utils.deleteFile(self.settings.certificates.privatekey)
        utils.delfolder(utils.getDirNameByPath(self.settings.certificates.privatekey))
        # delete all database tables
        self.init_db()
        self.db.drop()
        # delete all database file if use sqlite
        if self.settings.database.df:
            utils.deleteFile(self.settings.database.df)
            utils.delfolder(utils.getDirNameByPath(self.settings.database.df))
        # delete configure file
        utils.deleteFile(utils.getenv('COWRY_CONFIG'))
        self.log.info('Finished drop cowry system')
        exit()


    def createWorker(self, clientSocket, address):
        # workerId = hashlib.md5(str(address).encode('utf8')).hexdigest()
        worker = Worker(clientSocket, address, self.db.Session, sslContext=self.sslContext)
        worker.start()
