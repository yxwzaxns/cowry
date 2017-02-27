#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from action import Action_MainWindow

# if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # mainWindow = Action_MainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(mainWindow)
    # mainWindow.show()
    # sys.exit(app.exec_())

if __name__ == '__main__':
	sys.path.append('./')
	app = QApplication(sys.argv)
	prog = Action_MainWindow()
	prog.show()
	sys.exit(app.exec_())
