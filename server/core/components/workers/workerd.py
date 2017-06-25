#!/usr/bin/env python3
"""Cowry-workerd system core module."""
import socket
import ssl
import redis
import time
from worker import Worker
from syslog import Syslog
from etcd_store import etcd_wait_ready
from etcd_store import etcd_mkdir
from etcd_store import etcd_client
import utils

class Workerd():
    """docstring for Server."""

    def __init__(self):
        """Default model is start, Add some necessary for it."""
        super(Workerd, self).__init__()
        self.log = Syslog()

    def init_slave(self):
        """Pass."""
        self.r = redis.Redis(host='redis', port=6379, db=0)
        self.log.info(self.r.get('master_status'))
        while self.r.get('master_status') != b'1':
            time.sleep(1)
        self.log.info('get master info, start work with slave')
        # init_etcd
        if etcd_wait_ready():
            worker_uuid = utils.generateGUID()
            etcd_mkdir('workers')
            # etcd_set('/workers/{}'.format(worker_uuid),)

    def init_ssl(self):
        self.sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.log.info('start load certificates')
        # self.sslContext.load_cert_chain(certfile='/cowry-workers/certs/server.cert', keyfile='/cowry-workers/certs/server.key')
        self.sslContext.load_cert_chain(certfile='/certs/server.crt', keyfile='/certs/server.key')
        self.sslContext.load_verify_locations('/certs/server.crt')

    def init_socket(self):
        self.log.info('start init worker socket')
        # create an INET, STREAMing socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        self.serverSocket.bind(('0.0.0.0', 2334))
        # become a server socket
        self.serverSocket.listen(5)

    def start(self):
        self.init_slave()
        self.init_socket()
        self.init_ssl()
        self.log.info('start run cowry worker')
        while True:
            (clientSocket, clientAddress) = self.serverSocket.accept()
            self.log.info("{}<=====>{}".format(clientSocket, clientAddress))
            try:
                client = self.sslContext.wrap_socket(clientSocket, server_side=True)
            except Exception as e:
                self.log.info(str(e))
            else:
                self.create_worker_process(client, clientAddress)


    def create_worker_process(self, clientSocket, address):
        # workerId = hashlib.md5(str(address).encode('utf8')).hexdigest()
        worker = Worker(clientSocket, address, self.r)
        worker.start()

if __name__ == '__main__':
    wp = Workerd()
    wp.start()
