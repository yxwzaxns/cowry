class Example1(object):
    """docstring for Example."""
    def __init__(self):
        super(Example1, self).__init__()

    def call(self):
        print(self.name)

class Example2(Example1):
    """docstring for Example2."""
    def __init__(self):
        super(Example2, self).__init__()
        self.name = 'a'
        self.call()

app = Example2()
