import _thread, time

class Example(object):
    """docstring for Example."""
    def __init__(self):
        super(Example, self).__init__()

    def call_main_func(self):
        print("successd call main func")

    def deal_worker(self):
        _thread.start_new_thread(self.works, ())

    def works(self):
        print('start works')
        # time.sleep(5)
        self.call_main_func()
        # time.sleep(10)

app = Example()
app.deal_worker()
print('ok')
