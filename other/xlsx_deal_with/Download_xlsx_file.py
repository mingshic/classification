#!/usr/bin/python
#-*- coding: utf-8 -*-

import shutil
import os
from download_sftp import download
import sys
import xlrd  
import re  
import sqlite3  
from collections import Counter
  
def read_xlsx(filename):  
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_names()[0]  
    booksheet = workbook.sheet_by_name(sheet)  
    p = list()  
    for row in range(booksheet.nrows): #booksheet.nrows列出行数的循环 
        row_data = []  
        for col in range(booksheet.ncols): #booksheet.ncols列出列数的循环
            cel = booksheet.cell(row, col)  #根据行数和列数进行对应位置坐标找数据
            val = cel.value   #列出找到数据的value，去掉key
#            try:  
#                val = cel.value  
#                val = re.sub(r'\s+', '', val)  #re.sub把val中的'\s+'替换成''
#            except:  
#                pass  
            if type(val) == float:  
                val = int(val)  
            else:  
                val = str(val)  
            row_data.append(val)  
        p.append(row_data)  
    return  p  
  
def gain_data(filename, col, keyword):
    data_keyword_collect = []
    data = read_xlsx(filename)
    if type(col) == int:
        for row in range(1,len(data)):
    #        if keyword == data[row][int(col)]:
            data_keyword_collect.append(data[row][int(col)])
        counter = Counter(data_keyword_collect)
        if keyword:
            for key,value in counter.items():
                if key == keyword:
                    print (value)
        else:
            print (counter.most_common())

    if type(col) == str:
        if ',' in col:
            raise ValueError("""usage: python %s <filename> \033[1;31m<<col/col_list(According to a column of keyword statistics another column) Here need to create a directory to the selected column (local directory), to count the other column (for the remote directory)>>\033[0m Or <filename> <col> <keyword>""" % sys.argv[0])
        _dict = []
        new_list = []
        col_list = col.split(' ')
        for trim in range(col_list.count('')):
            col_list.remove('')
        col_list_before = col_list[:2]
        col_list_after = col_list[2:]
        new_list.append(col_list_before)
        new_list.append(col_list_after)
        way_path = ['local','remote']
        col = dict(zip(way_path,new_list))
           

        if type(col) == dict:
            for row in range(1,len(data)):
                data_keyword_collect.append(data[row][int(col['local'][1])])
            counter = Counter(data_keyword_collect)
            for keyword_pick in counter.keys():
                if keyword_pick in ['基础运维','基础运维-单次','专业化','其他专业化服务-单次','其他专业化服务','软件运维','软件运维-单次','安全运维','业务运维','资源池运维','运维服务','云运营服务']:
                    Big_classification(keyword_pick, '运维', data, col)
                elif keyword_pick in ['HRO','HRO-单次','MS','MS-单次','PS']:
                    Big_classification(keyword_pick, '外包', data, col)
                elif keyword_pick in ['HRO测试服务','解决方案服务','自动化测试解决方案','DEVOPS解决方案','测试产品','测试服务']:
                    Big_classification(keyword_pick, '测试', data, col)
                elif keyword_pick in ['代理','代维服务','纯代理','混合代理']:
                    Big_classification(keyword_pick, '代理', data, col)


def Big_classification(keyword_pick, classifi, data, col):
    if not os.path.exists(col['local'][0]+'/'+classifi):
        os.makedirs(col['local'][0]+'/'+classifi)
    if not os.path.exists(col['local'][0]+'/'+classifi+'/'+keyword_pick):
        os.makedirs(col['local'][0]+'/'+classifi+'/'+keyword_pick)
    for row in range(1,len(data)):                        
        if keyword_pick == data[row][int(col['local'][1])]:       
            dir_file = classifi+'/'+keyword_pick+'/'+data[row][int(col['remote'][1])]
            if os.path.exists(col['remote'][0]+'/'+data[row][int(col['remote'][1])]+'.doc'):
                download("192.168.52.141", 22, "mingsc", "123456", col['remote'][0]+'/'+data[row][int(col['remote'][1])]+'.doc', col['local'][0]+'/'+dir_file+'.doc')
 
            if os.path.exists(col['remote'][0]+'/'+data[row][int(col['remote'][1])]+'.docx'):
                download("192.168.52.141", 22, "mingsc", "123456", col['remote'][0]+'/'+data[row][int(col['remote'][1])]+'.docx', col['local'][0]+'/'+dir_file+'.docx') 


if __name__=='__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        raise ValueError("""usage: python %s <filename> \033[1;31m<<col/col_list(According to a column of keyword statistics another column) Here need to create a directory to the selected column (local directory), to count the other column (for the remote directory)>>\033[0m Or <filename> <col> <keyword>""" % sys.argv[0])
    xlsx_file = sys.argv[1]
    col = sys.argv[2]
    try:
        col = int(col)
    except:
        pass
    try:
        if sys.argv[3]:
            keyword = sys.argv[3]
    except:
        keyword = None
        pass
    gain_data(xlsx_file, col, keyword)

#download("192.168.52.129", 22, "root", "123456", "/root/test_python", "/sftp_download_relative_data")
