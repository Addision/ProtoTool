# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Designer/mod.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogMod(object):
    def setupUi(self, DialogMod):
        DialogMod.setObjectName("DialogMod")
        DialogMod.resize(246, 152)
        DialogMod.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.BtnModCancel = QtWidgets.QPushButton(DialogMod)
        self.BtnModCancel.setGeometry(QtCore.QRect(150, 110, 81, 31))
        self.BtnModCancel.setObjectName("BtnModCancel")
        self.LetModCmt = QtWidgets.QLineEdit(DialogMod)
        self.LetModCmt.setGeometry(QtCore.QRect(70, 60, 161, 31))
        self.LetModCmt.setObjectName("LetModCmt")
        self.BtnModOk = QtWidgets.QPushButton(DialogMod)
        self.BtnModOk.setGeometry(QtCore.QRect(20, 110, 81, 31))
        self.BtnModOk.setObjectName("BtnModOk")
        self.label_6 = QtWidgets.QLabel(DialogMod)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 51, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(DialogMod)
        self.label_7.setGeometry(QtCore.QRect(10, 60, 51, 21))
        self.label_7.setObjectName("label_7")
        self.LetModName = QtWidgets.QLineEdit(DialogMod)
        self.LetModName.setGeometry(QtCore.QRect(70, 10, 161, 31))
        self.LetModName.setObjectName("LetModName")

        self.retranslateUi(DialogMod)
        QtCore.QMetaObject.connectSlotsByName(DialogMod)

    def retranslateUi(self, DialogMod):
        _translate = QtCore.QCoreApplication.translate
        DialogMod.setWindowTitle(_translate("DialogMod", "模块信息"))
        self.BtnModCancel.setText(_translate("DialogMod", "取消"))
        self.BtnModOk.setText(_translate("DialogMod", "确定"))
        self.label_6.setText(_translate("DialogMod", "模块名称"))
        self.label_7.setText(_translate("DialogMod", "模块说明"))
