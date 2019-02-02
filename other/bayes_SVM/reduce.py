# -*- coding:UTF-8 -*-

import sys
import numpy as np
import math

def read_input(file):
    for line in file:
        yield line.strip()

input = read_input(sys.stdin)

length = 0

for line in input:
    fields = line.split("\t")
    if length == 0:
        length = len(fields)
        data = np.array([0.0 for _ in range(length)])
    fields = np.array(fields,dtype = float)
    data += fields

lenght = len(data)
varnums = int((-1+math.sqrt(1+4.0*length))/2.0)

part1 = np.mat(data[:varnums])
part1 = part1.T

part2 = data[varnums:]
part2 = part2.reshape(varnums,varnums)
part2 = np.mat(part2)
part2 = part2.I

result = part2*part1

print (result)
