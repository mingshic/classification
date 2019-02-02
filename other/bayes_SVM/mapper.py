# -*- coding:UTF-8 -*-

import sys
import numpy as np

def read_input(file):
    for line in file:
        yield line.strip()

def matmulti():
    
    input = read_input(sys.stdin)

    innerLength = 0
    length = 0
    for line in input:
        fields = line.split(",")
        if innerLength == 0:
            innerLength = len(fields) - 1
            data1 = np.array([0.0 for _ in range(innerLength)])
        temp = np.array(fields,float)[:innerLength]*float(fields[innerLength])
        data1 = data1 + temp
        
        if length == 0:
            length = len(fields) - 1
            data2 = np.diag(np.zeros(length))
        for index in range(length):
            data2[index] += np.array(fields[:length],dtype = float)*float(fields[index])
            
    return data1,data2

data1,data2 = matmulti()
data1 = list(data1)
length = len(data2)
data2 = data2.reshape(1,length**2)
data2 = list(data2[0])
data = data1 + data2
print("\t".join(str(i) for i in data))
