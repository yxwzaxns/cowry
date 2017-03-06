from m1 import C1
class C2(object):
    """docstring for C2."""

    client = None

    def __init__(self):
        super(C2, self).__init__()

    def login(self):
        self.client = C1()
