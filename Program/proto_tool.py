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
from setting_gui import *
from mod_gui import *
from common import *
import configparser


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        self.setStyleSheet('background-color: rgb(230, 230, 230);')
        # 禁用窗口最大化 拉伸
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        # widget 设置
        self.ui.WidMsgTree.setHeaderLabels(['模块消息', '说明'])
        self.ui.WidMsgTree.setStyle(QStyleFactory.create('windows'))
        self.ui.WidMsgTree.clicked.connect(self.onTreeClicked)
        self.ui.WidMsgTree.itemClicked.connect(self.onTreeItemClicked)
        # 右键菜单
        self.ui.WidMsgTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.WidMsgTree.customContextMenuRequested.connect(
            self.rightClickMenu)
        # frame 设置
        self.ui.FrameMsg.setEnabled(False)
        self.ui.FrameField.setEnabled(False)
        self.ui.FrameMsg.setStyleSheet('background-color: rgb(200, 200, 200);')
        self.ui.FrameField.setStyleSheet(
            'background-color: rgb(200, 200, 200);')
        # button 设置
        self.ui.BtnSave.setEnabled(False)
        self.ui.BtnDel.clicked.connect(lambda: self.onBtnClicked('del'))
        self.ui.BtnUpdate.clicked.connect(lambda: self.onBtnClicked('update'))
        self.ui.BtnSave.clicked.connect(lambda: self.onBtnClicked('save'))
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
        self.selected_item = None
        self.config = Config()
        self.module_mgr = ModuleMgr()
        self.openProto()
    pass

    def rightClickMenu(self, pos):
        try:
            self.contextMenu = QMenu(self.ui.WidMsgTree)  # 创建对象
            item = self.ui.WidMsgTree.itemAt(pos)
            add_menu = None
            del_menu = None
            update_menu = None
            if not item:
                add_menu = self.contextMenu.addAction(u'添加模块')  # 添加动作
                update_menu = self.contextMenu.addAction(u'更新模块')
                del_menu = self.contextMenu.addAction(u'删除模块')
            elif item.text(3) == ItemType.MODULE:
                add_menu = self.contextMenu.addAction(u'添加消息')
                update_menu = self.contextMenu.addAction(u'更新消息')
                del_menu = self.contextMenu.addAction(u'删除消息')
            add_menu.triggered.connect(lambda: self.actionHandler('add', item))
            update_menu.triggered.connect(
                lambda: self.actionHandler('update', item))
            del_menu.triggered.connect(lambda: self.actionHandler('del', item))
            self.contextMenu.exec_(QCursor.pos())  # 随指针的位置显示菜单
        except Exception as e:
            print(e)
            pass
        pass

    def addModule(self):
        
        pass

    def updateModule(self):
        pass

    def delModule(self):
        pass

    def addMsg(self):
        pass

    def updateMsg(self):
        pass

    def delMsg(self):
        pass

    def addField(self):
        pass

    def updateField(self):
        pass

    def delField(self):
        pass

    def actionHandler(self, op_flag, item=None):
        if not item:
            if op_flag == 'add':  # add mod
                pass
            if op_flag == 'update':  # update mod
                pass
            if op_flag == 'del':  # del mod
                pass
        if not item and op_flag == 'add':
            self.mod_form = ModGui()
            self.mod_form.show()

    def openProto(self):
        msg_path = self.config.getConfOne('msg_path')
        if msg_path:
            self.module_mgr.loadXmls(msg_path)
            self.showModuleMsg()

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
        self.setting = SettingGui()
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

    def getMsgTypeByItemName(self, item_name):
        if item_name.endswith('Req', 3):
            return MsgType.REQ
        if item_name.endswith('Reply', 5):
            return MsgType.REPLY
        if item_name.endswith('Notify', 6):
            return MsgType.NOTIFY

    def showModuleMsg(self):
        self.ui.WidMsgTree.clear()
        if not self.module_mgr.module_dic:
            return
        for id, module in self.module_mgr.module_dic.items():
            QApplication.processEvents()
            # add module
            item_module = QTreeWidgetItem(self.ui.WidMsgTree)
            item_module.setText(0, module.name)
            item_module.setText(1, module.comment)
            item_module.setText(2, module.id)
            item_module.setText(3, ItemType.MODULE)
            # add msg
            for msg_id, req_msg in module.req_msg_dic.items():
                # add req
                item_req_msg = QTreeWidgetItem()
                item_module.addChild(item_req_msg)
                item_req_msg.setText(0, req_msg.name)
                item_req_msg.setText(1, req_msg.comment)
                item_req_msg.setText(2, req_msg.id)
                item_req_msg.setText(3, ItemType.MSG)
                # add field
                for field in req_msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_req_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, req_msg.id)
                    item_field.setText(3, ItemType.FIELD)
                # add reply
                reply_msg = module.reply_msg_dic[msg_id]
                item_reply_msg = QTreeWidgetItem()
                item_module.addChild(item_reply_msg)
                item_reply_msg.setText(0, reply_msg.name)
                item_reply_msg.setText(1, reply_msg.comment)
                item_reply_msg.setText(2, reply_msg.id)
                item_reply_msg.setText(3, ItemType.MSG)
                for field in reply_msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_reply_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, reply_msg.id)
                    item_field.setText(3, ItemType.FIELD)

            for msg_id, msg in module.notify_msg_dic.items():
                item_msg = QTreeWidgetItem()
                item_module.addChild(item_msg)
                item_msg.setText(0, msg.name)
                item_msg.setText(1, msg.comment)
                item_msg.setText(2, msg.id)
                item_msg.setText(3, ItemType.MSG)
                # add field
                for field in msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, msg.id)
                    item_field.setText(3, ItemType.FIELD)

            self.ui.WidMsgTree.expandToDepth(0)

    def onTreeClicked(self, item_idx):
        tree_item = self.ui.WidMsgTree.currentItem()
        if tree_item.text(3) == ItemType.MODULE:
            self.ui.FrameMsg.setEnabled(True)

            pass
        pass

    def onTreeItemClicked(self, idx):
        self.selected_item = self.ui.WidMsgTree.currentItem()
        self.showItemDetail(self.selected_item)
        item_type = self.selected_item.text(3)
        self.setFrameEnable(item_type)

    def setFrameEnable(self, item_type):
        if item_type == ItemType.MODULE:  # add msg
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnUpdate.setEnabled(False)
            self.ui.BtnDel.setEnabled(False)
            pass

        if item_type == ItemType.MSG:   # modify del msg  or add Field
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnMsgAdd.setEnabled(False)
            self.ui.FrameField.setEnabled(True)
            self.ui.BtnFieldAdd.setEnabled(True)
            self.ui.BtnUpdate.setEnabled(True)
            self.ui.BtnDel.setEnabled(True)
            pass

        if item_type == ItemType.FIELD:   # modify del Field
            self.ui.FrameMsg.setEnabled(False)
            self.ui.FrameField.setEnabled(True)
            self.ui.BtnFieldAdd.setEnabled(False)
            pass
        # clear edit
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
        if not item:
            return None
        mod_item = item.parent().parent()
        msg_item = item.parent()
        module = self.module_mgr.getModule(mod_item.text(2))
        msg = module.getMsg(msg_item.text(2), int(msg_item.text(3)))
        return msg

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

    def showItemDetail(self, item):
        if not item:
            return
        item_type = item.text(3)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['名称', '说明'])
        if item_type == ItemType.MODULE:
            self.model.appendRow(
                [QStandardItem('module id'), QStandardItem(item.text(2))])
            self.model.appendRow(
                [QStandardItem('module name'), QStandardItem(item.text(0))])
            self.model.appendRow(
                [QStandardItem('comment'), QStandardItem(item.text(1))])
            pass

        if item_type == ItemType.MSG:
            module = self.module_mgr.getModule(item.parent().text(2))
            self.model.appendRow(
                [QStandardItem('msg id'), QStandardItem(item.text(2))])
            self.model.appendRow(
                [QStandardItem('msg name'), QStandardItem(item.text(0))])
            self.model.appendRow(
                [QStandardItem('belong module'), QStandardItem(module.name)])
            self.model.appendRow(
                [QStandardItem('comment'), QStandardItem(item.text(1))])
            pass

        if item_type == ItemType.FIELD:
            module = self.module_mgr.getModule(item.parent().parent().text(2))
            msg_type = self.getMsgTypeByItemName(item.parent().text(0))
            msg = module.getMsg(item.parent().text(2), msg_type)
            field = msg.getFieldByName(item.text(0))
            self.model.appendRow(
                [QStandardItem('name'), QStandardItem(field.field_name)])
            self.model.appendRow(
                [QStandardItem('tag'), QStandardItem(field.tag)])
            self.model.appendRow(
                [QStandardItem('value type'), QStandardItem(field.value_type)])
            self.model.appendRow(
                [QStandardItem('belong name'), QStandardItem(msg.name)])
            self.model.appendRow(
                [QStandardItem('comment'), QStandardItem(field.comment)])
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
