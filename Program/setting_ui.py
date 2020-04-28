# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Designer/setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName("SettingWindow")
        SettingWindow.resize(590, 511)
        self.centralwidget = QtWidgets.QWidget(SettingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 101, 21))
        self.label.setObjectName("label")
        self.LetMsgPath = QtWidgets.QLineEdit(self.centralwidget)
        self.LetMsgPath.setGeometry(QtCore.QRect(40, 60, 381, 31))
        self.LetMsgPath.setReadOnly(True)
        self.LetMsgPath.setObjectName("LetMsgPath")
        self.BtnMsg = QtWidgets.QPushButton(self.centralwidget)
        self.BtnMsg.setGeometry(QtCore.QRect(450, 60, 51, 31))
        self.BtnMsg.setObjectName("BtnMsg")
        self.BtnProtoGen = QtWidgets.QPushButton(self.centralwidget)
        self.BtnProtoGen.setGeometry(QtCore.QRect(450, 220, 51, 31))
        self.BtnProtoGen.setObjectName("BtnProtoGen")
        self.LetProtoGenPath = QtWidgets.QLineEdit(self.centralwidget)
        self.LetProtoGenPath.setGeometry(QtCore.QRect(40, 220, 381, 31))
        self.LetProtoGenPath.setReadOnly(True)
        self.LetProtoGenPath.setObjectName("LetProtoGenPath")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 190, 101, 21))
        self.label_2.setObjectName("label_2")
        self.BtnTable = QtWidgets.QPushButton(self.centralwidget)
        self.BtnTable.setGeometry(QtCore.QRect(450, 290, 51, 31))
        self.BtnTable.setObjectName("BtnTable")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 260, 101, 21))
        self.label_3.setObjectName("label_3")
        self.LetTablePath = QtWidgets.QLineEdit(self.centralwidget)
        self.LetTablePath.setGeometry(QtCore.QRect(40, 290, 381, 31))
        self.LetTablePath.setReadOnly(True)
        self.LetTablePath.setObjectName("LetTablePath")
        self.BtnProto = QtWidgets.QPushButton(self.centralwidget)
        self.BtnProto.setGeometry(QtCore.QRect(450, 140, 51, 31))
        self.BtnProto.setObjectName("BtnProto")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 110, 121, 21))
        self.label_4.setObjectName("label_4")
        self.LetProtoPath = QtWidgets.QLineEdit(self.centralwidget)
        self.LetProtoPath.setGeometry(QtCore.QRect(40, 140, 381, 31))
        self.LetProtoPath.setReadOnly(True)
        self.LetProtoPath.setObjectName("LetProtoPath")
        SettingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingWindow.setWindowTitle(_translate("SettingWindow", "选项"))
        self.label.setText(_translate("SettingWindow", "消息加载路径："))
        self.BtnMsg.setText(_translate("SettingWindow", "..."))
        self.BtnProtoGen.setText(_translate("SettingWindow", "..."))
        self.label_2.setText(_translate("SettingWindow", "导出协议路径："))
        self.BtnTable.setText(_translate("SettingWindow", "..."))
        self.label_3.setText(_translate("SettingWindow", "导表路径："))
        self.BtnProto.setText(_translate("SettingWindow", "..."))
        self.label_4.setText(_translate("SettingWindow", "proto文件保存路径："))
