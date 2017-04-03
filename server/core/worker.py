import threading
from core.baseSocket import BaseSocket
from core.database import Db
from core.upload import Upload
from core.download import Download
from db import schema
from sqlalchemy import and_
from core.config import Settings
from core.utils import *


class Worker(threading.Thread, BaseSocket):
    """docstring for Worker."""
    def __init__(self, client, address, db_session, sslContext= None):
        BaseSocket.__init__(self, clientSocket= client, clientAddress= address)
        threading.Thread.__init__(self)
        self.sslContext = sslContext
        self.authenticated = False
        self.settings = Settings()

        # db init
        self.session = db_session()
        self.user = schema.user.User
        self.file = schema.file.File


    def run(self):
        self.log.info('start worker process')
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                self.log.info("recvMsg error : {}".format(recvInfo[1]))
                self.log.error('exit worker process !!')
                self.exit()
            elif recvInfo[0] == 2:
                self.log.info('recvMsg is null, close the connecting.')
                self.exit()
            elif recvInfo[0] == 3:
                self.log.info('recvMsg can\'t convert a dict')
                self.exit()
            elif self.recvInfo:
                self.log.info('Received cmd code : {}'.format(self.recvInfo))
                cmd = self.recvInfo['info']
                try:
                    func = getattr(self, cmd)
                    func()
                except AttributeError as err:
                    self.log.info('Receive : {}'.format(err))
            else:
                self.exit()

    def auth(func):
        """A decorator for auth worker action."""
        def wrapper(self):
            if self.loginStatus == True:
                func(self)
            else:
                self.sendMsg('Not Login')
        return wrapper

    @auth
    def upload(self):
        # recv info code {'info': "upload", "code": "", "filename": filename, "filesize": filesize, "hash": fileHashCode }
        uploadFileHashCode = self.recvInfo['hash']
        uploadFileName, postfix = seperateFileName(self.recvInfo['filename'])
        uploadFileSize = self.recvInfo['filesize']
        currentTime = getCurrentTime()
        # to do
        # to determeine whether have repeat value in db
        try:
            self.session.add(self.file(uid= self.userid, name= uploadFileName, size= uploadFileSize, hashcode= uploadFileHashCode,updatetime= currentTime, postfix= postfix))
        except Exception as e:
            remsg = {'info': 'upload', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
            self.sendMsg(remsg)

        retInfo = self.createDataSock() #return (int, port)
        if retInfo[0] == 1:
            self.log.info('createDataSock fails: {}'.format(retInfo[1]))

        data_channel_info = (self.settings.certificates.cn, retInfo[1])
        authToken = generateAuthToken()
        remsg = {'info': 'upload', 'code': self.recvInfo['code'], 'status': '0', 'token': authToken, 'dataAddress': data_channel_info}
        retInfo = self.sendMsg(remsg)
        if retInfo[0] == 1:
            self.log.info('sendMsg fails: {}'.format(retInfo[1]))
        else:
            self.uploadProcess = Upload(self.sslContext, self.dataSocket, uploadFileHashCode, uploadFileSize, authToken)
            self.uploadProcess.start()

    @auth
    def uploadComfirm(self):
        if self.recvInfo['status'] == '0':
            self.session.commit()
        else:
            self.session.rollback()

    @auth
    def download(self):
        # recv info code {'info': 'download', 'code': '', 'filename': downloadFileName}

        downloadFileName = self.recvInfo['filename']
        # downloadFileSize = self.recvInfo['filesize']
        # currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        # to do
        # to determeine whether have repeat value in db
        try:
            fileInfo = self.session.query(self.file).filter(and_(self.file.uid == self.userid, self.file.name == downloadFileName)).first()
            # self.session.add(self.file(uid= self.userid, name= downloadFileName, size= downloadFileSize, hashcode= downloadFileHashCode,updatetime= currentTime, postfix= postfix))
        except Exception as e:
            remsg = {'info': 'download', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
            self.sendMsg(remsg)
        else:
            if fileInfo.id:
                retInfo = self.createDataSock() #return (int, tuple(ip,port))
                if retInfo[0] == 1:
                    self.log.info('createDataSock fails: {}'.format(retInfo[1]))

                data_channel_info = (self.settings.certificates.cn, retInfo[1])
                authToken = generateAuthToken()
                remsg = {'info': 'download', 'code': self.recvInfo['code'], 'status': '0', 'token': authToken, 'dataAddress': data_channel_info, 'hashcode': fileInfo.hashcode, 'size': fileInfo.size}
                retInfo = self.sendMsg(remsg)
                if retInfo[0] == 1:
                    self.log.info('sendMsg fails: {}'.format(retInfo[1]))
                else:
                    self.downloadProcess = Download(self.sslContext, self.dataSocket, fileInfo, authToken)
                    self.downloadProcess.start()

    @auth
    def list(self):
        listInfo = self.session.query(self.file).filter_by(uid= self.userid).all()

        res = []
        for l in listInfo:
            res_t = {}
            for i in l.__dict__:
                res_t[i] = getattr(l, i)
            del res_t['_sa_instance_state']
            res.append(res_t)

        remsg = {'info': 'list', 'code': self.recvInfo['code'], 'status': '0', 'list': res}
        self.sendMsg(remsg)

    def login(self):
        res = self.session.query(self.user).filter_by(username= self.recvInfo['u']).first()
        if res and res.password == calculateHashCodeForString(self.recvInfo['p']):
            self.username = res.username
            self.userid = res.id
            self.loginStatus = True

            remsg = {'info': 'login', 'code': self.recvInfo['code'], 'status': '0'}
            self.sendMsg(remsg)
        else:
            remsg = {'info': 'login', 'code': self.recvInfo['code'], 'status': '1', 'reason': 'user not exist or authentication fails'}
            self.sendMsg(remsg)
    @auth
    def logout(self):
        logoutInfo = {"info": "logout", "code": self.recvInfo['code'], 'status': '0'}
        self.sendMsg(logoutInfo)
        self.close()
        self.exit()

    def exit(self):
        self.session.close()
        exit()
