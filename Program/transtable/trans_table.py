# _*_coding:utf-8 _*_

import xlrd
from xlrd import xldate_as_tuple
import multiprocessing
import json
import os
import codecs
import datetime
import traceback
from transtable.trans_cpp import *
from transtable.trans_csharp import *


class TransTable:
    def __init__(self, excel_dir, json_dir, code_dir):
        self.excel_dir = excel_dir
        self.json_dir = json_dir
        self.cpp_dir = code_dir

    def get_excel(self):
        files = os.listdir(self.excel_dir)
        excels = [file for file in files if os.path.splitext(file)[
            1] == ".xlsx" and '~' not in file]

        for file in excels:
            tmp_name = os.path.splitext(file)[0]
            self.classes_name.append(tmp_name.split('_')[0])
        return excels, self.classes_name

    def read_excel(self, excel_name, table_name):
        try:
            excelFile = xlrd.open_workbook(
                os.path.join(self.excel_dir, excel_name))
            excelSheetNames = excelFile.sheet_names()
            sheet = excelFile.sheet_by_name(excelSheetNames[0])
            excel_data_type = sheet.row_values(0)
            self.fields = sheet.row_values(2)
            # 构造数据类型
            data_row_type = {}
            data_type = []
            for x in excel_data_type:
                data_type.append(data_type_dic[x])
            data_row_type = list(zip(data_type, self.fields))

            # 字段注释
            data_desc1 = sheet.row_values(3)
            data_desc2 = sheet.row_values(4)
            data_desc = [a+" "+b for a, b in zip(data_desc1, data_desc2)]

            trans_cpp = TransCpp(self.json_dir, self.code_dir)
            trans_csharp = TransCsharp(self.code_dir)

            # 生成cpp 文件及json文件
            trans_cpp.transport_json(table_name, data_row_type, sheet)
            trans_cpp.gen_cpp(table_name)

            trans_csharp.gen_csharp(table_name)

            print("transport table ok!", excel_name)
        except Exception as e:
            print('str(Exception):\t', str(e))
            print('traceback.print_exc():', traceback.print_exc())
        pass

    @staticmethod
    def transportTable(excel_dir, json_dir, code_dir):
        transTable = TransTable(excel_dir, json_dir, code_dir)
        excels, classes_name = transTable.get_excel()
        if not excels:
            return
        print(excels)
        pool = multiprocessing.Pool(processes=5)
        for excel in excels:
            class_name = excel.split('_')[0]
            print(class_name)
            pool.apply_async(transTable.read_excel, (excel, class_name))
        # gc pool
        pool.close()
        pool.join()
    pass
