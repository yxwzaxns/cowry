# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uploadfiledialog.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UploadFileDialog(object):
    def setupUi(self, UploadFileDialog):
        UploadFileDialog.setObjectName("UploadFileDialog")
        UploadFileDialog.resize(429, 193)
        self.buttonBox = QtWidgets.QDialogButtonBox(UploadFileDialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.progressBar = QtWidgets.QProgressBar(UploadFileDialog)
        self.progressBar.setGeometry(QtCore.QRect(160, 40, 181, 71))
        self.progressBar.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.progressBar.setFont(font)
        self.progressBar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(UploadFileDialog)
        self.label.setGeometry(QtCore.QRect(40, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(UploadFileDialog)
        self.buttonBox.accepted.connect(UploadFileDialog.accept)
        self.buttonBox.rejected.connect(UploadFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UploadFileDialog)

    def retranslateUi(self, UploadFileDialog):
        _translate = QtCore.QCoreApplication.translate
        UploadFileDialog.setWindowTitle(_translate("UploadFileDialog", "Dialog"))
        self.label.setText(_translate("UploadFileDialog", "上传进度:"))
