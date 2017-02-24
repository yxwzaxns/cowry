# def checkCmdCode(func):
#     def wrapper(msg):
#         self.lastCmdCode = ''
#         ret = func(msg)
#         recvInfo = literal_eval(ret.decode('utf8'))
#         if recvInfo['code'] == self.lastCmdCode:
#             print('ok')
#         else:
#             print('lastCmdCode is not same')
#     return wrapper
class Demo(object):
    """docstring for Demo."""
    def __init__(self):
        super(Demo, self).__init__()

    def deco(func):
        def wrapper(self, arg):
            print('decorater----')
            func(self, arg)
            print('end')
        return wrapper

    @deco
    def func(self,a):
        print('func', a)

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def put(arg):
    print('put', arg)
