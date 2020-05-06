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
                self.conf.set('project', 'msg_path', "C:/")
                self.conf.set('project', 'proto_path', "C:/")
                self.conf.set('project', 'proto_gen_path', 'C:/')
                self.conf.set('project', 'table_path', 'C:/')
                self.conf.write(f)
        else:
            self.conf.read(self.path, encoding='utf-8-sig')

    def updateConf(self, msg_path, proto_path, proto_gen_path, table_path):
        self.conf.set('project', 'msg_path', msg_path)
        self.conf.set('project', 'proto_path', proto_path)
        self.conf.set('project', 'proto_gen_path', proto_gen_path)
        self.conf.set('project', 'table_path', table_path)
        with open(self.path, 'w+') as f:
            self.conf.write(f)        

    def updateConfOne(self, conf_lable, content):
        self.conf.set('project', conf_lable, content)
        with open(self.path, 'w+') as f:
            self.conf.write(f)

    def getConfOne(self, conf_lable):
        self.conf.read(self.path, encoding='utf-8-sig')
        path = self.conf.get('project', conf_lable)
        return path



# if __name__ == '__main__':
#     config = Config()
    # config.updateProject('test', 'C:\\addd')
