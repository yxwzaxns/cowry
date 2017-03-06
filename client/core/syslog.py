import logging
from config import settings
def log(info):
    if Settings.debug == "True":
        print(info)

class Syslog(object):
    """docstring for Syslog."""
    def __init__(self):
        super(Syslog, self).__init__()
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.settings = settings()

    def checkSetting(func):
        def wrapper(self, arg):
            if self.settings['DEFAULT']['Debug'] == 'True':
                func(self, arg)
        return wrapper

    @checkSetting
    def info(self, i):
        logging.warning(i)
