'''
@Author: jia.lai
@Date: 2020-04-24 09:41:30
@LastEditors: jia.lai
@LastEditTime: 2020-04-24 11:02:28
@Description: 处理消息模块
'''
# -*-coding:utf-8-*-

import os
import sys
import codecs
import copy
import xml.etree.ElementTree as ET

from item_data import *


class Msg(object):
    def __init__(self, mod_id):
        super(Msg, self).__init__()
        self.mod_id = mod_id
        self.id = 0
        self.name = ""
        self.comment = ""
        self.type = ""
        self.item_type = ItemType.MSG
        # 保存属性值
        self.req_list = []
        self.reply_list = []
        self.notify_list = []

    def getField(self, name, field_flag):
        if field_flag == 'req':
            for field in self.req_list:
                if field['field_name'] == name:
                    return field
        if field_flag == 'reply':
            for field in self.reply_list:
                if field['field_name'] == name:
                    return field
        if field_flag == 'notify':
            for field in self.notify_list:
                if field['field_name'] == name:
                    return field
        pass

    def findField(self, field_name, field_flag):
        field = None
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    field = item
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    field = item
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    field = item
        return field


    def addField(self, field, field_flag):
        field['id'] = self.id
        if field_flag == 'req':
            self.req_list.append(field)
        if field_flag == 'reply':
            self.reply_list.append(field)
        if field_flag == 'notify':
            self.notify_list.append(field)
    
    def delField(self, field_name, field_flag):
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    self.req_list.remove(item)
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    self.reply_list.remove(item)
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    self.notify_list.remove(item)
    
    def updateField(self, field_name, field):
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    self.req_list.remove(item)
                    self.req_list.append(field)
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    self.reply_list.remove(item)
                    self.reply_list.append(field)
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    self.notify_list.remove(item)   
                    self.notify_list.append(field)     
        pass


    def getNextTag(self, field_flag):
        tag = 0
        if field_flag == "req":
            for field in self.req_list:
                if int(field['tag']) > tag:
                    tag = int(field['tag'])
        if field_flag == "reply":
            for field in self.reply_list:
                if int(field['tag'] > tag):
                    tag = int(field['tag'])
        if field_flag == 'notify':
            for field in self.notify_list:
                if int(field['tag'] > tag):
                    tag = int(field['tag'])
        return tag
    
    def updateMsg(self, msg_name, msg_comment):
        self.name = msg_name
        self.comment = msg_comment


