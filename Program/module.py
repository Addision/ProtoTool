# -*-coding:utf-8-*-

import os
import sys
import codecs
import copy
import xml.etree.ElementTree as ET
from msg import *
from common import *


class ModuleBase(object):
    def __init__(self):
        super(ModuleBase, self).__init__()
        self.xml_file = ""  # 模块保存的xml文件
        self.id = "1"     # 公共模块从1-9  协议模块从11开始
        self.name = ""
        self.comment = ""

        self.req_msg_dic = {}
        self.reply_msg_dic = {}
        self.notify_msg_dic = {}
        self.public_msg_dic = {}
        self.msg_next_id = "1"


    def getNextMsgId(self):
        msg_id = int(self.msg_next_id)
        str_msg_id = ""
        if msg_id > 0 and msg_id < 10:
            str_msg_id = self.id + "0" + str(msg_id)
        else:
            str_msg_id = self.id + str(msg_id)
        self.msg_next_id = str(int(self.msg_next_id)+1)
        return str_msg_id

    def getMsgList(self, msg_type):
        if msg_type == MsgType.REQ:
            return self.req_msg_dic
        if msg_type == MsgType.REPLY:
            return self.reply_msg_dic
        if msg_type == MsgType.NOTIFY:
            return self.notify_msg_dic
        if msg_type == MsgType.PUBLIC:
            return self.public_msg_dic

    def existMsg(self, msg_id, msg_type):
        msg_list = self.getMsgList(msg_type)
        if not msg_list:
            return False, None
        if msg_id in msg_list.keys():
            return True, msg_list[msg_id]
        return False, None

    def addMsg(self, msg, msg_type):
        is_exist, _ = self.existMsg(msg.id, msg_type)
        if not is_exist:
            msg_list = self.getMsgList(msg_type)
            msg_list[msg.id] = msg

    def getMsg(self, msg_id, msg_type):
        is_exist, msg = self.existMsg(msg_id, msg_type)
        if is_exist:
            return msg
        return None

    def delMsg(self, msg_id, msg_type):
        is_exist, _ = self.existMsg(msg_id, msg_type)
        if is_exist:
            if msg_type == MsgType.NOTIFY:
                self.notify_msg_dic.pop(msg_id)
            elif msg_type == MsgType.PUBLIC:
                self.public_msg_dic.pop(msg_id)
            else:
                self.req_msg_dic.pop(msg_id)
                self.reply_msg_dic.pop(msg_id)

    def updateMsg(self, msg_id, msg_type, msg_name='', msg_comment=''):
        if msg_type == MsgType.NOTIFY or msg_type == MsgType.PUBLIC:
            msg = self.getMsg(msg_id, msg_type)
            if not msg:
                return            
            if msg_name:
                msg.name = msg_name
            if msg_comment:
                msg.comment = msg_comment            
            pass
        else:
            msg_req = self.getMsg(msg_id, MsgType.REQ)
            msg_reply = self.getMsg(msg_id, MsgType.REPLY)
            if not msg_req or not msg_reply:
                return
            if msg_name:
                msg_req.name = msg_name+'Req'
                msg_reply.name = msg_name+'Reply'
            if msg_comment:
                msg_req.comment = msg_comment                
                msg_reply.comment = msg_name
            pass        


    def assignField(self, attrib):
        if not attrib:
            return
        field = Field()
        field.proto_type = attrib['proto_type']
        field.value_type = attrib['value_type']
        field.field_name = attrib['field_name']
        field.tag = attrib['tag']
        field.comment = attrib['comment']
        return field

    def writeField(self, xml_req_reply, field_list):
        for field in field_list:
            xml_field = ET.SubElement(xml_req_reply, 'field')
            xml_field.attrib['proto_type'] = field.proto_type
            xml_field.attrib['value_type'] = field.value_type
            xml_field.attrib['field_name'] = field.field_name
            xml_field.attrib['tag'] = field.tag
            xml_field.attrib['comment'] = field.comment
        pass


