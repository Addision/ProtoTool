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
        self.ui.WidMsgTree.itemClicked.connect(self.onTreeItemClicked)
        
        # frame 设置
        self.ui.FrameMod.setEnabled(True)
        self.ui.FrameMsg.setEnabled(False)
        self.ui.FrameField.setEnabled(False)
        self.ui.FrameMod.installEventFilter(self)
        self.ui.FrameMsg.installEventFilter(self)
        self.ui.FrameField.installEventFilter(self)
        # self.ui.FrameMod.setFrameStyle(QFrame.Box | QFrame.Sunken)
        # button 设置
        self.ui.BtnSave.setEnabled(False)
        self.ui.BtnAdd.clicked.connect(lambda: self.onBtnClicked('add'))
        self.ui.BtnDel.clicked.connect(lambda: self.onBtnClicked('del'))
        self.ui.BtnUpdate.clicked.connect(lambda: self.onBtnClicked('update'))
        self.ui.BtnSave.clicked.connect(lambda: self.onBtnClicked('save'))
        self.ui.BtnModAdd.clicked.connect(lambda: self.onBtnClicked('mod_add'))
        self.ui.BtnMsgAdd.clicked.connect(lambda: self.onBtnClicked('msg_add'))
        self.ui.BtnFieldAdd.clicked.connect(
            lambda: self.onBtnClicked('field_add'))
        # menu 设置
        self.ui.menuSave.setEnabled(False)
        self.ui.menuSaveAs.setEnabled(False)
        self.ui.menuFile.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuTool.triggered[QAction].connect(self.onMenuTrigger)
        # tableview 设置
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['name', 'value'])
        self.ui.BbvInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.BbvInfo.setEditTriggers(QTableView.NoEditTriggers)
        self.ui.BbvInfo.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.BbvInfo.setModel(self.model)
        # other 设置
        self.ui.BtnReq.setChecked(True)
        self.setFixedSize(self.width(), self.height())
        self.selected_item = None
        self.config = Config()
        self.module_mgr = ModuleMgr()
        self.xml_dir = self.config.getProtoXml()
        if self.xml_dir:
            self.module_mgr.loadXmls(self.xml_dir)
            self.showModuleMsg()
        self.is_add_msg = False
        self.is_add_field = False
    pass

    def mousePressEvent(self, event):
        print("mousePressEvent")
        print(event)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusOut:
            print("FocusOut......")
        if event.type() == QtCore.QEvent.FocusIn:
            print("XXXXXXXXXXXXXXXXXXXXXXXXX")
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if object != self.ui.FrameMod:
                self.ui.LetModName.clear()
                self.ui.LetModCmt.clear()
            if object != self.ui.FrameMsg:
                self.ui.LetMsgName.clear()
                self.ui.LetMsgCmt.clear()
            if object != self.ui.FrameField:
                self.ui.LetFieldName.clear()
                self.ui.LetFieldCmt.clear()
        return True

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
        self.module_mgr.loadXmls(self.xml_dir)
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
        self.ui.WidMsgTree.clear()
        if not self.module_mgr.modules:
            return
        for id, module in self.module_mgr.modules.items():
            QApplication.processEvents()
            # add module
            item_module = QTreeWidgetItem(self.ui.WidMsgTree)
            item_module.setText(0, module.name)
            item_module.setText(1, module.comment)
            item_module.setText(2, str(module.id))
            item_module.setText(3, str(ItemType.MODULE))
            # item_module.setFont(10, QFont("Arial", 15, QFont.Bold))
            for msg in module.msg_list:
                # add msg item
                item_msg = QTreeWidgetItem()
                item_msg.setText(0, msg.name)
                item_msg.setText(1, msg.comment)
                item_msg.setText(2, str(msg.id))
                item_msg.setText(3, str(ItemType.MSG))
                item_module.addChild(item_msg)
                if msg.type == 'ReqReplyMsg':
                    # add req reply item
                    item_req = QTreeWidgetItem()
                    item_req.setText(0, "req")
                    item_req.setText(3, ItemType.REQ)
                    item_reply = QTreeWidgetItem()
                    item_reply.setText(0, "reply")
                    item_reply.setText(3, ItemType.REPLY)
                    # item_reply.setSelected(False)
                    item_msg.addChild(item_req)
                    item_msg.addChild(item_reply)
                    for item in msg.req_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, str(msg.id))
                        item_field.setText(3, ItemType.FIELD)
                        item_req.addChild(item_field)
                    for item in msg.reply_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, str(msg.id))
                        item_field.setText(3, ItemType.FIELD)
                        item_reply.addChild(item_field)
                else:
                    item_msg.setText(3, ItemType.NOTIFY)
                    for item in msg.notify_list:
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, str(msg.id))
                        item_field.setText(3, ItemType.FIELD)
                        item_msg.addChild(item_field)
            self.ui.WidMsgTree.expandToDepth(0)


    def onTreeClicked(self, item_idx):
        tree_item = self.ui.WidMsgTree.currentItem()
        if tree_item.text(3) == ItemType.MODULE:
            self.ui.FrameMsg.setEnabled(True)

            pass
        pass

    def onTreeItemClicked(self, idx):
        self.selected_item = self.ui.WidMsgTree.currentItem()
        self.showItemInfo(self.selected_item)
        item_type = self.selected_item.text(3)
        if item_type == ItemType.MODULE:
            self.addMsgOrAddField(1)
        if item_type == ItemType.REQ or item_type == ItemType.REPLY or item_type == ItemType.NOTIFY:
            self.addMsgOrAddField(2)
        else:
            self.addMsgOrAddField(3)
        pass

    def addMsgOrAddField(self, add_flag):
        if add_flag == 1:
            self.is_add_msg = True
            self.is_add_field = False
            self.ui.FrameMsg.setEnabled(True)
            self.ui.FrameField.setEnabled(False)
        if add_flag == 2:
            self.is_add_msg = False
            self.is_add_field = True
            self.ui.FrameMsg.setEnabled(False)
            self.ui.FrameField.setEnabled(True)
        else:
            self.is_add_msg = False
            self.is_add_field = False
            self.ui.FrameMsg.setEnabled(False)
            self.ui.FrameField.setEnabled(False)
        # clear edit      
        self.ui.LetModName.clear()
        self.ui.LetModCmt.clear()
        self.ui.LetMsgName.clear()
        self.ui.LetMsgCmt.clear()
        self.ui.LetFieldName.clear()      
        self.ui.LetFieldCmt.clear()

    def onBtnClicked(self, btn):
        if btn == 'add':
            # 如果选中的是消息 增加字段 否则 增加新模块
            if self.selected_item and self.selected_item.text(3) == ItemType.MODULE:
                self.ui.FrameMsg.setEnabled(True)
                self.selected_item = None
            if self.selected_item and self.selected_item.text(3) == ItemType.MSG:
                self.ui.FrameField.setEnabled(True)
                self.ui.FrameMsg.setEnabled(False)
                self.selected_item = None
            else:
                print('add module')

            print('add')
        if btn == 'del':
            print('del')
        if btn == 'update':
            print('update')
        if btn == 'save':
            print('save')

        if btn == 'mod_add':
            self.modAdd()
        if btn == 'msg_add':
            self.msgAdd()
        if btn == 'field_add':
            self.fieldAdd()

    def fieldAdd(self):
        name = self.selected_item.text(0)
        msg_item = None
        if name == "req" or name == "reply":
            msg_item = self.selected_item.parent()
        else:
            msg_item = self.selected_item
        msg_id = msg_item.text(2)
        
        pass

    def msgAdd(self):
        mod_id = self.selected_item.text(2)
        msg = Msg(mod_id)
        msg.name = self.ui.LetMsgName.text().strip()
        if msg.name == "":
            return  
        msg.comment = self.ui.LetMsgCmt.text().strip()          
        mod = self.module_mgr.getModule(mod_id)
        if not mod:
            return
        msg.id = mod.nextMsgId()
        if self.ui.BtnReq.isChecked():
            # add req msg
            msg.type = "ReqReplyMsg"
        if self.ui.BtnNotify.isChecked():
            # add notify msg
            msg.type = "NotifyMsg"
        mod.addMsg(msg)
        self.showModuleMsg()

        pass

    def modAdd(self):
        mod = Module()
        mod.name = self.ui.LetModName.text().strip()
        if mod.name == "":
            return
        mod.id = self.module_mgr.nextModId()
        mod.comment = self.ui.LetModCmt.text().strip() or ""
        mod.proto_imp = ""
        self.module_mgr.addModule(mod)
        self.showModuleMsg()
        # clear
        self.ui.LetModCmt.clear()
        self.ui.LetModName.clear()

    def showItemInfo(self, item):
        item_type = item.text(3)

        if item_type == ItemType.MODULE or item_type == ItemType.MSG or item_type == ItemType.NOTIFY:
            self.model.removeRows(0, 3)
            name = item.text(0)
            comment = item.text(1)
            id = item.text(2)
            self.model.appendRow(
                [QStandardItem('id'), QStandardItem(id)])
            self.model.appendRow([QStandardItem('name'), QStandardItem(name)])
            self.model.appendRow(
                [QStandardItem('comment'), QStandardItem(comment)])
            pass
        if item_type == ItemType.FIELD:
            print(item.parent().text(3))
            print(item.parent().text(1))
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
