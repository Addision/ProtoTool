# -*-coding:utf-8-*-
import os
import sys
import codecs
from module import *
from common import *

class ModuleMgr(object):
    def __init__(self):
        super(ModuleMgr, self).__init__()
        self.module_dic = {}  # <mod_id, mod>
        self.mod_file_dic = {}  # <mod_id, path>
        self.public_next_id = '1'
        self.client_next_id = '11'
        self.proto_imp = ''

    def loadXmls(self, xml_dir):
        if not os.path.exists(xml_dir):
            return False
        listFiles = os.listdir(xml_dir)
        if not listFiles:
            return False
        
        self.module_dic.clear()
        self.mod_file_dic.clear()
        self.proto_imp = ''

        for file in listFiles:
            if not file.endswith(".xml", 4):
                continue
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            module = None
            if 'Public' in xml_file:
                module = ModulePublic()
                module.loadXml(xml_file)
                if int(module.id) >= int(self.public_next_id):
                    self.public_next_id = module.id
                    self.public_next_id = str(int(self.public_next_id)+1)
            else:
                module = ModuleMsg()
                module.loadXml(xml_file)
                if int(module.id) >= int(self.client_next_id):
                    self.client_next_id = module.id
                    self.client_next_id = str(int(self.client_next_id)+1)
                module.proto_imp = self.proto_imp

            if module.mod_type == ModType.PUBLIC:
                self.proto_imp = self.proto_imp + module.name+'.proto;'
                self.changeProtoImp()
            self.module_dic[module.id] = module

    def changeProtoImp(self):
        for mod_id, module in self.module_dic.items():
            if module.mod_type == ModType.CLIENT:
                module.proto_imp = self.proto_imp

    def getPublicModules(self):
        modules = []
        for mod_id, mod in self.module_dic.items():
            if mod.mod_type == ModType.PUBLIC:
                modules.append(mod)
        return modules

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

    def getModuleByName(self, mod_name):
        for mod_id, mod in self.module_dic.items():
            if mod.name == mod_name:
                return mod
        return None

    def addModule(self, module):
        is_exist, _ = self.existModule(module.id)
        if not is_exist:
            self.module_dic[module.id] = module
            if module.mod_type == ModType.PUBLIC and module.name not in self.proto_imp:
                self.proto_imp = self.proto_imp + module.name+'.proto;'
                self.changeProtoImp()
            else:
                module.proto_imp = self.proto_imp

    def delModule(self, mod_id):
        is_exist, _ = self.existModule(mod_id)
        if is_exist:
            module = self.module_dic[mod_id]
            if module.mod_type == ModType.PUBLIC:
                proto_imp = module.name+'.proto;'
                if proto_imp in self.proto_imp:
                    self.proto_imp = self.proto_imp.replace(proto_imp, '')
                # TODO 如果删除公共模块,其他模块引用公共模块的字段自动删除
            if os.path.exists(module.xml_file):
                os.remove(module.xml_file)
            self.module_dic.pop(mod_id)
            self.changeProtoImp()

    def getNextModId(self, mod_type):
        next_id = '0'
        if mod_type == ModType.CLIENT:
            next_id = self.client_next_id
            self.client_next_id = str(int(self.client_next_id) + 1)
        else:
            next_id = self.public_next_id
            self.public_next_id = str(int(self.public_next_id) + 1)

        return next_id