class ModuleMsg(ModuleBase):
    def __init__(self):
        super(ModuleMsg, self).__init__()
        self.proto_imp = ""  # 模块引用的文件
        self.mod_type = ModType.CLIENT
        self.id = "11"

    def readXml(self):
        try:
            contents = ""
            with codecs.open(self.xml_file, "r", "utf-8") as f:
                contents = f.read()
            if contents == "":
                return False, None
            root = ET.fromstring(contents)
            if root:
                self.id = root.attrib['id']
                self.name = root.attrib['name']
                self.comment = root.attrib['comment']
                self.proto_imp = root[0].text
                return True, root
            return False, None
        except Exception as e:
            print(e)

    def loadXml(self, xml_file):
        if not (xml_file and os.path.isfile(xml_file)):
            return False
        self.xml_file = xml_file
        read_ok, root = self.readXml()
        if not read_ok:
            return False

        for req_reply in root.findall("Message/ReqReplyMsg"):
            req_msg = MsgReq(self.id)
            req_msg.id = req_reply.attrib['id']
            req_msg.name = req_reply.attrib['name'] + 'Req'
            req_msg.comment = req_reply.attrib['comment']

            reply_msg = MsgReply(self.id)
            reply_msg.id = req_reply.attrib['id']
            reply_msg.name = req_reply.attrib['name'] + 'Reply'
            reply_msg.comment = req_reply.attrib['comment']

            # add field
            xml_req = req_reply[0]
            xml_reply = req_reply[1]
            for req in xml_req:
                field = self.assignField(req.attrib)
                if field:
                    req_msg.addField(field)
            for reply in xml_reply:
                field = self.assignField(reply.attrib)
                if field:
                    reply_msg.addField(field)

            self.req_msg_dic[req_msg.id] = req_msg
            self.reply_msg_dic[reply_msg.id] = reply_msg

        for notifys in root.findall("Message/NotifyMsg/Notify"):
            notify_msg = MsgNotify(self.id)
            notify_msg.id = notifys.attrib['id']
            notify_msg.name = notifys.attrib['name'] + 'Notify'
            notify_msg.comment = notifys.attrib['comment']

            for notify in notifys:
                field = self.assignField(notify.attrib)
                if field:
                    notify_msg.addField(field)
            self.notify_msg_dic[notify_msg.id] = notify_msg

        return True

    def saveXml(self, xml_file):
        if self.xml_file and self.xml_file != xml_file:
            self.xml_file = xml_file
        else:
            self.xml_file = xml_file

        root = ET.Element('Module')
        root.attrib['id'] = self.id
        root.attrib['name'] = self.name
        root.attrib['comment'] = self.comment
        proto_imp = ET.SubElement(root, 'Import')
        proto_imp.text = self.proto_imp
        xml_msg = ET.SubElement(root, 'Message')

        if self.req_msg_dic:
            for id, req_msg in self.req_msg_dic.items():
                xml_req_reply = ET.SubElement(xml_msg, 'ReqReplyMsg')
                xml_req_reply.attrib['id'] = req_msg.id
                xml_req_reply.attrib['name'] = req_msg.name[:-3]
                xml_req_reply.attrib['comment'] = req_msg.comment
                # 创建请求
                xml_req = ET.SubElement(xml_req_reply, 'Req')
                self.writeField(xml_req, req_msg.field_list)
                # 创建应答
                reply_msg = self.reply_msg_dic[id]
                xml_reply = ET.SubElement(xml_req_reply, 'Reply')
                self.writeField(xml_reply, reply_msg.field_list)
                pass

        if self.notify_msg_dic:
            xml_notify_msg = ET.SubElement(xml_msg, 'NotifyMsg')
            for id, msg in self.notify_msg_dic.items():
                xml_notify = ET.SubElement(xml_notify_msg, "Notify")
                xml_notify.attrib['id'] = msg.id
                xml_notify.attrib['name'] = msg.name[:-6]
                xml_notify.attrib['comment'] = msg.comment
                self.writeField(xml_notify, msg.field_list)

        # 将 xml tree 写入文件
        tree = ET.ElementTree(root)
        tree.write(self.xml_file, encoding='utf-8', xml_declaration=True)


class ModulePublic(ModuleBase):
    def __init__(self):
        super(ModulePublic, self).__init__()
        self.mod_type = ModType.PUBLIC
        self.id = "1"

    def getMsgNames(self):
        msg_names = []
        for msg_id, msg in self.public_msg_dic.items():
            msg_names.append(msg.name)
        return msg_names

    def readXml(self):
        try:
            contents = ""
            with codecs.open(self.xml_file, "r", "utf-8") as f:
                contents = f.read()
            if contents == "":
                return False, None
            root = ET.fromstring(contents)
            if root:
                self.id = root.attrib['id']
                self.name = root.attrib['name']
                self.comment = root.attrib['comment']
                return True, root
            return False, None
        except Exception as e:
            print(e)

    def loadXml(self, xml_file):
        if not (xml_file and os.path.isfile(xml_file)):
            return False
        self.xml_file = xml_file
        read_ok, root = self.readXml()
        if not read_ok:
            return False

        for publics in root.findall("Message/PublicMsg/Public"):
            public_msg = MsgPublic(self.id)
            public_msg.id = publics.attrib['id']
            public_msg.name = publics.attrib['name']
            public_msg.comment = publics.attrib['comment']

            for public in publics:
                field = self.assignField(public.attrib)
                if field:
                    public_msg.addField(field)
            self.public_msg_dic[public_msg.id] = public_msg

        return True

    def saveXml(self, xml_file):
        if self.xml_file and self.xml_file != xml_file:
            self.xml_file = xml_file
        else:
            self.xml_file = xml_file

        root = ET.Element('Module')
        root.attrib['id'] = self.id
        root.attrib['name'] = self.name
        root.attrib['comment'] = self.comment
        xml_msg = ET.SubElement(root, 'Message')
        xml_public_msg = ET.SubElement(xml_msg, 'PublicMsg')
        for id, msg in self.public_msg_dic.items():
            xml_public = ET.SubElement(xml_public_msg, "Public")
            xml_public.attrib['id'] = msg.id
            xml_public.attrib['name'] = msg.name
            xml_public.attrib['comment'] = msg.comment
            self.writeField(xml_public, msg.field_list)

        # 将 xml tree 写入文件
        tree = ET.ElementTree(root)
        tree.write(self.xml_file, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    module = ModuleMsg()
    module.loadXml('D:/ProtoTool/Program/xml_files/ModuleChat.xml')
    module.saveXml('D:/ProtoTool/Program/xml_files/ModuleChat2.xml')
