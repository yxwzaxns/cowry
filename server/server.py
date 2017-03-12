import sys
from core.system import Server

if __name__ == '__main__':
    sys.path.append('.')
    if '-c' in sys.argv:
        configurePath = sys.argv[sys.argv.index('-c') + 1]
    else:
        configurePath = "cowry.conf"
    server = Server(configurePath)
    server.start()
