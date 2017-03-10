class A(object):
    """docstring for A."""
    def __init__(self):
        super(A, self).__init__()

    def call(self):
        print("A")
    def calla(self):
        print('calla')

class B(object):
    """docstring for B."""
    def __init__(self):
        super(B, self).__init__()
    def call(self):
        print("B")

    def callb(self):
        print('callb')

class Example1(A, B):
    """docstring for Example."""
    def __init__(self):
        super(Example1, self).__init__()
        self.call()
        self.callb()

    def p(self):
        print(self.__mro__)

app = Example1()
app.p()
