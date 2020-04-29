# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Designer/mod.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormMod(object):
    def setupUi(self, FormMod):
        FormMod.setObjectName("FormMod")
        FormMod.resize(250, 159)
        self.BtnModAdd = QtWidgets.QPushButton(FormMod)
        self.BtnModAdd.setGeometry(QtCore.QRect(70, 120, 111, 31))
        self.BtnModAdd.setObjectName("BtnModAdd")
        self.LetModCmt = QtWidgets.QLineEdit(FormMod)
        self.LetModCmt.setGeometry(QtCore.QRect(70, 70, 161, 31))
        self.LetModCmt.setObjectName("LetModCmt")
        self.label_7 = QtWidgets.QLabel(FormMod)
        self.label_7.setGeometry(QtCore.QRect(10, 70, 51, 21))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(FormMod)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.label_6.setObjectName("label_6")
        self.LetModName = QtWidgets.QLineEdit(FormMod)
        self.LetModName.setGeometry(QtCore.QRect(70, 20, 161, 31))
        self.LetModName.setObjectName("LetModName")

        self.retranslateUi(FormMod)
        QtCore.QMetaObject.connectSlotsByName(FormMod)

    def retranslateUi(self, FormMod):
        _translate = QtCore.QCoreApplication.translate
        FormMod.setWindowTitle(_translate("FormMod", "模块"))
        self.BtnModAdd.setText(_translate("FormMod", "确定"))
        self.label_7.setText(_translate("FormMod", "模块说明"))
        self.label_6.setText(_translate("FormMod", "模块名称"))
