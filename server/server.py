import os
from core.system import Server
from core.utils import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="start init cowry server", action="store_true")
parser.add_argument("-s", "--start", help="start up cowry server", action="store_true")
parser.add_argument("-d", "--drop", help="stop cowry server and delete all data of server include database and user files", action="store_true")
parser.add_argument("-v", "--version", help="show version of cowry server", action="store_true")
parser.add_argument("-c", "--config", help="declare config path where cowry system will read from")
args = parser.parse_args()

if __name__ == '__main__':
    os.sys.path.append('.')
    cmd = 'start'
    if args.new:
        cmd = 'new'

    if args.drop:
        print('start drop cowry')
        cmd = 'drop'

    if args.config:
        print('read config from :', args.config)
        # configurePath = sys.argv[sys.argv.index('-c') + 1]
        setenv('COWRY_CONFIG', defaultConfigPath)
    else:
        currentPath = os.getcwd()
        setenv('COWRY_ROOT', currentPath)
        defaultConfigPath = os.path.join(currentPath, 'cowry.conf')
        if os.path.isfile(defaultConfigPath):
            setenv('COWRY_CONFIG', defaultConfigPath)
        else:
            print('Not find default configure file')
            exit()
    server = Server()
    getattr(server, cmd)()
