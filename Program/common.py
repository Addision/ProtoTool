
from enum import Enum
import os
import sys


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


def getRootDir():
    if getattr(sys, 'frozen', False):
        root_path = os.path.dirname(sys.executable)
    elif __file__:
        root_path = os.path.dirname(__file__)
    return root_path

if __name__ == '__main__':
    print(getRootDir())