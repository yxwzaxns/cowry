#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from core.action import Action_MainWindow

if __name__ == '__main__':
	sys.path.append('./')
	app = QApplication(sys.argv)
	prog = Action_MainWindow()
	prog.show()
	sys.exit(app.exec_())
