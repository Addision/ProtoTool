# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET
from gen_cpp import GenCpp
from gen_proto import GenProto


class Gen(object):
    def __init__(self):
        self.root = None
        self.module = ""
        self.gen_cpp = None
        self.gen_proto = None
        pass

    def load_xml(self, xml_file):
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

    def gen_cpp_file(self, cpp_dir):
        self.gen_cpp = GenCpp(self.root, self.module)
        self.gen_cpp.write_cpp(cpp_dir)
        pass

    def gen_proto_file(self, proto_dir):
        self.gen_proto = GenProto(self.root, self.module)
        self.gen_proto.write_proto(proto_dir)
        pass


if __name__ == "__main__":
    gen = Gen()
    gen.load_xml("protoxml/ModuleChat.xml")
    gen.gen_cpp_file()
    gen.gen_proto_file()
    pass
