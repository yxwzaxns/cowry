#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import argparse
from PyQt5.QtWidgets import QApplication
from core.action import Action_MainWindow
from core.config import Settings

parser = argparse.ArgumentParser()
# parser.add_argument("-n", "--new", help="start init cowry server", action="store_true")
parser.add_argument("-s", "--start", help="start up cowry server", action="store_true")
# parser.add_argument("-d", "--drop", help="stop cowry server and delete all data of server include database and user files", action="store_true")
parser.add_argument("-v", "--version", help="show version of cowry server", action="store_true")
parser.add_argument("-c", "--config", help="declare config path where cowry system will read from")
args = parser.parse_args()

if __name__ == '__main__':
	os.sys.path.append('.')
	cmd = 'start'
	if args.config:
		print('read config from :', args.config)
		# configurePath = sys.argv[sys.argv.index('-c') + 1]
		os.environ['COWRY_CONFIG'] = defaultConfigPath
	else:
		currentPath = os.getcwd()
		defaultConfigPath = os.path.join(currentPath, 'cowry.conf')
		if os.path.isfile(defaultConfigPath):
			os.environ['COWRY_CONFIG'] = defaultConfigPath
			# set default configure value, certificate path
			settings = Settings()
			setDefaultCertPath = os.path.join(currentPath, 'certs/server.crt')
			settings._set(('certificates', 'certificate', setDefaultCertPath))
		else:
			print('Not find default configure file')
			exit()

	app = QApplication(os.sys.argv)
	prog = Action_MainWindow()
	getattr(prog, cmd)()
	os.sys.exit(app.exec_())
