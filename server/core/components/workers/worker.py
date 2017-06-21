import threading
from baseSocket import BaseSocket
import utils


class Worker(threading.Thread, BaseSocket):
    """docstring for Worker."""
    def __init__(self, client, address, rd):
        BaseSocket.__init__(self, clientSocket= client, clientAddress= address)
        threading.Thread.__init__(self)
        self.r = rd

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

            if self.recvInfo:
                self.log.info('Received cmd code 2: {}'.format(self.recvInfo))
                cmd = self.recvInfo['info']
                try:
                    func = getattr(self, cmd)
                    func()
                except AttributeError as err:
                    self.log.info('Receive : {}'.format(err))
            else:
                self.exit()

    def uploadAuth(self):
        self.log.info(self.r.get(self.recvInfo['authtoken']))
        if self.r.get(self.recvInfo['authtoken']).decode() == '0':
            authCmdCode = {'info': 'uploadAuth', 'code': self.recvInfo['code'], "status": '0'}
            retInfo = self.sendMsg(authCmdCode)
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
                self.close()
            else:
                if self.recvInfo['file_info']['encryption'] == 1:
                    self.fileSize = self.recvInfo['file_info']['encsize']
                    self.fileHashCode = self.recvInfo['file_info']['hash']
                else:
                    self.fileSize = self.recvInfo['file_info']['filesize']
                    self.fileHashCode = self.recvInfo['file_info']['hash']

                self.uploadFilePath = utils.joinFilePath('/data/', self.fileHashCode)
                retInfo = self.recvFile()
                if retInfo[0] == 0:
                    self.checkFileIfUpload()
                else:
                    self.log.info(retInfo[1])

    def checkFileIfUpload(self):
        try:
            fileHashCode = utils.calculateHashCodeForFile(self.uploadFilePath)
        except Exception as e:
            self.log.info("checkFileIfUpload : {}".format(str(e)))
        else:
            self.log.info('upload file  md5 code is : {}'.format(fileHashCode))
            if fileHashCode == self.fileHashCode:
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '0'}
            else:
                # deleteFile(self.uploadFilePath)
                remsg = {"info": 'uploadReturn', 'code': '23333', 'status': '1', 'reason': "md5 code not same as upload file"}
            self.sendMsg(remsg)

            self.r.set(self.recvInfo['authtoken'], 1)
            # start backup file to backup system
            cmd = ['bash', '/cowry-workers/backup.sh', self.uploadFilePath]
            utils.execShell(cmd)

        self.close()
        exit()

    def downloadAuth(self):
        self.log.info(self.r.get(self.recvInfo['authtoken']))
        if self.r.get(self.recvInfo['authtoken']).decode() == '0':
            authCmdCode = {'info': 'downloadAuth', 'code': self.recvInfo['code'], "status": '0'}
            retInfo = self.sendMsg(authCmdCode)
            if retInfo[0] == 1:
                self.log.info(retInfo[1])
                self.close()
            else:
                self.downloadFilePath = utils.joinFilePath('/data/', self.recvInfo['hash'])
                # start send file
                self.sendFile()
                exit()

    def auth(func):
        """A decorator for auth worker action."""
        def wrapper(self):
            if self.loginStatus == True:
                func(self)
            else:
                self.sendMsg('Not Login')
        return wrapper

    # is't code of worker follow
    def upload(self):
        # recv info code {'info': "upload", "code": "", "filename": filename, "filesize": filesize, "hash": fileHashCode }
        uploadFileInfo = self.recvInfo
        fileHashCode = uploadFileInfo['hash']
        fileName, postfix = seperateFileName(uploadFileInfo['filename'])
        fileSize = uploadFileInfo['filesize']
        currentTime = getCurrentTime()

        encryption = uploadFileInfo['encryption']
        encryption_type = uploadFileInfo['encryption_type']
        encsize = uploadFileInfo['encsize']
        # to do
        # to determeine whether have repeat value in db
        try:
            self.session.add(self.file(uid= self.userid,
                                       name= fileName,
                                       size= fileSize,
                                       encryption= encryption,
                                       encryption_type= encryption_type,
                                       encsize= encsize,
                                       hashcode= fileHashCode,
                                       updatetime= currentTime,
                                       postfix= postfix))
        except Exception as e:
            remsg = {'info': 'upload', 'code': uploadFileInfo['code'], 'status': '1', 'reason': str(e)}
            self.sendMsg(remsg)

        retInfo = self.createDataSock() #return (int, port)
        if retInfo[0] == 1:
            self.log.info('createDataSock fails: {}'.format(retInfo[1]))

        data_channel_info = (self.settings.certificates.cn, retInfo[1])
        authToken = generateAuthToken()
        remsg = {'info': 'upload', 'code': uploadFileInfo['code'], 'status': '0', 'token': authToken, 'dataAddress': data_channel_info}
        retInfo = self.sendMsg(remsg)
        if retInfo[0] == 1:
            self.log.info('sendMsg fails: {}'.format(retInfo[1]))
        else:
            if uploadFileInfo['encryption'] == 1:
                uploadFileSize = uploadFileInfo['encsize']
            else:
                uploadFileSize = uploadFileInfo['filesize']
            self.uploadProcess = Upload(self.sslContext, self.dataSocket, fileHashCode, uploadFileSize, authToken)
            self.uploadProcess.start()

    def uploadComfirm(self):
        if self.recvInfo['status'] == '0':
            self.session.commit()
        else:
            self.session.rollback()

    def download(self):
        # recv info code {'info': 'download', 'code': '', 'filename': downloadFileName}

        downloadFileHash = self.recvInfo['filehash']
        # baseFileName, postfix = seperateFileName(downloadFileName)
        # downloadFileSize = self.recvInfo['filesize']
        # currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        # to do
        # to determeine whether have repeat value in db
        try:
            fileInfo = self.session.query(self.file).filter(or_(and_(self.file.uid==self.userid, self.file.hashcode==downloadFileHash),
                                                                and_(self.file.hashcode==downloadFileHash, self.file.public==1))).all()
            # self.session.add(self.file(uid= self.userid, name= downloadFileName, size= downloadFileSize, hashcode= downloadFileHashCode,updatetime= currentTime, postfix= postfix))
        except Exception as e:
            remsg = {'info': 'download', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
            self.sendMsg(remsg)
        else:
            self.log.info('search file has : {}\'s'.format(len(fileInfo)))
            if len(fileInfo) == 1:
                fileInfo = fileInfo[0]
                retInfo = self.createDataSock() #return (int, tuple(ip,port))
                if retInfo[0] == 1:
                    self.log.info('createDataSock fails: {}'.format(retInfo[1]))

                data_channel_info = (self.settings.certificates.cn, retInfo[1])
                authToken = generateAuthToken()
                fileInfo = fileInfo.__dict__
                del fileInfo['_sa_instance_state']
                remsg = {'info': 'download', 'code': self.recvInfo['code'], 'status': '0', 'token': authToken, 'dataAddress': data_channel_info, 'fileinfo': fileInfo}
                retInfo = self.sendMsg(remsg)
                if retInfo[0] == 1:
                    self.log.info('sendMsg fails: {}'.format(retInfo[1]))
                else:
                    downloadFilePath = joinFilePath(self.settings.storage.datapath, fileInfo['hashcode'])
                    self.downloadProcess = Download(self.sslContext, self.dataSocket, downloadFilePath, authToken)
                    self.downloadProcess.start()
            elif len(fileInfo) >= 2:
                pass
            else:
                remsg = {'info': 'download', 'code': self.recvInfo['code'], 'status': '1', 'reason': 'can\'t find download file'}
                retInfo = self.sendMsg(remsg)

    @auth
    def list(self):
        # listInfo = self.session.query(self.file).filter_by(uid= self.userid).all()
        files_list = self.session.query(self.file).filter(or_(and_(self.file.uid==self.userid, self.file.is_delete==0), and_(self.file.public==1, self.file.is_delete==0))).all()
        res = []
        for l in files_list:
            res_t = {}
            for i in l.__dict__:
                res_t[i] = getattr(l, i)
            del res_t['_sa_instance_state']
            res.append(res_t)

        remsg = {'info': 'list', 'code': self.recvInfo['code'], 'status': '0', 'list': res}
        self.sendMsg(remsg)

    @auth
    def openFile(self):
        try:
            openfile = self.session.query(self.file).filter(and_(self.file.uid==self.userid, self.file.hashcode==self.recvInfo['filehash'])).first()
            openfile.public = '1'
            self.session.commit()
        except Exception as e:
            remsg = {'info': 'openFile', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
        else:
            remsg = {'info': 'openFile', 'code': self.recvInfo['code'], 'status': '0'}
        self.sendMsg(remsg)

    @auth
    def closeFile(self):
        try:
            openfile = self.session.query(self.file).filter(and_(self.file.uid==self.userid, self.file.hashcode==self.recvInfo['filehash'])).first()
            openfile.public = '0'
            self.session.commit()
        except Exception as e:
            remsg = {'info': 'closeFile', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
        else:
            remsg = {'info': 'closeFile', 'code': self.recvInfo['code'], 'status': '0'}
        self.sendMsg(remsg)

    @auth
    def deleteFile(self):
        try:
            openfile = self.session.query(self.file).filter(and_(self.file.uid==self.userid, self.file.hashcode==self.recvInfo['filehash'])).first()
            openfile.is_delete = 1
            self.session.commit()
        except Exception as e:
            remsg = {'info': 'closeFile', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
        else:
            remsg = {'info': 'closeFile', 'code': self.recvInfo['code'], 'status': '0'}
        self.sendMsg(remsg)

    @auth
    def getPubKey(self):
        try:
            user = self.session.query(self.user).filter_by(email=self.recvInfo['email']).first()
        except Exception as e:
            remsg = {'info': 'getPubKey', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
        else:
            remsg = {'info': 'getPubKey', 'code': self.recvInfo['code'], 'public_key': user.pubkey}
        self.sendMsg(remsg)

    @auth
    def transferFile(self):
        try:
            user = self.session.query(self.user).filter_by(email=self.recvInfo['email']).first()
            openfile = self.session.query(self.file).filter_by(hashcode=self.recvInfo['filehash']).first()
            self.session.add(self.file(uid= user.id,
                                       name= openfile.name,
                                       size= openfile.size,
                                       encryption= openfile.encryption,
                                       encryption_type= openfile.encryption_type,
                                       encsize= openfile.encsize,
                                       hashcode= openfile.hashcode,
                                       updatetime= openfile.updatetime,
                                       postfix= openfile.postfix,
                                       is_transfer= 1,
                                       transfer_own= self.userid,
                                       c_enc= self.recvInfo['cipher_enc']
                                       ))
            self.session.commit()
        except Exception as e:
            remsg = {'info': 'transferFile', 'code': self.recvInfo['code'], 'status': '1', 'reason': str(e)}
        else:
            remsg = {'info': 'transferFile', 'code': self.recvInfo['code'], 'status': '0'}
        self.sendMsg(remsg)

    def login(self):
        res = self.session.query(self.user).filter_by(username= self.recvInfo['u']).first()
        if res and res.password == calculateHashCodeForString(self.recvInfo['p']):
            self.username = res.username
            self.userid = res.id
            self.loginStatus = True

            remsg = {'info': 'login', 'code': self.recvInfo['code'], 'status': '0', 'uid': str(self.userid)}
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
        # self.session.close()
        exit()
