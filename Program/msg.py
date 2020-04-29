# -*-coding:utf-8-*-
from common import *

# 消息分为三类 请求消息  回复消息  广播消息
# 请求消息、回复消息使用相同id


class Field(object):
    def __init__(self):
        super(Field, self).__init__()
        self.proto_type = ""
        self.value_type = ""
        self.field_name = ""
        self.tag = ""
        self.comment = ""


class MsgBase(object):
    def __init__(self, mod_id):
        super(MsgBase, self).__init__()
        self.mod_id = mod_id
        self.id = 0
        self.name = ""
        self.comment = ""
        self.next_tag = '1'
        # 保存属性值列表
        self.field_list = []

    def existField(self, field_name):
        if not field_name:
            return False
        for item in self.field_list:
            if field_name == item.field_name:
                return True, item
        return False, None

    def getFieldByName(self, field_name):
        for field in self.field_list:
            if field.field_name == field_name:
                return field
        return None

    def getFieldByTag(self, tag):
        for field in self.field_list:
            if field.tag == tag:
                return field
        return None

    def addField(self, field):
        is_exist, _ = self.existField(field.field_name)
        if not is_exist:
            field.tag = self.getNextTag()
            self.field_list.append(field)
        pass

    def delField(self, field_name):
        is_exist, item = self.existField(field_name)
        if is_exist:
            self.field_list.remove(item)
        pass

    def updateField(self, old_name, name, comment):
        is_exist, item = self.existField(old_name)
        if is_exist:
            if name:
                item.name = name
            if comment:
                item.comment = comment
        pass

    def getNextTag(self):
        next_tag = self.next_tag
        self.next_tag = str(int(self.next_tag)+1)
        return next_tag


class MsgReq(MsgBase):
    def __init__(self, mod_id):
        super(MsgReq, self).__init__(mod_id)
        self.mod_id = mod_id
        self.type = MsgType.REQ
        pass


class MsgReply(MsgBase):
    def __init__(self, mod_id):
        super(MsgReply, self).__init__(mod_id)
        self.mod_id = mod_id
        self.type = MsgType.REPLY
        pass


class MsgNotify(MsgBase):
    def __init__(self, mod_id):
        super(MsgNotify, self).__init__(mod_id)
        self.mod_id = mod_id
        self.type = MsgType.NOTIFY
        pass
