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


class Msg(object):
    def __init__(self):
        super(Msg, self).__init__()
        self.id = 0
        self.name = ""
        self.comment = ""
        self.type = ""
        # 保存属性值
        self.req_dic = {}
        self.reply_dic = {}
        self.notify_dic = {}


class Module(object):
    def __init__(self):
        super(Module, self).__init__()
        self.id = 0
        self.name = ""
        self.comment = ""
        self.proto_imp = ""
        self.msg_list = []

    def __loadXml(self, xml_file):
        contents = ""
        with codecs.open(xml_file, "r", "utf-8") as f:
            contents = f.read()
        if contents == "":
            return
        self.root = ET.fromstring(contents)
        if self.root:
            self.id = self.root.attrib['id']
            self.name = self.root.attrib['name']
            self.comment = self.root.attrib['comment']
            self.proto_imp = self.root[0].text
            return True
        return False

    def parseXml(self, xml_file):
        if not self.__loadXml(xml_file):
            return False
        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            proto_msg = Msg()
            proto_msg.id = req_reply.attrib['id']
            proto_msg.name = req_reply.attrib['name']
            proto_msg.comment = req_reply.attrib['comment']
            proto_msg.type = "ReqReplyMsg"
            req_msg = req_reply[0]
            reply_msg = req_reply[1]
            for req in req_msg:
                proto_msg.req_dic['proto_type'] = req.attrib['proto_type']
                proto_msg.req_dic['value_type'] = req.attrib['value_type']
                proto_msg.req_dic['field_name'] = req.attrib['field_name']
                proto_msg.req_dic['tag'] = req.attrib['tag']

            for reply in reply_msg:
                proto_msg.reply_dic['proto_type'] = reply.attrib['proto_type']
                proto_msg.reply_dic['value_type'] = reply.attrib['value_type']
                proto_msg.reply_dic['field_name'] = reply.attrib['field_name']
                proto_msg.reply_dic['tag'] = reply.attrib['tag']
            self.msg_list.append(proto_msg)

        for notify_msg in self.root.findall("Message/NotifyMsg"):
            for notify in notify_msg:
                proto_msg = Msg()
                proto_msg.id = notify.attrib['id']
                proto_msg.name = notify.attrib['name']
                proto_msg.comment = notify.attrib['comment']
                proto_msg.type = "NotifyMsg"
                for field in notify:
                    proto_msg.notify_dic['proto_type'] = field.attrib['proto_type']
                    proto_msg.notify_dic['value_type'] = field.attrib['value_type']
                    proto_msg.notify_dic['field_name'] = field.attrib['field_name']
                    proto_msg.notify_dic['tag'] = field.attrib['tag']
                self.msg_list.append(proto_msg)
            pass
        pass

    def writeXml(self, xml_file):
        # 如果已有删除，重新生成新xml文件 TODO 优化直接更改xml文件内容
        if os.path.exists(xml_file):
            os.remove(xml_file)
        root = ET.Element('Module')
        root.attrib['id'] = self.id
        root.attrib['name'] = self.name
        root.attrib['comment'] = self.comment
        proto_imp = ET.SubElement(root, 'Import')
        proto_imp.text = self.proto_imp
        message = ET.SubElement(root, 'Message')
        for msg in self.msg_list:
            if msg.type == "ReqReplyMsg":
                req_reply_msg = ET.SubElement(message, 'ReqReplyMsg')
                req_reply_msg.attrib['id'] = msg.id
                req_reply_msg.attrib['name'] = msg.name
                req_reply_msg.attrib['comment'] = msg.comment
                # 创建请求
                req_msg = ET.SubElement(req_reply_msg, 'Req')
                field = ET.SubElement(req_msg, 'field')
                field.attrib['proto_type'] = msg.req_dic['proto_type']
                field.attrib['value_type'] = msg.req_dic['value_type']
                field.attrib['field_name'] = msg.req_dic['field_name']
                field.attrib['tag'] = msg.req_dic['tag']
                # 创建应答
                reply_msg = ET.SubElement(req_reply_msg, 'Reply')
                field = ET.SubElement(reply_msg, 'field')
                field.attrib['proto_type'] = msg.reply_dic['proto_type']
                field.attrib['value_type'] = msg.reply_dic['value_type']
                field.attrib['field_name'] = msg.reply_dic['field_name']
                field.attrib['tag'] = msg.reply_dic['tag']
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
            pass

        # 将 xml tree 写入文件
        tree = ET.ElementTree(root)    
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
pass


class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr, self).__init__()
        self.modules = []

    def loadXmls(self, xml_dir):
        listFiles = os.listdir(xml_dir)
        if not listFiles:
            return False
        for file in listFiles:
            if not file.endswith("xml", 3):
                continue
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            module = Module()
            module.parseXml(xml_file)
            self.modules.append(module)
        return self.modules
    
    def writeXmls(self, xml_dir, modules):
        for module in modules:
            xml_file = xml_dir + "/Module" + module.name+".xml"
            if os.path.exists(xml_file):
                os.remove(xml_file)
            module.writeXml(xml_file)

if __name__ == "__main__":
    module = Module()
    module.parseXml('C:/ProtoTool/Program/protoxml/ModuleChat.xml')
    module.writeXml('C:/ProtoTool/Program/protoxml/ModuleChat2.xml')
    pass
    