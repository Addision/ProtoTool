'''
@Author: jia.lai
@Date: 2020-04-23 10:57:50
@LastEditors: jia.lai
@LastEditTime: 2020-04-23 13:59:15
@Description: 
'''
import os
import sys


def UiToPy():
    print(os.path.abspath(sys.argv[0]))
    path = os.path.split(os.path.abspath(sys.argv[0]))[0]
    os.system("cd "+path)

    os.system("pyuic5 -o ProtoUI.py ../Designer/ProtoUI.ui")
    #os.system("pyrcc5 -o resource_rc.py ./res/resource.qrc")

    print("transport ui to py ok...")


if __name__ == "__main__":
    UiToPy()
