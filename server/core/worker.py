import threading
import time
from core.baseSocket import BaseSocket
from core.database import Db
from core.upload import Upload
from db.schema import *
import hashlib, uuid, os


class Worker(threading.Thread, BaseSocket):
    """docstring for Worker."""
    def __init__(self, client, address, db_session, sslContext= None):
        BaseSocket.__init__(self, client, address)
        threading.Thread.__init__(self)
        self.sslContext = sslContext
        self.authenticated = False
        self.session = db_session()
        self.user = user.User
        self.file = file.File


    def run(self):
        print('start worker process')
        while True:
            recvInfo = self.recvMsg()
            if recvInfo[0] == 1:
                print("can't recvMsg :", recvInfo[1])
                self.exit()
            elif self.recvInfo:
                print('Received cmd code', self.recvInfo)
                cmd = self.recvInfo['info']
                try:
                    func = getattr(self, cmd)
                    func()
                except AttributeError as err:
                    print('Receive', err)
            else:
                self.exit()

    def auth(func):
        def wrapper(self):
            if self.loginStatus == True:
                func(self)
            else:
                self.sendMsg('Not Login')
        return wrapper

    @auth
    def sendFile(self, filename):
        pass

    @auth
    def upload(self):
        uploadFileHashCode = self.recvInfo['hash']
        uploadFileName, postfix = os.path.splitext(self.recvInfo['filename'])
        uploadFileSize = self.recvInfo['filesize']
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        try:
            self.session.add(self.file(uid= self.userid, name= uploadFileName, size= uploadFileSize, hashcode= uploadFileHashCode,updatetime= currentTime, postfix= postfix))
        except Exception as e:
            raise

        retInfo = self.createDataSock() #return (int, tuple(ip,port))
        if retInfo[0] == 1:
            self.log.info('createDataSock fails: {}'.format(retInfo[1]))

        authToken = uuid.uuid4().hex.upper()
        remsg = {'info': 'upload', 'code': self.recvInfo['code'], 'status': '0', 'token': authToken, 'dataAddress': retInfo[1]}
        retInfo = self.sendMsg(remsg)
        if retInfo[0] == 1:
            self.log.info('sendMsg fails: {}'.format(retInfo[1]))
        else:
            uploadProcess = Upload(self.sslContext, self.dataSocket, uploadFileHashCode, uploadFileSize, authToken)
            uploadProcess.start()

    @auth
    def uploadComfirm(self):
        if self.recvInfo['status'] == '0':
            self.session.commit()
        else:
            self.session.rollback()

    @auth
    def list(self):
        listInfo = self.session.query(self.file).filter_by(uid=self.userid).all()

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
        if res and res.password == hashlib.md5(self.recvInfo['p'].encode('utf8')).hexdigest():
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
        self.close()
        exit()


if __name__ == '__main__':
    for i in range(0,3):
        Worker().start()
        time.sleep(1)
