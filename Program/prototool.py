'''
@Author: jia.lai
@Date: 2020-01-16 17:03:02
@LastEditors: jia.lai
@LastEditTime: 2020-04-23 16:37:29
@Description: proto 协议生成工具
'''

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ProtoUI import *
from Config import *


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.98)

        self.config = Config()
        # 菜单设置
        self.initMenuBar()

    pass

    def initMenuBar(self):
        self.ui.menuSave.setEnabled(False)
        self.ui.menuSaveAs.setEnabled(False)
        self.ui.menuFile.triggered[QAction].connect(self.processMenuTrigger)
        self.ui.menuTool.triggered[QAction].connect(self.processMenuTrigger)

    def processMenuTrigger(self, menu):
        if menu == self.ui.menuOpen:
            self.menuBarOpen()
        if menu == self.ui.menuRecentOen:
            self.menuBarRecentOen()
        if menu == self.ui.menuSave:
            self.menuBarSave()
        if menu == self.ui.menuSaveAs:
            self.menuBarSaveAs()
        if menu == self.ui.menuClose:
            self.menuBarClose()
        if menu == self.ui.menuProto:
            self.menuBarProto()
        if menu == self.ui.menuProtoClient:
            self.menuBarProtoClient()
        if menu == self.ui.menuProtoServer:
            self.menuBarProtoServer()

    def menuBarOpen(self):
        print("start load xml files......")
        proto_xml = self.config.getProtoXml()
        # 打开文件对话框
        proto_xml = QFileDialog.getExistingDirectory(
            self, 'open dir', proto_xml)
        if not proto_xml:
            return
        self.config.updateProtoXml(proto_xml)
        self.showModuleMsg(proto_xml)
        pass

    def menuBarRecentOen(self):
        pass

    def menuBarSave(self):
        pass

    def menuBarSaveAs(self):
        pass

    def menuBarClose(self):
        os._exit(0)
        pass

    def menuBarProto(self):
        pass

    def menuBarProtoClient(self):
        pass

    def menuBarProtoServer(self):
        pass

    def showModuleMsg(self, proto_xml):

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
