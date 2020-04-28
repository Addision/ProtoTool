# -*-coding:utf-8-*-
import os
import sys
import codecs
from item_data import *
from module import *


class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr, self).__init__()
        self.modules = {}
        self.mod_next_id = 10

    def loadXmls(self, xml_dir):
        if not os.path.exists(xml_dir):
            return False
        listFiles = os.listdir(xml_dir)
        if not listFiles:
            return False
        mod_id = 0
        for file in listFiles:
            if not file.endswith(".xml", 4):
                continue
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            module = Module()
            module.parseXml(xml_file)
            self.modules[module.id] = module
            if int(module.id) > mod_id:
                mod_id = int(module.id)

        self.mod_next_id = mod_id

    def getModFile(self, xml_dir, mod):
        xml_file = xml_dir + "/Module" + mod.name+".xml"
        return xml_file

    def writeXmls(self, xml_dir):
        for _, module in self.modules.items():
            xml_file = self.getModFile(xml_dir, module)
            module.writeXml(xml_file)

    def getMod(self, id):
        if id == '':
            return None
        id = int(id)
        return self.modules[id]

    def getMsg(self, mod_id, msg_id):
        mod = self.getMod(mod_id)
        if not mod:
            return
        msg = mod.getMsg(msg_id)
        return msg

    def nextModId(self):
        self.mod_next_id += 1
        return self.mod_next_id

    def addModule(self, module):
        id = int(module.id)
        if id in self.modules.keys():
            return
        self.modules[id] = module

    def delModule(self, mod_id):
        id = int(mod_id)
        if not self.modules[id]:
            return
        os.remove(self.modules[id].xml_file)
        self.modules.pop(id)
