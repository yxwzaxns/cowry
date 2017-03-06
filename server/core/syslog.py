import logging
from config import Settings

class Syslog(object):
    """docstring for Syslog."""
    def __init__(self):
        super(Syslog, self).__init__()
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.settings = Settings()

    def checkSetting(func):
        def wrapper(self, arg):
            if self.settings.debug == 'True':
                func(self, arg)
        return wrapper

    @checkSetting
    def info(self, i):
        logging.warning(i)
