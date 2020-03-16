# -*- coding: utf-8 -*-
import numpy as np
import sys
import os

#dataset_txt = str(sys.argv[1])
#fd_result_txt = str(sys.argv[2])
#output_file_name = str(sys.argv[3])

dataset_txt = (r'D:\result_data\test\hole\n=500d=6\dataset.txt')
fd_result_txt = (r'D:\8.1. Result of Node Identifier Matching and Force-directed Algorithms\Result of peter_hole_detection_output_node_id\Sparse\DH\n=500d=6\\')
output_file_name = (r'D:\result_data\test\hole\n=500d=6\DH.txt')

def readData(fname):
    hole = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip()
        hole.append(nums)
    num_hole = len(hole)
    num_hole = num_hole - 1
    
    return num_hole

def outputNumHole(dataset_num_hole, fd_num_hole):
   result_num = dataset_num_hole - fd_num_hole
   with open(output_file_name,'a') as f:
       f.write(str(result_num))
       f.write('\n')

#Main Program:
folderlist = os.listdir(fd_result_txt)
for fd_txt in folderlist:
    dataset_num_hole = readData(dataset_txt)
    fd_num_hole = readData(fd_result_txt + fd_txt)
    outputNumHole(dataset_num_hole, fd_num_hole)
print('Done.')


