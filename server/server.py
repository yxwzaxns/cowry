"""cowry server sources."""

import os
import argparse
from core.system import Server
from core import utils
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="start init cowry server", action="store_true")
parser.add_argument("-s", "--start", help="start up cowry server", action="store_true")
parser.add_argument("-d", "--drop", help="stop cowry server and \
                    delete all data of server include database and user files", action="store_true")
parser.add_argument("-v", "--version", help="show version of cowry server", action="store_true")
parser.add_argument("-c", "--config", help="declare config path where cowry system will read from")
parser.add_argument("-q", "--quiet", help="don't echo system status", action="store_true")
args = parser.parse_args()

if __name__ == '__main__':
    utils.addAppPath('.')
    cmd = 'start'

    if args.config:
        defaultConfigPath = args.config
        if utils.checkFileExists(defaultConfigPath):
            utils.setenv('COWRY_CONFIG', defaultConfigPath)
    else:
        currentPath = utils.getCwd()
        utils.setenv('COWRY_ROOT', currentPath)
        defaultConfigPath = utils.joinFilePath(currentPath, 'cowry.conf')
        utils.setenv('COWRY_CONFIG', defaultConfigPath)

    if args.new:
        cmd = 'new'

    if args.drop:
        cmd = 'drop'

    if args.quiet:
        utils.setenv('COWRY_STATUS', 'NO')
    else:
        utils.setenv('COWRY_STATUS', 'YES')

    server = Server()
    getattr(server, cmd)()
