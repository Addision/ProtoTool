import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from setting_ui import *
from config import *


class SettingGui(QMainWindow):
    def __init__(self, parent=None):
        super(SettingGui, self).__init__()
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        self.setStyleSheet('background-color: rgb(230, 230, 230);')

        self.ui.btnMsg.clicked.connect(
            lambda: self.onBtnClicked('msg_path'))
        self.ui.btnProto.clicked.connect(
            lambda: self.onBtnClicked('proto_path'))
        self.ui.btnProtobuf.clicked.connect(
            lambda: self.onBtnClicked('protobuf_path'))
        self.ui.btnExcel.clicked.connect(
            lambda: self.onBtnClicked('excel_path'))
        self.ui.btnJson.clicked.connect(
            lambda: self.onBtnClicked('json_path'))
        self.ui.btnExcelCpp.clicked.connect(
            lambda: self.onBtnClicked('excel_cpp_path'))
        self.ui.btnExcelCsharp.clicked.connect(
            lambda: self.onBtnClicked('excel_csharp_path'))

        self.config = Config()
        self.showConf()

    def showConf(self):
        self.ui.letMsgPath.setText(self.config.getConfOne('msg_path'))
        self.ui.letProtoPath.setText(self.config.getConfOne('proto_path'))
        self.ui.letProtobufPath.setText(
            self.config.getConfOne('protobuf_path'))
        self.ui.letExcelPath.setText(self.config.getConfOne('excel_path'))
        self.ui.letJsonPath.setText(self.config.getConfOne('json_path'))
        self.ui.letExcelCppPath.setText(
            self.config.getConfOne('excel_cpp_path'))
        self.ui.letExcelCsharpPath.setText(
            self.config.getConfOne('excel_csharp_path'))

    def onBtnClicked(self, btn):
        # 打开文件对话框
        path = QFileDialog.getExistingDirectory(
            self, 'open dir', './')
        if not path and path == "":
            return
        if btn == 'msg_path':
            self.ui.letMsgPath.setText(path)
        if btn == 'proto_path':
            self.ui.letProtoPath.setText(path)
        if btn == 'protobuf_path':
            self.ui.letProtobufPath.setText(path)
        if btn == 'excel_path':
            self.ui.letExcelPath.setText(path)
        if btn == 'json_path':
            self.ui.letJsonPath.setText(path)
        if btn == 'excel_cpp_path':
            self.ui.letExcelCppPath.setText(path)
        if btn == 'excel_csharp_path':
            self.ui.letExcelCsharpPath.setText(path)

        self.config.updateConfOne(btn, path)
