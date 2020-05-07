from gen import *
from gen_csharp import *


class GenMgr(object):
    def __init__(self):
        self.gen_list = []
        pass

    def loadXmls(self, xml_dir):
        self.gen_list.clear()
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

    def genCsharp(self, csharp_dir):
        proto_enums = ''
        for gen in self.gen_list:
            gen_str = gen.gen_csharp_file() or ''
            proto_enums += gen_str
        proto_namespace = '''
using system;
namespace Protocol
{
    %(protos)s
}
        '''
        proto_namespace = proto_namespace % {
            "protos": proto_enums
        }
        csharp_file = csharp_dir+'/ProtoEnums.cs'
        with codecs.open(csharp_file, "w", 'utf-8') as f:
            f.write(proto_namespace)
            f.flush()
