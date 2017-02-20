class Base(object):
    b = 1
    # @staticmethod
    def fun(self,a):
        print(a,Base.b)

Base.fun('a')
a=Base()
a.fun('a')
