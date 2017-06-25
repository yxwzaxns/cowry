#!/usr/bin/env python3
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
parser.add_argument("-w", "--webconsole", help="open cowry console of web", action="store_true")
args = parser.parse_args()

def main():
    # currentPath = os.path.dirname(os.path.realpath(__file__))
    # utils.setenv('COWRY_ROOT', currentPath)
    # utils.addAppPath(currentPath)
    cmd = 'start'

    if args.config:
        defaultConfigPath = args.config
        if utils.checkFileExists(defaultConfigPath):
            utils.setenv('COWRY_CONFIG', defaultConfigPath)
            currentPath = os.path.dirname(os.path.realpath(defaultConfigPath))
            utils.setenv('COWRY_ROOT', currentPath)
    else:
        currentPath = os.path.dirname(os.path.realpath(__file__))
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

    if args.webconsole:
        utils.setenv('COWRY_WEB_CONSOLE', 'YES')
    else:
        utils.setenv('COWRY_WEB_CONSOLE', 'NO')

    server = Server()
    getattr(server, cmd)()

if __name__ == '__main__':
    main()
