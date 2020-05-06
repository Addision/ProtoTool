
from enum import Enum


class MsgType(Enum):
    REQ = 1
    REPLY = 2
    NOTIFY = 3
    PUBLIC = 4


class ItemType():
    MODULE = '1'
    MSG = '2'
    FIELD = '3'


class ModType(Enum):
    VOID = 0
    PUBLIC = 1
    CLIENT = 2
