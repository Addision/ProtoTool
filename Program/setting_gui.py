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

        self.ui.BtnMsg.clicked.connect(
            lambda: self.onBtnClicked('msg_path'))
        self.ui.BtnProto.clicked.connect(
            lambda: self.onBtnClicked('proto_path'))
        self.ui.BtnProtoGen.clicked.connect(
            lambda: self.onBtnClicked('proto_gen_path'))
        self.ui.BtnTable.clicked.connect(
            lambda: self.onBtnClicked('table_path'))
        self.config = Config()
        self.showConf()

    def showConf(self):
        self.ui.LetMsgPath.setText(self.config.getConfOne('msg_path'))
        self.ui.LetProtoPath.setText(self.config.getConfOne('proto_path'))
        self.ui.LetProtoGenPath.setText(
            self.config.getConfOne('proto_gen_path'))
        self.ui.LetTablePath.setText(self.config.getConfOne('table_path'))

    def onBtnClicked(self, btn):
        # 打开文件对话框
        path = QFileDialog.getExistingDirectory(
            self, 'open dir', './')
        if not path and path == "":
            return
        if btn == 'msg_path':
            self.ui.LetMsgPath.setText(path)
        if btn == 'proto_path':
            self.ui.LetProtoPath.setText(path)
        if btn == 'proto_gen_path':
            self.ui.LetProtoGenPath.setText(path)
        if btn == 'table_path':
            self.ui.LetTablePath.setText(path)

        self.config.updateConfOne(btn, path)
