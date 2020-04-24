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
from item_data import *


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.98)
        # widget 设置
        self.ui.WidMsgTree.setHeaderLabels(['proto msg', 'comment'])
        self.ui.WidMsgTree.setStyle(QStyleFactory.create('windows'))
        self.ui.WidMsgTree.clicked.connect(self.onTreeClicked)
        # frame 设置
        self.ui.FrameMsg.setEnabled(False)
        self.ui.FrameField.setEnabled(False)
        # button 设置
        self.ui.BtnSave.setEnabled(False)
        self.ui.BtnAdd.clicked.connect(lambda:self.onBtnClicked('add'))
        self.ui.BtnDel.clicked.connect(lambda:self.onBtnClicked('del'))
        self.ui.BtnUpdate.clicked.connect(lambda:self.onBtnClicked('update'))
        self.ui.BtnSave.clicked.connect(lambda:self.onBtnClicked('save'))
        # menu 设置
        self.ui.menuSave.setEnabled(False)
        self.ui.menuSaveAs.setEnabled(False)
        self.ui.menuFile.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuTool.triggered[QAction].connect(self.onMenuTrigger)
        # other 设置
        self.selected_item = None
        self.config = Config()
        self.module_mgr = ModuleMgr()
        self.xml_dir = self.config.getProtoXml()
        if self.xml_dir:
            self.showModuleMsg()
    pass

    def onMenuTrigger(self, menu):
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
            item_module.setText(0, module.name)
            item_module.setText(1, module.comment)
            item_module.setText(2, module.id)
            item_module.setText(3, str(ItemType.MODULE))
            # item_module.setFont(10, QFont("Arial", 15, QFont.Bold))
            for msg in module.msg_list:
                # add msg item
                item_msg = QTreeWidgetItem()
                item_msg.setText(0, msg.name)
                item_msg.setText(1, msg.comment)
                item_msg.setText(2, msg.id)
                item_msg.setText(3, str(ItemType.MSG))
                item_module.addChild(item_msg)
                if msg.type == 'ReqReplyMsg':
                    # add req reply item
                    item_req = QTreeWidgetItem()
                    # TODO 设置不可以选中
                    item_req.setText(0,"req")
                    item_reply = QTreeWidgetItem()
                    item_reply.setText(0, "reply")
                    item_msg.addChild(item_req)
                    item_msg.addChild(item_reply)
                    for item in msg.req_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, msg.id)
                        item_field.setText(3, str(ItemType.REQ))
                        item_req.addChild(item_field)
                    for item in msg.reply_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, msg.id)
                        item_field.setText(3, str(ItemType.REPLY))
                        item_reply.addChild(item_field)                                                    
                else:
                    for item in msg.notify_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, msg.id)
                        item_field.setText(3, str(ItemType.NOTIFY))
                        item_msg.addChild(item_field)
                                                

    def onTreeClicked(self, item_idx):
        print(item_idx)
        self.selected_item = self.ui.WidMsgTree.currentItem()
        print(self.selected_item.text(0))
        print(self.selected_item.text(3))
        pass

    def onBtnClicked(self, btn):
        if btn == 'add':

            print('add')
        if btn == 'del':
            print('del')
        if btn == 'update':
            print('update')
        if btn == 'save':
            print('save')
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
