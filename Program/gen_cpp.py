# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET
from common import *    

############################################################################
rpc_req_id = 'RPC_%(module)s_%(msg_name)s_REQ'
rpc_notify_id = 'RPC_%(module)s_%(msg_name)s_NOTIFY'
handle_field = 'g_pPacketMgr->RegisterHandle(%(msg_id)s, Handle%(module)s::%(msg_name)sReq);'
packet_field = 'g_pPacketMgr->RegisterPacket(%(msg_id)s, new CPacket<%(module)s_%(msg_name)sReq>());'
func_field_req = 'static int %(msg_name)sReq(Player* player, Packet* packet);'
func_field_notify = 'static int %(msg_name)sNotify(Player* player, Packet* packet);'
############################################################################


class GenCpp(object):
    def __init__(self, root, module):
        self.root = root
        self.module = module
        self.enum_fields = ""
        self.handle_fields = ""
        self.func_fields = ""
        self.module_id = 0
        pass

    def write_cpp(self, cpp_dir):
        if not self.parse_xml():
            return
        s = ""
        tmpl_file = os.path.join(getRootDir(), 'proto_cpp.tmpl')
        with codecs.open(tmpl_file, "r", "utf-8") as f:
            s = f.read()
        s = s % {
            "module": self.module,
            "module_upper": self.module.upper(),
            "module_id": self.module_id,
            "enum_fields": self.enum_fields,
            "handle_fields": self.handle_fields,
            "func_fields": self.func_fields
        }

        cpp_file = cpp_dir+"/Handle"+self.module+".h"
        with codecs.open(cpp_file, "w", 'utf-8') as f:
            f.write(s)
            f.flush()
        pass

    def parse_xml(self):
        self.module_id = self.root.attrib['id']
        if self.root.findall('Message/PublicMsg'):
            return False
        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            msg_id = req_reply.attrib["id"]
            msg_name = req_reply.attrib["name"]
            id_field = rpc_req_id % {"module": self.module, "msg_name": msg_name}
            id_field = id_field.upper()
            enum_field = id_field + " = "+msg_id+",\n\t\t"
            self.enum_fields += enum_field
            self.handle_fields += handle_field % {
                "msg_id": id_field, "module": self.module, "msg_name": msg_name}
            self.handle_fields += '\n\t\t'
            self.handle_fields += packet_field % {
                "msg_id": id_field, "module": self.module, "msg_name": msg_name}
            self.handle_fields += '\n\t\t'
            self.func_fields += func_field_req % {"msg_name": msg_name}
            self.func_fields += '\n\t'

        for notify in self.root.findall("Message/NotifyMsg/Notify"):
            msg_id = notify.attrib["id"]
            msg_name = notify.attrib["name"]
            id_field = rpc_notify_id % {"module": self.module, "msg_name": msg_name}
            id_field = id_field.upper()
            enum_field = id_field + " = "+msg_id+",\n\t\t"
            self.enum_fields += enum_field
            self.handle_fields += handle_field % {
                "msg_id": id_field, "module": self.module, "msg_name": msg_name}
            self.handle_fields += '\n\t\t'
            self.handle_fields += packet_field % {
                "msg_id": id_field, "module": self.module, "msg_name": msg_name}
            self.handle_fields += '\n\t\t'
            self.func_fields += func_field_notify % {"msg_name": msg_name}
            self.func_fields += '\n\t'            

        self.enum_fields = self.enum_fields[:-3]
        self.handle_fields = self.handle_fields[:-3]
        self.func_fields = self.func_fields[:-2]
        return True

if __name__ == '__main__':
    pass
    # print()