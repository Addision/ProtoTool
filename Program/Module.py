# -*-coding:utf-8-*-

import os,sys
import codecs
import xml.etree.ElementTree as ET

class Msg(object):
    def __init__(self):
        super(Msg, self).__init__()
        self.id = 0
        self.name = ""
        self.comment = ""
        self.req_dic = {}
        self.reply_dic = {}
        self.notify_dic = {}


class Module(object):
    def __init__(self):
        super(Module, self).__init__()
        self.id = 0
        self.name = ""
        self.comment = ""
        self.proto_import = ""
        self.msg_list = []
        self.proto_msg = Msg()

    def loadXml(self, xml_file):
        contents = ""
        with codecs.open(xml_file, "r", "utf-8") as f:
            contents = f.read()
        if contents == "":
            return
        # self.proto_file = os.path.splitext(xml_file)[0] + ".proto"
        # print(self.proto_file)
        self.root = ET.fromstring(contents)
        if self.root:
            self.id = self.root.attrib['id']
            self.name = self.root.attrib['name']
            self.comment = self.root.attrib['comment']
            self.proto_import = self.root[0].text
            return True
        return False

    def parseXml(self, xml_file):
        if ~self.loadXml(xml_file):
            return False
        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            self.proto_msg.id = req_reply.attrib['id']
            self.proto_msg.name = req_reply.attrib['name']
            self.proto_msg.comment = req_reply.attrib['comment']
            req_msg = req_reply[0]
            reply_msg = req_reply[1]
            for req in req_msg:
                self.proto_msg.req_dic['proto_type'] = req.attrib['proto_type']
                self.proto_msg.req_dic['value_type'] = req.attrib['value_type']
                self.proto_msg.req_dic['field_name'] = req.attrib['field_name']
                self.proto_msg.req_dic['tag'] = req.attrib['tag']
            
            for reply in reply_msg:
                self.proto_msg.reply_dic['proto_type'] = reply.attrib['proto_type']
                self.proto_msg.reply_dic['value_type'] = reply.attrib['value_type']
                self.proto_msg.reply_dic['field_name'] = reply.attrib['field_name']
                self.proto_msg.reply_dic['tag'] = reply.attrib['tag']

        for notify in self.root.findall("Message/NotifyMsg"):
            self.proto_msg.id = notify.attrib['id']
            self.proto_msg.name = notify.attrib['name']
            self.proto_msg.comment = notify.attrib['comment']
            notify_msg = notify[0]
            for notify in notify_msg:
                self.proto_msg.notify_dic['proto_type'] = notify.attrib['proto_type']
                self.proto_msg.notify_dic['value_type'] = notify.attrib['value_type']
                self.proto_msg.notify_dic['field_name'] = notify.attrib['field_name']
                self.proto_msg.notify_dic['tag'] = notify.attrib['tag']                    
            pass             
        pass

    def writeXml(self, xml_file):

        pass



class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr,self).__init__()
    
    def loadXml(self, xml_dir):
        
        pass

    def writeXml(self):
        pass