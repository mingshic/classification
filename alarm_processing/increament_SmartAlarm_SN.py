#!/usr/bin/env python

import sys
from deal_with_xlsx import Write_excel 
import xlrd
import shutil

import random
from test import SN, no_SN


def generate_xlsx(filename, generate_filename):
    shutil.copy(filename, generate_filename)
    workbook = xlrd.open_workbook(generate_filename)
    sheet = workbook.sheet_names()[0]
    booksheet = workbook.sheet_by_name(sheet)
    
    wr = Write_excel(generate_filename)
    wr.write(1,17,"SN")
#    new_workbook = xlsxwriter.Workbook(generate_filename)
#    table_name = sheet
#    read_worksheet = new_workbook.get_sheet(table_name)
#    read_worksheet.write_column("Q1": "SN")
    for row in range(1,booksheet.nrows): #booksheet.nrows列出行数的循环 
#        for col_ in range(booksheet.ncols): #booksheet.ncols列出列数的循环
        if int(booksheet.cell(row, 7).value) == 5 or int(booksheet.cell(row, 7).value) == 4: #根据行数和列数进行对应位置坐标找数据
            wr.write(row+1,17,random.sample(SN,1)[0])
        else:
            wr.write(row+1,17,random.sample(no_SN,1)[0])
    wr.close()

    
if __name__=='__main__':
    if len(sys.argv) != 3:
        raise ValueError("""usage: python %s <filename> <generate_filename>""" % sys.argv[0])
    filename = sys.argv[1]
    generate_filename = sys.argv[2]
    generate_xlsx(filename,generate_filename)
