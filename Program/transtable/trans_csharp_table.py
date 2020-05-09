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


class TransCSharpTable:
    def __init__(self, excel_dir, json_dir, code_dir):
        self.excel_dir = excel_dir
        self.json_dir = json_dir
        self.cpp_dir = code_dir
        self.init_attr()

    def __del__(self):
        pass

    def init_attr(self):
        self.row_fields = ""  # row_fields
        self.classes_name = []  # 表名
        self.key_field = ""
        self.fields = []  # 保存字段信息
        pass

    def get_excel(self):
        files = os.listdir(self.excel_dir)
        excels = [file for file in files if os.path.splitext(file)[
            1] == ".xlsx" and '~' not in file]

        for file in excels:
            tmp_name = os.path.splitext(file)[0]
            self.classes_name.append(tmp_name.split('_')[0])
        return excels, self.classes_name

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

    def transport_json(self, table_name, data_row_type, sheet):
        rows = 5
        rowe = sheet.nrows
        if rowe <= rows:
            return
        all_rows = {}
        while rows < rowe:
            row_dict = self.fix_row_dict(data_row_type, sheet.row_values(rows))
            all_rows[row_dict["id"]] = row_dict
            rows = rows+1

        # 写入json
        json_file = os.path.join(self.json_dir, table_name+'.json')
        with open(json_file, 'w+') as f:
            jsonStr = json.dumps(
                all_rows, indent=4, sort_keys=False, ensure_ascii=False)
            f.write(jsonStr + '\n')

    def read_excel(self, excel_name, table_name):
        try:
            excelFile = xlrd.open_workbook(
                os.path.join(self.excel_dir, excel_name))
            excelSheetNames = excelFile.sheet_names()
            sheet = excelFile.sheet_by_name(excelSheetNames[0])
            excel_data_type = sheet.row_values(0)
            self.fields = sheet.row_values(2)
            data_row_type = {}
            data_type = []
            # 转换成真实数据类型
            for x in excel_data_type:
                data_type.append(data_type_dic[x])
            # 构造每行数据类型声明
            # int id;     // 主键
            data_row_type = list(zip(data_type, self.fields))
            data_desc1 = sheet.row_values(3)
            data_desc2 = sheet.row_values(4)
            data_desc = [a+" "+b for a, b in zip(data_desc1, data_desc2)]

            self.gen_row_fields(data_row_type, data_desc)
            # 生成json文件
            self.transport_json(table_name, data_row_type, sheet)
            self.transport_config_csharp(table_name)
            self.init_attr()
            print("transport table ok!", excel_name)
        except Exception as e:
            print('str(Exception):\t', str(e))
            print('traceback.print_exc():', traceback.print_exc())
        pass

    @staticmethod
    def transportTable(excel_dir, json_dir, code_dir):
        transTable = TransCSharpTable(excel_dir, json_dir, code_dir)
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


if __name__ == '__main__':
    TransCSharpTable.transportTable('C:\\ProtoTool\\Program\\excels',
                                    'C:\\ProtoTool\\Program\\jsons', 'C:\\ProtoTool\\Program\\excel_code')

    pass
