def d1(func):
    def wrapper():
        print('this is d1')
        return func()
    return wrapper

def d2(func):
    def wrapper():
        print('this is d2')
        return func()

    return wrapper

@d1
@d2
def test():
    print('this is text')
    return 1


print(test())
