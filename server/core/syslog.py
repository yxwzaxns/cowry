import logging
from core.config import Settings
from core import utils

class Syslog(object):
    """docstring for Syslog."""
    def __init__(self):
        super(Syslog, self).__init__()
        self.settings = Settings()

        if self.settings.default.debug != 'True':
            logfile = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'log/access.log')
            logging.basicConfig(filename= logfile,
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p')
        else:
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def checkSetting(func):
        def wrapper(self, arg):
            if self.settings.default.debug == 'True':
                func(self, arg)
        return wrapper

    @checkSetting
    def info(self, i):
        logging.warning(i)

    def error(self, i):
        logging.error(i)

    def warning(self, i):
        logging.warning(i)
