#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QTreeWidget, QTreeWidgetItem, QAction, QMenu

# class myTreeWidget(QTreeWidget):
#     def __init__(self):
#         super(myTreeWidget, self).__init__()
#         self.connect(self.UI.BtnOpen, QtCore.SIGNAL('customContextMenuRequested (const QPoint&)'), self.openright)
#
#     def myListWidgetContext(self, point):
#         popMenu = QtGui.QMenu()
#         popMenu.addAction(QtGui.QAction(u'添加', self))
#         popMenu.addAction(QtGui.QAction(u'删除', self))
#         popMenu.addAction(QtGui.QAction(u'修改', self))
#
#         popMenu.exec_(QtGui.QCursor.pos())

class demo(QWidget):
    """docstring for demo."""
    def __init__(self):
        super(demo, self).__init__()

        self.resize(600, 500)
        self.move(300, 300)
        self.setWindowTitle('Simple')

        tab = QTabWidget()
        # tab.tabBarClicked.connect(lambda : print(tab.currentIndex))
        tab1 = QWidget()

        tab.addTab(tab1,'tab1')


        tab2 = QWidget()
        tab.addTab(tab2,'tab2')


        tl1 = QTreeWidgetItem([ "String A",  "String B",  "String C" ])

        for i in range(3):
            l1_child = QTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
            tl1.addChild(l1_child)

        # lmenu = QtGui.QMenu()
        # lmenu.addAction("New", self.new())



        self.ftree = QTreeWidget()
        self.ftree.setColumnCount(3)
        self.ftree.setHeaderLabels(['id', 'name', 'size'])
        self.ftree.header().resizeSection(1,0)
        # headerView.resizeSection(1,0)
        self.ftree.addTopLevelItem(tl1)

        # self.ftree, QtCore.SIGNAL('customContextMenuRequested (const QPoint&)'), self.openright)
        self.ftree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ftree.customContextMenuRequested.connect(self.openMenu)
        # self.ftree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.ftree.customContextMenuRequested.connect(self.on_context_menu)
        # ftree.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

        self.ftree1 = QTreeWidget()
        self.ftree1.setColumnCount(3)
        self.ftree1.setHeaderLabels(['id', 'name', 'size'])
        self.ftree1.header().resizeSection(1,0)
        # headerView.resizeSection(1,0)
        self.ftree1.addTopLevelItem(tl1)


        # self.customContextMenuRequested.connect(self.on_context_menu)

        # self.ftree.contextMenuEvent = self.menu

        self.ftree.clear()
        self.ftree1.clear()

        fvbox = QVBoxLayout()
        fvbox.addWidget(self.ftree)
        tab1.setLayout(fvbox)

        fvbox1 = QVBoxLayout()
        fvbox1.addWidget(self.ftree1)
        tab2.setLayout(fvbox1)


        button = QPushButton('ok')

        hbox1 = QHBoxLayout()
        # hbox.addStretch(1)
        hbox1.addWidget(tab)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(button)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def openMenu(self, position):
        indexes = self.ftree.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu(self)
        if level == 0:
            # menu.addAction(self.tr("Edit person"))
            pass
        elif level == 1:
            Items = ['delete', 'transfer', 'open']

            for item in Items:
                action = QAction(item, self)
                action.triggered.connect(getattr(self, 'file_{}'.format(item)))
                menu.addAction(action)
        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.ftree.mapToGlobal(position))

    def on_context_menu(self, point):
        popMenu = QMenu(self)
        Items = ['delete', 'transfer', 'open']

        for item in Items:
            action = QAction(item, self)
            action.triggered.connect(getattr(self, 'file_{}'.format(item)))
            popMenu.addAction(action)

        # popMenu = QMenu()
        # popMenu.addAction(QAction(u'添加', self))
        # popMenu.addAction(QAction(u'删除', self))
        # popMenu.addAction(QAction(u'修改', self))

        popMenu.exec_(QtGui.QCursor.pos())

    def file_transfer(self):
        print('transfer')

    def file_delete(self):
        selectFiles = self.ftree.selectedItems()
        downloadFileInfo = {}
        downloadFileInfo['filename'] = selectFiles[0].text(0)
        downloadFileInfo['postfix'] = selectFiles[0].text(1)
        downloadFileInfo['encryption_type'] = selectFiles[0].text(3)
        print(downloadFileInfo)

    def file_open(self):
        print('open')

    def new(self):
        print('ok')

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = demo()
    ex.show()
    sys.exit(app.exec_())
