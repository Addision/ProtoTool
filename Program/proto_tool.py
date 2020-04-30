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
        self.ui.BtnAdd.clicked.connect(lambda: self.onBtnClicked('add'))
        self.ui.BtnUpdate.clicked.connect(lambda: self.onBtnClicked('update'))
        self.ui.BtnDel.clicked.connect(lambda: self.onBtnClicked('del'))
        self.ui.BtnSave.clicked.connect(lambda: self.onBtnClicked('save'))
        self.ui.BtnAdd.setEnabled(False)
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

    def openProto(self):
        msg_path = self.config.getConfOne('msg_path')
        if msg_path:
            self.module_mgr.loadXmls(msg_path)
            self.showModuleMsg()

#########################右键菜单操作#########################
    def rightClickMenu(self, pos):
        try:
            self.contextMenu = QMenu(self.ui.WidMsgTree)  # 创建对象
            item = self.ui.WidMsgTree.itemAt(pos)
            addModAct = None
            updateModAct = None
            delDodAct = None
            addMsgAct = None
            updateMsgAct = None
            delMsgAct = None

            updateFieldAct = None
            delFieldAct = None
            if not item:
                addModAct = self.contextMenu.addAction(u'添加模块')  # 添加动作
                addModAct.triggered.connect(
                    lambda: self.actionHandler('add_mod'))
            elif item and item.text(3) == ItemType.MODULE:
                updateModAct = self.contextMenu.addAction(u'更新模块')
                delDodAct = self.contextMenu.addAction(u'删除模块')
                addMsgAct = self.contextMenu.addAction(u'添加消息')
                updateModAct.triggered.connect(
                    lambda: self.actionHandler('update_mod', item))
                delDodAct.triggered.connect(
                    lambda: self.actionHandler('del_mod', item))
                addMsgAct.triggered.connect(
                    lambda: self.actionHandler('add_msg', item))
            elif item and item.text(3) == ItemType.MSG:
                updateMsgAct = self.contextMenu.addAction(u'更新消息')
                delMsgAct = self.contextMenu.addAction(u'删除消息')
                updateMsgAct.triggered.connect(
                    lambda: self.actionHandler('update_msg', item))
                delMsgAct.triggered.connect(
                    lambda: self.actionHandler('del_msg', item))
            elif item and item.text(3) == ItemType.FIELD:
                updateFieldAct = self.contextMenu.addAction(u'更新字段')
                delFieldAct = self.contextMenu.addAction(u'删除字段')
                updateFieldAct.triggered.connect(
                    lambda: self.actionHandler('update_field', item))
                delFieldAct.triggered.connect(
                    lambda: self.actionHandler('del_field', item))
            self.contextMenu.exec_(QCursor.pos())  # 随指针的位置显示菜单
        except Exception as e:
            print(e)
        pass

    def actionHandler(self, op_flag, item=None):
        if not item and op_flag == 'add_mod':  # add mod
            is_ok, mod_name, mod_comment = ModGui.getModInfo()
            if not is_ok:
                return
            self.addModule(mod_name, mod_comment)
            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()

        if op_flag == 'update_mod':  # update mod
            is_ok, mod_name, mod_comment = ModGui.getModInfo()
            if not is_ok:
                return
            self.updateModule(item.text(2), mod_name, mod_comment)
            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()

        if op_flag == 'del_mod':  # del mod
            reply = QMessageBox.information(
                self, "warning", "是否删除模块?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delModule(item.text(2))
            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()

        if op_flag == 'add_msg':
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnAdd.setEnabled(True)
            self.ui.BtnSave.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(False)

        if op_flag == 'update_msg':
            self.ui.FrameMsg.setEnabled(True)
            self.ui.FrameField.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(True)
            self.ui.BtnAdd.setEnabled(False)
            self.ui.BtnDel.setEnabled(False)
            msg_type = self.getMsgTypeByItemName(item.text(0))
            if msg_type == MsgType.REQ:
                self.ui.BtnReq.setChecked(True)
            else:
                self.ui.BtnNotify.setChecked(True)

        if op_flag == 'del_msg':
            self.delMsg()
            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()

        if op_flag == 'update_field':
            self.ui.FrameField.setEnabled(True)
            self.ui.BtnUpdate.setEnabled(True)

        if op_flag == 'del_field':
            self.delField()
            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()

####################增删改查操作##############################

    def addModule(self, mod_name, mod_comment):
        module = Module()
        module.name = mod_name.title()  # 首字母大写
        module.comment = mod_comment or ""
        module.id = self.module_mgr.getNextModId()
        print('module id===', module.id)
        module.proto_imp = ""
        self.module_mgr.addModule(module)
        pass

    def updateModule(self, mod_id, mod_name, mod_comment):
        module = self.module_mgr.getModule(mod_id)
        if mod_name != "":
            module.name = mod_name
        if mod_comment != "":
            module.comment = mod_comment
        pass

    def delModule(self, mod_id):
        self.module_mgr.delModule(mod_id)
        pass

    def addMsg(self):
        msg_name = self.ui.LetMsgName.text().strip()
        if msg_name == '':
            return
        mod_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(mod_id)
        if not module:
            return
        if self.ui.BtnReq.isChecked():
            # add req and reply msg
            req_msg = MsgReq(mod_id)
            reply_msg = MsgReply(mod_id)
            req_msg.id = reply_msg.id = module.getNextMsgId()
            req_msg.name = msg_name+'Req'
            reply_msg.name = msg_name+'Reply'
            req_msg.comment = reply_msg.comment = self.ui.LetMsgCmt.text().strip()
            module.addMsg(req_msg, MsgType.REQ)
            module.addMsg(reply_msg, MsgType.REPLY)
        elif self.ui.BtnNotify.isChecked():
            # add notify msg
            notify_msg = MsgNotify(mod_id)
            notify_msg.id = module.getNextMsgId()
            notify_msg.name = msg_name+'Notify'
            notify_msg.comment = self.ui.LetMsgCmt.text().strip()
            module.addMsg(notify_msg, MsgType.NOTIFY)
            pass

    def updateMsg(self):
        msg_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(self.selected_item.parent().text(2))
        if not module:
            return
        msg_type = self.getMsgTypeByItemName(self.selected_item.text(0))
        msg_name = self.ui.LetMsgName.text().strip()
        msg_comment = self.ui.LetMsgCmt.text().strip()
        module.updateMsg(msg_id, msg_type, msg_name, msg_comment)

    def delMsg(self):
        msg_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(self.selected_item.parent().text(2))
        if not module:
            return
        msg_type = self.getMsgTypeByItemName(self.selected_item.text(0))
        module.delMsg(msg_id, msg_type)
        pass

    def addField(self):
        msg = self.getMsgByFieldItem(self.selected_item)
        if not msg:
            return
        field_name = self.ui.LetFieldName.text().strip() or ''
        field_comment = self.ui.LetFieldCmt.text().strip() or ''
        if not field_name:
            return
        field = Field()
        field.field_name = field_name
        field.field_comment = field_comment
        field.proto_type = self.ui.CbxProtoType.currentText()
        field.value_type = self.ui.CbxValueType.currentText()
        msg.addField(field)
        pass

    def updateField(self):
        msg = self.getMsgByFieldItem(self.selected_item)
        if not msg:
            return
        field = msg.getFieldByName(self.selected_item.text(0))
        field_name = self.ui.LetFieldName.text().strip() or ''
        field_comment = self.ui.LetFieldCmt.text().strip() or ''
        if not field_name:
            return
        field.field_name = field_name
        field.field_comment = field_comment
        field.proto_type = self.ui.CbxProtoType.currentText()
        field.value_type = self.ui.CbxValueType.currentText()
        pass

    def delField(self):
        msg = self.getMsgByFieldItem(self.selected_item)
        if not msg:
            return
        msg.delField(self.selected_item.text(0))
        pass

##################菜单操作###############################
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

###################################################

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


    def onTreeItemClicked(self, idx):
        self.selected_item = self.ui.WidMsgTree.currentItem()
        self.showItemDetail(self.selected_item)
        print(self.selected_item.text(0))
        # clear edit
        self.ui.LetMsgName.clear()
        self.ui.LetMsgCmt.clear()
        self.ui.LetFieldName.clear()
        self.ui.LetFieldCmt.clear()

    def saveAll(self):
        save_dir = self.config.getConfOne('msg_path')
        self.module_mgr.saveXmls(save_dir)
        self.clearTreeWidgetSelect()
        # TODO 生成proto 文件

        pass

    def clearTreeWidgetSelect(self):
        self.ui.WidMsgTree.clearSelection()
        self.selected_item = None

    def getMsgTypeByItemName(self, item_name):  # msg item name
        if item_name.endswith('Req', 3):
            return MsgType.REQ
        if item_name.endswith('Reply', 5):
            return MsgType.REPLY
        if item_name.endswith('Notify', 6):
            return MsgType.NOTIFY

    def getMsgByFieldItem(self, item):
        if not item:
            return None
        mod_item = item.parent().parent()
        msg_item = item.parent()
        module = self.module_mgr.getModule(mod_item.text(2))
        msg_type = self.getMsgTypeByItemName(msg_item.text(0))
        msg = module.getMsg(msg_item.text(2), msg_type)
        return msg

    def onBtnClicked(self, btn):
        try:
            if btn == 'save':
                self.saveAll()
                self.ui.BtnSave.setEnabled(False)
                return
            if not self.selected_item:
                return
            item_type = self.selected_item.text(3)
            if btn == 'add':
                if item_type == ItemType.MODULE:
                    self.addMsg()
                else:
                    self.addField()
            if btn == 'del':
                if item_type == ItemType.MSG:
                    self.delMsg()
                else:
                    self.delField()
                pass
            if btn == 'update':
                if item_type == ItemType.MSG:
                    self.updateMsg()
                else:
                    self.updateField()

            self.ui.BtnSave.setEnabled(True)
            self.showModuleMsg()
        except Exception as e:
            print(e)

    def showItemDetail(self, item):
        if not item:
            return
        item_type = item.text(3)
        self.model.clear()
        self.model.setHorizontalHeaderLabels([u'名称', u'说明'])
        if item_type == ItemType.MODULE:
            self.model.appendRow(
                [QStandardItem(u'模块ID'), QStandardItem(item.text(2))])
            self.model.appendRow(
                [QStandardItem(u'模块名称'), QStandardItem(item.text(0))])
            self.model.appendRow(
                [QStandardItem(u'说明'), QStandardItem(item.text(1))])
            pass

        if item_type == ItemType.MSG:
            module = self.module_mgr.getModule(item.parent().text(2))
            self.model.appendRow(
                [QStandardItem(u'消息ID'), QStandardItem(item.text(2))])
            self.model.appendRow(
                [QStandardItem(u'消息名称'), QStandardItem(item.text(0))])
            self.model.appendRow(
                [QStandardItem(u'所属模块'), QStandardItem(module.name)])
            self.model.appendRow(
                [QStandardItem(u'说明'), QStandardItem(item.text(1))])
            pass

        if item_type == ItemType.FIELD:
            module = self.module_mgr.getModule(item.parent().parent().text(2))
            msg_type = self.getMsgTypeByItemName(item.parent().text(0))
            msg = module.getMsg(item.parent().text(2), msg_type)
            field = msg.getFieldByName(item.text(0))
            self.model.appendRow(
                [QStandardItem(u'字段名称'), QStandardItem(field.field_name)])
            self.model.appendRow(
                [QStandardItem(u'标签'), QStandardItem(field.tag)])
            self.model.appendRow(
                [QStandardItem(u'数值类型'), QStandardItem(field.value_type)])
            self.model.appendRow(
                [QStandardItem(u'所属消息'), QStandardItem(msg.name)])
            self.model.appendRow(
                [QStandardItem(u'说明'), QStandardItem(field.comment)])
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainForm = ProtoTool()
    mainForm.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setAttribute(QtCore.Qt.AA_NativeWindows)
    app.setAttribute(QtCore.Qt.AA_MSWindowsUseDirect3DByDefault)

    sys.exit(app.exec_())
