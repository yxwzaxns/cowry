# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/aong/workspace/qt/cowry/certinfo.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Cert_Info(object):
    def setupUi(self, Cert_Info):
        Cert_Info.setObjectName("Cert_Info")
        Cert_Info.resize(610, 444)
        self.verticalLayout = QtWidgets.QVBoxLayout(Cert_Info)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Cert_Info)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.Signature = QtWidgets.QLabel(self.groupBox)
        self.Signature.setMinimumSize(QtCore.QSize(200, 0))
        self.Signature.setAlignment(QtCore.Qt.AlignCenter)
        self.Signature.setObjectName("Signature")
        self.gridLayout.addWidget(self.Signature, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.Filehash = QtWidgets.QLabel(self.groupBox)
        self.Filehash.setAlignment(QtCore.Qt.AlignCenter)
        self.Filehash.setObjectName("Filehash")
        self.gridLayout.addWidget(self.Filehash, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setText("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setText("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Cert_Info)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Cert_Info)
        self.buttonBox.accepted.connect(Cert_Info.accept)
        self.buttonBox.clicked['QAbstractButton*'].connect(Cert_Info.close)
        QtCore.QMetaObject.connectSlotsByName(Cert_Info)

    def retranslateUi(self, Cert_Info):
        _translate = QtCore.QCoreApplication.translate
        Cert_Info.setWindowTitle(_translate("Cert_Info", "Certificate Info"))
        self.groupBox.setTitle(_translate("Cert_Info", "Info"))
        self.label.setText(_translate("Cert_Info", "Signature sha256"))
        self.Signature.setText(_translate("Cert_Info", "sdfs"))
        self.label_3.setText(_translate("Cert_Info", "sha256 code"))
        self.Filehash.setText(_translate("Cert_Info", "TextLabel"))

