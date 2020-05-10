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
    def __init__(self):
        pass

    def get_excel(self, excel_dir):
        files = os.listdir(excel_dir)
        excels = [file for file in files if os.path.splitext(file)[
            1] == ".xlsx" and '~' not in file]
        classes_name = []
        for file in excels:
            tmp_name = os.path.splitext(file)[0]
            classes_name.append(tmp_name.split('_')[0])
        return excels, classes_name

    def read_excel(self, excel_name, table_name, excel_dir, json_dir, code_dir):
        try:
            excelFile = xlrd.open_workbook(
                os.path.join(excel_dir, excel_name))
            excelSheetNames = excelFile.sheet_names()
            sheet = excelFile.sheet_by_name(excelSheetNames[0])
            if not sheet:
                return
            # 字段注释
            data_desc1 = sheet.row_values(3)
            data_desc2 = sheet.row_values(4)
            data_desc = [a+" "+b for a, b in zip(data_desc1, data_desc2)]

            trans_cpp = TransCpp(sheet, json_dir, code_dir)
            trans_csharp = TransCsharp(sheet, code_dir)

            # 生成cpp 文件及json文件
            trans_cpp.transport_json(table_name)
            trans_cpp.gen_cpp(table_name, data_desc)
            trans_csharp.gen_csharp(table_name, data_desc)

            print("transport table ok!", excel_name)
        except Exception as e:
            print('str(Exception):\t', str(e))
            print('traceback.print_exc():', traceback.print_exc())
        pass

    @staticmethod
    def transportTable(excel_dir, json_dir, code_dir):
        transTable = TransTable()
        excels, classes_name = transTable.get_excel(excel_dir)
        if not excels:
            return
        print(excels)
        pool = multiprocessing.Pool(processes=5)
        for excel in excels:
            class_name = excel.split('_')[0]
            print(class_name)
            pool.apply_async(transTable.read_excel, (excel, class_name, excel_dir, json_dir, code_dir))
        # gc pool
        pool.close()
        pool.join()
    pass
