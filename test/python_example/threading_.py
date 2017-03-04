import threading
import time

count = 0

threadLock = threading.Lock()

class Example(threading.Thread):
    """docstring for Example."""
    def __init__(self,worker):
        super(Example, self).__init__()
        self.worker = worker
    def run(self):
        while True:
            print()

workers = []

for i in range(10):
    worker = 'worker-' + str(i)
    worker = Example(worker)
    workers.append(worker)

for i in workers:
    # time.sleep(1)
    i.start()

for w in workers:
    print(w)

time.sleep(3)

for i in workers:
    print(i)
