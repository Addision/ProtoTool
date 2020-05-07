# -*- coding: UTF-8 -*-

import os
import sys
import codecs
import xml.etree.ElementTree as ET
#############################################
rpc_req_id = 'RPC_%(module)s_%(msg_name)s_REQ'
rpc_notify_id = 'RPC_%(module)s_%(msg_name)s_NOTIFY'
#############################################

class GenCsharp(object):
    def __init__(self, root, module):
        self.root = root
        self.module = module
        self.enum_fields = ""
        self.module_id = 0
        pass

    def write_csharp(self):
        if not self.parse_xml():
            return
        proto_enum = '''
enum E%(module)s
{
    MODULE_ID_%(module_upper)s = %(module_id)s,
    %(enum_fields)s
}
'''           
        proto_enum = proto_enum % {
            "module": self.module,
            "module_upper": self.module.upper(),
            "module_id": self.module_id,
            "enum_fields": self.enum_fields,
        }
        return proto_enum

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

        for notify in self.root.findall("Message/NotifyMsg/Notify"):
            msg_id = notify.attrib["id"]
            msg_name = notify.attrib["name"]
            id_field = rpc_notify_id % {"module": self.module, "msg_name": msg_name}
            id_field = id_field.upper()
            enum_field = id_field + " = "+msg_id+",\n\t\t"
            self.enum_fields += enum_field

        self.enum_fields = self.enum_fields[:-3]
        return True
