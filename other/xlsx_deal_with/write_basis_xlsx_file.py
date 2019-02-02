#!/usr/bin/python
#-*- coding: utf-8 -*-

import shutil
import os
from download_sftp import download
import sys
import xlrd  
import re  
import json
import sqlite3  
from collections import Counter
  
def read_xlsx(filename, col):  
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_names()[0]  
    booksheet = workbook.sheet_by_name(sheet)  
    p = list()  
    col_one = [] 
    for row in range(booksheet.nrows): #booksheet.nrows列出行数的循环 
        data = [] 
        for col_ in range(booksheet.ncols): #booksheet.ncols列出列数的循环
            cel = booksheet.cell(row, col_)  #根据行数和列数进行对应位置坐标找数据
            col_o = booksheet.cell(row, int(col))
            val = cel.value   #列出找到数据的value，去掉key
            data.append(val)  
        col_one.append(col_o.value)
        p.append(data)
    return col_one, p  

def write(filename, col):
    write_json = {}
    write_filename = "alarm_file"
    read_one_, read_ = read_xlsx(filename, col)
    counter = Counter(read_one_)
    for key in counter.keys():
        write_list = []
        for i in range(1, len(read_)):
            if key is read_[i][int(col)]:
#                write_list.append([read_[i][3],read_[i][7],read_[i][9],read_[i][10]])
#                if int(read_[i][7]) == 4 and int(read_[i][7]) == 5:
                write_list.append({"id": read_[i][0],"alarm_title": read_[i][3],"alarm_level": read_[i][7],"alarm_content": read_[i][9],"processer": read_[i][10]})
                write_json.update({read_[i][int(col)]: write_list})
#    for i in range(1, len(write_json)):
#        for value in write_json.values():
#            write_json.values.append(
#    a = json.dumps(write_json)
    print (len(write_json.keys()), len(write_json.values()))
    with open(write_filename, "w") as rp:
        rp.write(json.dumps(write_json))
    
    
  
        

if __name__=='__main__':
    if len(sys.argv) != 3:
        raise ValueError("""usage: python %s <filename> <col>""" % sys.argv[0])
    xlsx_file = sys.argv[1]
    col = sys.argv[2]
    write(xlsx_file,col)

#download("192.168.52.129", 22, "root", "123456", "/root/test_python", "/sftp_download_relative_data")
