# _*_coding:utf-8 _*_

import xlrd
from xlrd import xldate_as_tuple
import multiprocessing
import json
import os
import codecs
import datetime
import traceback

# 数据类型字典
data_type_dic = {
    "INT": "int",
    "FLOAT": "float",
    "DOUBLE": "double",
    "STRING": "string",
    "LI": "List<int>",
    "LD": "List<double>",
    "LF": "List<float>",
    "LS": "List<string>"
}


class TransCSharp:
    def __init__(self, code_dir):
        self.excel_dir = excel_dir
        self.code_dir = code_dir
        self.init_attr()

    def __del__(self):
        pass

    def init_attr(self):
        self.row_fields = ""  # row_fields
        self.key_field = ""
        self.fields = []  # 保存字段信息
        pass


    def gen_row_fields(self, data_row_type, data_desc):
        self.row_fields = "\t"
        tmp_field = ""
        for i in range(len(data_row_type)):
            x = data_row_type[i]
            tmp_field = x[0]+" " + x[1] + ";"
            strlen = 50
            data_desc[i] = data_desc[i].replace("\n", " ")
            self.row_fields += (tmp_field + " " *
                                (strlen-len(tmp_field)) + "// "+data_desc[i])
            self.row_fields += "\n\t"

    def transport_config_csharp(self, table_name):
        s = ""
        with codecs.open("./transtable/table_csharp.tmpl", "r", "utf-8") as f:
            s = f.read()
        if not s:
            return
        s = s % {"class_name": table_name,
                 "row_fields": self.row_fields}

        cpp_file = os.path.join(self.cpp_dir, table_name+'.cs')
        with codecs.open(cpp_file, "w", "GB2312") as f:
            f.write(s)
            f.flush()
            pass

    def fix_row_dict(self, data_row_type, row_values):
        row_dict = {}
        for i in range(len(data_row_type)):
            if row_values[i] is None:
                row_values[i] = ""
            data_type = data_row_type[i]  # (int, id)
            field_type = data_type[0]
            field_id = data_type[1]

            if "int" == field_type:
                row_dict[field_id] = int(row_values[i])
            if "float" == field_type:
                row_dict[field_id] = float(row_values[i])
            if "double" == field_type:
                row_dict[field_id] = float(row_values[i])
            if "string" == field_type:
                row_dict[field_id] = str(row_values[i])
            if "List" in field_type and row_values[i] == "":
                row_dict[field_id] = []
                continue
            if "List" in field_type and row_values[i] != "":
                if isinstance(row_values[i], float):
                    row_dict[field_id] = [int(row_values[i])]
                    continue
            if "List<int>" == field_type:
                row_dict[field_id] = list(
                    map(int, row_values[i].split('|')))
            if "List<double>" == field_type:
                row_dict[field_id] = list(
                    map(float, row_values[i].split('|')))
            if "List<float>" == field_type:
                row_dict[field_id] = list(
                    map(float, row_values[i].split('|')))
            if "List<string>" == field_type:
                row_dict[field_id] = list(
                    map(str, row_values[i].split('|')))
        # print("=============", row_dict)
        return row_dict
        pass


