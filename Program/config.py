# -*-coding:utf-8-*-
from configparser import ConfigParser
import os


class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        self.conf = ConfigParser()
        conf_dir = os.path.split(os.path.realpath(__file__))[0]
        self.conf_path = os.path.join(conf_dir, 'config.ini')
        if not os.path.exists(self.conf_path):
            with open(self.conf_path, 'w+') as f:
                self.conf.add_section('project')
                self.conf.set('project', 'name', "proto tool")
                self.conf.set('project', 'msg_path', '')
                self.conf.set('project', 'proto_path', '')
                self.conf.set('project', 'protobuf_path', '')
                self.conf.set('project', 'excel_path', '')
                self.conf.set('project', 'json_path', '')
                self.conf.set('project', 'excel_cpp_path', '')
                self.conf.set('project', 'excel_csharp_path', '')
                self.conf.write(f)

        self.conf.read(self.conf_path, encoding='utf-8-sig')

    def updateConfOne(self, conf_lable, content):
        self.conf.set('project', conf_lable, content)
        with open(self.conf_path, 'w+') as f:
            self.conf.write(f)

    def getConfOne(self, conf_lable):
        self.conf.read(self.conf_path, encoding='utf-8-sig')
        config = self.conf.get('project', conf_lable)
        return config


# if __name__ == '__main__':
#     config = Config()
    # config.updateProject('test', 'C:\\addd')
