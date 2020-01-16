# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET

tmpl_msg = '''
message %(msgname)s
{
%(fields)s
}\n
'''

# tmpl_field = '%(proto_type)s %(value_type)s %(field_name)s = %(tag)s'
tmpl_field = '%s %s %s = %s;'

class GenProto(object):
    def __init__(self):
        self.import_files = []
        self.root = None
        self.proto_file = ""
        pass
    
    def get_import_files(self):
        import_files = self.root.findall("Import")
        for files in import_files:
            self.import_files.append(files.text)
        print(self.import_files)
        pass

    def make_one_message(self, msg_name, msg):
        field_str = ""
        for field in msg:
            field_str += tmpl_field % (field.attrib["proto_type"],field.attrib["value_type"],field.attrib["field_name"],field.attrib["tag"])
            field_str +='\n'
        message = tmpl_msg % {"msgname":msg_name, "fields":field_str}    
        return message

    def get_proto_contents(self):
        message_contents = ""
        for replymsg in self.root.findall("Message/ReplyMsg"):
            # get req message
            req = replymsg[0]
            req_msgname = req.attrib['name']
            message_contents += self.make_one_message(req_msgname, req)
            # get reply message
            reply = replymsg[1]
            reply_msgname = reply.attrib['name']
            message_contents += self.make_one_message(reply_msgname, reply)           
        
        for notifymsg in self.root.findall("Message/NotifyMsg"):
            for notify in notifymsg:
                notify_name = notify.attrib["name"]
                message_contents += self.make_one_message(notify_name, notify)         
        
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
        proto_contents = 'syntax = "proto3";\n'
        for other in self.import_files:
            proto_contents += 'import "%s";\n' % other

        proto_contents += self.get_proto_contents()
        with open(self.proto_file, 'w+') as f:
            f.write(proto_contents + '\n')
        pass


if __name__ == "__main__":
    gen_proto = GenProto()
    gen_proto.load_xml("ModuleChat.xml")
    gen_proto.get_import_files()
    gen_proto.get_proto_contents()
    gen_proto.write_proto()
    
    pass
