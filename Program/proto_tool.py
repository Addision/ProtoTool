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
from msg import *
from module_mgr import *
from item_data import *
from setting import *
import configparser


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        self.setStyleSheet('background-color: rgb(230, 230, 230);')

        # widget 设置
        self.ui.WidMsgTree.setHeaderLabels(['模块消息', '说明'])
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
        self.ui.FrameMod.setStyleSheet('background-color: rgb(200, 200, 200);')
        self.ui.FrameMsg.setStyleSheet('background-color: rgb(200, 200, 200);')
        self.ui.FrameField.setStyleSheet(
            'background-color: rgb(200, 200, 200);')
        # button 设置
        self.ui.BtnSave.setEnabled(False)
        self.ui.BtnDel.clicked.connect(lambda: self.onBtnClicked('del'))
        self.ui.BtnUpdate.clicked.connect(lambda: self.onBtnClicked('update'))
        self.ui.BtnSave.clicked.connect(lambda: self.onBtnClicked('save'))
        self.ui.BtnModAdd.clicked.connect(lambda: self.onBtnClicked('mod_add'))
        self.ui.BtnMsgAdd.clicked.connect(lambda: self.onBtnClicked('msg_add'))
        self.ui.BtnFieldAdd.clicked.connect(
            lambda: self.onBtnClicked('field_add'))
        self.ui.BtnDel.setEnabled(False)
        self.ui.BtnUpdate.setEnabled(False)
        self.ui.BtnSave.setEnabled(False)
        # menu 设置
        self.ui.menuOpen.setEnabled(True)
        self.ui.menuSave.setEnabled(False)
        self.ui.menuSaveAs.setEnabled(False)
        self.ui.menuClose.setEnabled(True)
        self.ui.menuFile.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuTool.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuSet.triggered[QAction].connect(self.onMenuTrigger)

        # tableview 设置
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['名称', '说明'])
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
        self.openProto()
        self.is_add_msg = False
        self.is_add_field = False
    pass

    def openProto(self):
        msg_path = self.config.getConfOne('msg_path')
        if msg_path:
            self.module_mgr.loadXmls(msg_path)
            self.showModuleMsg()

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
        if menu == self.ui.menuSave:
            self.menuBarSave()
        if menu == self.ui.menuSaveAs:
            self.menuBarSaveAs()
        if menu == self.ui.menuClose:
            self.menuBarClose()
        if menu == self.ui.menuProtoServer:
            self.menuBarProtoServer()
        if menu == self.ui.menuProtoClient:
            self.menuBarProtoClient()
        if menu == self.ui.menuSetting:
            self.menuSetting()

    def menuSetting(self):
        self.setting = Setting()
        self.setting.show()

    def menuBarOpen(self):
        print("start load xml files......")
        # 打开文件对话框
        msg_path = QFileDialog.getExistingDirectory(
            self, 'open dir', './')
        if not msg_path:
            return
        self.config.updateConfOne('msg_path', msg_path)
        self.openProto()
        pass

    def menuBarSave(self):
        pass

    def menuBarSaveAs(self):
        pass

    def menuBarClose(self):
        os._exit(0)
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
                        if not item:
                            continue
                        item_field = QTreeWidgetItem()
                        item_field.setText(0, item['field_name'])
                        item_field.setText(1, item['comment'])
                        item_field.setText(2, str(msg.id))
                        item_field.setText(3, ItemType.FIELD)
                        item_req.addChild(item_field)
                    for item in msg.reply_list:
                        if not item:
                            continue
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
        self.ui.BtnDel.setEnabled(True)
        self.ui.BtnUpdate.setEnabled(True)
        self.selected_item = self.ui.WidMsgTree.currentItem()
        self.showItemInfo(self.selected_item)
        item_type = self.selected_item.text(3)
        if item_type == ItemType.MODULE:
            self.addMsgOrAddField(1)
        if item_type == ItemType.REQ or item_type == ItemType.REPLY or item_type == ItemType.NOTIFY:
            self.addMsgOrAddField(2)
        else:
            self.addMsgOrAddField(3)

        if item_type == ItemType.MODULE:
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnMsgAdd.setEnabled(True)

        if item_type == ItemType.MSG or item_type == ItemType.NOTIFY:
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnMsgAdd.setEnabled(False)
            self.ui.BtnFieldAdd.setEnabled(True)
        if item_type == ItemType.REPLY or item_type == ItemType.REQ:
            self.ui.BtnDel.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(False)
            self.ui.BtnFieldAdd.setEnabled(True)
        if item_type == ItemType.FIELD:
            self.ui.FrameField.setEnabled(True)
            self.ui.BtnFieldAdd.setEnabled(False)

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

    def saveAll(self):
        save_dir = self.config.getConfOne('msg_path')
        self.module_mgr.writeXmls(save_dir)
        self.clearTreeWidgetSelect()
        # 生成proto 文件

        pass

    def clearTreeWidgetSelect(self):
        self.ui.WidMsgTree.clearSelection()
        self.selected_item = None

    def onBtnDelMod(self):
        mod_id = self.selected_item.text(2)
        self.module_mgr.delModule(mod_id)

    def onBtnUpdateMod(self):
        mod_id = self.selected_item.text(2)
        mod_name = self.ui.LetModName.text().strip()
        mod_comment = self.ui.LetModCmt.text().strip()
        mod = self.module_mgr.getMod(mod_id)
        if not mod or not mod_name:
            return
        mod.update(mod_name, mod_comment)

    def onBtnDelMsg(self):
        mod_id = self.selected_item.parent().text(2)
        mod = self.module_mgr.getMod(mod_id)
        if not mod:
            return
        msg_id = self.selected_item.text(2)
        mod.delMsg(msg_id)

    def onBtnUpdateMsg(self):
        mod_id = self.selected_item.parent().text(2)
        mod = self.module_mgr.getMod(mod_id)
        if not mod:
            return
        msg_name = self.ui.LetMsgName.text().strip()
        msg_comment = self.ui.LetMsgCmt.text().strip()
        msg = mod.getMsg(self.selected_item.text(2))
        if not msg or not msg_name:
            return
        msg.updateMsg(msg_name, msg_comment)

    def onBtnDelField(self):
        msg = self.getMsgByFieldItem(self.selected_item)
        field_name = self.selected_item.text(0)
        if not msg:
            return
        msg_item = self.selected_item.parent()
        if msg_item.text(3) == ItemType.REQ:
            msg.delField(field_name, 'req')
        if msg_item.text(3) == ItemType.REPLY:
            msg.delField(field_name, 'reply')
        if msg_item.text(3) == ItemType.NOTIFY:
            msg.delField(field_name, 'notify')

    def onBtnUpdateField(self):

        msg = self.getMsgByFieldItem(self.selected_item)
        field_name = self.selected_item.text(0)
        if not msg:
            return
        field = None
        msg_item = self.selected_item.parent()
        if msg_item.text(3) == ItemType.REQ:
            field = msg.findField(field_name, 'req')
        if msg_item.text(3) == ItemType.REPLY:
            field = msg.findField(field_name, 'reply')
        if msg_item.text(3) == ItemType.NOTIFY:
            field = msg.findField(field_name, 'notify')
        field['proto_type'] = self.ui.CbxProtoType
        field['proto_value'] = self.ui.CbxValueType
        field_name = self.ui.LetFieldName.text().strip()
        field_comment = self.ui.LetFieldCmt.text().strip()
        if field_name != "":
            field['field_name'] = field_name
        if field_comment != "":
            field['comment'] = field_comment

    def onBtnClicked(self, btn):
        try:
            self.ui.BtnSave.setEnabled(True)
            if btn == 'mod_add':
                self.modAdd()
            if btn == 'save':
                self.saveAll()
                self.ui.BtnSave.setEnabled(False)
            if not self.selected_item:
                return
            item_type = self.selected_item.text(3)
            if item_type == ItemType.MODULE:
                if btn == 'del':
                    self.onBtnDelMod()
                if btn == 'update':
                    self.onBtnUpdateMod()
                pass
            if item_type == ItemType.MSG or item_type == ItemType.NOTIFY:
                if btn == 'del':
                    self.onBtnDelMsg()
                if btn == 'update':
                    self.onBtnUpdateMsg()
                pass
            if item_type == ItemType.FIELD:
                if btn == 'del':
                    self.onBtnDelField()
                if btn == 'update':
                    self.onBtnUpdateField()

            if btn == 'msg_add':
                self.msgAdd()
            if btn == 'field_add':
                self.fieldAdd()

            self.ui.BtnDel.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(False)
            self.ui.WidMsgTree.clearSelection()
            self.selected_item = None
            self.showModuleMsg()
        except Exception as e:
            print(e)

    def getMsgByFieldItem(self, item):
        name = item.text(0)
        msg_item = None
        if item.text(3) != ItemType.FIELD:
            return None
        if item.parent().text(3) == ItemType.NOTIFY:
            msg_item = item.parent()
        else:
            msg_item = item.parent().parent()
        msg_id = msg_item.text(2)
        mod_id = msg_item.parent().text(2)
        msg = self.module_mgr.getMsg(mod_id, msg_id)
        return msg
        pass

    def getMsgByMsgItem(self, item):
        msg_item = None
        if item.text(0) == 'req' or item.text(0) == 'reply':
            msg_item = item.parent()
        else:
            msg_item = item

        msg_id = msg_item.text(2)
        mod_id = msg_item.parent().text(2)
        msg = self.module_mgr.getMsg(mod_id, msg_id)
        return msg

    def fieldAdd(self):
        if self.ui.LetFieldName == "":
            return
        name = self.selected_item.text(0)
        msg = self.getMsgByMsgItem(self.selected_item)
        if not msg:
            return
        next_tag = 0
        if name == 'req' or name == 'reply':
            next_tag = msg.getNextTag(name)
        else:
            next_tag = msg.getNextTag('notify')
        field = {}
        field['proto_type'] = self.ui.CbxProtoType.currentText()
        field['value_type'] = self.ui.CbxValueType.currentText()
        field['field_name'] = self.ui.LetFieldName.text().strip()
        field['tag'] = str(next_tag)
        field['comment'] = self.ui.LetFieldCmt.text().strip()
        if name == 'req' or name == 'reply':
            msg.addField(field, name)
        else:
            msg.addField(field, 'notify')
            pass

    def msgAdd(self):
        mod_id = self.selected_item.text(2)
        msg = Msg(mod_id)
        msg.name = self.ui.LetMsgName.text().strip()
        if msg.name == "":
            return
        msg.comment = self.ui.LetMsgCmt.text().strip()
        mod = self.module_mgr.getMod(mod_id)
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
        pass

    def modAdd(self):
        mod = Module()
        mod.name = self.ui.LetModName.text().strip()
        if mod.name == "":
            return
        mod.name = mod.name.title()  # 首字母大写
        mod.id = self.module_mgr.nextModId()
        mod.comment = self.ui.LetModCmt.text().strip() or ""
        mod.proto_imp = ""
        self.module_mgr.addModule(mod)
        # clear
        self.ui.LetModCmt.clear()
        self.ui.LetModName.clear()
        self.showModuleMsg()
        self.clearTreeWidgetSelect()

    def showItemInfo(self, item):
        item_type = item.text(3)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['名称', '说明'])
        if item_type == ItemType.MODULE or item_type == ItemType.MSG or item_type == ItemType.NOTIFY:
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
            msg = self.getMsgByFieldItem(item)
            item_name = item.text(0)
            field = None
            item_parent_name = item.parent().text(0)
            if item_parent_name == 'req' or item_parent_name == 'reply':
                field = msg.getField(item_name, item_parent_name)
            else:
                field = msg.getField(item_name, 'notify')
            if not field:
                return
            self.model.appendRow(
                [QStandardItem('msg'), QStandardItem(msg.name)])
            self.model.appendRow(
                [QStandardItem('name'), QStandardItem(field['field_name'])])
            self.model.appendRow(
                [QStandardItem('tag'), QStandardItem(field['tag'])])
            self.model.appendRow(
                [QStandardItem('value type'), QStandardItem(field['value_type'])])
            self.model.appendRow(
                [QStandardItem('comment'), QStandardItem(field['comment'])])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
