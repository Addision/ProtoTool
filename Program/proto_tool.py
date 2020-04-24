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
from proto_ui import *
from config import *
from module import *


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.98)
        # widget 组件设置
        self.ui.WidMsgTree.setHeaderLabels(['proto msg', 'comment'])
        self.ui.WidMsgTree.setStyle(QStyleFactory.create('windows'))
        self.ui.WidMsgTree.clicked.connect(self.onTreeClicked)

        self.config = Config()
        self.module_mgr = ModuleMgr()
        # 菜单设置
        self.initMenuBar()

        self.xml_dir = self.config.getProtoXml()
        if self.xml_dir:
            self.showModuleMsg()
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
        # 打开文件对话框
        self.xml_dir = QFileDialog.getExistingDirectory(
            self, 'open dir', self.xml_dir)
        if not self.xml_dir:
            return
        self.config.updateProtoXml(self.xml_dir)
        self.showModuleMsg()
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

    def showModuleMsg(self):
        self.module_mgr.loadXmls(self.xml_dir)
        if not self.module_mgr.modules:
            return
        for module in self.module_mgr.modules:
            QApplication.processEvents()
            # add module
            item_module = QTreeWidgetItem(self.ui.WidMsgTree)
            item_module.setText(0,module.name)
            # item_module.setFont(10, QFont("Arial", 15, QFont.Bold))
            for msg in module.msg_list:
                # add msg item
                item_msg = QTreeWidgetItem()
                item_msg.setText(0,msg.name)
                item_module.addChild(item_msg)
                if msg.type == 'ReqReplyMsg':
                    # add req reply item
                    item_req = QTreeWidgetItem()
                    item_req.setText(0,"req")
                    item_reply = QTreeWidgetItem()
                    item_reply.setText(0, "reply")
                    item_msg.addChild(item_req)
                    item_msg.addChild(item_reply)
                    for item in msg.req_list:
                        for k,v in item.items():
                            if k == 'field_name':
                                item_field = QTreeWidgetItem()
                                item_field.setText(0,v)
                                item_req.addChild(item_field)
                    for item in msg.reply_list:
                        for k,v in item.items():
                            if k == 'field_name':
                                item_field = QTreeWidgetItem()
                                item_field.setText(0,v)
                                item_reply.addChild(item_field)                                                    
                else:
                    for item in msg.notify_list:
                        for k,v in item.items():
                            if k == 'field_name':
                                item_field = QTreeWidgetItem()
                                item_field.setText(0,v)
                                item_msg.addChild(item_field)                          
                            pass
            pass

        pass

    def onTreeClicked(self, item_idx):
        print(item_idx)
        item = self.ui.WidMsgTree.currentItem()
        print(item.text(0))
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
