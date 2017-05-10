# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/aong/workspace/qt/cowry/open.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Open_File(object):
    def setupUi(self, Open_File):
        Open_File.setObjectName("Open_File")
        Open_File.resize(400, 159)
        self.verticalLayout = QtWidgets.QVBoxLayout(Open_File)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Open_File)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Open_File)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Open_File)
        self.buttonBox.accepted.connect(Open_File.accept)
        self.buttonBox.rejected.connect(Open_File.reject)
        QtCore.QMetaObject.connectSlotsByName(Open_File)

    def retranslateUi(self, Open_File):
        _translate = QtCore.QCoreApplication.translate
        Open_File.setWindowTitle(_translate("Open_File", "Dialog"))
        self.groupBox.setTitle(_translate("Open_File", "Confirm Info"))
        self.label.setText(_translate("Open_File", "Are you sure you want to open this file?"))

