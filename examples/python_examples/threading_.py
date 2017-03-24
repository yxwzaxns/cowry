import threading
import time


class Example(object):
    """docstring for Example."""
    def __init__(self,):
        super(Example, self).__init__()

    def gen_worker(self):
        worker = Worker(self)
        worker.start()

    def call(self):
        print('call main successd')

class Worker(threading.Thread):
    """docstring for Worker."""
    def __init__(self, main):
        super(Worker, self).__init__()
        self.main = main

    def run(self):
        self.main.call()

app = Example()
app.gen_worker()
