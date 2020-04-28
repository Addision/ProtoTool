# -*-coding:utf-8-*-
from item_data import *


class Msg(object):
    def __init__(self, mod_id):
        super(Msg, self).__init__()
        self.mod_id = mod_id
        self.id = 0
        self.name = ""
        self.comment = ""
        self.type = ""
        self.item_type = ItemType.MSG
        # 保存属性值
        self.req_list = []
        self.reply_list = []
        self.notify_list = []

    def getField(self, name, field_flag):
        if field_flag == 'req':
            for field in self.req_list:
                if field['field_name'] == name:
                    return field
        if field_flag == 'reply':
            for field in self.reply_list:
                if field['field_name'] == name:
                    return field
        if field_flag == 'notify':
            for field in self.notify_list:
                if field['field_name'] == name:
                    return field
        pass

    def findField(self, field_name, field_flag):
        field = None
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    field = item
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    field = item
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    field = item
        return field

    def addField(self, field, field_flag):
        if not field:
            return
        if field_flag == 'req':
            self.req_list.append(field)
        if field_flag == 'reply':
            self.reply_list.append(field)
        if field_flag == 'notify':
            self.notify_list.append(field)

    def delField(self, field_name, field_flag):
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    self.req_list.remove(item)
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    self.reply_list.remove(item)
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    self.notify_list.remove(item)

    def updateField(self, field_name, field, field_flag):
        if field_flag == 'req':
            for item in self.req_list:
                if item.field_name == field_name:
                    self.req_list.remove(item)
                    self.req_list.append(field)
        if field_flag == 'reply':
            for item in self.reply_list:
                if item.field_name == field_name:
                    self.reply_list.remove(item)
                    self.reply_list.append(field)
        if field_flag == 'notify':
            for item in self.notify_list:
                if item.field_name == field_name:
                    self.notify_list.remove(item)
                    self.notify_list.append(field)
        pass

    def getNextTag(self, field_flag):
        tag = 0
        if field_flag == "req":
            for field in self.req_list:
                if int(field['tag']) > tag:
                    tag = int(field['tag'])
        if field_flag == "reply":
            for field in self.reply_list:
                if int(field['tag'] > tag):
                    tag = int(field['tag'])
        if field_flag == 'notify':
            for field in self.notify_list:
                if int(field['tag'] > tag):
                    tag = int(field['tag'])
        tag = tag + 1
        return tag

    def updateMsg(self, msg_name, msg_comment):
        self.name = msg_name
        self.comment = msg_comment
