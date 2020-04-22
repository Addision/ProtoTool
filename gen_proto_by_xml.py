# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET

############################################################################
proto_msg = '''
message %(module)s_%(msg_name)s%(msg_type)s
{
%(fields)s
}\n
'''
# tmpl_field = '%(proto_type)s %(value_type)s %(field_name)s = %(tag)s'
tmpl_field = '%s %s %s = %s;'
############################################################################

class GenProto(object):
    def __init__(self):
        self.import_files = []
        self.root = None
        self.proto_file = ""
        self.module = ""
        pass
    
    def get_import_files(self):
        import_files = self.root.findall("Import")
        self.module = self.root.attrib['name']
        for files in import_files:
            self.import_files.append(files.text)
        print(self.import_files)
        pass

    def make_message(self, msg_name, msg, msg_type):
        field_str = ""
        for field in msg:
            field_str += tmpl_field % (field.attrib["proto_type"],field.attrib["value_type"],field.attrib["field_name"],field.attrib["tag"])
            field_str +='\n'
        if msg_type == 1:
            message = proto_msg % {"module":self.module, "msg_name":msg_name, "fields":field_str, "msg_type":"Req"}    
        elif msg_type == 2:
            message = proto_msg % {"module":self.module, "msg_name":msg_name, "fields":field_str, "msg_type":"Reply"}    
        elif msg_type == 3:
            message = proto_msg % {"module":self.module, "msg_name":msg_name, "fields":field_str, "msg_type":"Notify"}    
        return message

    def get_proto_contents(self):
        message_contents = ""
        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            msg_name = req_reply.attrib['name']
            # get req message
            req = req_reply[0]
            message_contents += self.make_message(msg_name, req, 1)
            # get reply message
            reply = req_reply[1]
            message_contents += self.make_message(msg_name, reply, 2)           
        
        for notify_msg in self.root.findall("Message/NotifyMsg"):
            for notify in notify_msg:
                notify_name = notify.attrib["name"]
                message_contents += self.make_message(notify_name, notify, 3)         
        
        return message_contents
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
        print(self.root)
        pass

    def write_proto(self):
        self.get_import_files()
        proto_contents = 'syntax = "proto3";\n'
        for imp_file in self.import_files:
            proto_contents += 'import "%s";\n' % imp_file

        proto_contents += self.get_proto_contents()
        with open(self.proto_file, 'w+') as f:
            f.write(proto_contents + '\n')
        pass

if __name__ == "__main__":
    gen_proto = GenProto()
    gen_proto.load_xml("ModuleChat.xml")
    gen_proto.write_proto()
    pass
