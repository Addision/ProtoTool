
from enum import Enum


class MsgType(Enum):
    REQ = 1
    REPLY = 2
    NOTIFY = 3


class ItemType():
    MODULE = '1'
    MSG = '2'
    FIELD = '3'
