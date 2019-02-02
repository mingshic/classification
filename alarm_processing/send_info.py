#!/usr/bin/python
#-*- coding: utf-8 -*-

import time

import sys
import xlrd  
import json
import requests
from collections import Counter


url = "http://192.168.52.141:5000/api/test"  
headers = {'Content-Type': 'application/json'}
opre_filename = "alarm_file"


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

def opreate(filename, col):
    opre_json = {}
    read_one_, read_ = read_xlsx(filename, col)
    counter = Counter(read_one_)
    print (len(read_))
    nums = 0
    for key in counter.keys():
        num = 0
        opre_list = []
        for i in range(1, len(read_)):
            if key is read_[i][int(col)]:
                num += 1
                nums += 1
                opre_list.append({"id": read_[i][0],"rule_id": read_[i][2],"alarm_title": read_[i][3],"alarm_level": read_[i][7],"alarm_content": read_[i][9],"processer": read_[i][10],"instance": read_[i][11],"service_name": read_[i][13],"SN": read_[i][16]})
                opre_json.update({read_[i][int(col)]: opre_list})
        print (num, nums)
    print (len(opre_json.keys()), len(opre_json.values()))
    send(opre_json)

#send data
def send(opre_json):
    nums = 0
    print (12121212121212121221212,len(opre_json.keys()))
    for key in opre_json.keys():
        if key == "":
            continue
        else:
            num = 0
            for data in opre_json[key]:
                num += 1
                nums += 1
                time.sleep(0.5)
                r = requests.post(url, json={"request_type": "", "request_data": data})
#                print ({"request_type": "", "request_data": data}) 
            print (len(opre_json[key]), "r", num, "qqqq", nums)


#    write(opre_json)
#    
#
def write(content):
    with open(opre_filename, "w") as rp:
        rp.write(json.dumps(content))
 

        

if __name__=='__main__':
    if len(sys.argv) != 3:
        raise ValueError("""usage: python %s <filename> <col>""" % sys.argv[0])
    xlsx_file = sys.argv[1]
    col = sys.argv[2]
    opreate(xlsx_file,col)

#download("192.168.52.129", 22, "root", "123456", "/root/test_python", "/sftp_download_relative_data")
