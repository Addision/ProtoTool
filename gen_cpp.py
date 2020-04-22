# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET

############################################################################
rpc_id = 'RPC_%(module)s_%(msg_name)s_REQ'
handle_field = 'g_pPacketMgr->RegisterHandle(%(msg_id)s, Handle%(module)s::%(msg_name)sReq);'
packet_field = 'g_pPacketMgr->RegisterPacket(%(msg_id)s, new CPacket<%(module)s_%(msg_name)sReq>());'
func_field = 'static int %(msg_name)sReq(Player* player, Packet* packet);'
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

    def write_cpp(self):
        self.parse_xml()
        s = ""
        with codecs.open("./proto_cpp.tmpl", "r", "utf-8") as f:
            s = f.read()
        s = s % {
                    "module":self.module,
                    "module_upper":self.module.upper(),
                    "module_id":self.module_id,
                    "enum_fields":self.enum_fields, 
                    "handle_fields":self.handle_fields,
                    "func_fields":self.func_fields
                }

        with codecs.open("Handle"+self.module+".h", "w", "utf-8") as f:
            f.write(s)
            f.flush()
        pass

    def parse_xml(self):
        self.module_id = self.root[0].text
        for req_reply in self.root.findall("Message/ReqReplyMsg"):
            msg_id = req_reply.attrib["id"]
            msg_name = req_reply.attrib["name"]
            id_field = rpc_id % {"module":self.module, "msg_name":msg_name}
            id_field = id_field.upper()
            enum_field = id_field +" = "+msg_id+",\n\t\t"
            self.enum_fields += enum_field
            self.handle_fields += handle_field % {"msg_id":id_field, "module":self.module, "msg_name":msg_name}
            self.handle_fields +='\n\t\t'
            self.handle_fields += packet_field % {"msg_id":id_field, "module":self.module, "msg_name":msg_name}
            self.handle_fields +='\n\t\t'
            self.func_fields += func_field % {"msg_name":msg_name}
            self.func_fields +='\n\t'
        
        self.enum_fields = self.enum_fields[:-3]
        self.handle_fields = self.handle_fields[:-3]
        self.func_fields = self.func_fields[:-2]
        pass

