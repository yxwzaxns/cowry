import sys
from core.system import Server

if __name__ == '__main__':
    sys.path.append('./')
    if len(sys.argv) >= 3:
        server = Server(address= sys.argv[1], port= sys.argv[2]).start()
    else:
        server = Server()
    server.start()
