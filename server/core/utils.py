def checkCmdCode(func):
    def wrapper(self, msg):
        self.lastCmdCode = ''
        ret = func(msg)
        recvInfo = literal_eval(ret.decode('utf8'))
        if recvInfo['code'] == self.lastCmdCode:
            return wrapper
        else:
            print('lastCmdCode is not same')
            return 1
