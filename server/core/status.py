import time
import threading

class Status(threading.Thread):
    """docstring for Status."""
    def __init__(self):
        super(Status, self).__init__()

    def run(self):
        while True:
            time.sleep(5)
            print("============================")
            print("now have {} worker".format(threading.active_count() - 2))
            print("============================")
