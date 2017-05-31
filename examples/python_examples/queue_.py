from queue import Queue
import threading

class Example(object):
    """docstring for Example."""
    def __init__(self, arg):
        super(Example, self).__init__()
        if arg:
            self.arg = arg

    def run(self):
        q.put()


q = Queue(20)

for i in range(3):
    Example().start()
