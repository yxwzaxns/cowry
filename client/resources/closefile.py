# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/aong/workspace/qt/cowry/close_open.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Close_File(object):
    def setupUi(self, Close_File):
        Close_File.setObjectName("Close_File")
        Close_File.resize(445, 184)
        self.groupBox = QtWidgets.QGroupBox(Close_File)
        self.groupBox.setGeometry(QtCore.QRect(36, 17, 376, 114))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Close_File)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 388, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Close_File)
        self.buttonBox.accepted.connect(Close_File.accept)
        QtCore.QMetaObject.connectSlotsByName(Close_File)

    def retranslateUi(self, Close_File):
        _translate = QtCore.QCoreApplication.translate
        Close_File.setWindowTitle(_translate("Close_File", "Dialog"))
        self.groupBox.setTitle(_translate("Close_File", "Confirm Info"))
        self.label_2.setText(_translate("Close_File", "Are you sure you want to cancel share the file?"))

