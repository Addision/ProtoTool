'''
@Author: jia.lai
@Date: 2020-04-23 16:38:37
@LastEditors: jia.lai
@LastEditTime: 2020-04-23 17:29:13
@Description: 处理单个xml文件的解析
'''
import os
import sys
import codecs
import xml.etree.ElementTree as ET


class ModuleXml(object):
    def __init__(self):
        self.root = None
        self.module_id = 0
        self.module_comment = ""
        self.list_msg = []
        self.dic_req_reply_msg = {}
        self.dic_notify_msg = {}

    def loadXml(self, xml_file):
        contents = ""
        with codecs.open(xml_file, "r", "utf-8") as f:
            contents = f.read()
        if contents == "":
            return
        self.proto_file = os.path.splitext(xml_file)[0] + ".proto"
        print(self.proto_file)
        self.root = ET.fromstring(contents)
        self.module = self.root.attrib['name']
        print(self.root)
        pass
