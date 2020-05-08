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
from gen_mgr import *
import configparser
from subprocess import *
import time
import PyQt5.sip


class ProtoTool(QMainWindow):
    def __init__(self, parent=None):
        super(ProtoTool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        # self.setStyleSheet('background-color: rgb(230, 230, 230);')
        self.setWindowIcon(QtGui.QIcon('./icons/Icon_.ico'))
        self.setFixedSize(self.width(), self.height())
        # widget 设置
        self.ui.WidMsgTree.setHeaderLabels([u'模块消息', u'说明'])
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
        self.ui.BtnSave.clicked.connect(lambda: self.onBtnClicked('save'))
        self.ui.BtnAdd.setEnabled(False)
        self.ui.BtnUpdate.setEnabled(False)
        self.ui.BtnSave.setEnabled(False)
        # menu 设置
        self.ui.menuOpen.setEnabled(True)
        self.ui.menuSave.setEnabled(False)
        self.ui.menuClose.setEnabled(True)
        self.ui.menuFile.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuTool.triggered[QAction].connect(self.onMenuTrigger)
        self.ui.menuSet.triggered[QAction].connect(self.onMenuTrigger)
        # tableview 设置
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([u'名称', u'说明'])
        self.ui.BbvInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.BbvInfo.setEditTriggers(QTableView.NoEditTriggers)
        self.ui.BbvInfo.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.BbvInfo.setModel(self.model)
        # 状态栏
        self.status = self.statusBar()
        self.status.showMessage(u'实时状态信息...')
        # other 设置
        self.ui.CbxValueMod.activated.connect(self.selectModChange)
        self.ui.CbxValueType.activated.connect(self.selectTypeChange)

        self.selected_item_text = ''
        self.ui.BtnReq.setChecked(True)
        self.selected_item = None

        self.value_types = ['int32', 'int64', 'string', 'float',
                            'double', 'bytes', 'bool', 'uint32', 'uint64']
        # 生成 proto文件和cpp文件
        self.module_mgr = ModuleMgr()
        self.gen_mgr = GenMgr()
        self.config = Config()
        self.openProto(self.config.getConfOne('msg_path'))
    pass

    def openProto(self, msg_path):
        if msg_path:
            self.module_mgr.loadXmls(msg_path)
            self.updateCbxValues()
            self.showModuleMsg()

    def updateCbxValues(self):
        modules = self.module_mgr.getPublicModules()
        if not modules:
            return
        self.ui.CbxValueMod.clear()
        for mod in modules:
            self.ui.CbxValueMod.addItem(mod.name)
        mod = modules[0]
        msg_names = mod.getMsgNames()
        value_types = self.value_types + msg_names
        self.ui.CbxValueType.addItems(value_types)

    def selectModChange(self):
        mod_name = self.ui.CbxValueMod.currentText()
        print(mod_name)
        mod = self.module_mgr.getModuleByName(mod_name)
        if not mod:
            return
        self.ui.CbxValueType.clear()
        msg_names = mod.getMsgNames()
        value_types = self.value_types + msg_names
        if self.selected_item_text in value_types:
            value_types.remove(self.selected_item_text)
        self.ui.CbxValueType.addItems(value_types)

    def selectTypeChange(self):
        pass
        # value_type = self.ui.CbxValueType.currentText()
        # if value_type in self.value_types:
        #     return
        # mod_name = self.ui.CbxValueMod.currentText()
        # mod = self.module_mgr.getModuleByName(mod_name)
        # if not mod:
        #     return
        # if mod.mod_type == 'public':
        #     self.proto_imp = mod.name

#########################右键菜单操作#########################
    def rightClickMenu(self, pos):
        try:
            self.contextMenu = QMenu(self.ui.WidMsgTree)  # 创建对象
            item = self.ui.WidMsgTree.itemAt(pos)
            addPublicModAct = None
            addModAct = None
            updateModAct = None
            delDodAct = None
            addMsgAct = None
            updateMsgAct = None
            delMsgAct = None
            addFieldAct = None
            updateFieldAct = None
            delFieldAct = None
            if not item:
                addPublicModAct = self.contextMenu.addAction(u'添加公共模块')  # 添加动作
                addPublicModAct.triggered.connect(
                    lambda: self.actionHandler('add_public_mod'))
                addModAct = self.contextMenu.addAction(u'添加客户端模块')  # 添加动作
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
                addFieldAct = self.contextMenu.addAction(u'添加字段')
                updateMsgAct.triggered.connect(
                    lambda: self.actionHandler('update_msg', item))
                delMsgAct.triggered.connect(
                    lambda: self.actionHandler('del_msg', item))
                addFieldAct.triggered.connect(
                    lambda: self.actionHandler('add_field', item))
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
        if not item and op_flag == 'add_public_mod':  # add mod
            is_ok, mod_name, mod_comment = ModGui.getModInfo(ModType.PUBLIC)
            if not is_ok or not mod_name:
                return
            self.addModule(mod_name, mod_comment, ModType.PUBLIC)
            self.setSaveOk()

        if not item and op_flag == 'add_mod':  # add mod
            is_ok, mod_name, mod_comment = ModGui.getModInfo(ModType.CLIENT)
            if not is_ok or not mod_name:
                return
            self.addModule(mod_name.title(), mod_comment, ModType.CLIENT)
            self.setSaveOk()

        if op_flag == 'update_mod':  # update mod
            is_ok, mod_name, mod_comment = ModGui.getModInfo(ModType.VOID)
            if not is_ok:
                return
            self.updateModule(item.text(2), mod_name.title(), mod_comment)
            self.setSaveOk()

        if op_flag == 'del_mod':  # del mod
            reply = QMessageBox.information(
                self, "warning", u"是否删除模块?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delModule(item.text(2))
            self.setSaveOk()

        if op_flag == 'add_msg':
            self.ui.FrameMsg.setEnabled(True)
            self.ui.BtnAdd.setEnabled(True)
            self.ui.BtnSave.setEnabled(False)
            self.ui.menuSave.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(False)

        if op_flag == 'update_msg':
            self.ui.FrameMsg.setEnabled(True)
            self.ui.FrameField.setEnabled(False)
            self.ui.BtnUpdate.setEnabled(True)
            self.ui.BtnAdd.setEnabled(False)
            msg_type = self.getMsgTypeByItemName(item.text(0))
            if msg_type == MsgType.REQ:
                self.ui.BtnReq.setChecked(True)
            else:
                self.ui.BtnNotify.setChecked(True)

        if op_flag == 'del_msg':
            self.delMsg()
            self.setSaveOk()

        if op_flag == 'add_field':
            self.ui.BtnAdd.setEnabled(True)
            self.ui.FrameField.setEnabled(True)

        if op_flag == 'update_field':
            self.ui.FrameField.setEnabled(True)
            self.ui.BtnUpdate.setEnabled(True)

        if op_flag == 'del_field':
            self.delField()
            self.setSaveOk()

    def setSaveOk(self):
        self.ui.BtnSave.setEnabled(True)
        self.ui.menuSave.setEnabled(True)
        self.showModuleMsg()

####################增删改查操作##############################

    def addModule(self, mod_name, mod_comment, mod_type):
        module = None
        if mod_type == ModType.PUBLIC:
            module = ModulePublic()
        else:
            module = ModuleMsg()
        module.id = self.module_mgr.getNextModId(module.mod_type)
        module.name = mod_name  # 首字母大写
        module.comment = mod_comment or ""
        print('module id===', module.id)
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
        self.clearModel()
        pass

    def addMsg(self):
        msg_name = self.ui.LetMsgName.text().strip()
        if msg_name == '':
            return
        mod_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(mod_id)
        if not module:
            return
        if module.mod_type == ModType.CLIENT:
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
        else:
            public_msg = MsgPublic(mod_id)
            public_msg.id = module.getNextMsgId()
            public_msg.name = msg_name
            public_msg.comment = self.ui.LetMsgCmt.text().strip()
            module.addMsg(public_msg, MsgType.PUBLIC)

    def updateMsg(self):
        msg_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(self.selected_item.parent().text(2))
        if not module:
            return
        msg_type = self.getMsgTypeByItemName(self.selected_item_text)
        msg_name = self.ui.LetMsgName.text().strip()
        msg_comment = self.ui.LetMsgCmt.text().strip()
        module.updateMsg(msg_id, msg_type, msg_name, msg_comment)

    def delMsg(self):
        msg_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(self.selected_item.parent().text(2))
        if not module:
            return
        msg_type = self.getMsgTypeByItemName(self.selected_item_text)
        module.delMsg(msg_id, msg_type)
        self.clearModel()
        pass

    def addField(self):
        msg_id = self.selected_item.text(2)
        module = self.module_mgr.getModule(self.selected_item.parent().text(2))
        msg_type = self.getMsgTypeByItemName(self.selected_item_text)
        msg = module.getMsg(msg_id, msg_type)
        if not msg:
            return
        field_name = self.ui.LetFieldName.text().strip() or ''
        field_comment = self.ui.LetFieldCmt.text().strip() or ''
        if not field_name:
            return
        field = Field()
        field.field_name = field_name
        field.comment = field_comment
        field.proto_type = self.ui.CbxProtoType.currentText()
        if field.proto_type == 'optional':
            field.proto_type = ''
        field.value_type = self.ui.CbxValueType.currentText()
        msg.addField(field)
        pass

    def updateField(self):
        msg = self.getMsgByFieldItem(self.selected_item)
        if not msg:
            return
        field = msg.getFieldByName(self.selected_item_text)
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
        msg.delField(self.selected_item_text)
        self.clearModel()
        pass

##################菜单操作###############################
    def onMenuTrigger(self, menu):
        if menu == self.ui.menuOpen:
            self.menuBarOpen()
        if menu == self.ui.menuSave:
            self.menuBarSave()
        if menu == self.ui.menuClose:
            self.menuBarClose()
        if menu == self.ui.menuProto:
            self.menuBarProto()
        if menu == self.ui.menuTable:
            self.menuBarTable()
        if menu == self.ui.menuServer:
            self.menuBarServer()
        if menu == self.ui.menuClient:
            self.menuBarClient()
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
        self.openProto(msg_path)
        pass

    def menuBarSave(self):
        self.saveProtoXml()
        pass

    def menuBarClose(self):
        os._exit(0)
        pass

    # 导出proto文件
    def menuBarProto(self):
        try:
            self.saveProtoXml()
            # 生成proto文件
            self.status.showMessage(u'开始生成protobuffer')
            xml_dir = self.config.getConfOne('msg_path')
            self.gen_mgr.loadXmls(xml_dir)
            save_proto_dir = self.config.getConfOne('proto_path')
            self.gen_mgr.genProto(save_proto_dir)
            # 生成protobuffer 代码
            proto_gen_dir = self.config.getConfOne('proto_gen_path')
            if not os.path.exists(proto_gen_dir):
                QMessageBox.warning(self, u"警告", u"请重新设置路径", QMessageBox.Yes)
                return
            for proto in os.listdir(save_proto_dir):
                if proto.endswith('.proto'):
                    proto_name = proto[:-6]
                    protobuf_dir = proto_gen_dir+'/' + proto_name
                    if not os.path.exists(protobuf_dir):
                        os.makedirs(protobuf_dir)
                    cmd_cpp_str = 'protoc -I='+save_proto_dir+' --proto_path=' + \
                        save_proto_dir+' --cpp_out='+protobuf_dir+'  ' + proto
                    cmd_csharp_str = 'protoc -I='+save_proto_dir+' --proto_path=' + \
                        save_proto_dir+' --csharp_out='+protobuf_dir+'  ' + proto
                    self.status.showMessage(u'正在生成('+proto_name+')'+'消息协议')
                    run(cmd_cpp_str, shell=True)
                    run(cmd_csharp_str, shell=True)

            self.status.showMessage(u'消息协议生成完成')
        except Exception as e:
            print(e)
    # 导出数据表

    def menuBarTable(self):
        pass

    # 生成服务器代码
    def menuBarServer(self):
        self.gen_mgr.loadXmls(self.config.getConfOne('msg_path'))
        self.gen_mgr.genCpp(self.config.getConfOne('proto_path'))
        pass

    # 生成客户端代码
    def menuBarClient(self):
        # 生成 csharp 协议枚举文件
        self.gen_mgr.loadXmls(self.config.getConfOne('msg_path'))
        self.gen_mgr.genCsharp(self.config.getConfOne('proto_path'))
        pass

###################################################

    def showModuleMsg(self):
        self.ui.WidMsgTree.clear()
        if not self.module_mgr.module_dic:
            return
        item_proto_root = QTreeWidgetItem(self.ui.WidMsgTree)
        item_proto_root.setText(0, 'Protocol')
        item_proto_root.setText(1, u'通信协议')
        item_proto_root.setIcon(0, QIcon('./icons/Montreal.ico'))
        for _, module in self.module_mgr.module_dic.items():
            QApplication.processEvents()
            item_module = None
            if module.mod_type == ModType.PUBLIC:
                # add module
                item_module = QTreeWidgetItem(self.ui.WidMsgTree)
                item_module.setIcon(0, QIcon('./icons/Montreal.ico'))
            else:
                item_module = QTreeWidgetItem()
                item_proto_root.addChild(item_module)
                item_module.setIcon(0, QIcon('./icons/Milwaukee.ico'))
            item_module.setText(0, module.name)
            item_module.setText(1, module.comment)
            item_module.setText(2, module.id)
            item_module.setText(3, ItemType.MODULE)

            for msg_id, msg in module.public_msg_dic.items():
                item_msg = QTreeWidgetItem()
                item_module.addChild(item_msg)
                item_msg.setText(0, msg.name)
                item_msg.setText(1, msg.comment)
                item_msg.setText(2, msg.id)
                item_msg.setText(3, ItemType.MSG)
                item_msg.setIcon(0, QIcon('./icons/Toronto.ico'))
                # add field
                for field in msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, msg.id)
                    item_field.setText(3, ItemType.FIELD)
                    item_field.setIcon(0, QIcon('./icons/Tampa Bay.ico'))

            # add msg
            for msg_id, req_msg in module.req_msg_dic.items():
                # add req
                item_req_msg = QTreeWidgetItem()
                item_module.addChild(item_req_msg)
                item_req_msg.setText(0, req_msg.name)
                item_req_msg.setText(1, req_msg.comment)
                item_req_msg.setText(2, req_msg.id)
                item_req_msg.setText(3, ItemType.MSG)
                item_req_msg.setIcon(0, QIcon('./icons/Cleveland.ico'))
                for field in req_msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_req_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, req_msg.id)
                    item_field.setText(3, ItemType.FIELD)
                    item_field.setIcon(0, QIcon('./icons/Tampa Bay.ico'))
                # add reply
                reply_msg = module.reply_msg_dic[msg_id]
                item_reply_msg = QTreeWidgetItem()
                item_module.addChild(item_reply_msg)
                item_reply_msg.setText(0, reply_msg.name)
                item_reply_msg.setText(1, reply_msg.comment)
                item_reply_msg.setText(2, reply_msg.id)
                item_reply_msg.setText(3, ItemType.MSG)
                item_reply_msg.setIcon(0, QIcon('./icons/Cleveland.ico'))
                for field in reply_msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_reply_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, reply_msg.id)
                    item_field.setText(3, ItemType.FIELD)
                    item_field.setIcon(0, QIcon('./icons/Tampa Bay.ico'))

            for msg_id, msg in module.notify_msg_dic.items():
                item_msg = QTreeWidgetItem()
                item_module.addChild(item_msg)
                item_msg.setText(0, msg.name)
                item_msg.setText(1, msg.comment)
                item_msg.setText(2, msg.id)
                item_msg.setText(3, ItemType.MSG)
                item_msg.setIcon(0, QIcon('./icons/New York.ico'))
                # add field
                for field in msg.field_list:
                    item_field = QTreeWidgetItem()
                    item_msg.addChild(item_field)
                    item_field.setText(0, field.field_name)
                    item_field.setText(1, field.comment)
                    item_field.setText(2, msg.id)
                    item_field.setText(3, ItemType.FIELD)
                    item_field.setIcon(0, QIcon('./icons/Tampa Bay.ico'))

            # self.ui.WidMsgTree.expandToDepth(1)

    def getModBySelectedItem(self):
        mod_id = None
        if self.selected_item.text(3) == ItemType.FIELD:
            mod_id = self.selected_item.parent().parent().text(2)
        elif self.selected_item.text(3) == ItemType.MSG:
            mod_id = self.selected_item.parent().text(2)
        else:
            mod_id = self.selected_item.text(2)
        mod = self.module_mgr.getModule(mod_id)
        return mod

    def onTreeItemClicked(self, idx):
        self.selected_item = self.ui.WidMsgTree.currentItem()
        self.showItemDetail(self.selected_item)
        self.selected_item_text = self.selected_item.text(0)

        mod = self.getModBySelectedItem()
        if mod and mod.mod_type == ModType.PUBLIC:
            self.ui.CbxValueMod.setEnabled(False)
        else:
            self.ui.CbxValueMod.setEnabled(True)
        # clear edit
        self.ui.LetMsgName.clear()
        self.ui.LetMsgCmt.clear()
        self.ui.LetFieldName.clear()
        self.ui.LetFieldCmt.clear()

        self.ui.CbxValueType.clear()
        self.ui.CbxValueType.addItems(self.value_types)

    def saveProtoXml(self):
        self.module_mgr.saveXmls(self.config.getConfOne('msg_path'))
        self.ui.BtnSave.setEnabled(False)
        self.ui.menuSave.setEnabled(False)
        self.clearTreeWidgetSelect()
        self.status.showMessage(u'保存信息完成')

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
        else:
            return MsgType.PUBLIC

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
                self.saveProtoXml()
                return
            if not self.selected_item:
                return
            item_type = self.selected_item.text(3)
            if btn == 'add':
                if item_type == ItemType.MODULE:
                    self.addMsg()
                else:
                    self.addField()
                self.ui.FrameMsg.setEnabled(False)
                self.ui.FrameField.setEnabled(False)

            if btn == 'update':
                if item_type == ItemType.MSG:
                    self.updateMsg()
                else:
                    self.updateField()
                self.ui.FrameField.setEnabled(False)

            self.ui.BtnSave.setEnabled(True)
            self.ui.menuSave.setEnabled(True)
            self.showModuleMsg()
        except Exception as e:
            with open('proto_log', 'a+') as f:
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(now, e, file=f)

    def clearModel(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels([u'名称', u'说明'])

    def showItemDetail(self, item):
        if not item or item.text(0) == 'Proto':
            return
        self.clearModel()
        item_type = item.text(3)
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
