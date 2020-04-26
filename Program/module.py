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
                req_msg_dic = {}
                req_msg_dic['proto_type'] = req.attrib['proto_type']
                req_msg_dic['value_type'] = req.attrib['value_type']
                req_msg_dic['field_name'] = req.attrib['field_name']
                req_msg_dic['comment'] = req.attrib['comment']
                req_msg_dic['tag'] = req.attrib['tag']
                req_msg_dic['id'] = proto_msg.id
                proto_msg.req_list.append(req_msg_dic)

            for reply in reply_msg:
                reply_msg_dic = {}
                reply_msg_dic['proto_type'] = reply.attrib['proto_type']
                reply_msg_dic['value_type'] = reply.attrib['value_type']
                reply_msg_dic['field_name'] = reply.attrib['field_name']
                reply_msg_dic['tag'] = reply.attrib['tag']
                reply_msg_dic['comment'] = reply.attrib['comment']
                reply_msg_dic['id'] = proto_msg.id
                proto_msg.reply_list.append(reply_msg_dic)
            self.msg_list.append(proto_msg)
            if self.msg_next_id < int(proto_msg.id):
                self.msg_next_id = int(proto_msg.id)


        for notify in self.root.findall("Message/NotifyMsg/Notify"):
            proto_msg = Msg(self.id)
            proto_msg.id = int(notify.attrib['id'])
            proto_msg.name = notify.attrib['name']
            proto_msg.comment = notify.attrib['comment']
            proto_msg.type = "NotifyMsg"
            for field in notify:
                notify_msg_dic = {}
                notify_msg_dic['proto_type'] = field.attrib['proto_type']
                notify_msg_dic['value_type'] = field.attrib['value_type']
                notify_msg_dic['field_name'] = field.attrib['field_name']
                notify_msg_dic['tag'] = field.attrib['tag']
                notify_msg_dic['comment'] = field.attrib['comment']
                notify_msg_dic['id'] = proto_msg.id
                proto_msg.notify_list.append(notify_msg_dic)
            self.msg_list.append(proto_msg)
            if self.msg_next_id < int(proto_msg.id):
                self.msg_next_id = int(proto_msg.id)
        self.msg_next_id = self.msg_next_id + 1
        return True

    def addMsg(self, msg):
        self.msg_list.append(msg)
    
    def getMsg(self, msg_id):
        for msg in self.msg_list:
            if msg.id == msg_id:
                return msg

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
                field.attrib['proto_type'] = msg.req_dic['proto_type']
                field.attrib['value_type'] = msg.req_dic['value_type']
                field.attrib['field_name'] = msg.req_dic['field_name']
                field.attrib['tag'] = msg.req_dic['tag']
                field.attrib['comment'] = msg.req_dic['comment']
                # 创建应答
                reply_msg = ET.SubElement(req_reply_msg, 'Reply')
                field = ET.SubElement(reply_msg, 'field')
                field.attrib['proto_type'] = msg.reply_dic['proto_type']
                field.attrib['value_type'] = msg.reply_dic['value_type']
                field.attrib['field_name'] = msg.reply_dic['field_name']
                field.attrib['tag'] = msg.reply_dic['tag']
                field.attrib['comment'] = msg.reply_dic['comment']
            else:
                # 创建广播消息
                notify_msg = ET.SubElement(message, 'NotifyMsg')
                notify = ET.SubElement(notify_msg, "Notify")
                notify.attrib['id'] = msg.id
                notify.attrib['name'] = msg.name
                notify.attrib['comment'] = msg.comment  
                field = ET.SubElement(notify, 'field')
                field.attrib['proto_type'] = msg.notify_dic['proto_type']
                field.attrib['value_type'] = msg.notify_dic['value_type']
                field.attrib['field_name'] = msg.notify_dic['field_name']
                field.attrib['tag'] = msg.notify_dic['tag']   
                field.attrib['comment'] = msg.notify_dic['comment']                          
            pass

        # 将 xml tree 写入文件
        tree = ET.ElementTree(root)    
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    def nextMsgId(self):
        return self.msg_next_id



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
    
    def writeXmls(self, xml_dir, modules):
        for module in modules:
            xml_file = xml_dir + "/Module" + module.name+".xml"
            if os.path.exists(xml_file):
                os.remove(xml_file)
            module.writeXml(xml_file)

    def getModule(self, id):
        id = int(id)
        return self.modules[id]

    def nextModId(self):
        return self.mod_next_id

    def addModule(self, module):
        id = int(module.id)
        if self.modules[id]:
            return
        self.modules[id] = module

if __name__ == "__main__":
    module = Module()
    module.parseXml('C:/ProtoTool/Program/protoxml/ModuleChat.xml')
    # module.writeXml('C:/ProtoTool/Program/protoxml/ModuleChat2.xml')
    pass
    