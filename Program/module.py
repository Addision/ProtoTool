# -*-coding:utf-8-*-

import os
import sys
import codecs
import copy
import xml.etree.ElementTree as ET

from item_data import *
from msg import *


class Module(object):
    def __init__(self):
        super(Module, self).__init__()
        self.xml_file =""  # 模块保存的xml 文件
        self.id = 10   # 模块id 从11开始
        self.name = ""
        self.comment = ""
        self.proto_imp = ""
        self.item_type = ItemType.MODULE
        self.msg_list = []
        self.msg_next_id = 0

    def __loadXml(self):
        contents = ""
        with codecs.open(self.xml_file, "r", "utf-8") as f:
            contents = f.read()
        if contents == "":
            return False
        self.root = ET.fromstring(contents)
        if self.root:
            self.id = int(self.root.attrib['id'])
            self.name = self.root.attrib['name']
            self.comment = self.root.attrib['comment']
            self.proto_imp = self.root[0].text
            return True
        return False

    def parseXml(self, xml_file):
        self.xml_file = xml_file
        if not self.__loadXml():
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

    def writeField(self, field, field_list):
        for field_dic in field_list:
            field.attrib['proto_type'] = field_dic['proto_type']
            field.attrib['value_type'] = field_dic['value_type']
            field.attrib['field_name'] = field_dic['field_name']
            field.attrib['tag'] = field_dic['tag']
            field.attrib['comment'] = field_dic['comment']
        pass

    def writeXml(self, xml_file):
        # 如果已有删除，重新生成新xml文件 TODO 优化直接更改xml文件内容
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
                self.writeField(field, msg.req_list)
                # 创建应答
                reply_msg = ET.SubElement(req_reply_msg, 'Reply')
                field = ET.SubElement(reply_msg, 'field')
                self.writeField(field, msg.reply_list)
            else:
                # 创建广播消息
                notify_msg = ET.SubElement(message, 'NotifyMsg')
                notify = ET.SubElement(notify_msg, "Notify")
                notify.attrib['id'] = msg.id
                notify.attrib['name'] = msg.name
                notify.attrib['comment'] = msg.comment
                field = ET.SubElement(notify, 'field')
                self.writeField(field, msg.notify_list)
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
            if msg.id == id:
                self.msg_list.remove(msg)



