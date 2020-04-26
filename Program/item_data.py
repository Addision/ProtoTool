
class ItemType(object):
    VOID = '0'
    MODULE = '1'
    MSG = '2'
    REQ = '3'
    REPLY = '4'
    NOTIFY = '5'
    FIELD = '6'

class ItemData(object):
    def __init__(self, id, item_type):
        super(ItemData,self).__init__()
        self.id = id
        self.type = item_type