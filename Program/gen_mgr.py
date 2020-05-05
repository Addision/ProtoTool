from gen import *


class GenMgr(object):
    def __init__(self):
        self.gen_list = []
        pass

    def loadXmls(self, xml_dir):
        for file in os.listdir(xml_dir):
            xml_file = os.path.join(xml_dir, file).replace('\\', '/')
            if os.path.isdir(xml_file):
                continue
            gen = Gen()
            gen.load_xml(xml_file)
            self.gen_list.append(gen)
        pass

    def genProto(self, proto_dir):
        for gen in self.gen_list:
            gen.gen_proto_file(proto_dir)

    def genCpp(self, cpp_dir):
        for gen in self.gen_list:
            gen.gen_cpp_file(cpp_dir)
