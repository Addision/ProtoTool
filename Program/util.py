'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-08-26 14:47:44
@LastEditTime: 2019-08-30 17:53:47
@LastEditors: Please set LastEditors
'''
import sys
import os
import shutil
import json
import xmltodict
import re

def getCurrentDir():
    return os.getcwd().replace("\\", '/')

def DelDir(dir):
    shutil.rmtree(dir)

def cpDir(srcDir, desDir):
    if srcDir is None or desDir is None:
        return

    if os.path.exists(desDir):
        DelDir(desDir)
    shutil.copytree(srcDir, desDir)
    
def jsontoxml(jsonstr):
    #xmltodict库的unparse()json转xml
    xmlstr = xmltodict.unparse(jsonstr)
    print(xmlstr)

def xmltojson(xmlstr):
    # parse是的xml解析器
    # xmlstr = "<工程><ISubsystem><ActorPkg /></ISubsystem></工程>"
    xmlparse = xmltodict.parse(xmlstr)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse, indent=1)
    return jsonstr

def dictojson(dic):
    jsoninfo = json.dumps(dic)
    return jsoninfo 

def fileContents(fileName,xmlFlag = False):
    with open(fileName, encoding='utf-8') as file:
        lines = file.readlines()
        newlines = []
        newlines.append(lines[0])
        newlines.append("".join(re.split('<\w+ />', lines[1])))
        contents = None
        if not xmlFlag:
            contents = "".join(newlines[1:])
        else:
            contents = "".join(newlines[:])
    return contents

def writeContents(fileName, contents):
    with open(fileName, "w+", encoding="utf-8") as file:
        file.write(contents)



def prettyXml(element, indent, newline, level = 0):
    if element:    
        if element.text == None or element.text.isspace():    
            element.text = newline + indent * (level + 1)      
        else:    
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)     
    temp = list(element) 
    for subelement in temp:    
        if temp.index(subelement) < (len(temp) - 1):   
            subelement.tail = newline + indent * (level + 1)    
        else: 
            subelement.tail = newline + indent * level    
        prettyXml(subelement, indent, newline, level = level + 1) 
        
def setStyleSheet(path, obj):
    with open(path, 'r') as f:
        css = f.read()
        # print(css)
        obj.setStyleSheet(css)


        
        
if __name__ == '__main__':
    string = "<project><DesignSynthesisPkg><ISubsystem /><ISubsystem>ArchitecturalDesignPkg</ISubsystem><ISubsystem2 /><ISubsystem>ArchitecturalAnalysisPkg</ISubsystem></DesignSynthesisPkg></project>"
    newstring = None
    while string:
        m = re.search('<\w+ />', string)
        print(m.regs[0][0])
        print(re.split('<\w+ />', string))
        break
        #newstring = string.sub(0, m.regs[0], )
    


    
