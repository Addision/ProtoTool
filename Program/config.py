'''
@Author: jia.lai
@Date: 2020-04-23 10:55:24
@LastEditors: jia.lai
@LastEditTime: 2020-04-23 16:17:23
@Description: 
'''
'''
[project]
name = proj
path = C:/aaa/bb
'''
# -*-coding:utf-8-*-

from configparser import ConfigParser
import os
class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        self.confName = 'config.ini'
        self.conf = ConfigParser()
        self.dir = os.path.split(os.path.realpath(__file__))[0]
        self.path = os.path.join(self.dir, self.confName)
        if not os.path.exists(self.path):
            with open(self.path, 'w+') as f:
                self.conf.read(self.path)
                self.conf.add_section('project')
                self.conf.set('project', 'name', "proto tool")
                self.conf.set('project', 'proto_xml', "/")
                self.conf.set('project', 'proto_dir', "/")
                self.conf.write(open(self.path, "w"))
        else:
            self.conf.read(self.path)

    def updateProtoXml(self, proto_xml):
        self.conf.set('project', 'proto_xml', proto_xml)
        self.conf.write(open(self.path, "w"))

    def getProtoXml(self):
        proto_xml = self.conf.get('project', 'proto_xml')
        return proto_xml

# if __name__ == '__main__':
#     config = Config()
    # config.updateProject('test', 'C:\\addd')
