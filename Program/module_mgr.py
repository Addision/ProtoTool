# -*-coding:utf-8-*-
import os
import sys
import codecs
from module import *

class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr, self).__init__()
        self.module_dic = {}  # <mod_id, mod>
        self.mod_file_dic = {}  # <mod_id, path>
        self.mod_next_id = '0'

    def loadXmls(self, xml_dir):
        if not os.path.exists(xml_dir):
            return False
        listFiles = os.listdir(xml_dir)
        if not listFiles:
            return False

        for file in listFiles:
            if not file.endswith(".xml", 4):
                continue
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            module = Module()
            module.loadXml(xml_file)
            self.module_dic[module.id] = module

            if int(module.id) > int(self.mod_next_id):
                self.mod_next_id = module.id
        self.mod_next_id = str(int(self.mod_next_id)+1)

    def getModFile(self, xml_dir, mod_name):
        xml_file = xml_dir + "/Module" + mod_name+".xml"
        return xml_file

    def saveXmls(self, xml_dir):
        for mod_id, module in self.module_dic.items():
            xml_file = self.getModFile(xml_dir, module.name)
            module.saveXml(xml_file)

    def existModule(self, mod_id):
        if not mod_id:
            return False, None
        if mod_id in self.module_dic.keys():
            return True, self.module_dic[mod_id]
        return False, None

    def getModule(self, mod_id):
        is_exist, module = self.existModule(mod_id)
        if is_exist:
            return module
        return None

    def addModule(self, module):
        is_exist, module = self.existModule(module.id)
        if not is_exist:
            self.module_dic[module.id] = module

    def delModule(self, mod_id):
        is_exist, module = self.existModule(mod_id)
        if is_exist:
            os.remove(self.modules[mod_id].xml_file)
            self.module_dic.pop(mod_id)

    def getNextModId(self):
        next_id = self.mod_next_id
        self.mod_next_id = self.mod_next_id + 1
        return next_id
