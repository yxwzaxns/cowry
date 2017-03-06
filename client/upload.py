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
        self.horizontalLayoutWidget = QtWidgets.QWidget(UploadFileDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 40, 341, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Note_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Note_label.setFont(font)
        self.Note_label.setObjectName("Note_label")
        self.horizontalLayout.addWidget(self.Note_label)
        self.UploadProgress = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.UploadProgress.setSizeIncrement(QtCore.QSize(0, 0))
        self.UploadProgress.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        self.UploadProgress.setFont(font)
        self.UploadProgress.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.UploadProgress.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.UploadProgress.setAutoFillBackground(False)
        self.UploadProgress.setProperty("value", 24)
        self.UploadProgress.setOrientation(QtCore.Qt.Horizontal)
        self.UploadProgress.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.UploadProgress.setObjectName("UploadProgress")
        self.horizontalLayout.addWidget(self.UploadProgress)
        self.Percentage_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.Percentage_label.setFont(font)
        self.Percentage_label.setObjectName("Percentage_label")
        self.horizontalLayout.addWidget(self.Percentage_label)

        self.retranslateUi(UploadFileDialog)
        self.buttonBox.accepted.connect(UploadFileDialog.accept)
        self.buttonBox.rejected.connect(UploadFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UploadFileDialog)

    def retranslateUi(self, UploadFileDialog):
        _translate = QtCore.QCoreApplication.translate
        UploadFileDialog.setWindowTitle(_translate("UploadFileDialog", "Dialog"))
        self.Note_label.setText(_translate("UploadFileDialog", "上传进度:"))
        self.Percentage_label.setText(_translate("UploadFileDialog", "100%"))

