#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from mainwindow import *
from action import *
from config import settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Action_MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
