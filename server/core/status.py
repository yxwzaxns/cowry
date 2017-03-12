import time
import threading
from core.syslog import Syslog

class Status(threading.Thread):
    """docstring for Status."""
    def __init__(self):
        super(Status, self).__init__()
        self.log = Syslog()
    def run(self):
        while True:
            time.sleep(5)
            self.log.info("============================")
            self.log.info("now have {} worker".format(threading.active_count() - 2))
            self.log.info("============================")
