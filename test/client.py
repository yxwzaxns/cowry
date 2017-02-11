#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, qApp, QAction, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
# The QtGui.QDesktopWidget class provides information about the user's desktop, including the screen size.
from PyQt5.QtWidgets import QMainWindow
# The QMainWindow class provides a main application window. This enables to create a classic application skeleton with a statusbar, toolbars, and a menubar.
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
# The QHBoxLayout and QVBoxLayout are basic layout classes that line up widgets horizontally and vertically.

class InitUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        # The resize() method resizes the widget
        self.resize(800, 600)
        # The move() method moves the widget to a position on the screen
        # self.move(150, 150)

        self.center()

        # The setGeometry() does two things: it locates the window on the screen and sets it size. The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window
        # w.setGeometry(150, 150, 800, 600)

        # The statusbar is created with the help of the QMainWindow widget.
        # self.statusBar().showMessage('Version: 0.0.1')

        self.setWindowTitle("Cowry System")
        # The setWindowIcon() sets the application icon
        self.setWindowIcon(QIcon('resources/icon.png'))

        # self.menu_exit()
        self.button()
        self.show()

    def button(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


    def menu_exit(self):
        exitAction = QAction(QIcon('resources/icon.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = InitUI()
    sys.exit(app.exec_())