class Module(object):
    def __init__(self):
        super(Module, self).__init__()
        self.id = 0
        self.name = ""
        self.comment = ""
        self.proto_imp = ""
        self.item_type = ItemType.MODULE
        self.msg_list = []
        self.msg_next_id = 0

    def __loadXml(self, xml_file):
        contents = ""
        with codecs.open(xml_file, "r", "utf-8") as f:
            contents = f.read()
        if contents == "":
            return
        self.root = ET.fromstring(contents)
        if self.root:
            self.id = int(self.root.attrib['id'])
            self.name = self.root.attrib['name']
            self.comment = self.root.attrib['comment']
            self.proto_imp = self.root[0].text
            return True
        return False

    def parseXml(self, xml_file):
        if not self.__loadXml(xml_file):
            return False

        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            proto_msg = Msg(self.id)
            proto_msg.id = int(req_reply.attrib['id'])
            proto_msg.name = req_reply.attrib['name']
            proto_msg.comment = req_reply.attrib['comment']
            proto_msg.type = "ReqReplyMsg"
            req_msg = req_reply[0]
            reply_msg = req_reply[1]
            for req in req_msg:
                proto_msg.addField(req.attrib, 'req')

            for reply in reply_msg:
                proto_msg.addField(reply.attrib, 'reply')
            self.msg_list.append(proto_msg)
            if self.msg_next_id < int(proto_msg.id):
                self.msg_next_id = int(proto_msg.id)

        for notifys in self.root.findall("Message/NotifyMsg/Notify"):
            proto_msg = Msg(self.id)
            proto_msg.id = int(notifys.attrib['id'])
            proto_msg.name = notifys.attrib['name']
            proto_msg.comment = notifys.attrib['comment']
            proto_msg.type = "NotifyMsg"
            for notify in notifys:
                proto_msg.addField(notify.attrib, 'notify')
            self.msg_list.append(proto_msg)
            if self.msg_next_id < int(proto_msg.id):
                self.msg_next_id = int(proto_msg.id)
        self.msg_next_id = self.msg_next_id + 1
        return True

    def addMsg(self, msg):
        self.msg_list.append(msg)

    def getMsg(self, msg_id):
        id = int(msg_id)
        for msg in self.msg_list:
            if msg.id == id:
                return msg

    def writeField(self, field, field_dic):
        field.attrib['proto_type'] = field_dic['proto_type']
        field.attrib['value_type'] = field_dic['value_type']
        field.attrib['field_name'] = field_dic['field_name']
        field.attrib['tag'] = field_dic['tag']
        field.attrib['comment'] = field_dic['comment']
        pass

    def writeXml(self, xml_file):
        # 如果已有删除，重新生成新xml文件 TODO 优化直接更改xml文件内容
        if os.path.exists(xml_file):
            os.remove(xml_file)
        root = ET.Element('Module')
        root.attrib['id'] = str(self.id)
        root.attrib['name'] = self.name
        root.attrib['comment'] = self.comment
        proto_imp = ET.SubElement(root, 'Import')
        proto_imp.text = self.proto_imp
        message = ET.SubElement(root, 'Message')
        for msg in self.msg_list:
            if msg.type == "ReqReplyMsg":
                req_reply_msg = ET.SubElement(message, 'ReqReplyMsg')
                req_reply_msg.attrib['id'] = str(msg.id)
                req_reply_msg.attrib['name'] = msg.name
                req_reply_msg.attrib['comment'] = msg.comment
                # 创建请求
                req_msg = ET.SubElement(req_reply_msg, 'Req')
                field = ET.SubElement(req_msg, 'field')
                self.writeField(field, msg.req_dic)
                # 创建应答
                reply_msg = ET.SubElement(req_reply_msg, 'Reply')
                field = ET.SubElement(reply_msg, 'field')
                self.writeField(field, msg.reply_dic)
            else:
                # 创建广播消息
                notify_msg = ET.SubElement(message, 'NotifyMsg')
                notify = ET.SubElement(notify_msg, "Notify")
                notify.attrib['id'] = msg.id
                notify.attrib['name'] = msg.name
                notify.attrib['comment'] = msg.comment
                field = ET.SubElement(notify, 'field')
                self.writeField(field, msg.notify_dic)
            pass

        # 将 xml tree 写入文件
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    def nextMsgId(self):
        next_id = self.msg_next_id
        self.msg_next_id += 1
        return next_id

    def update(self, name, comment):
        if name == "":
            return
        self.name = name
        self.comment = comment
    
    def delMsg(self, msg_id):
        id = int(msg_id)
        for msg in self.msg_list:
            if msg.id == msg_id:
                self.msg_list.remove(msg)
    


class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr, self).__init__()
        self.modules = {}
        self.mod_next_id = 0

    def loadXmls(self, xml_dir):
        if not os.path.exists(xml_dir):
            return False
        listFiles = os.listdir(xml_dir)
        if not listFiles:
            return False
        mod_id = 0
        for file in listFiles:
            if not file.endswith("xml", 3):
                continue
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            module = Module()
            module.parseXml(xml_file)
            self.modules[module.id] = module
            if int(module.id) > mod_id:
                mod_id = int(module.id)

        self.mod_next_id = mod_id + 1

    def writeXmls(self, xml_dir):
        for _, module in self.modules.items():
            xml_file = xml_dir + "/Module" + module.name+".xml"
            if os.path.exists(xml_file):
                os.remove(xml_file)
            module.writeXml(xml_file)

    def getModule(self, id):
        id = int(id)
        return self.modules[id]

    def getMsg(self, mod_id, msg_id):
        mod = self.getModule(mod_id)
        if not mod:
            return
        msg = mod.getMsg(msg_id)
        return msg

    def nextModId(self):
        next_id = self.mod_next_id
        self.mod_next_id = self.mod_next_id + 1
        return next_id

    def addModule(self, module):
        id = int(module.id)
        if id in self.modules.keys():
            return
        self.modules[id] = module

    def delModule(self, mod_id):
        id = int(mod_id)
        if not self.modules[id]:
            return
        self.modules.pop(id)


if __name__ == "__main__":
    module = Module()
    module.parseXml('C:/ProtoTool/Program/protoxml/ModuleChat.xml')
    # module.writeXml('C:/ProtoTool/Program/protoxml/ModuleChat2.xml')
    pass
