# -*- coding: utf-8 -*-
import numpy as np
import sys
import os

#dataset_txt = str(sys.argv[1])
#fd_result_txt = str(sys.argv[2])
#output_file_name = str(sys.argv[3])

#dataset_txt = (r'D:\result_data\test\hole\n=500d=6\dataset.txt')


file_name = ['n=500d=6', 'n=500d=8', 'n=500d=10', 'n=500d=12', 'n=500d=15', 'n=1000d=6', 'n=1000d=8', 'n=1000d=10', 'n=1000d=12', 'n=1000d=15', 'n=2000d=6', 'n=2000d=8', 'n=2000d=10', 'n=2000d=12', 'n=2000d=15', 'n=3000d=6', 'n=3000d=8', 'n=3000d=10', 'n=3000d=12', 'n=3000d=15']

def readData(fname):
    hole = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip()
        hole.append(nums)
    num_hole = len(hole)
    num_hole = num_hole - 1
    
    return num_hole
       
def isZeroHole(num_hole):
    if num_hole == 0:
        with open(output_file_name ,'a') as f:
            f.write(str(index))
            f.write('\n')
    
    

#Main Program:
for index in file_name:
    num_hole = readData(r'D:\result_data\dataset\Sparse\node id\\' + index + '.txt')
    output_file_name = (r'D:\result_data\dataset\Sparse\node id\Sparse_0_hole_list.txt')
    isZeroHole(num_hole)

    #outputNumHole(fd_num_hole)
    print('finish ' + index)
print('Done.')


