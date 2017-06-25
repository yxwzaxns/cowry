#!/usr/bin/env python3
"""cowry client sources."""
import os
import argparse
import PyQt5
from PyQt5.QtWidgets import QApplication
from core.action import Action_MainWindow
from core import utils

parser = argparse.ArgumentParser()
# parser.add_argument("-n", "--new", help="start init cowry server", action="store_true")
parser.add_argument("-s", "--start", help="start up cowry server", action="store_true")
parser.add_argument("-v", "--version", help="show version of cowry client", action="store_true")
parser.add_argument("-c", "--config", help="declare config path where cowry client will read from")
args = parser.parse_args()

def main():
    cmd = 'start'

    if args.config:
        print('read config from :', args.config)
        defaultConfigPath = args.config
        if utils.checkFileExists(defaultConfigPath):
            utils.setenv('COWRY_CONFIG', defaultConfigPath)
    else:
        currentPath = os.path.dirname(os.path.realpath(__file__))
        utils.setenv('COWRY_ROOT', currentPath)
        defaultConfigPath = utils.joinFilePath(currentPath, 'cowry.conf')
        utils.setenv('COWRY_CONFIG', defaultConfigPath)

    app = QApplication(os.sys.argv)
    prog = Action_MainWindow()
    getattr(prog, cmd)()
    os.sys.exit(app.exec_())

if __name__ == '__main__':
    main()
