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
        self.public_next_id = '1'
        self.client_next_id = '11'

        # 公共文件
        self.public_messages = {} # <mod_name, msg_name>

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
            module = None
            if 'Public' in xml_file:
                module = ModulePublic()
                if int(module.id) > int(self.public_next_id):
                    self.public_next_id = module.id                
            else:
                module = ModuleMsg()
                if int(module.id) > int(self.client_next_id):
                    self.client_next_id = module.id                
            module.loadXml(xml_file)
            self.module_dic[module.id] = module

        self.public_next_id = str(int(self.public_next_id)+1)
        self.client_next_id = str(int(self.client_next_id)+1)
        

    def getModFile(self, xml_dir, mod_name):
        xml_file = xml_dir + "/Module" + mod_name+".xml"
        return xml_file

    def saveXmls(self, xml_dir):
        if not self.module_dic:
            return
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
        is_exist, _ = self.existModule(module.id)
        if not is_exist:
            self.module_dic[module.id] = module

    def delModule(self, mod_id):
        is_exist, _ = self.existModule(mod_id)
        if is_exist:
            print(self.module_dic[mod_id].xml_file)
            # TODO test
            os.remove(self.module_dic[mod_id].xml_file)
            self.module_dic.pop(mod_id)

    def getNextModId(self, mod_type):
        next_id = '0'
        if mod_type == 'client':
            next_id = self.client_next_id
            self.client_next_id = str(int(self.client_next_id) + 1)
        else:
            next_id = self.public_next_id
            self.public_next_id = str(int(self.public_next_id) + 1)

        return next_id
